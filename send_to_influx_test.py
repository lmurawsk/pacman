#!/usr/bin/python
import toml
from influxdb import InfluxDBClient

def read_conf(CONF_FILE):
    with open(CONF_FILE) as conffile:
        conf = toml.loads(conffile.read())
    return conf


if __name__ == '__main__':
    CONF_FILE = '/conf/conf.toml'
    CONF = read_conf(CONF_FILE)
    INFLUX_CFG = CONF['output']['influxdb']
    INFLUXDB_CONN = InfluxDBClient(INFLUX_CFG['url'], INFLUX_CFG['port'], INFLUX_CFG['username'], INFLUX_CFG['password'], INFLUX_CFG['database'])
    body = [{u'fields': {u'PING_INTERVAL': 0.2, u'PING_STDEV': 0.036, u'PING_MAX': 5.619, u'PING_SIZE': 1200, u'PING_AVG': 5.572, u'PING_TIMEOUT': 1.0, u'PING_COUNT': 3, u'PING_PACKETLOSS': 0, u'PING_MIN': 5.533}, u'measurement': u'resul
ts', u'tags': {u'host': u'10.245.134.5', u'SITE4G_NAME': u'LB42508', u'geohash': u'u3ky1z2ns6h7', u'ZONE': 4, u'ADDRESS': u'BYDGOSZCZ GIMNAZJALNA'}, u'time': 1482497462}, {u'fields': {u'PING_INTERVAL': 0.2, u'PING_STDEV': 0.071, u'PING_M
AX': 6.022, u'PING_SIZE': 1200, u'PING_AVG': 5.949, u'PING_TIMEOUT': 1.0, u'PING_COUNT': 3, u'PING_PACKETLOSS': 0, u'PING_MIN': 5.853}, u'measurement': u'results', u'tags': {u'host': u'10.245.138.129', u'SITE4G_NAME': u'LB42510', u'geoha
sh': u'u3kyhp05x9yb', u'ZONE': 4, u'ADDRESS': u'BYDGOSZCZ PRZEMYSLOWA'}, u'time': 1482497462}, {u'fields': {u'PING_INTERVAL': 0.2, u'PING_STDEV': 0.8, u'PING_MAX': 9.004, u'PING_SIZE': 1200, u'PING_AVG': 7.906, u'PING_TIMEOUT': 1.0, u'PI
NG_COUNT': 3, u'PING_PACKETLOSS': 0, u'PING_MIN': 7.119}, u'measurement': u'results', u'tags': {u'host': u'10.245.160.90', u'SITE4G_NAME': u'LB42523', u'geohash': u'u3kur0c65qyc', u'ZONE': 4, u'ADDRESS': u'INOWROCLAW GROCHOWA'}, u'time':
 1482497462}, {u'fields': {u'PING_INTERVAL': 0.2, u'PING_STDEV': 0.195, u'PING_MAX': 7.722, u'PING_SIZE': 1200, u'PING_AVG': 7.452, u'PING_TIMEOUT': 1.0, u'PING_COUNT': 3, u'PING_PACKETLOSS': 0, u'PING_MIN': 7.267}, u'measurement': u'res
ults', u'tags': {u'host': u'10.245.160.75', u'SITE4G_NAME': u'LB42531', u'geohash': u'u3ku6x032d7m', u'ZONE': 4, u'ADDRESS': u'PIECHCIN'}, u'time': 1482497462}, {u'fields': {u'PING_INTERVAL': 0.2, u'PING_STDEV': 0.023, u'PING_MAX': 5.922
, u'PING_SIZE': 1200, u'PING_AVG': 5.89, u'PING_TIMEOUT': 1.0, u'PING_COUNT': 3, u'PING_PACKETLOSS': 0, u'PING_MIN': 5.867}, u'measurement': u'results', u'tags': {u'host': u'10.245.153.70', u'SITE4G_NAME': u'LB42619', u'geohash': u'u3m7v
zvbnpju', u'ZONE': 4, u'ADDRESS': u'LUBANIE'}, u'time': 1482497462}, {u'fields': {u'PING_INTERVAL': 0.2, u'PING_STDEV': 0.169, u'PING_MAX': 6.359, u'PING_SIZE': 1200, u'PING_AVG': 6.125, u'PING_TIMEOUT': 1.0, u'PING_COUNT': 3, u'PING_PAC
KETLOSS': 0, u'PING_MIN': 5.963}, u'measurement': u'results', u'tags': {u'host': u'10.245.165.69', u'SITE4G_NAME': u'LB42622', u'geohash': u'u3mz0bzr2v58', u'ZONE': 4, u'ADDRESS': u'BRODNICA KRUSZYNKI'}, u'time': 1482497462}, {u'fields':
 {u'PING_INTERVAL': 0.2, u'PING_STDEV': 0.053, u'PING_MAX': 5.103, u'PING_SIZE': 1200, u'PING_AVG': 5.045, u'PING_TIMEOUT': 1.0, u'PING_COUNT': 3, u'PING_PACKETLOSS': 0, u'PING_MIN': 4.974}, u'measurement': u'results', u'tags': {u'host':
 u'10.245.164.2', u'SITE4G_NAME': u'LB42771', u'geohash': u'u3mjwzsr8m12', u'ZONE': 4, u'ADDRESS': u'TORUN WRZOSY 3'}, u'time': 1482497462}, {u'fields': {u'PING_INTERVAL': 0.2, u'PING_STDEV': 0.096, u'PING_MAX': 4.685, u'PING_SIZE': 1200
, u'PING_AVG': 4.554, u'PING_TIMEOUT': 1.0, u'PING_COUNT': 3, u'PING_PACKETLOSS': 0, u'PING_MIN': 4.46}, u'measurement': u'results', u'tags': {u'host': u'10.245.134.151', u'SITE4G_NAME': u'LB42790', u'geohash': u'u3mjrxsg70q4', u'ZONE':
4, u'ADDRESS': u'TORUN HALLERA AQUA'}, u'time': 1482497462}, {u'fields': {u'PING_INTERVAL': 0.2, u'PING_STDEV': 0.07, u'PING_MAX': 13.921, u'PING_SIZE': 1200, u'PING_AVG': 13.825, u'PING_TIMEOUT': 1.0, u'PING_COUNT': 3, u'PING_PACKETLOSS
': 0, u'PING_MIN': 13.758}, u'measurement': u'results', u'tags': {u'host': u'10.245.140.132', u'SITE4G_NAME': u'LB42807', u'geohash': u'u3d2536bbwmr', u'ZONE': 4, u'ADDRESS': u'SZCZ_SZCZANIECKIEJ'}, u'time': 1482497462}, {u'fields': {u'P
ING_INTERVAL': 0.2, u'PING_STDEV': 0.709, u'PING_MAX': 19.417, u'PING_SIZE': 1200, u'PING_AVG': 18.417, u'PING_TIMEOUT': 1.0, u'PING_COUNT': 3, u'PING_PACKETLOSS': 0, u'PING_MIN': 17.864}, u'measurement': u'results', u'tags': {u'host': u
'10.245.145.216', u'SITE4G_NAME': u'LB42927', u'geohash': u'u3e2s8v3nx59', u'ZONE': 4, u'ADDRESS': u'ZLOCIENIEC WSCHOD'}, u'time': 1482497462}, {u'fields': {u'PING_INTERVAL': 0.2, u'PING_STDEV': 0.094, u'PING_MAX': 11.197, u'PING_SIZE':
1200, u'PING_AVG': 11.066, u'PING_TIMEOUT': 1.0, u'PING_COUNT': 3, u'PING_PACKETLOSS': 0, u'PING_MIN': 10.983}, u'measurement': u'results', u'tags': {u'host': u'10.245.144.77', u'SITE4G_NAME': u'LB42983', u'geohash': u'u3es0wtm1jz1', u'Z
ONE': 4, u'ADDRESS': u'KOSZALIN FORUM'}, u'time': 1482497462}, {u'fields': {u'PING_INTERVAL': 0.2, u'PING_STDEV': 0.069, u'PING_MAX': 11.154, u'PING_SIZE': 1200, u'PING_AVG': 11.069, u'PING_TIMEOUT': 1.0, u'PING_COUNT': 3, u'PING_PACKETL
OSS': 0, u'PING_MIN': 10.986}, u'measurement': u'results', u'tags': {u'host': u'10.245.144.74', u'SITE4G_NAME': u'LB42998', u'geohash': u'u3es2cbrjfu3', u'ZONE': 4, u'ADDRESS': u'KOSZALIN PILSUDSKIEGO'}, u'time': 1482497462}, {u'fields':
 {u'PING_INTERVAL': 0.2, u'PING_STDEV': 0.705, u'PING_MAX': 9.207, u'PING_SIZE': 1200, u'PING_AVG': 8.214, u'PING_TIMEOUT': 1.0, u'PING_COUNT': 3, u'PING_PACKETLOSS': 0, u'PING_MIN': 7.637}, u'measurement': u'results', u'tags': {u'host':
 u'10.245.134.215', u'SITE4G_NAME': u'LB43032', u'geohash': u'u3w9fp732yne', u'ZONE': 4, u'ADDRESS': u'OLSZTYN AL. WOJSKA POLSKIEGO'}, u'time': 1482497462}, {u'fields': {u'PING_INTERVAL': 0.2, u'PING_STDEV': 0.509, u'PING_MAX': 17.885, u
'PING_SIZE': 1200, u'PING_AVG': 17.211, u'PING_TIMEOUT': 1.0, u'PING_COUNT': 3, u'PING_PACKETLOSS': 0, u'PING_MIN': 16.654}, u'measurement': u'results', u'tags': {u'host': u'10.245.143.76', u'SITE4G_NAME': u'LB43105', u'geohash': u'u36r2
jx86eb7', u'ZONE': 4, u'ADDRESS': u'KOLBASKOWO'}, u'time': 1482497462}, {u'fields': {u'PING_INTERVAL': 0.2, u'PING_STDEV': 0.054, u'PING_MAX': 16.744, u'PING_SIZE': 1200, u'PING_AVG': 16.676, u'PING_TIMEOUT': 1.0, u'PING_COUNT': 3, u'PIN
G_PACKETLOSS': 0, u'PING_MIN': 16.613}, u'measurement': u'results', u'tags': {u'host': u'10.245.143.68', u'SITE4G_NAME': u'LB43116', u'geohash': u'u36r6gjv7y86', u'ZONE': 4, u'ADDRESS': u'SZCZ_KLUCZEWKO'}, u'time': 1482497462}, {u'fields
': {u'PING_INTERVAL': 0.2, u'PING_STDEV': 1.05, u'PING_MAX': 17.422, u'PING_SIZE': 1200, u'PING_AVG': 16.164, u'PING_TIMEOUT': 1.0, u'PING_COUNT': 3, u'PING_PACKETLOSS': 0, u'PING_MIN': 14.851}, u'measurement': u'results', u'tags': {u'ho
st': u'10.245.142.77', u'SITE4G_NAME': u'LB43146', u'geohash': u'u3d805szfk7u', u'ZONE': 4, u'ADDRESS': u'KLINISKA'}, u'time': 1482497462}, {u'fields': {u'PING_INTERVAL': 0.2, u'PING_STDEV': 0.047, u'PING_MAX': 8.224, u'PING_SIZE': 1200,
 u'PING_AVG': 8.158, u'PING_TIMEOUT': 1.0, u'PING_COUNT': 3, u'PING_PACKETLOSS': 0, u'PING_MIN': 8.122}, u'measurement': u'results', u'tags': {u'host': u'10.245.128.22', u'SITE4G_NAME': u'LB42443', u'geohash': u'u3tn97xgdww0', u'ZONE': 4
, u'ADDRESS': u'REDA 3 TEMP'}, u'time': 1482497462}, {u'fields': {u'PING_INTERVAL': 0.2, u'PING_STDEV': 0.0, u'PING_MAX': 13.366, u'PING_SIZE': 1200, u'PING_AVG': 13.35, u'PING_TIMEOUT': 1.0, u'PING_COUNT': 3, u'PING_PACKETLOSS': 0, u'PI
NG_MIN': 13.325}, u'measurement': u'results', u'tags': {u'host': u'10.245.162.145', u'SITE4G_NAME': u'LB42450', u'geohash': u'u3ecs1x1smu2', u'ZONE': 4, u'ADDRESS': u'SZCZECINEK POLNOC 2'}, u'time': 1482497462}, {u'fields': {u'PING_INTER
VAL': 0.2, u'PING_STDEV': 0.032, u'PING_MAX': 11.904, u'PING_SIZE': 1200, u'PING_AVG': 11.88, u'PING_TIMEOUT': 1.0, u'PING_COUNT': 3, u'PING_PACKETLOSS': 0, u'PING_MIN': 11.835}, u'measurement': u'results', u'tags': {u'host': u'10.245.15
3.198', u'SITE4G_NAME': u'LB42481', u'geohash': u'u3x64dfkkf0q', u'ZONE': 4, u'ADDRESS': u'HOTEL GOLEBIEWSKI 2'}, u'time': 1482497462}, {u'fields': {u'PING_INTERVAL': 0.2, u'PING_STDEV': -1.0, u'PING_MAX': -1.0, u'PING_SIZE': 1200, u'PIN
G_AVG': -1.0, u'PING_TIMEOUT': 1.0, u'PING_COUNT': 3, u'PING_PACKETLOSS': 100, u'PING_MIN': -1.0}, u'measurement': u'results', u'tags': {u'host': u'10.245.153.198', u'SITE4G_NAME': u'LB42481', u'geohash': u'u3x64dfkkf0q', u'ZONE': 4, u'A
DDRESS': u'HOTEL GOLEBIEWSKI 2'}, u'time': 1482497462}]

    res = INFLUXDB_CONN.write_points(body, time_precision='s')

