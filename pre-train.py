import torch
from torch import nn
from torch.utils import data as torch_data
from torchdrug import core, datasets, tasks, models

dataset = datasets.ZINC2m("~/zinc2m/", atom_feature="pretrain", bond_feature="pretrain")
gin_model = models.GIN(input_dim=dataset.node_feature_dim, hidden_dims=[300, 300, 300, 300, 300], 
                        edge_input_dim=dataset.edge_feature_dim, batch_norm=True, readout="mean")
model = models.InfoGraph(gin_model, separate_model=False)

task = tasks.Unsupervised(model)
optimizer = torch.optim.Adam(task.parameters(), lr=1e-3)

solver = core.Engine(task, dataset, None, None, optimizer, gpus=[0], batch_size=256)
solver.train(num_epoch=100)
solver.save("zinc2m_gin_infograph.pth")