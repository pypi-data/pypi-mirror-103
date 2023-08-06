import logging
from pydantic import BaseModel
from dependency_injector import containers, providers
from applauncher.applauncher import Configuration
from confluent_kafka import Producer, Consumer


def consumer_reader(consumer):
    while True:
        try:
            msg = consumer.poll()
            if msg is None:
                continue
            if msg.error():
                error = msg.error()
                print(error)
            else:
                yield msg

        except Exception as e:
            print(e)


class KafkaDefaultTopicConfig(BaseModel):
    auto_offset_reset: str = 'earliest'


class KafkaConfig(BaseModel):
    bootstrap_servers: str
    session_timeout_ms: int = 6000
    default_topic_config: KafkaDefaultTopicConfig = KafkaDefaultTopicConfig()
    security_protocol: str = 'SASL_SSL'
    sasl_mechanisms: str = 'SCRAM-SHA-256'
    partition_assignment_strategy: str = 'roundrobin'
    sasl_username: str = ''
    sasl_password: str = ''
    group_id: str


def applauncher_config_to_confluent(config):
    c = dict()
    if not isinstance(config, dict):
        config = config.dict()

    for k, v in config.items():
        k = k.replace("_", ".")
        if isinstance(v, dict):
            c[k] = applauncher_config_to_confluent(v)
        else:
            c[k] = v
    if "bootstrap.servers" in c:
        if c["bootstrap.servers"].startswith("sasl://"):
            # sasl://username:password@servers
            credentials, servers = c["bootstrap.servers"][7:].split("@")
            username, password = credentials.split(":")
            c["bootstrap.servers"] = servers
            c["sasl.username"] = username
            c["sasl.password"] = password

    return c


class KafkaConsumer(Consumer):
    def __init__(self, config):
        super(KafkaConsumer, self).__init__(**applauncher_config_to_confluent(config))


class KafkaProducer(Producer):
    def __init__(self, config):
        super(KafkaProducer, self).__init__(**applauncher_config_to_confluent(config))


class KafkaContainer(containers.DeclarativeContainer):
    config = providers.Dependency(instance_of=KafkaConfig)
    configuration = Configuration()
    consumer = providers.Factory(
        KafkaConsumer,
        config=configuration.provided.kafka
    )

    producer = providers.Factory(
        KafkaProducer,
        config=configuration.provided.kafka
    )


class KafkaBundle(object):
    def __init__(self):
        self.logger = logging.getLogger("kafka")
        self.config_mapping = {"kafka": KafkaConfig}
        self.injection_bindings = {"kafka", KafkaContainer}

