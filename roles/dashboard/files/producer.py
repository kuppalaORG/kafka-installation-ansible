# producer.py
import requests
import json
import time
from kafka import KafkaProducer
from kafka.errors import KafkaError

KAFKA_BROKERS = [
    "kafka-broker-1.codedeploywithbharath.tech:9092",
    "kafka-broker-2.codedeploywithbharath.tech:9092",
    "kafka-broker-3.codedeploywithbharath.tech:9092"
]

TOPIC_NAME = "crypto-price"

def log(msg):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# Create Kafka producer
try:
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    log("✅ KafkaProducer initialized")
except KafkaError as e:
    log(f"❌ Kafka initialization failed: {e}")
    raise

# Send a test message to check connectivity
try:
    test_msg = {"test": "Kafka connection test", "timestamp": time.time()}
    producer.send(TOPIC_NAME, value=test_msg)
    log(f"✅ Test message sent to '{TOPIC_NAME}': {test_msg}")
except Exception as e:
    log(f"❌ Failed to send test message: {e}")
    raise

# Main loop
while True:
    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin\&vs_currencies=usd", timeout=10)
        if response.status_code == 200:
            data = response.json()
            data['timestamp'] = time.time()
            producer.send(TOPIC_NAME, value=data)
            log(f"📤 Sent BTC price: {data}")
        else:
            log(f"⚠️ Binance API returned status {response.status_code}")
    except Exception as e:
        log(f"❌ API fetch/send error: {e}")

    time.sleep(5)
