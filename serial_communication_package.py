import sys
import copy
import json

class CRC(object):
    ESCAPE_CHAR = b'\x7D'
    MAX_PAYLOAD_VAL = 25
    OFFSET=4
    flag_stuff = 0

    key_list=[  'Delimiter_1st_position',
                'Length',
                'Control',
                'Opcode',
                'Payload_1_byte',
                'Payload_2_byte',
                'Payload_3_byte',
                'Payload_4_byte',
                'Payload_5_byte',
                'Payload_6_byte',
                'Payload_7_byte',
                'Payload_8_byte',
                'Payload_9_byte',
                'Payload_10_byte',
                'Payload_11_byte',
                'Payload_12_byte',
                'Payload_13_byte',
                'Payload_14_byte',
                'Payload_15_byte',
                'Payload_16_byte',
                'Payload_17_byte',
                'Payload_18_byte',
                'Payload_19_byte',
                'Payload_20_byte',
                'Payload_21_byte',
                'Payload_22_byte',
                'Payload_23_byte',
                'Payload_24_byte',
                'Payload_25_byte',
                'Checksum',
                'Delimiter_last_position']
    Request_Package = {};
    Encapsulate_Package = {};
    Response_Package = {};
    Basic_Package = dict(Delimiter_1st_position=b'\x7E', Length=b'\x30', Control=b'\x00', Opcode=b'\x17',
                         Payload_1_byte=b'\x01', Payload_2_byte=b'\x02', Payload_3_byte=b'\x03', Payload_4_byte=b'\x04',
                         Payload_5_byte=b'\x05', Payload_6_byte=b'\x06', Payload_7_byte=b'\x07', Payload_8_byte=b'\x08',
                         Payload_9_byte=b'\x09', Payload_10_byte=b'\x0A', Payload_11_byte=b'\x0B',
                         Payload_12_byte=b'\x0C', Payload_13_byte=b'\x0D', Payload_14_byte=b'\x0E',
                         Payload_15_byte=b'\x0F', Payload_16_byte=b'\x11', Payload_17_byte=b'\x10',
                         Payload_18_byte=b'\x11', Payload_19_byte=b'\x12', Payload_20_byte=b'\x13',
                         Payload_21_byte=b'\x14', Payload_22_byte=b'\x15', Payload_23_byte=b'\x16',
                         Payload_24_byte=b'\x17', Payload_25_byte=b'\x18', Checksum=b'\x34',
                         Delimiter_last_position=b'\x87')
    send_package:list()

    def __init__(self, polynomial=0x9B, crc_len=8):
        self.poly = polynomial & 0xFF
        self.crc_len = crc_len
        self.table_len = pow(2, crc_len)
        self.cs_table = [' ' for x in range(self.table_len)]

        self.Request_Package = copy.deepcopy(self.Basic_Package)
        self.generate_table()

    def generate_table(self):
        for i in range(len(self.cs_table)):
            curr = i

            for j in range(8):
                if (curr & 0x80) != 0:
                    curr = ((curr << 1) & 0xFF) ^ self.poly
                else:
                    curr <<= 1

            self.cs_table[i] = curr

    def print_table(self):
        for i in range(len(self.cs_table)):
            sys.stdout.write(hex(self.cs_table[i]).upper().replace('X', 'x'))

            if (i + 1) % 16:
                sys.stdout.write(' ')
            else:
                sys.stdout.write('\n')

    def calculate(self, arr, dist=None):
        crc = 0

        try:
            if dist:
                indicies = dist
            else:
                indicies = len(arr)

            for i in range(indicies):
                try:
                    nex_el = int(arr[i])
                except ValueError:
                    nex_el = ord(arr[i])

                crc = self.cs_table[crc ^ nex_el]

        except TypeError:
            crc = self.cs_table[arr]

        return crc

    def encapsulte(self, opcode:int, payload:list):
        temp_payload: list = copy.deepcopy(payload)
        lengthofpayload: int = (len(temp_payload))-1

        try:
            if len(temp_payload):
                #key_list()
                #indicies = dist
                print("list is not empty")
            else:
                print("list is empty")

            for t in range(0,lengthofpayload):
                try:
                    #stuff_Byte
                    if payload[t] == 126:#b'\x7E':
                        print("**********found 7e byte***************")
                        self.flag_stuff = 1
                        temp_loc_i= payload[t]
                        temp_loc_i_plus_1= payload[t+1]
                        payload.insert(t, b'\x7d')
                        temp_loc_i^(1<<5)#flip_bit_location_5
                        payload.insert(t+1, temp_loc_i)
                        payload.insert(t+2, temp_loc_i_plus_1)

                except ValueError:
                    print("Dictionary stuff bytes update exception")

            if(self.flag_stuff == 1):
                self.flag_stuff = 0
                lengthofpayload += 1

            self.Encapsulate_Package = copy.deepcopy(self.Basic_Package)

            for i in range(0,lengthofpayload):
                 try:
                    self.Encapsulate_Package[self.key_list[i+self.OFFSET]] = temp_payload[i];#insert payload to package
                    #print("temp_payload[i]=",temp_payload[i])
                    #print("elf.Encapsulate_Package[self.key_list[i+self.OFFSET]]=",self.Encapsulate_Package[self.key_list[i]])
                 except ValueError:
                    print("Dictionary encapsulate update exception")

            for j in range((self.OFFSET+lengthofpayload),(self.MAX_PAYLOAD_VAL+self.OFFSET)):
                try:
                    print("enter delete location=",j)
                    #print("enter delete items iteration=",(self.MAX_PAYLOAD_VAL-lengthofpayload))
                    print("enter delete KEY=",self.key_list[j])
                    print("enter delete VALUE=",self.Encapsulate_Package[self.key_list[j]])
                    del self.Encapsulate_Package[self.key_list[j]]
                   # self.removekeyValue(self.Encapsulate_Package,self.key_list[j+lengthofpayload])
                except ValueError:
                    print("Dictionary encapsulate remove items from payload exception")
                    #nex_el = ord(arr[i])

                #crc = self.cs_table[crc ^ nex_el]


        except TypeError:
            print("TypeError exception2")
            #crc = self.cs_table[arr]
        return 0

    def dict_to_binary(the_dict):
        str = json.dumps(the_dict)
        binary = ' '.join(format(ord(letter), 'b') for letter in str)
        return binary

    def binary_to_dict(the_binary):
        jsn = ''.join(chr(int(x, 2)) for x in the_binary.split())
        d = json.loads(jsn)
        return d

    def dic_2_list(self,the_dictionary):
        self.send_package=[*the_dictionary.values()]
        return self.send_package

