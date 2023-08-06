import os
import numpy as np
import pandas as pd

import torch
import torch.utils.data
import torch.nn.functional as F

from torch.utils.data import DataLoader

from scipy import sparse as sp
from scipy.sparse import csr_matrix



def get_csr_matrix(interactions_scaled, customer_features, item_category_scaled):

    interaction_f = csr_matrix(interactions_scaled)
    user_f = csr_matrix(customer_features) 
    item_f = csr_matrix(item_category_scaled)

    return interaction_f, user_f, item_f


def interaction_masking(interactions):
    '''
    This function will "mask" (a.k.a "hide") 20% of original interactions
    Masked items wil be considered not purchased

    '''
    mask_size = len(interactions.data)
    mask = np.random.choice(a=[False, True], size=mask_size, p=[.2, .8])
    not_mask = np.invert(mask)

    train_interactions = csr_matrix((interactions.data[mask],
                                        (interactions.row[mask],
                                         interactions.col[mask])),
                                       shape=interactions.shape)

    test_interactions = csr_matrix((interactions.data[not_mask],
                                       (interactions.row[not_mask],
                                        interactions.col[not_mask])),
                                      shape=interactions.shape)

    return train_interactions, test_interactions


class RetailDataset(torch.utils.data.Dataset):
    """ PyTorch Dataset for Training
   
    """

    def __init__(self, sparse_matrix, user_features, item_features, device='cpu'):

        if not isinstance(sparse_matrix, sp.coo_matrix):
          sparse_matrix = sp.coo_matrix(sparse_matrix)

        self.users, self.items, self.labels = self.get_dataset(sparse_matrix)
        self._item_features = torch.tensor(item_features.toarray(), dtype=torch.float32, device=device)
        self._user_features = torch.tensor(user_features.toarray(), dtype=torch.float32, device=device)

    def __len__(self):
        return len(self.users)
  
    def __getitem__(self, index):
        return {
            "user": self.users[index], 
            "item": self.items[index], 
            "target": self.labels[index], 
            "users_features": self._user_features[self.users[index], :], 
            "items_features": self._item_features[self.items[index], :]
            }

    def get_dataset(self, interactions):

        users, items, labels = [], [], []
        user_item_set = set(zip(interactions.row, interactions.col))
        num_negatives = 4
        for u, i in user_item_set:
            users.append(u)
            items.append(i)
            labels.append(1)
            for _ in range(num_negatives):
                negative_item = np.random.choice(interactions.shape[1])
                while (u, negative_item) in user_item_set:
                    negative_item = np.random.choice(interactions.shape[1])
                users.append(u)
                items.append(negative_item)
                labels.append(0)

        return torch.tensor(users), torch.tensor(items), torch.tensor(labels)


def get_dataset(dataset_name, path_interactions, path_customer_features, path_item_category, batch_size, muestra=None):
    
    interactions_scaled = pd.read_csv(path_interactions).set_index('Customer ID')
    customer_features = pd.read_csv(path_customer_features).set_index('Customer ID')
    item_category_scaled = pd.read_csv(path_item_category).set_index('Material')

    interaction_f, user_f, item_f = get_csr_matrix(interactions_scaled, customer_features, item_category_scaled)

    # Create a masked train and test dataset of the interaction features
    train_interactions, test_interactions = interaction_masking(interaction_f.tocoo())

    # Feed the user and item features
    user_features  = user_f
    item_features = item_f

    num_users = interaction_f.shape[0]
    num_items = interaction_f.shape[1]

    train_dataset = RetailDataset(train_interactions[0:muestra, 0:muestra], user_features, item_features)
    test_dataset = RetailDataset(test_interactions[0:muestra, 0:muestra], user_features, item_features)

    train_data_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    test_data_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=0)

    return train_data_loader, test_data_loader, user_features, item_features, num_users, num_items

