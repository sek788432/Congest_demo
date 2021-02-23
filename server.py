import socket, pickle
import os
from thread import*
import random
import time
from tcp_packet import *
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = "127.0.0.1"
port = 1234
ThreadCount = 0

try:
    server.bind((IP,port))
except socket.error as e:
    print(str(e))

print("socket is listening")
server.listen(5)



def send_file(connection, file_name):
    file_name = './server_place/'+ file_name
    file_size = os.stat(file_name).st_size
    with open(file_name, 'rb') as file:

        State = "slow_start"
        MSS = 1024
        cwnd = 1 * MSS     # cwnd initialization 1 MSS = 1KB
        ssthresh = 64 * MSS
        dup_ack = 0
        last_ack_num = -1
        data = 1
        # pkt initialization
        type = "new_ack"
        seq_num = 1
        ack_num = -1
        recv_size = 0

        while( (file_size - recv_size) > 0 ):
            if (file_size - recv_size) < cwnd:
                cwnd = file_size - recv_size

            data = file.read(cwnd)
            recv_size += cwnd
            cwnd_str = str(cwnd)
            while len(cwnd_str) < 6:
                cwnd_str = '0'+ cwnd_str
            connection.send(str.encode(cwnd_str))
            connection.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, cwnd)
            connection.send(data)

            print(State)
            packet = tcp_packet(type=type, seq_num=seq_num, ack_num=ack_num, data=1, packet_size=cwnd)
            print("send packet size: ", packet.packet_size, " bytes")

            chose = random.randint(0, 19)
            if chose < 5:
                packet.type = "timeout"
            elif chose < 10:
                packet.type = "duplicate_ack"
            else:
                packet.type = "new_ack"

            if packet.type == "timeout":
                case = "timeout"
            elif packet.type == "duplicate_ack":
                case = "duplicate_ack"
            else:
                case = "new_ack"

            if State == "slow_start":
                if case == "new_ack":
                    cwnd *= 2
                    dup_ack = 0
                elif case == "duplicate_ack":
                    dup_ack += 1
                elif case == "timeout":
                    ssthresh = cwnd / 2
                    cwnd = 1 * MSS
                    dup_ack = 0

                if cwnd >= ssthresh:
                    State = "congestionAvoidence"
                if dup_ack >= 3:
                    State = "fastRecovery"

            elif State == "fastRecovery":
                if case == "duplicate_ack":
                    cwnd = cwnd + MSS
                elif case == "new_ack":
                    cwnd = ssthresh
                    dup_ack = 0
                    State = "congestionAvoidence"
                elif case == "timeout":
                    ssthresh = cwnd / 2
                    cwnd = 1 * MSS
                    dup_ack = 0
                    State = "slow_start"

            elif State == "congestionAvoidence":
                if case == "new_ack":
                    cwnd = cwnd + MSS * (MSS / cwnd)
                    #cwnd = cwnd
                    dup_ack = 0
                elif case == "duplicate_ack":
                    dup_ack += 1
                elif case == "timeout":
                    ssthresh = cwnd / 2
                    cwnd = 1 * MSS
                    dup_ack = 0
                    State = "slow_start"
                if dup_ack >= 3:
                    State = "fastRecovery"

        file.close()


def multi_thread_client(connection, client_info):
    connection.send(str.encode("Server is working:"))
    file_name_length = connection.recv(2)
    file_name = connection.recv(int(file_name_length))     # file name size
    send_file(connection, file_name)
    print("Finish sending ",file_name," to ",client_info[0]," : ",client_info[1])
    connection.close()


while True:
    client, cli_IP = server.accept()
    print("Connected to: IP",cli_IP[0]," port: ",cli_IP[1])
    start_new_thread(multi_thread_client, (client,cli_IP ))
    time.sleep(0.1)
    ThreadCount += 1
server.close()


#print("Server get:",data.decode('utf-8'))
#connection.sendall(str.encode("HI"))


# FSM
