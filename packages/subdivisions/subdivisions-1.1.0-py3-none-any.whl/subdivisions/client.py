import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import arrow
from loguru import logger

from subdivisions.base import AWSClientMixin, SubDivisions
from subdivisions.builders.events import SubDivisionsEventsBuilder
from subdivisions.builders.sns import SubDivisionsSNSBuilder
from subdivisions.builders.sqs import SubDivisionsSQSBuilder
from subdivisions.config import sub_config
from subdivisions.exceptions import PubSubException

# TODO(Chris) Precisamos de um cloudformation ou terraform para:
#  1. Chave KMS "PubSubKey"
#  2. Atualizar o IAM do barramento "default"
#  3. CloudTrail
#  4. IAM dos logs do SNS de entrega


@dataclass
class SubClient(SubDivisions, AWSClientMixin):
    _event_name: Optional[str] = None
    received_handlers: Optional[List[Tuple[str, str]]] = field(default_factory=list)

    @property
    def event_name(self):
        return SubDivisionsEventsBuilder(topic=self.topic).event_name

    def _prepare_subscribe(self):
        events_builder = SubDivisionsEventsBuilder(topic=self.topic)
        # 1. If Topic exists, proceed
        if not events_builder.topic_exists():
            # 2. Raise and suggest best match if found
            if events_builder.similar_topic_exists():
                raise PubSubException(
                    f"Topic '{self.event_name}' not found. "
                    f"Did you mean '{events_builder.best_match}'?"
                )
            raise PubSubException(f"Topic '{self.event_name}' not found.")

        # 2. If queue does not exist, create it
        sqs_builder = SubDivisionsSQSBuilder(topic=self.topic)
        if not sqs_builder.queue_exists():
            # Create SQS Queue with encryption and dead_letter

            dead_letter_queue_arn = sqs_builder.create_queue(
                is_dead_letter=True
            ).queue_arn
            topic_queue_arn = sqs_builder.create_queue(
                dead_letter_arn=dead_letter_queue_arn
            ).queue_arn

            # Subscribe Queue with SNS
            sns_builder = SubDivisionsSNSBuilder(topic=self.topic)
            sns_builder.create_sns_topic()
            sns_builder.subscribe_sns_topic(topic_queue_arn)

    def _create_topic(self):
        # 2. Create SNS Topic
        sns_builder = SubDivisionsSNSBuilder(topic=self.topic)
        topic_sns_arn = sns_builder.create_sns_topic().sns_arn

        # Create/Update Eventbridge Rule
        events_builder = SubDivisionsEventsBuilder(topic=self.topic)
        events_builder.put_rule()
        events_builder.put_target(topic_sns_arn)

    def _prepare_send_message(self):
        # 1. If Topic exists, send message
        events_builder = SubDivisionsEventsBuilder(topic=self.topic)
        if events_builder.topic_exists():
            return
        # 2. If not exists, check for similar. If exists raise and suggest best match
        if events_builder.similar_topic_exists():
            raise PubSubException(
                f"Topic '{self.event_name}' not found. "
                f"Did you mean '{events_builder.best_match}'?"
            )

        # 3. If not exists and we dont find similar,
        # and auto-create are forbidden, raise error
        if not sub_config.auto_create_new_topic:
            raise PubSubException(
                f"Topic '{self.event_name}' not found. Auto creation not allowed."
            )

        # 4. Create new Topic
        self._create_topic()

    def send(self, message: Dict[Any, Any]):

        if not isinstance(message, dict):
            raise ValueError("PubSub Message must be a dictionary")

        self._prepare_send_message()

        logger.info(f"Send message for topic: {self.topic}...")

        payload = {
            "event": self.topic,
            "datetime": arrow.utcnow().isoformat(),
            "payload": message,
        }

        logger.debug(
            f"Source is: {sub_config.source_name}. "
            f"Detail Type is: {self.topic}. Message is: {payload}"
        )
        response = self.get_client("events").put_events(
            Entries=[
                {
                    "DetailType": self.topic,
                    "Source": sub_config.source_name,
                    "Detail": json.dumps(payload),
                }
            ]
        )
        logger.debug(f"Send message response: {response}")

        if response["FailedEntryCount"] > 0:
            raise PubSubException("Cannot send message.")
        logger.info(f"Message send successfully for topic: {self.topic}")

    def get_messages(self, from_dead_letter: bool = False, auto_remove: bool = False):

        self._prepare_subscribe()

        sqs_builder = SubDivisionsSQSBuilder(topic=self.topic)
        queue_url = sqs_builder.get_queue(from_dead_letter=from_dead_letter).queue_url

        message_list = []
        while True:
            response = self.get_client("sqs").receive_message(
                QueueUrl=queue_url, MaxNumberOfMessages=10
            )
            if not response.get("Messages"):
                break

            message_list += [
                json.loads(json.loads(message["Body"])["Message"])
                for message in response["Messages"]
            ]
            self.received_handlers += [
                (queue_url, message["ReceiptHandle"])
                for message in response["Messages"]
            ]

        logger.info(
            f"Received {len(message_list)} message(s) "
            f"from queue: {sqs_builder.queue_name}."
        )

        if (sub_config.auto_remove_from_queue or auto_remove) and len(
            self.received_handlers
        ) > 0:
            self.delete_received_messages()
        else:
            logger.debug(
                f"Received {len(message_list)} message(s) "
                f"are still in queue: {sqs_builder.queue_name}."
            )

        return message_list

    def delete_received_messages(self):
        for queue_url, receipt_handle in self.received_handlers:
            self.get_client("sqs").delete_message(
                QueueUrl=queue_url, ReceiptHandle=receipt_handle
            )
        queue_name = SubDivisionsSQSBuilder(topic=self.topic).get_queue
        logger.info(
            f"Removed {len(self.received_handlers)} "
            f"message(s) from queue: {queue_name}."
        )
        self.received_handlers = []
