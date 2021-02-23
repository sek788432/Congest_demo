import socket, pickle
import select
from tcp_packet import *
import sys

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = "127.0.0.1"
port = 1234


try:
    client.connect((IP, port))
except socket.error as e:
    print(str(e))

def get_file(client, type):
    with open('./clients/client_'+sys.argv[1]+'/client_recv'+type, 'wb') as recv_file:
        recv_byte = list()
        while True:
            ready = select.select([client], [], [], 0.3)
            size = 0
            data = "ignore"
            if ready[0]:
                size = client.recv(6)
                size = size.decode()
                if size == "":
                    break
                data = client.recv(int(size))
                print("receive packet: ", len(data), " bytes")
                recv_byte.append(len(data))

            if data == "ignore":
                break
            recv_file.write(data)

    recv_file.close()
    print("Get a file from server")


first_message = client.recv(18)
print(first_message)

Input = sys.argv[2]
file_name_len = str(len(Input))
while len(file_name_len) < 2:
    file_name_len = '0'+ file_name_len

client.send(str.encode(file_name_len))
client.send(str.encode(Input))
type = Input[-4:]
get_file(client, type)
client.close()
