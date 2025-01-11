import json
from kafka import KafkaProducer

BOOTSTRAP_SERVERS = "localhost:9092"  
TOPIC = "main_topic"  

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"))

def send_message(message):
    """
     Send a message to the subject Kafka specified"""
    try:
        producer.send(TOPIC, message)
        producer.flush()
        print(f"Message sent: {message}")
    except Exception as exception:
        print(f"The message could not be sent: {exception}")


if __name__ == "__main__":
    sample_message = {
        "operations": [
            {"id": "1", "object_identifier": "testList", "object_type": "RList", "operation": "append", "args": {"item": "sadsasdasd"}},
            #{"id": "2", "object_identifier": "testList", "object_type": "RList", "operation": "pop", "args": {"index": 0}},
            {"id": "3", "object_identifier": "testList", "object_type": "RList", "operation": "getItem", "args": {"index": 0}},

            {"id": "4", "object_identifier": "testDict", "object_type": "RDict", "operation": "setItem", "args": {"key": "name", "item": "Juan"}},
            {"id": "5", "object_identifier": "testDict", "object_type": "RDict", "operation": "getItem", "args": {"key": "name"}},
            {"id": "6", "object_identifier": "testDict", "object_type": "RDict", "operation": "pop", "args": {"key": "name"}},

            {"id": "7", "object_identifier": "testSet", "object_type": "RSet", "operation": "add", "args": {"item": "newItem"}},
            {"id": "8", "object_identifier": "testSet", "object_type": "RSet", "operation": "pop", "args": {}},

            {"id": "9", "object_identifier": "testList", "object_type": "RList", "operation": "identifier", "args": {}},
            {"id": "10", "object_identifier": "testList", "object_type": "RList", "operation": "length", "args": {}},
            {"id": "11", "object_identifier": "testList", "object_type": "RList", "operation": "contains", "args": {"item": "example"}},
            {"id": "12", "object_identifier": "testList", "object_type": "RList", "operation": "hash", "args": {}},
            {"id": "13", "object_identifier": "testList", "object_type": "RList", "operation": "remove", "args": {"item": "example"}},
            {"id": "14", "object_identifier": "testList", "object_type": "RList", "operation": "iter", "args": {}}
        ]
    }

    send_message(sample_message)
