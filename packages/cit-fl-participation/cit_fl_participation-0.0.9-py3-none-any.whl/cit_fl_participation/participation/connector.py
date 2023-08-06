import threading
import string
import random
from abc import ABC, abstractmethod
from cit_fl_participation.coordinator_interface.coordinator_pb2 import HeartbeatResponse
from numpy import ndarray

from cit_fl_participation.participation.store import AbstractLocalWeightsWriter, AbstractGlobalWeightsReader

def random_string(string_length=12):
    '''Generates a random string of fixed length'''
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(string_length))


class Connector(ABC):
    '''
    The abstract Connector handles the connection to the FL coordinator

    Args:
        heartbeat_time (int): Interval to wait between sending heartbeats to the coordinator
        local_weights_writer: ``AbstractLocalWeighsWriter`` to upload weigts
        global_weighs_reader: ``AbstractGlobalWeighsReader`` to download weigts
    '''
    def __init__(self,
                heartbeat_time : int,
                local_weights_writer: AbstractLocalWeightsWriter,
                global_weights_reader: AbstractGlobalWeightsReader
            ) -> None:
        super(Connector, self)
        self.heartbeat_time: int = heartbeat_time
        self.round: int = -1
        self.state: HeartbeatResponse.LearningState = 0   
        self.id: str = random_string(16)
        self.local_weights_writer: AbstractLocalWeightsWriter = local_weights_writer
        self.global_weights_reader: AbstractGlobalWeightsReader = global_weights_reader

    def write_local_weights(self, weights: ndarray, round: int) -> None:
        '''
        Uploads the local weights
        
        Args:
            weighst (ndarray): weights to upload
            round (int): current reound
        '''
        self.local_weights_writer.write_weights(round, self.id, weights)

    def read_global_weights(self, round: int) -> ndarray:
        '''
        Downloads the global weights
        
        Args:
            round (int): current reound
        
        Return:
            ndarray: downloaded weights
        '''
        return self.global_weights_reader.read_weights(round)

    @abstractmethod
    def rendezvous(self) -> bool:
        '''
        Redezvous with coordinator

        Returns:
            bool: successful rendezvous
        '''
        raise NotImplementedError

    @abstractmethod
    def heartbeat_request(self) -> (bool, HeartbeatResponse.LearningState, int):
        '''
        Sends a hearbeat to the coordinator

        Returns:
            bool: connected?
            State: coordinator state
            int: round number
        '''
        raise NotImplementedError

    @abstractmethod
    def start_training(self) -> int:
        '''
        Tells the coordinator the training started
        
        Returns:
            int: number of epochs
        '''
        raise NotImplementedError

    @abstractmethod
    def end_training(self, num_samples: int) -> None:
        '''
        Tells the coordinator that the training ended

        Args:
            num_samples: number of samples in training required for weighted aggregation
        '''
        raise NotImplementedError
   