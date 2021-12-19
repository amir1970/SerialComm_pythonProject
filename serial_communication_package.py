import sys
import functools
import struct

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

        tmp_payload = bytearray(payload)
        index_7e: int = tmp_payload.find(126)

        if index_7e == -1:
            print("Not Found 7e ")
        else:
            print("Found 7e at location ", index_7e)
            tmp_payload.insert(index_7e, 125)  # 7D
            tmp_payload.insert(index_7e + 1, tmp_payload[index_7e + 1] ^ (1 << 5))  # 7E inverted bit 5
            del tmp_payload[index_7e + 2:index_7e + 3]  # 7E deleted

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

    def handle_read_opcode_0x3b(self,read_packet_btained):  # , rx_pack_opcode_0x3b:bytearray):
        list_index: list = [5, 9, 13, 17, 21]
        meas_result = []
        print("meas_result", meas_result)
        for index_i in list_index:
            int_val1: int = int.from_bytes(read_packet_btained[index_i:index_i + 3], "big")
            print("index i is = ", index_i, "struct.pack1 new = ", int_val1)
            meas_result.append(int_val1)
            print("meas_result after append", meas_result)
            return meas_result

    def encapsulate_read_frame(self, read_payload: list):
        # print(" payload rx =", read_payload)
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
            self.handle_read_opcode_0x3b(self.read_package)

        for x in self.read_package: print(x)
        print()
        for y in self.read_package: print(hex(y))
        print()
        return self.read_package

    def access_bit(self, data, num):
        base = int(num // 8)
        shift = int(num % 8)
        return (data[base] >> shift) & 0x1

    # def read_channel_and_milivolt(self,rd_packet:bytearray):
    #     milivolt:int=0
    #     print("rd_packet[x:x+2]=", rd_packet[0:2])
    #     self.channel_mask_location = self.rd_packet[0:1] & 0xE0  # bits 7:5 are relevant for channel
    #     milivolt = self.rd_packet[0:3] & 0x1F_FF_FF  # bits 7:5 are relevant for channel
    #     print("milivolt=", milivolt)
    #     return milivolt

    def extractKBits(num, k, p):
        # convert number into binary first
        binary = bin(num)

        # remove first two characters
        binary = binary[2:]

        end = len(binary) - p
        start = end - k + 1

        # extract k  bit sub-string
        kBitSubStr = binary[start: end + 1]

        # convert extracted sub-string into decimal again
        print(int(kBitSubStr, 2))


myWrite_read_Packet_Cls_Obj = Write_Read_Packet_Cls()

print("================  Write First try   ==========================")

myWrite_read_Packet_Cls_Obj.write_encapsulate_frame(0x12, [1, 7, 0, 8, 0])

print("=========================================================\n\n\n")

print("==================Write Second try ======================")

myWrite_read_Packet_Cls_Obj.write_encapsulate_frame(0x12, [1, 7, 0, 8, 0, 36, 126, 53])

print("=========================================================\n\n\n")

# myRead_Packet_Cls2 = Read_Packet_Cls()

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
#channels_read2 = bytes(myWrite_read_Packet_Cls_Obj.read_package)
# channels_read2.append(myWrite_read_Packet_Cls_Obj.read_package[5] & 0xE0)
# channels_read2.append(myWrite_read_Packet_Cls_Obj.read_package[9] & 0xE0)
# channels_read2.append(myWrite_read_Packet_Cls_Obj.read_package[13] & 0xE0)
# channels_read2.append(myWrite_read_Packet_Cls_Obj.read_package[17] & 0xE0)
# channels_read2.append(myWrite_read_Packet_Cls_Obj.read_package[21] & 0xE0)

#print("channels_read2=", channels_read2)

# measured_voltage_read2=bytes(myWrite_read_Packet_Cls_Obj.read_package)
# index_i: int = 5
# sliced_meas_volt1 = bytearray(myWrite_read_Packet_Cls_Obj.read_package[index_i:index_i + 3])
# sliced_meas_volt2 = bytearray(myWrite_read_Packet_Cls_Obj.read_package[index_i + 4:index_i + 7])
# sliced_meas_volt3 = bytearray(myWrite_read_Packet_Cls_Obj.read_package[index_i + 8:index_i + 11])
# sliced_meas_volt4 = bytearray(myWrite_read_Packet_Cls_Obj.read_package[index_i + 12:index_i + 15])
# sliced_meas_volt5 = bytearray(myWrite_read_Packet_Cls_Obj.read_package[index_i + 16:index_i + 19])
# print("sliced_meas_volt_1=", sliced_meas_volt1)
# print("sliced_meas_volt_2=", sliced_meas_volt2)
# print("sliced_meas_volt_3=", sliced_meas_volt3)
# print("sliced_meas_volt_4=", sliced_meas_volt4)
# print("sliced_meas_volt_5=", sliced_meas_volt5)

# measured_voltage_read2.append(myWrite_read_Packet_Cls_Obj.read_package[5:8])
# measured_voltage_read2.append(myWrite_read_Packet_Cls_Obj.read_package[9:12])
# measured_voltage_read2.append(myWrite_read_Packet_Cls_Obj.read_package[13:15])
# measured_voltage_read2.append(myWrite_read_Packet_Cls_Obj.read_package[17:20])
# measured_voltage_read2.append(myWrite_read_Packet_Cls_Obj.read_package[21:24])

# print("measured_voltage_read2=", measured_voltage_read2)
# return 0
# print([myWrite_read_Packet_Cls_Obj.access_bit(myWrite_read_Packet_Cls_Obj.read_package, y) for y in
#        range(len(myWrite_read_Packet_Cls_Obj.read_package) * 8)])
#
# print("sliced_meas_volt1=",
#       [myWrite_read_Packet_Cls_Obj.access_bit(sliced_meas_volt1, y) for y in range(len(sliced_meas_volt1) * 8)])
# print("sliced_meas_volt2=",
#       [myWrite_read_Packet_Cls_Obj.access_bit(sliced_meas_volt2, y) for y in range(len(sliced_meas_volt2) * 8)])
# print("sliced_meas_volt3=",
#       [myWrite_read_Packet_Cls_Obj.access_bit(sliced_meas_volt3, y) for y in range(len(sliced_meas_volt3) * 8)])
# print("sliced_meas_volt4=",
#       [myWrite_read_Packet_Cls_Obj.access_bit(sliced_meas_volt4, y) for y in range(len(sliced_meas_volt4) * 8)])
# print("sliced_meas_volt5=",
#       [myWrite_read_Packet_Cls_Obj.access_bit(sliced_meas_volt5, y) for y in range(len(sliced_meas_volt5) * 8)])

#var = struct.pack(sliced_meas_volt1)
list_index:list=[5,9,13,17,21]
meas_result=[]
print("meas_result",meas_result)
for index_i in list_index:
    #print("index i is = ",index_i)
    int_val1: int = int.from_bytes(myWrite_read_Packet_Cls_Obj.read_package[index_i:index_i + 3], "big")
    print("index i is = ",index_i,"struct.pack1 new = ", int_val1)
    meas_result.append(int_val1)
    print("meas_result after append",meas_result)

#meas_result.append(5)
#index_i: int = 5
#int_val1 = int.from_bytes(myWrite_read_Packet_Cls_Obj.read_package[index_i:index_i + 3], "big")
#int_val2 = int.from_bytes(myWrite_read_Packet_Cls_Obj.read_package[index_i+4:index_i + 7], "big")
#int_val3 = int.from_bytes(myWrite_read_Packet_Cls_Obj.read_package[index_i+8:index_i + 11], "big")
#int_val4 = int.from_bytes(myWrite_read_Packet_Cls_Obj.read_package[index_i+12:index_i + 15], "big")
#int_val5 = int.from_bytes(myWrite_read_Packet_Cls_Obj.read_package[index_i+16:index_i + 19], "big")

#print("struct.pack1 new = ",int_val1)
#print("struct.pack2 = ",int_val2)
#print("struct.pack3 = ",int_val3)
#print("struct.pack4 = ",int_val4)
#print("struct.pack5 = ",int_val5)
#print("struct.pack",var)

sys.exit()



