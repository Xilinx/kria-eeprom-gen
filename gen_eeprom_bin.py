###################################################################################################
#Description      : This script generates EEPROM Content in alignment to Xilinx_SOM_EEPROM_r7 
#                   Specification by processing user data for K24_SOM K26_SOM, KV_CC, KR_CC
#                   KD_CC boards
#Author           : Sharathk
#Version          : 2.0
###################################################################################################
import os
import sys
import struct
import shutil
import datetime
import uuid


bArray = bytearray()
sel = 0

def total_seconds(td):
    # Keep backward compatibility with Python 2.6 which doesn't have
    # this method
    if hasattr(td, 'total_seconds'):
        return td.total_seconds()
    else:
        return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6

def calc_uuid4(fp, pos):
    id = uuid.uuid4()
    data = id.hex
    for i in range(16):
        fp.seek(pos+i)
        fp.write(struct.pack("B", int(data[i*2:i*2+2], 16)))

def write_to_bin_file(fp, data, pos, size):
    fp.seek(pos)
    if len(data) > size:
        for i in range(size):
            fp.write(data[i])
    else:
        fp.write(data)

def calc_checksum(fp, num, pos):
    total_sum = 0
    fp.seek(pos)
    for i in range(num):
        #print(i)
        total_sum = total_sum + int(fp.read(1).encode('hex'), 16)
    #print(total_sum)
    lsb_byte = (total_sum & 0xFF)
    if lsb_byte == 0:
        return 0xFF
    else:
        return (0x100 - lsb_byte)
    
def calc_mfg_time():
    current_time = datetime.datetime.now()
    diff_date = (current_time - datetime.datetime(1996, 1, 1))
    minutes = total_seconds(diff_date)/60
    #print(minutes)
    return minutes

#Menu selection for SOM/KV/KR/KD EEPROMS
sys.path.insert(1, './InputData/')
print("Please provide proper user inputs in data.py file")
print("Select 1 for k26_som_eeprom")
print("Select 2 for k24_som_eeprom")
print("Select 3 for kv_cc_eeprom")
print("Select 4 for kr_cc_eeprom")
print("Select 5 for kd_cc_eeprom")
print("Select 6 for removing Output dir")
if not os.path.exists("Output"):
    os.makedirs("Output")
sel = input ("Please Select any one of above: ")
if sel == 1:
    shutil.copyfile("./DataFeed/k26_som_ref.bin", "./Output/k26_som_eeprom.bin")
    filePtr = open("./Output/k26_som_eeprom.bin", "r+b")
    from k26_data import *
elif sel == 2:
    shutil.copyfile("./DataFeed/k24_som_ref.bin", "./Output/k24_som_eeprom.bin")
    filePtr = open("./Output/k24_som_eeprom.bin", "r+b")
    from k24_data import *
elif sel == 3:
    shutil.copyfile("./DataFeed/kv_cc_ref.bin", "./Output/kv_cc_eeprom.bin")
    filePtr = open("./Output/kv_cc_eeprom.bin", "r+b")
    from kv_cc_data import *
elif sel == 4:
    shutil.copyfile("./DataFeed/kr_cc_ref.bin", "./Output/kr_cc_eeprom.bin")
    filePtr = open("./Output/kr_cc_eeprom.bin", "r+b")
    from kr_cc_data import *
elif sel == 5:
    shutil.copyfile("./DataFeed/kd_cc_ref.bin", "./Output/kd_cc_eeprom.bin")
    filePtr = open("./Output/kd_cc_eeprom.bin", "r+b")
    from kd_cc_data import *
elif sel == 6:
    shutil.rmtree("Output")
    exit()
else:
    print("Invalid Choice.")
    exit()

#Table: 4, SOM & CC Common Header and Board Area
#Common Header (8 Bytes)
print('Writing Common Header Area...')
write_to_bin_file(filePtr, PRD_INFO_0x04.decode("hex"), 0x4, 1)
write_to_bin_file(filePtr, struct.pack("B", calc_checksum(filePtr, 0x7, 0x0)),0x7, 1)
#Board Area(96 or 72 Bytes)
print('Writing Board Area...')
bArray = struct.pack("<L", calc_mfg_time())
write_to_bin_file(filePtr, bArray[:3], 0xB, 3)
write_to_bin_file(filePtr, BRD_MANUFACTURER_0x0F, 0xF, 6)
if sel == 1 or sel == 2:
    write_to_bin_file(filePtr, BRD_PRODUCT_0x16, 0x16, 16)
