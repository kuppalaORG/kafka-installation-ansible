# producer.py
import requests
import json
from kafka import KafkaProducer
import time

producer = KafkaProducer(
    bootstrap_servers = [
        "kafka-broker-1.codedeploywithbharath.tech:9092",
        "kafka-broker-2.codedeploywithbharath.tech:9092",
        "kafka-broker-3.codedeploywithbharath.tech:9092"
    ],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

while True:
    try:
        response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
        if response.status_code == 200:
            data = response.json()
            data['timestamp'] = time.time()
            producer.send("crypto-price", value=data)
            print(f"Sent: {data}")
    except Exception as e:
        print("Error:", e)
    time.sleep(5)
