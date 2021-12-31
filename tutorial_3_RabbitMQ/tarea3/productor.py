#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#Creamos el exchange 'logs' de tipo 'fanout'
channel.exchange_declare(exchange='logs', exchange_type='fanout')
query = str(input("Búsqueda en wikipedia:  "))
message = ' '.join(sys.argv[1:]) or ("Se buscó: " , query )

#Publicamos los mensajes a través del exchange 'logs' 
channel.basic_publish(exchange='logs', routing_key='', body=message)

print(" [x] Sent %r" % message)
connection.close()