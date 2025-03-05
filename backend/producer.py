from kafka import KafkaProducer
import json
from datetime import datetime
from kafka.errors import KafkaError
import os

# Get Kafka broker address from environment variable
kafka_broker = os.getenv("KAFKA_BROKER", 'kafka:9092')


# Kafka Producer Configuration
kafka_config = {
    'bootstrap_servers': kafka_broker,
    'value_serializer': lambda v: json.dumps(v).encode("utf-8"),
    'key_serializer': str.encode
}

producer = KafkaProducer(**kafka_config)
topic = "resume-views"


def log_cv_view(user_agent):
    try:
        event = {
            "event_type": "cv_view",
            "timestamp": datetime.now().isoformat(),
            "user_agent": user_agent,
        }

        key = "view"
        future = producer.send(topic, key=key, value=event)
        future.get(timeout=5)  # Ensure the message is sent
        print(f"Message sent: key={key}, value={event}", flush=True)

    except KafkaError as e:
        print(f"Failed to send message: {e}")

# The main function can still test it, but it's no longer needed for imports
def main():
    log_cv_view("Mozilla/5.0")  # Test call

if __name__ == "__main__":
    main()

