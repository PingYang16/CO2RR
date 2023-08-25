import os
import schnetpack as spk
from schnetpack.datasets import QM9
import schnetpack.transform as trm

import torch
import torchmetrics
import pytorch_lightning as pl

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
schnet = spk.representation.SchNet()