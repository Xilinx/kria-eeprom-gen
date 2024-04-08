#!/usr/bin/env python3
#******************************************************************************
# Copyright (c) 2023-2024 Advanced Micro Devices, Inc. All Rights Reserved.
# SPDX-License-Identifier: MIT
#
#Description      : This script generates user data file by processing
#                   EEPROM bins
#Author           : Sharathk
#Version          : 4.0
#
#******************************************************************************
import sys
import os
import codecs
import shutil

def write_binary_data_to_file(fp, loop, data, posRd, posWr):
    for i in range(loop):
            fp.seek(posWr+i*2)
            fp.write(str(format(data[posRd+i], '02x')))

def write_ascii_data_to_file(fp, loop, data, posRd, posWr):
    for i in range(loop):
        if ((data[posRd+i] == 0) or (data[posRd+i] == 0x20)):
            fp.seek(posWr+i)
            fp.write('"')
            break
        else:
            fp.seek(posWr+i)
            fp.write(chr(data[posRd+i]))
            if i == loop-1:
                fp.write('"')

if not os.path.exists("Output"):
    os.makedirs("Output")

if len(sys.argv) == 1:
   print('Pass eeprom bin file to process')
   sys.exit()

filePtrRd = open(sys.argv[1], "r+b")
binData = filePtrRd.read()

brdNm = str(binData[22:29], 'utf-8')
brd=""
if ((brdNm == "SM-K26-") or (brdNm == "SMK-K26")):
    print("K26 SOM EEPROM")
    shutil.copyfile("./DataFeed/k26_data_ref.py", "./Output/k26_data_read.py")
    filePtrWr = open("./Output/k26_data_read.py", "r+")
    brd = "K26"
elif ((brdNm == "SM-K24-") or (brdNm == "SMK-K24")):
    print("K24 SOM EEPROM")
    shutil.copyfile("./DataFeed/k24_data_ref.py", "./Output/k24_data_read.py")
    filePtrWr = open("./Output/k24_data_read.py", "r+")
    brd = "K24"
elif (brdNm == "SCK-KV-"):
    print("KV CC SOM EEPROM")
    shutil.copyfile("./DataFeed/kv_cc_data_ref.py", "./Output/kv_cc_data_read.py")
    filePtrWr = open("./Output/kv_cc_data_read.py", "r+")
    brd = "KVCC"
elif (brdNm == "SCK-KR-"):
    print("KR CC SOM EEPROM")
    shutil.copyfile("./DataFeed/kr_cc_data_ref.py", "./Output/kr_cc_data_read.py")
    filePtrWr = open("./Output/kr_cc_data_read.py", "r+")
    brd = "KRCC"
elif (brdNm == "SCK-KD-"):
    print("KD CC SOM EEPROM")
    shutil.copyfile("./DataFeed/kd_cc_data_ref.py", "./Output/kd_cc_data_read.py")
    filePtrWr = open("./Output/kd_cc_data_read.py", "r+")
    brd = "KDCC"
else:
    print("Not a valid EEPROM bin")
    exit()

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
    if (brd == "K26") or (brd == "K24"):
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
    if (brd == "KDCC"):
        #KD CC PL MAC ID 0
        write_binary_data_to_file(filePtrWr, 0x6, binData, 0x83, 0x36A)
        #KD CC PL MAC ID 1
        write_binary_data_to_file(filePtrWr, 0x6, binData, 0x89, 0x3A4)
