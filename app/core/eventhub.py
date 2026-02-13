from azure.eventhub import EventHubProducerClient
from app.core.config import EVENTHUB_CONNECTION_STRING, EVENTHUB_NAME

producer = EventHubProducerClient.from_connection_string(
    EVENTHUB_CONNECTION_STRING,
    eventhub_name=EVENTHUB_NAME
)
