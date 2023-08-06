import typing
from abc import ABC, abstractmethod
from typing import Tuple, Optional, Generator, TypeVar, Union

import numpy as np


T = TypeVar('T')
TensorTuple = Union[np.ndarray, Tuple[np.ndarray, ...]]
BatchType = Union[
    Tuple[TensorTuple, None],
    Tuple[TensorTuple, TensorTuple],
    Tuple[TensorTuple, TensorTuple, np.ndarray],
]


class Dataset(ABC):
    size: int
    targets: Optional[np.ndarray] = None

    @abstractmethod
    @typing.no_type_check
    def get_batches(self, *args) -> Generator[BatchType, None, None]:
        ...

    @abstractmethod
    def subset(self: T, indices: np.ndarray) -> T:
        ...
