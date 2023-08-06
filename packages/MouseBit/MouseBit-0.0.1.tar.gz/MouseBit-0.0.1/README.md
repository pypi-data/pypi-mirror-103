# MouseBit

An easy to use PyTorch utility for easy DataLoader creation. DataLoader creation can be redundant at times, keeping that in mind MouseBit was created to quickly create DataLoaders quickly. 

## Tutorial

Currently it only supports structured data but I'll be extending it's support for image and text data soon.

###### Creating Dataloaders for Structured Data

In order to get the dataloader start by creating the FetchDataLoader instance and calling get_dataloader method to get dataloader for the corresponding data.

```
>>> from mousebit.structured import FetchDataLoader
>>> msb = FetchDataLoader(X,Y)
>>> dataloader = msb.get_dataloader(self, batch_size = 64, drop_last = True, shuffle = True)
```

###### Getting Train and Test Dataloaders for Structured Data

To get train and test dataloaders MouseBit has get_dataloader_splits method in FetchDataLoader.

```
>>> from mousebit.structured import FetchDataLoader
>>> msb = FetchDataLoader(X,Y)
>>> trainloader, testloader = msb.get_dataloader_splits(self, batch_size = 64, stratify_on_y = False, random_state = 101, test_size = 0.3)
```
