
import torch
import torch.nn as nn

import pytorch_lightning as pl
from pytorch_lightning.callbacks import EarlyStopping, ModelCheckpoint, GPUStatsMonitor
from pytorch_lightning.loggers import WandbLogger
from pytorch_lightning.metrics.classification import AUROC , AUC

import wandb

from deeprec.models.deepfm import DeepFactorizationMachineModel
# from data.dataset import get_dataset


class NCF(pl.LightningModule):
  
    """DeepFactorizationMachineModel
    """
    
    def __init__(self, num_users, num_items, user_features, item_features, 
                 lr=1e-3, embed_dim=16, dnn_dim=16, dropout=0.5):
        super().__init__()
        self.save_hyperparameters()

        self.num_users = num_users
        self.num_items = num_items
        self.user_features = user_features
        self.item_features = item_features
        self.lr = lr
        self.embed_dim = embed_dim
        self.auroc = AUROC()

        self.model = DeepFactorizationMachineModel(
            users_dim = num_users, 
            items_dim = num_items, 
            user_feature_dim = user_features.shape[1], 
            item_feature_dim = item_features.shape[1],
            embed_dim=self.embed_dim, 
            mlp_dims=(dnn_dim, dnn_dim), 
            dropout=0.5)
        
    def forward(self, x):
        
        # Output layer
        pred = self.model(x)

        return pred
    
    def training_step(self, batch, batch_idx):
        x = batch
        predicted_labels = self(x)
        loss = nn.BCELoss()(predicted_labels, x["target"].view(-1, 1).float())
        auc = self.auroc(predicted_labels, x["target"].view(-1, 1))
        metrics = {'train_loss': loss, "train_auc": auc}
        self.log_dict(metrics, on_step=True, on_epoch=True, prog_bar=True, logger=True)
        return loss

    def validation_step(self, batch, batch_idx):
        x = batch
        predicted_labels = self(x)
        loss = nn.BCELoss()(predicted_labels, x["target"].view(-1, 1).float())
        auc = self.auroc(predicted_labels, x["target"].view(-1, 1))
        metrics = {'val_loss': loss, "val_auc": auc}
        self.log_dict(metrics)
        return loss

    def test_step(self, batch, batch_idx):
        x = batch
        predicted_labels = self(x)
        loss = nn.BCELoss()(predicted_labels, x["target"].view(-1, 1).float())
        auc = self.auroc(predicted_labels, x["target"].view(-1, 1))
        metrics = {'test_loss': loss, "test_auc": auc}
        self.log_dict(metrics)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(
            self.parameters(),
            lr=self.lr)



def train(args, model, train_data_loader, test_data_loader, device):

    early_stop_callback = EarlyStopping(
        monitor='val_loss',
        min_delta=0.05,
        patience=3,
        verbose=False,
        mode='min'
        )
    checkpoint_callback = ModelCheckpoint(
        dirpath='chkpt/',
        filename='DeepFM-{epoch:02d}-{val_loss:.2f}-{val_auc:.2f}',
        monitor='val_auc',
        )

    if device is 'cuda:0':
        gpu_stats = GPUStatsMonitor() 
        trainer = pl.Trainer(max_epochs=args.epoch, 
                    gpus=-1, 
                    reload_dataloaders_every_epoch=True,
                    progress_bar_refresh_rate=20, 
                    # logger=wandb_logger, 
                    checkpoint_callback=True,
                    callbacks=[
                        early_stop_callback, 
                        checkpoint_callback, 
                        gpu_stats
                        ],
                    profiler=True
                    )
    else:
        trainer = pl.Trainer(
            max_epochs=args.epoch, 
            reload_dataloaders_every_epoch=True,
            progress_bar_refresh_rate=20, 
            checkpoint_callback=True,
            callbacks=[
                early_stop_callback, 
                checkpoint_callback, 
                ],
            )

    trainer.fit(model, train_data_loader, test_data_loader)

