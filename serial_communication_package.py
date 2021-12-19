
import sys
import functools
import struct
from re import match




class Write_Read_Packet_Cls(object):
    global write_package

    global read_package
    global opcode
    global read_request_channel_index
    global channel_mask_location

    global channels_read
    global measured_voltage_read

    def __init__(self):
        self.write_package: bytearray = 0

        self.read_package: bytearray = 0
        self.opcode: int = 0
        self.read_request_channel_index: int = 0
        self.channel_mask_location: int = 0

        self.channels_read: bytearray = 0
        self.measured_voltage_read: bytearray = 0

    def write_encapsulate_frame(self, opcode, payload: list):
        print(" payload tx =", payload)

        indices = []
        for i in range(len(payload)):
            if payload[i] == 126:
                indices.append(i)
        print("!!!!!!!!!!!!!!!!!!!    indices     =     !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", indices)

        tmp_payload = bytearray(payload)
        for index_7e in indices:
            if index_7e == -1:
                print("Not Found 7e ")
            else:
                print("Found 7e at location ", index_7e)
                tmp_payload.insert(index_7e, 125)  # 7D
                tmp_payload.insert(index_7e + 1, tmp_payload[index_7e + 1] ^ (1 << 5))  # 7E inverted bit 5
                del tmp_payload[index_7e + 2:index_7e + 3]  # 7E deleted

        print("tmp_payload = ",''.join('{:02x}'.format(x) for x in tmp_payload))

        packet_length: int = len(tmp_payload) + 2
        print("Write packet_length = ", packet_length)
        self.write_package = bytearray(tmp_payload)
        self.write_package.insert(0, 126)  # 1st Delimiter byte
        self.write_package.insert(1, packet_length)  # length byte
        self.write_package.insert(2, 0)  # Control byte
        self.write_package.insert(3, int(opcode))  # Opcode byte
        print("Write first element checksum = ", self.write_package[1])
        print("Write Last element checksum = ", self.write_package[packet_length + 1])
        self.write_package.append(self.write_read_calc_checksum(self.write_package[1:packet_length + 2]))  # Checksum
        self.write_package.append(126)  # Last Delimiter byte
        for x in self.write_package: print(x)
        print()
        for y in self.write_package: print(hex(y))
        print()
        return self.write_package

    def write_read_calc_checksum(self, lst: list):
        print("calc checksum write lst = ", lst)
        return functools.reduce(lambda x, y: x + y, lst) % 256


    def handle_read_opcode_0x3b(self,read_packet_obtained:bytearray,index_num:int,channel_request:int):
        print("index num = " , index_num)

        find_channel_desired_to_Meas= [i for i, digit in enumerate(reversed(bin(channel_request)), 0) if digit == '1']
        print("The position of all ones are : find_pos =" , find_channel_desired_to_Meas)

        filter_channel_num:int= int(0xE0)
        filter_meas:int= int(0x1F_FF_FF)

        number_of_elements = len(find_channel_desired_to_Meas)
        channel_selected=[]
        meas_result = []
        for index_i in range(0,number_of_elements):
            int_chan_sel: int = int.from_bytes(read_packet_obtained[3*index_i+5:3*index_i+6], "big")
            print("***DEBUG ONLY****  index_i = ",index_i , "int_chan_sel HEX = " , hex(int_chan_sel))
            int_chan_sel = (int_chan_sel & filter_channel_num)>>5
            channel_selected.append(int_chan_sel)
            int_meas: int = int.from_bytes(read_packet_obtained[3*index_i+5:3*index_i+8], "big")
            int_meas = int_meas & filter_meas
            meas_result.append(int_meas)
        print("channel_selected new = ", channel_selected)
        print("meas_result after append", meas_result)
        return meas_result


    def encapsulate_read_frame(self, read_payload: list):
        self.read_package = bytearray(read_payload)
        packet_length: int = len(self.read_package)
        calc_read_checksum: int = self.write_read_calc_checksum(self.read_package[1:packet_length - 2])  # Checksum

        if calc_read_checksum == self.read_package[packet_length - 2]:
            print("Correct Read Checksum", calc_read_checksum)
        else:
            print("Error in Read Checksum calculated checksum = ", calc_read_checksum, "Received checksum =",
                  self.read_package[packet_length - 2])

        index_7d: int = self.read_package.find(125)

        if index_7d == -1:
            print("Not Found 7d ")
        else:
            print("Found 7d at location ", index_7d)
            self.read_package[index_7d + 1] = (self.read_package[index_7d + 1] ^ (1 << 5))  # 7E inverted bit 5
            del self.read_package[index_7d:index_7d + 1]  # 7E deleted

        temp_rd_pck = self.read_package

        if self.read_package[3] == 0x3B:
            print("3B detected : ", self.read_package)
            self.handle_read_opcode_0x3b(self.read_package,0x01,0x67)

        for x in self.read_package: print(x)
        print()
        for y in self.read_package: print(hex(y))
        print()
        return self.read_package

myWrite_read_Packet_Cls_Obj = Write_Read_Packet_Cls()

print("================  Write First try   ==========================")

myWrite_read_Packet_Cls_Obj.write_encapsulate_frame(0x12, [1, 7, 0, 8, 0])

print("=========================================================\n\n\n")

print("==================Write Second try ======================")

myWrite_read_Packet_Cls_Obj.write_encapsulate_frame(0x12, [1, 7, 0, 8, 0, 36, 126, 53])
#myWrite_read_Packet_Cls_Obj.write_encapsulate_frame(0x12, [1, 126, 0, 126, 0, 36, 126, 53])

print("=========================================================\n\n\n")

print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$  Read First try  $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

read_test_packet: list = (126, 7, 0, 18, 1, 7, 0, 8, 0, 41, 126)
myWrite_read_Packet_Cls_Obj.encapsulate_read_frame(read_test_packet)
print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n\n\n")

print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Read Second try $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

read_test2_packet: list = (126, 11, 0, 18, 1, 7, 0, 8, 0, 36, 125, 94, 53, 97, 126)
myWrite_read_Packet_Cls_Obj.encapsulate_read_frame(read_test2_packet)

print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n\n\n")

print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Read 3rd try $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

read_test3_packet: list = (126, 18, 0, 59, 0, 0, 0, 2, 32, 0, 1, 64, 0, 0, 160, 0, 0, 192, 0, 16, 32, 126)
myWrite_read_Packet_Cls_Obj.encapsulate_read_frame(read_test3_packet)

print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n\n\n")

sys.exit()