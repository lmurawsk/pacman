# -*- coding: utf-8 -*-
import os
import pika
from pika import exceptions
from influxdb import InfluxDBClient
import time
import toml
import json
from datetime import datetime
import pymssql
import pandas.io.sql as psql
from ZabbixReader import ZabbixReader


CONF_FILE = '/conf/conf.toml'

## MS_SQL QUERY CONFIG
NODEBs_CONF = ''
NODEB_CONF_READ_INTERVAL_h = 24
NODEB_CONF_READ_TIMESTAMP = 0

def read_conf(CONF_FILE):
    with open(CONF_FILE) as conffile:
        conf = toml.loads(conffile.read())
    return conf

def transform_func(body):
    # before forwarding data, perform operations on fetched data, before forwarding them further

    global CONF
    global NODEBs_CONF
    global NODEB_CONF_READ_TIMESTAMP

    if 'transform' in CONF.viewkeys():
        if 'mssql' in CONF['transform'].viewkeys(): 
            body = json.loads(body)    
            
            ## query MSSQL if config is empty or only once per given NODEB_CONF_READ_INTERVAL_h
            if(NODEBs_CONF=='' or ((time.time() - NODEB_CONF_READ_TIMESTAMP) > (60*60*NODEB_CONF_READ_INTERVAL_h))):
                NODEB_CONF_READ_TIMESTAMP = time.time()
                MSSQL_CFG = CONF['transform']['mssql']
                mssql_conn = pymssql.connect(host=MSSQL_CFG['url'], user=MSSQL_CFG['username'], password=MSSQL_CFG['password'], database=MSSQL_CFG['database'], as_dict=True, charset='utf8')
                sql = """SELECT IP_ADDRESS,ADDRESS, SITE4G_NAME, ZONE, GEOHASH AS geohash FROM objects"""
                config_data = psql.read_sql(sql, mssql_conn, index_col='IP_ADDRESS')
                NODEBs_CONF = config_data.T.to_dict()
                mssql_conn.close()


            for object_x in body:
                try:
                    # print 'try to add tags..'
                    object_x['tags'].update(NODEBs_CONF[object_x['tags']['host']])
                except:
                    # print '....except'
                    object_x['tags'].update({'ADDRESS': 'Null','SITE4G_NAME': 'Null', 'ZONE': 0,'geohash': 'Null'})
    
            body = json.dumps(body)

    return body

def send_to_rabbit(body):

    global CONF
    print ('Rabbit output conn params', CONF['output']['rabbitmq'])
    sslOptions = CONF['output']['rabbitmq']['ssl_options']

    connectionParams = []

    rmqaccess = CONF['output']['rabbitmq']
    credentials = pika.PlainCredentials(rmqaccess['username'], rmqaccess['password'])
    for rabbit in CONF['output']['rabbitmq']['host']:
        connection_x = pika.ConnectionParameters(rabbit['url']
					,rabbit['port']
					,rmqaccess['vhost']
					,credentials
					,ssl = rmqaccess['ssl']
					,ssl_options = sslOptions)
        connectionParams.append(connection_x)

    connection = connect_to_rabbit_node(connectionParams)
    channel = connection.channel()
    channel.basic_publish(exchange='',routing_key=rmqaccess['queue_name'],body=body,properties=pika.BasicProperties(delivery_mode = 2))
    print (" [x] Sent to Rabbit %r" % body)
    connection.close()


def send_to_influx(body):

    global CONF
    print ('Infludb output conn params', CONF['output']['influxdb'])
    INFLUX_CFG = CONF['output']['influxdb']
    client = InfluxDBClient(INFLUX_CFG['url'], INFLUX_CFG['port'], INFLUX_CFG['username'], INFLUX_CFG['password'], INFLUX_CFG['database'])
    client.create_database(INFLUX_CFG['database'])

    body = json.loads(body)

    #print("Write points to InfluxDB: {0}".format(body))
    res = client.write_points(body, time_precision='s')