write_to_bin_file(filePtr, BRD_SERIAL_0x27, 0x27, 16)
write_to_bin_file(filePtr, BRD_PART_0x38, 0x38, 9)
write_to_bin_file(filePtr, REV_NUM_0x44, 0x44, 8)
write_to_bin_file(filePtr, DEV_ID_0x4F.decode("hex"), 0x4F, 2)
write_to_bin_file(filePtr, SUB_VEN_ID_0x51.decode("hex"), 0x51, 2)
write_to_bin_file(filePtr, SUB_DEV_ID_0x53.decode("hex"), 0x53, 2)
calc_uuid4(filePtr,0x56)
write_to_bin_file(filePtr, struct.pack("B", calc_checksum(filePtr, 0x5F, 0x8)),0x67, 1)

if sel == 1 or sel == 2:
    #Table: 8, Xilinx SOM MAC Addr Multi Record
    print('Writing MAC Addr Multi Record Area...')
    write_to_bin_file(filePtr, SOM_MAC_ID_0_0x83.decode("hex"), 0x83, 6)
    write_to_bin_file(filePtr, struct.pack("B", calc_checksum(filePtr, 0xA, 0x7F)),0x7D, 1)
    write_to_bin_file(filePtr, struct.pack("B", calc_checksum(filePtr, 0x4, 0x7A)),0x7E, 1)

    #Table: 11, Xilinx SOM Memory Config Multi Record
    print('Writing Config Multi Record Area...')
    write_to_bin_file(filePtr, MEM_PRIMARY_0x99, 0x99, 12)
    write_to_bin_file(filePtr, MEM_SECONDARY_0xAE, 0xAE, 12)
    write_to_bin_file(filePtr, MEM_PS_DDR_0xC3, 0xC3, 12)
    write_to_bin_file(filePtr, MEM_PL_DDR_0xD8, 0xD8, 12)
    write_to_bin_file(filePtr, struct.pack("B", calc_checksum(filePtr, 0x57, 0x8E)),0x8C, 1)
    write_to_bin_file(filePtr, struct.pack("B", calc_checksum(filePtr, 0x4, 0x89)),0x8D, 1)
elif sel == 4:
    #Table: 9, Xilinx KR CC MAC Addr Multi Record
    print('Writing KR CC MAC Addr Multi Record Area...')
    write_to_bin_file(filePtr, KR_PS_MAC_ID_1_0x83.decode("hex"), 0x83, 6)
    write_to_bin_file(filePtr, KR_PL_MAC_ID_0_0x89.decode("hex"), 0x89, 6)
    write_to_bin_file(filePtr, KR_PL_MAC_ID_1_0x8F.decode("hex"), 0x8F, 6)
    write_to_bin_file(filePtr, struct.pack("B", calc_checksum(filePtr, 0x16, 0x7F)),0x7D, 1)
    write_to_bin_file(filePtr, struct.pack("B", calc_checksum(filePtr, 0x4, 0x7A)),0x7E, 1)
elif sel == 5:
    #Table: 9, Xilinx KD CC MAC Addr Multi Record
    print('Writing KD CC MAC Addr Multi Record Area...')
    write_to_bin_file(filePtr, KD_PL_MAC_ID_0_0x83.decode("hex"), 0x83, 6)
    write_to_bin_file(filePtr, KD_PL_MAC_ID_1_0x89.decode("hex"), 0x89, 6)
    write_to_bin_file(filePtr, struct.pack("B", calc_checksum(filePtr, 0x10, 0x7F)),0x7D, 1)
    write_to_bin_file(filePtr, struct.pack("B", calc_checksum(filePtr, 0x4, 0x7A)),0x7E, 1)
else:
    pass

print("EEPROM bin sucessfully generated")
filePtr.close()

