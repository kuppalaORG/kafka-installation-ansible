# consumer_ui.py
import streamlit as st
from kafka import KafkaConsumer
import json
import time

st.title("📊 Live Crypto Price Dashboard")

consumer = KafkaConsumer(
    'crypto-price',
    bootstrap_servers=[
        "kafka-broker-1.codedeploywithbharath.tech:9092",
        "kafka-broker-2.codedeploywithbharath.tech:9092",
        "kafka-broker-3.codedeploywithbharath.tech:9092"
    ],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest',
    group_id='crypto-ui'
)

placeholder = st.empty()

for message in consumer:
    data = message.value
    with placeholder.container():
        st.metric("BTC/USDT Price", data.get("price"))
        st.write("⏰ Timestamp:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data.get("timestamp"))))

if __name__ == "__main__":
    import streamlit as st
    from streamlit.web import cli as stcli
    import sys

    sys.argv = ["streamlit", "run", __file__]
    sys.exit(stcli.main())
