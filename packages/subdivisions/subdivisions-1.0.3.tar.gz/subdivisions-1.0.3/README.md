# Welcome to Subdivisions

[![PyPI](https://img.shields.io/pypi/v/subdivisions)](https://pypi.org/project/subdivisions/)
[![Publish](https://github.com/access55/subdivisions/workflows/publish/badge.svg)](https://github.com/access55/subdivisions/actions)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/subdivisions)](https://www.python.org)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

[A55 Python library for PubSub Messaging.](https://www.youtube.com/watch?v=EYYdQB0mkEU)

### Install

```toml
# pyproject.toml
[tool.subdivisions]
default_prefix = "a55"
source_name = "YourProjectName"

[tool.poetry.dependencies]
subdivisions = "*"
```
Run `poetry update`

### Usage
#### Send Messages
```python
from enum import Enum
from subdivisions.client import SubClient

class ProjectTopics(Enum):
    USER_REGISTERED = "user_registered"

client = SubClient()
client.topic = ProjectTopics.USER_REGISTERED # or just "user_registered"
client.send({"foo": "bar"})
```

#### Receive Messages
```python
from enum import Enum
from subdivisions.client import SubClient

class ProjectTopics(Enum):
    USER_REGISTERED = "user_registered"

client = SubClient()
client.topic = ProjectTopics.USER_REGISTERED # or just "user_registered"
messages = client.get_messages()
# Process messages
client.delete_received_messages()
```

### AWS Credentials

Subdivisions will use AWS environment variables. If you need to define another credentials, use the following variables:

```env
SUBDIVISIONS_USE_AWS_ENV_VARS="false"
SUBDIVISIONS_AWS_ACCESS_KEY_ID="your id"
SUBDIVISIONS_AWS_SECRET_ACCESS_KEY="your key"
SUBDIVISIONS_AWS_SESSION_TOKEN="your token" # optional
```

### Configuration

Configure subdivisions options in `pyproject.toml` file, inside `[tool.subdivisions]` table:

```toml
# pyproject.toml
[tool.subdivisions]
aws_region = "us-east-1"            # AWS Region
pub_key = "alias/PubSubKey"         # KMS PubSubKey (must be created first)
sqs_tags = []                       # SQS tags for new queues. Example [{"foo": "bar"}]
queue_prefix = ""                   # Prefix for new SQS queues
queue_suffix = ""                   # Suffix for new SQS queues
queue_max_receive_count = 1000      # SQS MaxReceiveCount setting
sns_prefix = ""                     # Prefix for new SNS topics
sns_suffix = ""                     # Suffix for new SNS topics
sns_tags = []                       # SNS tags for new topics. Example [{"foo": "bar"}]
event_prefix = ""                   # Prefix for new Eventbride rules
event_suffix = ""                   # Suffix for new Eventbride rules
event_tags = []                     # Eventbridge tags for new rules. Example [{"foo": "bar"}]
event_bus = "default"               # Eventbridge Bus
source_name = "Subdivisions"        # Eventbridge default source name
auto_create_new_topic = true        # Auto create new topic if not exists in Eventbridge
auto_remove_from_queue = false      # Acknowledge first messages on receive
use_aws_env_vars = true             # Use AWS default env vars. If false append "SUBDIVISION_" on env vars. Example: "SUBDIVISION_AWS_ACCESS_KEY_ID"
default_prefix = "subdivisions"     # Default prefix for all sns, sqs and rule created
default_suffix = ""                 # Default suffix for all sns, sqs and rule created
```

All options above can be configured in environment variables. Just append `SUBDIVISIONS_` on name. Example: `SUBDIVISIONS_SOURCE_NAME="my_project"`
