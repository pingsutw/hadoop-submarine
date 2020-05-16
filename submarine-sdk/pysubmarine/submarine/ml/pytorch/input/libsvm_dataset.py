from ..utils import read_file

import torch
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torch.utils.data.distributed import DistributedSampler
import pandas as pd


class LIBSVMDataset(Dataset):
    def __init__(self, path):
        self.data, self.label = self.preprocess_data(read_file(path))

    def __getitem__(self, idx):
        return self.data.iloc[idx], self.label.iloc[idx]

    def __len__(self):
        return len(self.data)

    def preprocess_data(self, stream):
        def _convert_line(line):
            feat_ids = []
            feat_vals = []
            for x in line:
                feat_id, feat_val = x.split(':')
                feat_ids.append(int(feat_id))
                feat_vals.append(float(feat_val))
            return (torch.as_tensor(feat_ids, dtype=torch.int64),
                    torch.as_tensor(feat_vals, dtype=torch.float32))

        df = pd.read_table(stream, header=None)
        df = df.loc[:, 0].str.split(n=1, expand=True)
        label = df.loc[:, 0].apply(int)
        data = df.loc[:, 1].str.split().apply(_convert_line)
        return data, label

    def collate_fn(self, batch):
        data, label = tuple(zip(*batch))
        feat_id, feat_val = tuple(zip(*data))
        return (
            torch.stack(feat_val, dim=0).type(torch.long),
            torch.as_tensor(label, dtype=torch.float32).unsqueeze(dim=-1)
        )


def libsvm_input_fn(filepath, batch_size=256, num_threads=1, **kwargs):
    def _input_fn():
        dataset = LIBSVMDataset(filepath)
        sampler = DistributedSampler(dataset)
        return DataLoader(
            dataset=dataset,
            batch_size=batch_size,
            sampler=sampler,
            num_workers=num_threads,
            collate_fn=dataset.collate_fn
        )
    return _input_fn
