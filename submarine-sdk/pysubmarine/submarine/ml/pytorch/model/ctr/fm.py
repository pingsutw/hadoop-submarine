from submarine.ml.pytorch.layers.core import FieldLinear
from submarine.ml.pytorch.layers.core import FieldEmbedding
from submarine.ml.pytorch.layers.core import PairwiseInteraction

from torch import nn


class FM(nn.Module):
    def __init__(self, field_dims, embedding_dim, out_features):
        super().__init__()
        self.field_linear = FieldLinear(field_dims=field_dims, out_features=out_features)
        self.field_embedding = FieldEmbedding(field_dims=field_dims, embedding_dim=embedding_dim)
        self.pairwise_interaction = PairwiseInteraction()

    def forward(self, x):
        """
        :param x: torch.LongTensor (batch_size, num_fields)
        """
        return self.field_linear(x) + self.pairwise_interaction(self.field_embedding(x))