# metoda nasluchuje na odbir danych po otrzymaniu wysyla do bazy MongoDB
def callback(ch, method, properties, body):
    #print(" [x] Received %r" % body)

    body = transform_func(body)

    global CONF
    if 'influxdb' in CONF['output'].viewkeys():
        send_to_influx(body)
    
    if 'rabbitmq' in CONF['output'].viewkeys():
        send_to_rabbit(body)

    ch.basic_ack(delivery_tag = method.delivery_tag)


def connect_to_rabbit_node(connectionParams):
    # polacz sie z pierwszym dostepnym nodem rabbitowym z listy
    i=-1
    while True:
        try:
            # id of rabbit node on the list
            i=(i+1)%len(connectionParams)

            # Step #1: Connect to RabbitMQ using the default parameters
            connection = pika.BlockingConnection(connectionParams[i])
            return connection

        except exceptions.AMQPConnectionError as e:
            print "Rabbitmq Connection error " + e.message
            pass
        except:
            print "Unexpected error:"
            raise


# metoda podlaczenia do RabbitMQ
def mRabbitMQConnector():

    global CONF
    print ('Rabbit Input conn params', CONF['input']['rabbitmq'])
    sslOptions = CONF['input']['rabbitmq']['ssl_options']
    connectionParams = []
    rmqaccess = CONF['input']['rabbitmq']
    credentials = pika.PlainCredentials(rmqaccess['username'], rmqaccess['password'])

    for rabbit in CONF['input']['rabbitmq']['host']:
        connection_x = pika.ConnectionParameters(rabbit['url']
					,rabbit['port']
					,rmqaccess['vhost']
					,credentials
					,ssl = rmqaccess['ssl']
					,ssl_options = sslOptions)
        connectionParams.append(connection_x)

    connection = connect_to_rabbit_node(connectionParams)

    channel = connection.channel()

    # opcjonalna deklaracja kolejki
    # channel.queue_declare(queue=CONF['input']['rabbitmq'][0]['queue_name'], durable=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')


    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback,
                          queue=rmqaccess['queue_name'])

    channel.start_consuming()
    print(' [*] BYE')


def getZabbixData():
    """ Get data from Zabbix based on configuration, send to RMq """
    # zabbix connection 
    global CONF
    ZAB_CONF = CONF['input']['zabbix']
    zab_url = ZAB_CONF['url']
    zab_user = ZAB_CONF['user']
    zab_password = ZAB_CONF['password']
    zr = ZabbixReader(zab_url, zab_user, zab_password)
    
    # iterate through groups defined in conf and send  data to RMq
    try:
    	for group in CONF['input']['zabbix']['group']:
    	    stats = zr.get_stats_from_gname_json(group['gname'])
	    send_to_rabbit(stats)
    except Exception as e:
	print e
	pass

    # iterate through hosts defined in conf and send data to RMq
    try:
    	for host in CONF['input']['zabbix']['host']:
            stats = zr.get_stats_from_hname_json(host['hname'])
            send_to_rabbit(stats)
    except Exception as e:
	print e
	pass

def mZabbixConnector():
    global CONF
    CONF = read_conf(CONF_FILE)
    sleep_time = CONF['input']['zabbix']['repeat_time']
    while True:
        getZabbixData()
        print "Sleep for %d seconds ..zzz..zzz..zzz..." % sleep_time
        time.sleep(sleep_time)


if __name__ == '__main__':
    global CONF
    CONF = read_conf(CONF_FILE)
    # check for zabbix input configuration
    try:
	CONF['input']['zabbix']
    except KeyError as e:
	print "No valid input for zabbix in file: [%s] " % CONF_FILE
    else:
	print "pacman in Zabbix mode"
        mZabbixConnector()
    # check for rabbit input configuration
    try:
	CONF['input']['rabbitmq']
    except KeyError as e:
        print "No valid input for rabbit in file: [%s] " % CONF_FILE
    else:
	print "pacman in Rabbit mode" 
	mRabbitMQConnector()
    
