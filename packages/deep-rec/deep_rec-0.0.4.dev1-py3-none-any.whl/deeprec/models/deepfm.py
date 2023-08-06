
import torch
import torch.utils.data
import torch.nn.functional as F

from deeprec.models.layers import FeaturesLinear, FeaturesEmbedding, FactorizationMachine, MultiLayerPerceptron


class DeepFactorizationMachineModel(torch.nn.Module):
    """
    A Pytorch implementation of DeepFM.

    Reference:
        H Guo, et al. DeepFM: A Factorization-Machine based Neural Network for CTR Prediction, 2017.
    """

    def __init__(self, users_dim, items_dim, user_feature_dim, item_feature_dim, embed_dim, mlp_dims, dropout):
        super().__init__()
        self.linear = FeaturesLinear(users_dim, items_dim, user_feature_dim, item_feature_dim)
        self.fm = FactorizationMachine(reduce_sum=True)
        self.embedding = FeaturesEmbedding(users_dim, items_dim, user_feature_dim, item_feature_dim, embed_dim)
        self.embed_output_dim = len([users_dim, items_dim, user_feature_dim, item_feature_dim]) * embed_dim
        self.mlp = MultiLayerPerceptron(self.embed_output_dim, mlp_dims, dropout)

    def forward(self, x):
        """
        :param x: Long tensor of size ``(batch_size, num_fields)``
        """
        embed_x = self.embedding(x)
        x = self.linear(x) + self.fm(embed_x) + self.mlp(embed_x.view(-1, self.embed_output_dim))
        return torch.sigmoid(x)
        # return torch.sigmoid(x.squeeze(1))