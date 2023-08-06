"""PubSub Events.

Declare here all PubSub topics which will be used.

These Topics will be created on AWS, when you send his first message.

"""
from enum import Enum


class UserEvents(Enum):
    USER_REGISTERED = "user_registered"
    USER_ACTIVATED = "user_activated"
    USER_LOGGED_IN = "user_logged_in"


class AccountEvents(Enum):
    BANK_ACCOUNT_REGISTERED = "user_registered"
    AD_ACCOUNT_REGISTERED = "user_activated"


class ProposalEvents(Enum):
    PROPOSAL_SELECTED = "proposal_selected"
