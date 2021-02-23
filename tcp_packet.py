class tcp_packet:

    def __init__(self, type, seq_num, ack_num, data, packet_size):
        self. type = type
        self. seq_num = seq_num
        self. ack_num = ack_num
        self. data = data
        self. packet_size = packet_size
