'''
This module contains the functionality to participate on the federated learning
'''
from cit_fl_participation.participation.participate import ParticipationServicer
from cit_fl_participation.participation.connector import Connector
from cit_fl_participation.participation.connector_grpc import ConnectorGrpc
from cit_fl_participation.participation.training import AbstractTrainer
from cit_fl_participation.participation.store import (
    AbstractLocalWeightsWriter,
    S3LocalWeightsWriter,
    AbstractGlobalWeightsReader,
    S3GlobalWeightsReader
)