import numpy as np
from typing import List

# pylint: disable=import-error
import cit_fl_participation.serialization.vector.vector_pb2 as vpb2

def numpy_array_to_protobuf_vector(numpy_array: np.ndarray) -> vpb2.Vector:
    def rec_nparr_to_pbvec(nparr: np.ndarray, pbvec: vpb2.Vector):
        pbvec.dimension = nparr.shape[0]
        pbvec.nested = len(nparr.shape) > 1
        if pbvec.nested:
            for array in nparr:
                rec_nparr_to_pbvec(array, pbvec.vectors.add())
        else:
            for value in nparr:
                pbvec.values.append(value)

    vector = vpb2.Vector()

    rec_nparr_to_pbvec(numpy_array, vector)

    return vector

def protobuf_vector_to_numpy_array(protobuf_vector: vpb2.Vector) -> np.ndarray:
    def rec_pbvec_to_list(pbvec: vpb2.Vector):
        if pbvec.nested:
            return np.array([rec_pbvec_to_list(vector) for vector in pbvec.vectors])
        else:
            return pbvec.values
    
    return np.array(rec_pbvec_to_list(protobuf_vector))