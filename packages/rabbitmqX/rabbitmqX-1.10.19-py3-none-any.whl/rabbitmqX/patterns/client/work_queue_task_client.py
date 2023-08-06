from pprint import pprint
import pika
import os
import json
import time

class Work_Queue_Task_Client():

    def __init__(self, queue_name = None,host='localhost'):
        
        if host.startswith('amqp'):
            params = pika.URLParameters(host)
            self.connection = pika.BlockingConnection(params)
        else:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host,heartbeat=60000,blocked_connection_timeout=30000))
        
        self.channel = self.connection.channel()
        self.queue_name = queue_name 
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def send (self,journal):
        
        self.channel.basic_publish(
                exchange='',
                routing_key=self.queue_name, 
                 properties=pika.BasicProperties(
                     content_type = "application/json",
                     delivery_mode=2),  
                body=json.dumps(journal.__dict__))

    def close():
        self.connection.close()
  
        

        

        

        







