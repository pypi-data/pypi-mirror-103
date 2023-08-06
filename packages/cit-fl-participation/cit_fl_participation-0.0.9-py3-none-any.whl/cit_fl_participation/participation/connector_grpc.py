import logging
import grpc
import os

from cit_fl_participation.coordinator_interface import coordinator_pb2_grpc
from cit_fl_participation.coordinator_interface.coordinator_pb2 import (
    EndTrainingRoundRequest,
    EndTrainingRoundResponse,
    HeartbeatRequest,
    HeartbeatResponse,
    RendezvousResponse,
    RendezvousRequest,
    StartTrainingRoundRequest,
    StartTrainingRoundResponse,
)
from cit_fl_participation.participation.connector import Connector
from cit_fl_participation.participation.store import (
    AbstractLocalWeightsWriter,
    AbstractGlobalWeightsReader
)


class ConnectorGrpc(Connector):
    '''
    The ``ConnectorGrpc`` using GRPC to communicate with the coordinator

    Args:
        heartbear_time (int): Interval to wait between sending heartbeats to the coordinator
        coordinator_url (str): URL to reach the coordinator
        local_weights_writer: ``AbstractLocalWeighsWriter`` to upload weigts
        global_weighs_reader: ``AbstractGlobalWeighsReader`` to download weigts
    '''
    def __init__(self,
                heartbeat_time: int,
                coordinator_url: str,
                api_token:str,
                tsl_certificate: str,
                local_weights_writer: AbstractLocalWeightsWriter,
                global_weights_reader: AbstractGlobalWeightsReader
            ) -> None:
        Connector.__init__(self, heartbeat_time, local_weights_writer, global_weights_reader)
        self.target = coordinator_url
        self.api_token = api_token

        self.channel = None
        if tsl_certificate:
            # add secure channel
            certs = None
            try:
                with open(tsl_certificate, 'rb') as f:
                    certs = f.read()
            except IOError as e:
                print("Cannot load TLS certificate")
                exit(1)

            credentials = grpc.ssl_channel_credentials(root_certificates=certs)

            self.channel = grpc.secure_channel(coordinator_url, credentials)
            
        else:
            # insecure channel
            self.channel = grpc.insecure_channel(coordinator_url)

        self.stub = coordinator_pb2_grpc.CoordinatorServiceStub(self.channel)

    def __del__(self) -> None:
        if self.channel:
            self.channel.close()
            self.channel = None

    
    def heartbeat_request(self) -> (bool, HeartbeatResponse.LearningState, int):
        '''
        Sends a hearbeat to the coordinator

        Returns:
            bool: connected?
            State: coordinator state
            int: round number
        '''
        try:
            response = self.stub.Heartbeat(HeartbeatRequest())
            return(True, response.State, response.RoundNumber)
        except grpc.RpcError as e:
            logging.error("lost server connection")
            return (False, -1, -1)
    
    def rendezvous(self) -> bool:
        '''
        Redezvous with coordinator

        Returns:
            bool: successful rendezvous
        '''
        try:
            response = self.stub.Rendezvous(RendezvousRequest(ApiToken = self.api_token))
            if response and response.Participate == RendezvousResponse.ParticipationState.ACCEPTED:
                logging.debug(f"Rendezvous with {self.target}")
                return True
            return False
        except grpc.RpcError as e:
            print(e)
            logging.error("No server connection")
            return False
    
    def start_training(self) -> int:
        '''
        Tells the coordinator the training started
        
        Returns:
            int: number of epochs
        '''
        result = self.stub.StartRound(StartTrainingRoundRequest())
        return result.epochs

    def end_training(self, num_samples: int) -> None:
        '''
        Tells the coordinator that the training ended

        Args:
            num_samples: number of samples in training required for weighted aggregation
        '''
        self.stub.EndRound(EndTrainingRoundRequest(WeightsId=self.id, NumberSamples=num_samples))