import torch
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split

class FetchDataset(Dataset):
    def __init__(self, X, Y, x_dtype = torch.float32, y_dtype = torch.float32):
        self.X = X
        self.Y = Y
        self.x_dtype = x_dtype
        self.y_dtype = y_dtype

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return {
            'x' : torch.tensor(self.X[idx], dtype = self.x_dtype),
            'y' : torch.tensor(self.Y[idx], dtype = self.y_dtype)
        }

class FetchDataLoader:
    def __init__(self, features, target):
        self.X = features
        self.Y = target
        
    def get_dataloader(self, batch_size = 32, sampler = None, num_workers = 0, drop_last = False, shuffle = False):
        dataset = FetchDataset(self.X, self.Y)
        return DataLoader(dataset, batch_size = batch_size, sampler = sampler, num_workers = num_workers, drop_last = drop_last, shuffle = shuffle)

    def get_dataloader_splits(self, test_size = 0.25, random_state = 0, stratify_on_y = True, batch_size = 32):
        if stratify_on_y:
            x_train, x_test, y_train, y_test = train_test_split(self.X, self.Y, random_state = random_state, stratify = self.Y)
        else:
            x_train, x_test, y_train, y_test = train_test_split(self.X, self.Y, random_state = random_state)
        
        train_dataset = FetchDataset(x_train, y_train)
        test_dataset = FetchDataset(x_test, y_test)

        trainloader = DataLoader(train_dataset, batch_size = batch_size)
        testloader = DataLoader(test_dataset, batch_size = batch_size)
        return trainloader, testloader