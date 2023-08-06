
import torch
import torch.utils.data
import torch.nn.functional as F


class FeaturesLinear(torch.nn.Module):
    """
    Class to perform a linear transformation on the features
    """

    def __init__(self, users_dim, items_dim, user_feature_dim, item_feature_dim, output_dim=1):
        super().__init__()

        self.dense_user_features = torch.nn.Linear(user_feature_dim, output_dim)
        self.dense_item_features = torch.nn.Linear(item_feature_dim, output_dim)
        self.embed_user = torch.nn.Embedding(users_dim, output_dim)
        self.embed_item = torch.nn.Embedding(items_dim, output_dim)

        self.bias = torch.nn.Parameter(torch.zeros((output_dim,)))


    def forward(self, x):
        """
        :param x: Long tensor of size ``(batch_size, num_fields)``
        """
        fc = self.dense_user_features(x["users_features"]) + self.dense_item_features(x["items_features"]) \
              + self.embed_user(x["user"]) + self.embed_item(x["item"])
        return (torch.sum(fc, dim=1) + self.bias).unsqueeze(1)


class FeaturesEmbedding(torch.nn.Module):
    """
    Class to get feature embeddings
    """

    def __init__(self, users_dim, items_dim, user_feature_dim, item_feature_dim, embed_dim=20):
        super().__init__()
        self.dense_user_features = torch.nn.Linear(user_feature_dim, embed_dim)
        self.dense_item_features = torch.nn.Linear(item_feature_dim, embed_dim)
        self.embed_user = torch.nn.Embedding(users_dim, embed_dim)
        self.embed_item = torch.nn.Embedding(items_dim, embed_dim)
        
        torch.nn.init.xavier_uniform_(self.dense_user_features.weight.data)
        torch.nn.init.xavier_uniform_(self.dense_item_features.weight.data)
        torch.nn.init.xavier_uniform_(self.embed_user.weight.data)
        torch.nn.init.xavier_uniform_(self.embed_item.weight.data)

    def forward(self, x):
        """
        :param x: Long tensor of size ``(batch_size, num_fields)``
        """
        embed = torch.cat((self.dense_user_features(x["users_features"]).unsqueeze(1),
                          self.dense_item_features(x["items_features"]).unsqueeze(1),
                          self.embed_user(x["user"]).unsqueeze(1),
                          self.embed_item(x["item"]).unsqueeze(1)), 1)
        return embed


class FactorizationMachine(torch.nn.Module):
    """
        Class to instantiate a Factorization Machine model
    """

    def __init__(self, reduce_sum=True):
        super().__init__()
        self.reduce_sum = reduce_sum

    def forward(self, x):
        """
        :param x: Float tensor of size ``(batch_size, num_fields, embed_dim)``
        """
        square_of_sum = torch.sum(x, dim=1) ** 2
        sum_of_square = torch.sum(x ** 2, dim=1)
        ix = square_of_sum - sum_of_square
        if self.reduce_sum:
            ix = torch.sum(ix, dim=1, keepdim=True)
        return 0.5 * ix


class MultiLayerPerceptron(torch.nn.Module):
    """
    Class to instantiate a Multilayer Perceptron model
    """

    def __init__(self, input_dim, embed_dims, dropout, output_layer=True):
        super().__init__()
        layers = list()
        for embed_dim in embed_dims:
            layers.append(torch.nn.Linear(input_dim, embed_dim))
            layers.append(torch.nn.BatchNorm1d(embed_dim))
            layers.append(torch.nn.ReLU())
            layers.append(torch.nn.Dropout(p=dropout))
            input_dim = embed_dim
        if output_layer:
            layers.append(torch.nn.Linear(input_dim, 1))
        self.mlp = torch.nn.Sequential(*layers)

    def forward(self, x):
        """
        :param x: Float tensor of size ``(batch_size, num_fields, embed_dim)``
        """
        return self.mlp(x)

