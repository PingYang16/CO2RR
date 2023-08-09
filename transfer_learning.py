import torch
from torch import nn, optim
from torch.utils import data as torch_data

import torchdrug
from torchdrug import core, datasets, tasks, models, data, utils
from torchdrug.core import Registry as R

@R.register("datasets.CO2RR")
@utils.copy_args(data.MoleculeDataset.load_csv, ignore=("smiles_field", "target_fields"))
class CO2RR(data.MoleculeDataset):
    """
    A screening study on the performance of CO2 reduction reactions using Cu nanoparticle 
        (CuNP) + small molecule modifiers

    Statistics:
        - #Molecule: 17
        - #Classification task: 1

    Parameters:
        path (str): path to store the dataset
        verbose (int, optional): output verbose level
        **kwargs
    """
    target_filed = "General effects"
    smiles_filed = "SMILES"

    def __init__(self, path, verbose=1, **kwargs):
        
        csv_file = path + "CO2RR.csv"

        self.load_csv(csv_file, smiles_field=self.smiles_filed, target_fields=self.target_filed, 
                        verbose=verbose, **kwargs)

co2rr_data = CO2RR('/home/pinyang_umass_edu/CO2RR/', atom_feature="pretrain", bond_feature="pretrain")

lengths = [int(0.8 * len(co2rr_data)), int(0.1 * len(co2rr_data))]
lengths += [len(co2rr_data) - sum(lengths)]
train_set, valid_set, test_set = data.ordered_scaffold_split(co2rr_data, lengths)

model = models.GIN(
    input_dim=co2rr_data.node_feature_dim,
    hidden_dims=[300, 300, 300, 300, 300],
    edge_input_dim=co2rr_data.edge_feature_dim,
    batch_norm=True,
    readout="mean"
)
task = tasks.PropertyPrediction(model, task=co2rr_data.tasks,
                                criterion="bce", metric=("auprc", "auroc"))
optimizer = optim.Adam(task.parameters(), lr=1e-3)
solver = core.Engine(task, train_set, valid_set, test_set, optimizer, gpus=[0], batch_size = 4)

checkpoint = torch.load("zinc2m_gin_infograph.pth")["model"]
task.load_state_dict(checkpoint, strict=False)

solver.train(num_epoch=100)
solver.evaluate("valid")
solver.evaluate("test")
