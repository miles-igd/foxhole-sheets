#derived from UassetTool by FluffyQuack http://modderbase.com/showthread.php?tid=369

import os

from ctypes import c_ulong
from collections import namedtuple

DDSHeaderDefaults_DXT5 = [
    c_ulong(542327876),     #dwMagicWord
    c_ulong(124),           #dwSize
    c_ulong(135175),        #dwFlags
    c_ulong(1024),          #dwHeight
    c_ulong(1024),          #dwWidth
    c_ulong(0),             #dwPitchOrLinearSize
    c_ulong(0),             #dwDepth
    c_ulong(11),            #dwMipMapCount
    c_ulong(0),             #dwReserved1
    c_ulong(32),            #dwSize
    c_ulong(4),             #dwFlags
    c_ulong(894720068),     #dwFourCC (DXT5)
    c_ulong(0),             #dwRGBBitCount
    c_ulong(0),             #dwRBitMask
    c_ulong(0),             #dwGBitMask
    c_ulong(0),             #dwBBitMask
    c_ulong(0),             #dwABitMask
    c_ulong(4198408),       #dwCaps
    c_ulong(0),             #dwCaps2
    c_ulong(0),             #dwCaps3
    c_ulong(0),             #dwCaps4
    c_ulong(0),             #dwReserved2
]

DDSHeaderDefaults_DXT1 = [
    c_ulong(542327876),     #dwMagicWord
    c_ulong(124),           #dwSize
    c_ulong(135175),        #dwFlags
    c_ulong(1024),          #dwHeight
    c_ulong(1024),          #dwWidth
    c_ulong(0),             #dwPitchOrLinearSize
    c_ulong(0),             #dwDepth
    c_ulong(11),            #dwMipMapCount
    c_ulong(0),             #dwReserved1
    c_ulong(32),            #dwSize
    c_ulong(4),             #dwFlags
    c_ulong(827611204),     #dwFourCC (DXT1)
    c_ulong(0),             #dwRGBBitCount
    c_ulong(0),             #dwRBitMask
    c_ulong(0),             #dwGBitMask
    c_ulong(0),             #dwBBitMask
    c_ulong(0),             #dwABitMask
    c_ulong(4096),          #dwCaps
    c_ulong(0),             #dwCaps2
    c_ulong(0),             #dwCaps3
    c_ulong(0),             #dwCaps4
    c_ulong(0),             #dwReserved2
]

DDSHeaderDefaults_RGBA = [
    c_ulong(542327876),     #dwMagicWord
    c_ulong(124),           #dwSize
    c_ulong(4111),          #dwFlags
    c_ulong(32),            #dwHeight
    c_ulong(32),            #dwWidth
    c_ulong(128),           #dwPitchOrLinearSize
    c_ulong(0),             #dwDepth
    c_ulong(11),            #dwMipMapCount
    c_ulong(0),             #dwReserved1
    c_ulong(32),            #dwSize
    c_ulong(65),            #dwFlags
    c_ulong(0),             #dwFourCC (DXT1)
    c_ulong(32),            #dwRGBBitCount
    c_ulong(16711680),      #dwRBitMask
    c_ulong(65280),         #dwGBitMask
    c_ulong(255),           #dwBBitMask
    c_ulong(4278190080),    #dwABitMask
    c_ulong(4096),          #dwCaps
    c_ulong(0),             #dwCaps2
    c_ulong(0),             #dwCaps3
    c_ulong(0),             #dwCaps4
    c_ulong(0),             #dwReserved2
]

DDSHeaderDefaults_RGB = [
    c_ulong(542327876),     #dwMagicWord
    c_ulong(124),           #dwSize
    c_ulong(4111),          #dwFlags
    c_ulong(32),            #dwHeight
    c_ulong(32),            #dwWidth
    c_ulong(128),           #dwPitchOrLinearSize
    c_ulong(0),             #dwDepth
    c_ulong(11),            #dwMipMapCount
    c_ulong(0),             #dwReserved1
    c_ulong(32),            #dwSize
    c_ulong(65),            #dwFlags
    c_ulong(0),             #dwFourCC
    c_ulong(24),            #dwRGBBitCount
    c_ulong(16711680),      #dwRBitMask
    c_ulong(65280),         #dwGBitMask
    c_ulong(255),           #dwBBitMask
    c_ulong(4278190080),    #dwABitMask
    c_ulong(4096),          #dwCaps
    c_ulong(0),             #dwCaps2
    c_ulong(0),             #dwCaps3
    c_ulong(0),             #dwCaps4
    c_ulong(0),             #dwReserved2
]

