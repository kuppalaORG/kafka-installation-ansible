# /opt/dashboard/producer.py
import json
import time
import random
import logging
from kafka import KafkaProducer
from kafka.errors import KafkaError
import sys

logging.basicConfig(
    filename="/opt/dashboard/producer.log",
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO
)

def get_mock_price():
    return {
        "symbol": "BTCUSDT",
        "price": round(random.uniform(28000, 32000), 2),
        "timestamp": time.time()
    }

def send_message(producer, topic, message, retries=5):
    delay = 1
    for attempt in range(retries):
        try:
            producer.send(topic, value=message)
            logging.info(f"📤 Sent BTC price: {message}")
            return True
        except KafkaError as e:
            logging.warning(f"⚠️ Kafka send failed: {e} (retrying in {delay}s)")
            time.sleep(delay)
            delay *= 2  # Exponential backoff
    logging.error("❌ Failed to send message after retries")
    return False

def main():
    try:
        producer = KafkaProducer(
            bootstrap_servers=[
                "kafka-broker-1.codedeploywithbharath.tech:9092",
                "kafka-broker-2.codedeploywithbharath.tech:9092",
                "kafka-broker-3.codedeploywithbharath.tech:9092"
            ],
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            linger_ms=10,
            retries=0
        )
        logging.info("✅ KafkaProducer initialized")
    except Exception as e:
        logging.error(f"❌ Failed to initialize KafkaProducer: {e}")
        sys.exit(1)

    while True:
        mock_data = get_mock_price()
        send_message(producer, "crypto-price", mock_data)
        time.sleep(5)

if __name__ == "__main__":
    main()
