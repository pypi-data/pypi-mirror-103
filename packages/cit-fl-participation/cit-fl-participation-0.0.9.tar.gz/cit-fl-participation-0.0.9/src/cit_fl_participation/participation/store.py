import boto3
from abc import ABC, abstractmethod
from numpy import ndarray
from io import BytesIO
from cit_fl_participation.config import StorageConfig

from cit_fl_participation.serialization.vector_serialization import (
    serialize_numpy_array,
    deserialize_numpy_array,
)

class AbstractLocalWeightsWriter(ABC):

    @abstractmethod
    def write_weights(self, round: int, id: str, weights: ndarray) -> None:
        raise NotImplementedError

class AbstractGlobalWeightsReader(ABC):
    @abstractmethod
    def read_weights(self) -> ndarray:
        raise NotImplementedError


class S3BaseClass:
    # pylint: disable=too-few-public-methods
    """A base class for implementating AWS S3 clients.

    Args:
        config: the storage configuration (endpoint URL, credentials, etc.)

    """

    def __init__(self, config: StorageConfig):
        self.config = config
        self.s3 = boto3.resource(  # pylint: disable=invalid-name
            "s3",
            endpoint_url=self.config.endpoint,
            aws_access_key_id=self.config.access_key_id,
            aws_secret_access_key=self.config.secret_access_key,
            # FIXME: not sure what this should be for now
            region_name="dummy",
            verify=False
        )


class S3LocalWeightsWriter(AbstractLocalWeightsWriter, S3BaseClass):
    """``AbstractLocalWeightsWriter`` implementor for AWS S3 storage
    backend.

    """

    def write_weights(self, round: int, id: str, weights: ndarray) -> None:
        """Store the given `weights`, corresponding to the given `round`.

        Args:
            round: A round number the weights correspond to.
            weights: The weights to store.
        """
        bucket = self.s3.Bucket(self.config.bucket)
        bucket.put_object(Body=serialize_numpy_array(weights), Key=f"{round}/{id}")

class S3GlobalWeightsReader(AbstractGlobalWeightsReader, S3BaseClass):
    """``AbstractGlobalWeightsReader`` implementor for AWS S3 storage
    backend.

    """

    def read_weights(self, round: int) -> ndarray:
        """Download the global weights for the given round, from an S3 bucket.

        Args:
            round: round number the weights correspond to

        Return:
            The weights read from the S3 bucket.
        """
        bucket = self.s3.Bucket(self.config.bucket)
        data = BytesIO()
        bucket.download_fileobj(f"{round}/global", data)
        # FIXME: not sure whether getvalue() copies the data. If so we
        # should probably prefer getbuffer() instead.
        return deserialize_numpy_array(data.getvalue())