DDSHeaderDefaults_3Dc = [
    c_ulong(542327876),     #0 dwMagicWord 
    c_ulong(124),           #1 dwSize
    c_ulong(659463),        #2 dwFlags
    c_ulong(1024),          #3 dwHeight
    c_ulong(512),           #4 dwWidth
    c_ulong(524288),        #5 dwPitchOrLinearSize
    c_ulong(0),             #6 dwDepth
    c_ulong(10),            #7 dwMipMapCount
    c_ulong(0),             #8 dwReserved1
    c_ulong(32),            #9 dwSize
    c_ulong(2147483652),    #10 dwFlags
    c_ulong(843666497),     #11 dwFourCC
    c_ulong(1498952257),    #12 dwRGBBitCount
    c_ulong(0),             #13 dwRBitMask
    c_ulong(0),             #14 dwGBitMask
    c_ulong(0),             #15 dwBBitMask
    c_ulong(0),             #16 dwABitMask
    c_ulong(4198408),       #17 dwCaps
    c_ulong(0),             #18 dwCaps2
    c_ulong(0),             #19 dwCaps3
    c_ulong(0),             #20 dwCaps4
    c_ulong(0),             #21 dwReserved2
]

MAGIC_WORD = b"\x00\x08\x00\x00\x00\x50\x46\x5F"
MIP_MAGIC_WORD = b"\x01\x00\x00\x00\x48\x00\x00\x00"
BIT_SIZES = {
    "DXT1": 8,
    "DXT3": 16,
    "DXT5": 16,
    "BC5": 16,
    "RGBA": 32,
}

MipInfo = namedtuple("MipInfo", ["size", "offset", "width", "height"])

def acquire_texture_information(data):
    mips = []
    mip_count = 0
    location = data.find(MAGIC_WORD)

    if location == -1:
        print("Error: Could not find DDS data in file.")
        return

    dxt_type = data[location+8: location+8+4]
    location += 12

    while True:
        next_offset = data[location:].find(MIP_MAGIC_WORD)
        location = location + next_offset

        if next_offset == -1:
            if mip_count == 0:
                print("Error: No mips found.")
            break
        
        new_MipInfo = []
        location +=8
        new_MipInfo.append(data[location:location+4])
        location +=4

        if new_MipInfo[0] != data[location:location+4]:
            print("Error: Size values not matching up.");
            return
        location += 4

        new_MipInfo.append(data[location:location+8])
        offset = int.from_bytes(new_MipInfo[1], "little")
        size = int.from_bytes(new_MipInfo[0], "little")
        location = offset + size
        new_MipInfo.append(data[location:location+4])
        location += 4
        new_MipInfo.append(data[location:location+4])
        location += 4

        mip_count += 1
        mips.append(MipInfo(*new_MipInfo))

    return mips, dxt_type

def extract_dds(filename):
    '''
    returns dds fileobj bytestring (ready to write)
    '''

    with open(filename, "rb") as file:
        data = file.read()
        mips, dxt_type = acquire_texture_information(data)

    header = None
    if dxt_type == b"DXT1":
        header = list(DDSHeaderDefaults_DXT1)
    elif dxt_type == b"DXT3":
        header = list(DDSHeaderDefaults_DXT1)
        header[11] = c_ulong(861165636)
    elif dxt_type == b"DXT5":
        header = list(DDSHeaderDefaults_DXT5)
    
    header[4] = mips[0][2]
    header[3] = mips[0][3]
    header[7] = c_ulong(len(mips))
    header[8] = b"\x00\x00\x00\x00"*11 #HEADER-HAX

    if filename.endswith(".Texture2D"):
        filename = filename.rsplit(".")[0]
        
    dds_path = f"{os.path.basename(filename)}.dds"
    dds_header = b""
    for part in header:
        dds_header = dds_header + bytes(part)

    for mip in mips:
        offset = int.from_bytes(mip[1], "little")
        size = int.from_bytes(mip[0], "little")
        dds_header = dds_header + data[offset:offset+size]
    '''
    with open(dds_path, "wb") as file:
        file.write(dds_header)
        for mip in mips:
            offset = int.from_bytes(mip[1], "little")
            size = int.from_bytes(mip[0], "little")
            file.write(data[offset:offset+size])
    '''
    return dds_header