myCRC = CRC(polynomial=0x9B, crc_len=8)
#print(myCRC.calculate([2, 5, 8, 1]))
print(myCRC.calculate([2, 5, 8, 1,10,23,45,67]))

print("type(Basic_Package)=",type(myCRC.Basic_Package))
print("Basic_Package=",myCRC.Basic_Package)

result = bytes.fromhex("84")
amir=b'\x87'
print("Result=",result)
print("amir=",amir)
print("Hello World")

myCRC2 = CRC(polynomial=0x9B, crc_len=8)

list1=[15,126,19,12,5]
opcode= 124#int(b'\xd7')
myCRC2.encapsulte(opcode,list1)

#test=byte_array(myCRC2.Encapsulate_Package)



#print(myCRC.calculate([2, 5, 8, 1]))
print("myCRC2.key_list = ",myCRC2.key_list)
print("myCRC2.RequestPackage = ",myCRC2.key_list)
print("myCRC2 = ",myCRC2.calculate([myCRC2.Encapsulate_Package.get('Opcode'), myCRC2.Encapsulate_Package.get('Payload_1_byte'), myCRC2.Encapsulate_Package.get('Payload_2_byte'), 1,10,23,45,67]))
print("myCRC2.Encapsulate_Package AFTER = ",myCRC2.Encapsulate_Package)
print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

#s = json.dumps(myCRC2.Encapsulate_Package)
variables2:list = myCRC2.dic_2_list(myCRC2.Encapsulate_Package)
#assert variables == variables2
print("variables2=",variables2)