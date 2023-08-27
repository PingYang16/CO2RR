import os
import schnetpack as spk
from schnetpack.datasets import QM9
import schnetpack.transform as trn

import torch
import torchmetrics
import pytorch_lightning as pl

qm9tut = './qm9tut'
if not os.path.exists('qm9tut'):
    os.makedirs(qm9tut)

qm9data = QM9('./data/qm9.db', 
              batch_size=128,
              num_train=107108,
              num_val=26777,
              transforms=[
                trn.ASENeighborList(cutoff=5.),
                trn.RemoveOffsets(QM9.U0, remove_mean=True, remove_atomrefs=True),
                trn.CastTo32()
              ],
              property_unit={QM9.U0: 'ev'},
              num_workers=1,
              pin_memory=False,
              )
qm9data.prepare_data()
qm9data.setup()

cutoff = 5.
n_atom_basis = 30

pairwise_distance = spk.atomistic.PairwiseDistance()
radial_basis = spk.nn.GaussianRBF(n_rbf=20, cutoff=cutoff)
schnet = spk.representation.SchNet(
    n_atom_basis=n_atom_basis,
    radial_basis=radial_basis,
    cutoff_fn=spk.nn.CosineCutoff(cutoff)
)
pred_U0 = spk.atomistic.Atomwise(n_in=n_atom_basis, output_key=QM9.U0)

nnpot = spk.model.NeuralNetworkPotential(
    representation=schnet,
    input_modules=[pairwise_distance],
    output_modules=[pred_U0],
    postprocessors=[trn.CastTo64(), trn.AddOffsets(QM9.U0, add_mean=True, add_atomrefs=True)]
)

output_U0 = spk.task.ModelOutput(
    name=QM9.U0,
    loss_fn=torch.nn.MSELoss(),
    loss_weight=1,
    metrics={
        "MAE": torchmetrics.MeanAbsoluteError(),
    }
)

task = spk.task.AtomisticTask(
    model=nnpot,
    outputs=[output_U0],
    optimizer_cls=torch.optim.AdamW,
    optimizer_kwargs={"lr": 1e-4}
)

logger = pl.loggers.TensorBoardLogger(save_dir=qm9tut)
callbacks = [
    spk.train.ModelCheckpoint(
        model_path=os.path.join(qm9tut, "best_inference_model"),
        save_top_k=1,
        monitor="val_loss"
    )
]

trainer = pl.Trainer(
    callbacks=callbacks,
    logger=logger,
    default_root_dir=qm9tut,
    max_epochs=100,
)

trainer.fit(task, datamodule=qm9data)