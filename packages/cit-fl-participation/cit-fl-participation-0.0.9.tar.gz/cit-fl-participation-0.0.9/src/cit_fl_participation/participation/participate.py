import logging
import numpy as np
import threading

from cit_fl_participation.coordinator_interface.coordinator_pb2 import HeartbeatResponse

from cit_fl_participation.participation.connector import Connector
from cit_fl_participation.participation.training import AbstractTrainer

logger = logging.getLogger('participation')

class ParticipationServicer:

    def __init__(self, connector: Connector, trainer: AbstractTrainer) -> None:
        self._active: threading.Lock = threading.Lock()
        self._lock: threading.Lock = threading.Lock()
        self.connector: Connector = connector
        self.trainer = trainer

    def _monitor_heartbeats(self, terminate_event: threading.Event) -> None:
        logger.info("Monitoring heartbeats")
        while not terminate_event.is_set():
            logger.debug("Sending Heartbeat")
            connected, state, current_round = self.connector.heartbeat_request()
            if not connected:
                terminate_event.set()
            else:
                # check for state changes
                if self.connector.state != state or self.connector.round != current_round:
                    old_state = self.connector.state
                    old_round = self.connector.round
                    thread = threading.Thread(
                                target=self._handle_changed,
                                args=(old_state, state, old_round, current_round, terminate_event)
                            )
                    thread.start()

                terminate_event.wait(self.connector.heartbeat_time)

    def _handle_changed(
            self,
            old_state: HeartbeatResponse.LearningState,
            new_state: HeartbeatResponse.LearningState,
            old_round: int,
            new_round: int,
            terminate_event: threading.Event) -> None:
        
        logger.debug(f"Round updated: {old_round}->{new_round}")
        logger.debug(f"State updated: {HeartbeatResponse.LearningState.Name(old_state)}->{HeartbeatResponse.LearningState.Name(new_state)}")
        self.connector.state = new_state
        self.connector.round = new_round

        if new_state == HeartbeatResponse.LearningState.TRAINIG:
            with self._lock:
                self._perform_round(new_round)
        elif new_state == HeartbeatResponse.LearningState.FINISHED:
            with self._lock:
                self._finish_training()
                terminate_event.set()

    def _perform_round(self, round: int) -> None:
        logger.info(f"Starting round {round}")
        # start training
        epochs = self.connector.start_training()
        # download global weights
        weights = self.connector.read_global_weights(round=round)

        # train model
        weights, num_samples = self.trainer.train(weights, epochs)

        # upload local weights
        self.connector.write_local_weights(weights=weights, round=round)
        # end training
        self.connector.end_training(num_samples)

    def _finish_training(self) -> None:
        logger.info("Finished training")
        weights = self.connector.read_global_weights(round=self.connector.round + 1)
        self.trainer.training_finished(weights)

    def start(self, terminate_event: threading.Event = threading.Event()) -> None:
        with self._active:
            if self.connector.rendezvous():
                try:
                    self._monitor_heartbeats(terminate_event)
                except KeyboardInterrupt:
                    terminate_event.set()
            else:
                logger.warning("No Rendezvous")
