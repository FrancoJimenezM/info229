from logging import NullHandler
import pika
import pageviewapi 
from datetime import date, datetime

from six import viewitems


def obtainDate():
    dates = str(datetime.today().strftime('%Y-%m-%d'))
    dates = ''.join( x for x in dates if x not in "-")
    return dates

#Conexión al servidor RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#El consumidor utiliza el exchange 'log'
channel.exchange_declare(exchange='logs', exchange_type='fanout')

#Se crea un cola temporaria exclusiva para este consumidor (búzon de correos)
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

#La cola se asigna a un 'exchange'
channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r" % body)
    search = body.decode('utf-8')
    search = search[16:len(search)-1]
    fecha = obtainDate()
    c = 0
    results =  pageviewapi.per_article('en.wikipedia', search, '20151106', fecha, access='all-access', agent='all-agents', granularity='daily')

    for  i in  results["items"]:
        c += i["views"]
    print(c)

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()