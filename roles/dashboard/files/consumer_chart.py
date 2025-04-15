# consumer_chart.py
from kafka import KafkaConsumer
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime

consumer = KafkaConsumer(
    'crypto-price',
    bootstrap_servers = [
        "kafka-broker-1.codedeploywithbharath.tech:9092",
        "kafka-broker-2.codedeploywithbharath.tech:9092",
        "kafka-broker-3.codedeploywithbharath.tech:9092"
    ],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest',
    group_id='crypto-chart'
)

# Live chart data holders
timestamps = []
prices = []

fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)

def update(frame):
    global timestamps, prices
    for msg in consumer:
        data = msg.value
        price = float(data["price"])
        ts = datetime.fromtimestamp(data["timestamp"])
        print(f"Received: {price} at {ts}")

        timestamps.append(ts)
        prices.append(price)

        # Keep last 20
        timestamps = timestamps[-20:]
        prices = prices[-20:]

        line.set_data(timestamps, prices)
        ax.relim()
        ax.autoscale_view()
        break  # Important: so it returns for each frame

    return line,

ani = animation.FuncAnimation(fig, update, blit=False, interval=1000)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
