import socket as plc

DREG = 1
RREG = 2
WREG = 3
MBIT = 4
BBIT = 5


class Conn:
    def __init__(self, ipaddress, port):
        self.ip = ipaddress
        self.port = port


class WDataObj:
    def __init__(self, start_address, data_length, data):
        self.start_address = start_address
        self.data_length = data_length
        self.data = data


class RDataObj:
    def __init__(self, start_address, data_length):
        self.start_address = start_address
        self.data_length = data_length


def write_data(conn, wdataobj, datatype):
    if wdataobj.data_length == len(wdataobj.data):
        # First command
        data = ""
        for x in range(wdataobj.data_length):
            if 0 < datatype < 4:
                data = data + format(wdataobj.data[x], '04x').upper()
            elif 3 < datatype < 6:
                data = data + format(wdataobj.data[x], '0x').upper()
        rd = __get_common_data_2(2, wdataobj.start_address, wdataobj.data_length, datatype) + data
        dl = format(len(rd), '04x').upper()
        cmd = __get_common_data_1() + dl + rd
        print(cmd)
        __socket_send(conn, cmd)
    else:
        print("Data Error")
        return 0


def read_data(conn, read_data_obj, datatype):
    # First command
    rd = __get_common_data_2(1, read_data_obj.start_address, read_data_obj.data_length, datatype)
    dl = format(len(rd), '04x').upper()
    cmd = __get_common_data_1() + dl + rd
    print(cmd)
    __socket_send(conn, cmd)
