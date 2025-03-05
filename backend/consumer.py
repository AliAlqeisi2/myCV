from kafka import KafkaConsumer
import os 
import json
from emailsender1.emailsender import send_email
from dotenv import load_dotenv


kafka_broker = os.getenv("KAFKA_BROKER", 'kafka:9092')

topic = 'resume-views'

def start_consumer():
    consumer= KafkaConsumer(
    topic,
    bootstrap_servers = kafka_broker,
    auto_offset_reset='earliest',
    key_deserializer = lambda k: k.decode('utf-8'),
    value_deserializer = lambda v : json.loads(v.decode('utf-8'))
    )

    for message in consumer:
        print(f"offset = {message.offset}, key = {message.key}, value = {message.value}")
    
        send_email(consumer_message= "someone just viewed your CV")



if __name__ == '__main__':
    start_consumer()




    



