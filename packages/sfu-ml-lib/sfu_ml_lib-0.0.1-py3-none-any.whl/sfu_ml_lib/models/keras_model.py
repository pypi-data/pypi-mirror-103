import json
import os
from abc import ABC
from typing import List, Dict, Mapping, Tuple, Optional, TypeVar, Callable, Iterable, Any

import sfu_data_io.helpers as io
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.callbacks import Callback

import sfu_ml_lib.base.metrics as metric_helpers
from sfu_ml_lib.base.dataset import BatchType
from sfu_ml_lib.base.metrics import Metric, MetricKeyType, NumericType
from sfu_ml_lib.metrics.aggregator import KerasMetric
from sfu_ml_lib.models.schema import Schema


T = TypeVar('T')
W = TypeVar('W')
Z = TypeVar('Z')
BatchFunction = Callable[[], Iterable[BatchType]]


class KerasModel(keras.Model, ABC):
    input_schema: Schema

    @classmethod
    def deconstruct_inputs(cls, features: T, targets: W, weights: Optional[Z] = None) -> Tuple[T, W, Optional[Z]]:
        """
        Converts the outputs of a tf.Dataset into features, targets and optional weights.
        Used in combination with `deconstruct_inputs(*args)`.
        """
        return features, targets, weights

    @classmethod
    def to_metric(cls, label: str) -> MetricKeyType:
        try:
            return Metric(label)
        except ValueError:
            return label

    @classmethod
    def convert_metrics(cls, metrics: Mapping[str, tf.Tensor]) -> Mapping[MetricKeyType, NumericType]:
        return {
            cls.to_metric(label): value.numpy()
            for label, value
            in metrics.items()
        }

    @classmethod
    def from_config_path(cls, path: str, **kwargs) -> 'KerasModel':
        with io.open(os.path.join(path, 'config.json'), mode='r') as json_file:
            config = json.load(json_file)

        config.update(kwargs)

        return cls.from_config(config)

    @classmethod
    def from_config(cls, config: Mapping[str, Any], custom_objects=None) -> 'KerasModel':
        return cls(**config)

    def save_config(self, path: str) -> None:
        with io.open(os.path.join(path, 'config.json'), mode='w') as json_file:
            json.dump(self.get_config(), json_file)

    def get_metrics(self) -> Mapping[str, tf.Tensor]:
        metrics: Dict[str, tf.Tensor] = {}

        for metric in self.metrics_copy:
            if isinstance(metric, KerasMetric):
                metrics.update(metric.get_metrics())
            else:
                metrics[metric.name] = metric.result()

        return metrics

    def reset_metrics(self) -> None:
        for metric in self.metrics_copy:
            metric.reset_states()

    def create_tf_dataset(self, batches: BatchFunction, queue_size: int = -1) -> tf.data.Dataset:
        tensorflow_dataset = tf.data.Dataset.from_generator(
            generator=batches,
            output_types=self.input_schema.get_types(),
            output_shapes=self.input_schema.get_shapes(),
        )

        return tensorflow_dataset.prefetch(queue_size)

    @tf.function
    def _train_dataset(self, dataset: tf.data.Dataset) -> Mapping[str, tf.Tensor]:
        self.reset_metrics()

        for arguments in dataset:
            features, targets, weights = self.deconstruct_inputs(*arguments)

            predictions = self(features, training=True)

            loss = self.loss(targets, predictions, weights)
            if len(self.losses) > 0:
                loss += tf.add_n(self.losses)

            gradients = tf.gradients(loss, self.trainable_weights)
            self.optimizer.apply_gradients(zip(gradients, self.trainable_weights))

            for metric in self.metrics_copy:
                metric(targets, predictions, weights)

        metrics = self.get_metrics()

        return metrics

    def train_dataset(self, batches: BatchFunction) -> Mapping[MetricKeyType, NumericType]:
        """
        Trains a dataset given a generator of input batches. For example:
        ```
        train_dataset(lambda: ((np.random.random((10, 10)), None) for _ in range(100)))
        ```
        If the batching function requires some arguments, they can be curried:
        ```
        train_dataset(functools.partial(dataset.get_batches, batch_size=100))
        ```
        :param batches: A function that receives no arguments and returns an iterator of `BatchType`.
        :return: A dictionary of metrics.
        """
        return self.convert_metrics(self._train_dataset(self.create_tf_dataset(batches)))

    @tf.function
    def _test_dataset(self, dataset: tf.data.Dataset) -> Mapping[str, tf.Tensor]:
        self.reset_metrics()

        for arguments in dataset:
            features, targets, weights = self.deconstruct_inputs(*arguments)

            predictions = self(features, training=False)

            for metric in self.metrics_copy:
                metric(targets, predictions, weights)

        metrics = self.get_metrics()

        return metrics

    def test_dataset(self, batches: BatchFunction) -> Mapping[MetricKeyType, NumericType]:
        """
        Please look at `train_dataset` for details on how to construct `batches`.
        """
        return self.convert_metrics(self._test_dataset(self.create_tf_dataset(batches)))

    def fit_dataset(
            self,
            train_batches: BatchFunction,
            max_num_epochs: int = 1,
            validation_batches: Optional[BatchFunction] = None,
            test_batches: Optional[BatchFunction] = None,
            callbacks: Optional[List[Callback]] = None) -> None:
        """
        Please look at `train_dataset` for details on how to construct `batches`.
        """
        callbacks = callbacks if callbacks else []

        for callback in callbacks:
            callback.set_model(self)
            callback.on_train_begin()

        for epoch in range(max_num_epochs):
            for callback in callbacks:
                callback.on_epoch_begin(epoch)

            train_metrics = self.train_dataset(train_batches)
            metrics = metric_helpers.prefix_metrics_train(train_metrics)

            if validation_batches is not None:
                validation_metrics = self.test_dataset(validation_batches)
                metrics.update(metric_helpers.prefix_metrics_validation(validation_metrics))

            for callback in callbacks:
                callback.on_epoch_end(epoch, metrics)

            if self.stop_training:
                break

        test_metrics = None

        if test_batches is not None:
            test_metrics = metric_helpers.prefix_metrics_test(self.test_dataset(test_batches))

        for callback in callbacks:
            callback.on_train_end(test_metrics)

    def compile(
            self,
            optimizer='rmsprop',
            loss=None,
            metrics=None,
            loss_weights=None,
            sample_weight_mode=None,
            weighted_metrics=None,
            **kwargs) -> None:
        """
        There's a bug in TensorFlow 2.1 that does not set the `metrics` property when compiling.
        So we create our own. This is a hack that should be removed as soon as they fix it.
        """
        super().compile(optimizer, loss, metrics, loss_weights, sample_weight_mode, weighted_metrics, **kwargs)

        self.metrics_copy = metrics if metrics else []
