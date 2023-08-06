import numpy as np



# pylint: disable=import-error
import cit_fl_participation.serialization.vector.vector_pb2 as vpb2

from cit_fl_participation.serialization.vector.conversion import (
    numpy_array_to_protobuf_vector,
    protobuf_vector_to_numpy_array,
)


def serialize_numpy_array(array: np.ndarray) -> str:
    return numpy_array_to_protobuf_vector(array).SerializeToString()

def deserialize_numpy_array(serialized: str) -> np.ndarray:
    vector = vpb2.Vector()
    vector.ParseFromString(serialized)

    return protobuf_vector_to_numpy_array(vector)