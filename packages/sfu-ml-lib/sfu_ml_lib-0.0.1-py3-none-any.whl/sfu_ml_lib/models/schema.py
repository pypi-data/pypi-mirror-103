from typing import Union, TypeVar, Callable, Tuple, Iterable

import tensorflow as tf


T = TypeVar('T')
Specification = Union[tf.SparseTensorSpec, tf.RaggedTensorSpec, tf.TensorSpec]
Structure = Union[T, Iterable['Structure']]  # type: ignore
TupleStructure = Union[T, Tuple['TupleStructure', ...]]  # type: ignore


class Schema:
    def __init__(self, specification: Structure[Specification]) -> None:
        self.specification = specification

    @classmethod
    def transform(
            cls,
            specification: Structure[Specification],
            transformer: Callable[[tf.TensorSpec], T]) -> TupleStructure[T]:

        if isinstance(specification, Iterable):
            return tuple(cls.transform(item, transformer) for item in specification)
        else:
            return transformer(specification)

    def get_types(self) -> TupleStructure[tf.DType]:
        return self.transform(self.specification, lambda specification: specification.dtype)

    def get_shapes(self) -> TupleStructure[tf.TensorShape]:
        return self.transform(self.specification, lambda specification: specification.shape)
