###################################################################################################
#Description      : This script generates user data file by processing EEPROM bins for K26_SOM,
#                   KV_CC, KR_CC
#Author           : Sharathk
#Version          : 2.0
###################################################################################################
import sys
import os
import codecs
import shutil

def write_binary_data_to_file(fp, loop, data, posRd, posWr):
    for i in range(loop):
            fp.seek(posWr+i*2)
            fp.write(data[posRd+i].encode("hex"))

def write_ascii_data_to_file(fp, loop, data, posRd, posWr):
    for i in range(loop):
        if (ord(data[posRd+i]) is 0 or ord(data[posRd+i]) is 0x20):
            fp.seek(posWr+i)
            fp.write('"')
            break
        else:
            fp.seek(posWr+i)
            fp.write(data[posRd+i])
            if i == loop-1:
                fp.write('"')

def strngConv(num):
    strn = ""
    for x in range(num):
        strn += binData[x+22]
    return strn

if not os.path.exists("Output"):
    os.makedirs("Output")
filePtrRd = open(sys.argv[1], "r+b")
binData = filePtrRd.read()

brdNm = strngConv(7)
brd=""
if ((brdNm == "SM-K26-") or (brdNm == "SMK-K26")):
    print("K26 SOM EEPROM")
    shutil.copyfile("./DataFeed/k26_data_ref.py", "./Output/k26_data_read.py")
    filePtrWr = open("./Output/k26_data_read.py", "r+w")
    brd = "K26"
elif (brdNm == "SCK-KV-"):
    print("KV CC SOM EEPROM")
    shutil.copyfile("./DataFeed/kv_cc_data_ref.py", "./Output/kv_cc_data_read.py")
    filePtrWr = open("./Output/kv_cc_data_read.py", "r+w")
    brd = "KVCC"
elif (brdNm == "SCK-KR-"):
    print("KR CC SOM EEPROM")
    shutil.copyfile("./DataFeed/kr_cc_data_ref.py", "./Output/kr_cc_data_read.py")
    filePtrWr = open("./Output/kr_cc_data_read.py", "r+w")
    brd = "KRCC"
else:
    print("Not a valid EEPROM bin")

#Product Info Area
write_binary_data_to_file(filePtrWr, 0x1, binData, 0x4, 0x1BC)
#Board Manufacturer
write_ascii_data_to_file(filePtrWr, 0x6, binData, 0xF, 0x1EF)
#Board Product name
write_ascii_data_to_file(filePtrWr, 0x10, binData, 0x16, 0x220)
#Board Serial number
write_ascii_data_to_file(filePtrWr, 0x10, binData, 0x27, 0x25B)
#Board Part number
write_ascii_data_to_file(filePtrWr, 0x9, binData, 0x38, 0x292)
#Revision Number
write_ascii_data_to_file(filePtrWr, 0x8, binData, 0x44, 0x2BF)
#Device ID
write_binary_data_to_file(filePtrWr, 0x2, binData, 0x4F, 0x2E4)
#Sub Vendor ID
write_binary_data_to_file(filePtrWr, 0x2, binData, 0x51, 0x30E)
#Sub Device ID
write_binary_data_to_file(filePtrWr, 0x2, binData, 0x53, 0x338)

if (brd != "KVCC"):
    if (brd == "K26"):
        #SOM MAC ID 0
        write_binary_data_to_file(filePtrWr, 0x6, binData, 0x83, 0x363)
        #Primary boot memory
        write_ascii_data_to_file(filePtrWr, 0xC, binData, 0x99, 0x39C)
        #Secondary boot memory
        write_ascii_data_to_file(filePtrWr, 0xC, binData, 0xAE, 0x3D8)
        #SOM PS DDR memory
        write_ascii_data_to_file(filePtrWr, 0xC, binData, 0xC3, 0x40D)
        #SOM PL DDR memory
        write_ascii_data_to_file(filePtrWr, 0xC, binData, 0xD8, 0x442)
    if (brd == "KRCC"):
        #KR CC PS MAC ID 1
        write_binary_data_to_file(filePtrWr, 0x6, binData, 0x83, 0x36A)
        #KR CC PL MAC ID 0
        write_binary_data_to_file(filePtrWr, 0x6, binData, 0x89, 0x3A4)
        #KR CC PL MAC ID 1
        write_binary_data_to_file(filePtrWr, 0x6, binData, 0x8F, 0x3DE)
