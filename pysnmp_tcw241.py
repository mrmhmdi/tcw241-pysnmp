import csv
import time
from pysnmp.hlapi import *

filename:str = "snmp_data.csv"
header:list = ["Timestamp", "Temp", 'Humidity']

temp_iod:str = '1.3.6.1.4.1.38783.3.3.1.1.1.0'
humidity:str = '1.3.6.1.4.1.38783.3.3.1.1.2.0'
oid_lst:list = [temp_iod, humidity]


def snmp_get_oid(iod):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
            CommunityData('public'),
            UdpTransportTarget(('192.168.10.42', 161)),
            ContextData(),
            ObjectType(ObjectIdentity(iod))
        )
    )

    if errorIndication:
        print(errorIndication)
    else:
        if errorStatus:
            error = errorIndex and varBinds[int(errorIndex) - 1][0] or '?'
            with open(filename, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=header)
                writer.writerow(f'{errorStatus.prettyPrint()} at {error}')
            
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                oid, value = [x.prettyPrint() for x in varBind]
            return int(value)/1000


def result_to_file():
    result = []
    for oid in oid_lst:
        result.append(snmp_get_oid(oid))
    data = {'Timestamp': time.ctime(), 'Temp': result[0], 'Humidity': result[1]}
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writerow(data)


if __name__ == '__main__':
    while True:
        result_to_file()
        time.sleep(5)