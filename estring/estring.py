import struct
import elist.elist as elel
import re


#LE           Little- Endian
#BE           Big-Endian
#OOB          Out-Of-Band

#chbyts      char-bytes
#bytstrm     bytes-stream
#rm          remove

#BOM 是整个字节流有一个，而不是每个char-bytes
#不带le ,be 的encode keywords,既可以处理 带LE-BOM的(LE 的) 也能处理不带BOM的
#BOM 可以用来标明字节顺序 LE or BE
#utf-8 不需要
#这样如果接收者收到 FEFF，就表明这个字节流是 Big-Endian 的；
#如果收到FFFE 就表明这个字节流是 Little- Endian 的
# '你'.encode('utf_16')
# b'\xff\xfe`O'
# 表明utf_16的编码默认是 LE
# b'`O' == b'\x60\x4f'
# 那么 就是说4f在前60在后
# >>> '\u4f60'
# '你'
# >>>
# '你'.encode('utf_16_le')  是不带BOM的
# b'`O'
# '你'.encode('utf_16_be')  是不带BOM的
# b'O`' == b'\x4f\x60'
# 使用\u显示时 都是BE 序列 

def get_bominfo(bs,**kwargs):
    '''
        #only support utf-16 utf-32
        #LE           Little- Endian
        #BE           Big-Endian
        #OOB          Out-Of-Band (withour BOM)
        
        bs = b'\xff\xfe\x60\x4f'
        get_bominfo(bs)
        bs = b'\x60\x4f'
        get_bominfo(bs)
        bs = b'\xfe\xff\x4f\x60'
        get_bominfo(bs)
        bs = b'\x4f\x60'
        get_bominfo(bs)
        bs = b'\xff\xfe\x00\x00\x60\x4f\x00\x00'
        get_bominfo(bs)
        bs = b'\x60\x4f\x00\x00'
        get_bominfo(bs)
        bs = b'\x00\x00\xfe\xff\x00\x00\x4f\x60'
        get_bominfo(bs)
        bs = b'\x00\x00\x4f\x60'
        get_bominfo(bs)
        
    '''
    bom = bs[:4]
    if(bom == b'\xff\xfe\x00\x00'):
        b = bs[4:]
        t = 'LE'
    elif(bom == b'\x00\x00\xfe\xff'):
        b = bs[4:]
        t = 'BE'
    else:
        bom = bs[:2]
        if(bom == b'\xff\xfe'):
            b = bs[2:]
            t = 'LE'
        elif(bom == b'\xfe\xff'):
            b = bs[2:]
            t = 'BE'
        else:
            b = bs
            t = 'OOB'
    return((b,t))

def remove_bom(bs,**kwargs):
    '''
        #only support utf-16 utf-32 
        
        #LE           Little- Endian
        #BE           Big-Endian
        #OOB          Out-Of-Band (withour BOM)
        
        bs = b'\xff\xfe\x60\x4f'
        remove_bom(bs)
        bs = b'\x60\x4f'
        remove_bom(bs)
        bs = b'\xfe\xff\x4f\x60'
        remove_bom(bs)
        bs = b'\x4f\x60'
        remove_bom(bs)
        bs = b'\xff\xfe\x00\x00\x60\x4f\x00\x00'
        remove_bom(bs)
        bs = b'\x60\x4f\x00\x00'
        remove_bom(bs)
        bs = b'\x00\x00\xfe\xff\x00\x00\x4f\x60'
        remove_bom(bs)
        bs = b'\x00\x00\x4f\x60'
        remove_bom(bs)
    '''
    bominfo = get_bominfo(bs,**kwargs)
    return(bominfo[0])


#decode_chbyts         decode-char-bytes (to char)
#byts2chstr            decode-char-bytes (to char)
#unpack_chbyts         decode-char-bytes (to char)

def decode_chbyts(bs,**kwargs):
    '''
        #only support utf-8 utf-16 utf-32 
        
        
        #LE           Little- Endian
        #BE           Big-Endian
        #OOB          Out-Of-Band (withour BOM)
        
        bs = b'\x4f\x60'
        decode_chbyts(bs)
        bs = b'\x4f\x60'
        decode_chbyts(bs,style='js')
        bs = b'\\u4f60'
        decode_chbyts(bs,style='py')
        bs = b'\xff\xfe\x60\x4f'
        decode_chbyts(bs,encode = 'utf_16')
        bs = b'\x60\x4f'
        decode_chbyts(bs,encode = 'utf_16_le')
        bs = b'\xfe\xff\x4f\x60'
        decode_chbyts(bs,encode = 'utf_16_be')
        bs = b'\x4f\x60'
        decode_chbyts(bs,encode = 'utf_16_be')
        bs = b'\xff\xfe\x00\x00\x60\x4f\x00\x00'
        decode_chbyts(bs,encode = 'utf_32')
        bs = b'\x60\x4f\x00\x00'
        decode_chbyts(bs,encode = 'utf_32_le')
        bs = b'\x00\x00\xfe\xff\x00\x00\x4f\x60'
        decode_chbyts(bs,encode = 'utf_32_be')
        bs = b'\x00\x00\x4f\x60'
        decode_chbyts(bs,encode = 'utf_32_be')
    '''
    if('encode' in kwargs):
        encode=kwargs['encode']
    else:
        if('style' in kwargs):
            style = kwargs['style']
        else:
            style = 'js'
        if(style == 'js'):
            encode = 'utf_16_be'
        elif(style == 'py'):
            encode = 'raw_unicode_escape'
        else:
            encode = 'raw_unicode_escape'
    bs = remove_bom(bs,**kwargs)
    ch = bs.decode(encode)
    return(ch)

unpack_chbyts = decode_chbyts
byts2chstr = decode_chbyts

def get_bomtype(bs,**kwargs):
    '''
        #only support utf-16 utf-32 
        
        #LE           Little- Endian
        #BE           Big-Endian
        #OOB          Out-Of-Band (withour BOM)
        
        bs = b'\xff\xfe\x60\x4f'
        bs.decode('utf_16')
        get_bomtype(bs)
        '\u4f60'
        bs = b'\x60\x4f'
        bs.decode('utf_16_le')
        get_bomtype(bs)
        '\u4f60'
        bs = b'\xfe\xff\x4f\x60'
        get_bomtype(bs)
        decode_chbyts(bs,encode='utf_16_be')
        '\u4f60'
        bs = b'\x4f\x60'
        bs.decode('utf_16_be')
        get_bomtype(bs)
        '\u4f60'
        bs = b'\xff\xfe\x00\x00\x60\x4f\x00\x00'
        bs.decode('utf_32')
        get_bomtype(bs)
        '\U00004f60'
        bs = b'\x60\x4f\x00\x00'
        bs.decode('utf_32_le')
        get_bomtype(bs)
        '\U00004f60'
        bs = b'\x00\x00\xfe\xff\x00\x00\x4f\x60'
        decode_chbyts(bs,encode = 'utf_32_be')
        get_bomtype(bs)
        '\U00004f60'
        bs = b'\x00\x00\x4f\x60'
        bs.decode('utf_32_be')
        get_bomtype(bs)
        '\U00004f60'
    '''
    bominfo = get_bominfo(bs,**kwargs)
    return(bominfo[1])


#chstr                        char-string
#pack_chstr                   pack-char-string (to bytes-stream)
#chstr2byts                   pack-char-string (to bytes-stream)
#encode_chstr                 pack-char-string (to bytes-stream)
#chnum                        char-number
#pack_chnum                   pack-char-number (to bytes-stream)
#chnum2byts                   pack-char-number (to bytes-stream)
#encode_chnum                 pack-char-number (to bytes-stream)
#byts2chnum                   bytes-to-char-number

def pack_chstr(chstr,**kwargs):
    '''
        # most javascript use utf_16_be encode
        chstr = '问'
        pack_chstr(chstr)
        pack_chstr(chstr,style='py')
        pack_chstr(chstr,style='js')
        pack_chstr(chstr,encode = 'utf_16')
        pack_chstr(chstr,encode = 'utf_16_le')
    '''
    if('encode' in kwargs):
        encode=kwargs['encode']
    else:
        if('style' in kwargs):
            style = kwargs['style']
        else:
            style = 'js'
        if(style == 'js'):
            encode = 'utf_16_be'
        elif(style == 'py'):
            encode = 'raw_unicode_escape'
        else:
            encode = 'raw_unicode_escape'
    bs = chstr.encode(encode)
    return(bs)

chstr2byts = pack_chstr
encode_chstr = pack_chstr

def pack_chnum(chnum,**kwargs):
    '''
        # most javascript use utf_16_be encode
        chnum = 38382
        pack_chnum(chnum)
        pack_chnum(chnum,style='py')
        pack_chnum(chnum,style='js')
        pack_chnum(chnum,encode = 'utf_16')
        pack_chnum(chnum,encode = 'utf_16_le')
        
        '\u95ee'
    '''
    chstr = chr(chnum)
    bs = pack_chstr(chstr,**kwargs)
    return(bs)

chnum2byts = pack_chnum
encode_chnum = pack_chnum


def byts2chnum(bs,**kwargs):
    '''
        # most javascript use utf_16_be encode
        bs = b'\x95\xee'
        byts2chnum(bs)
        bs = b'\\u95ee'
        byts2chnum(bs,style='py')
        bs = b'\x95\xee'
        byts2chnum(bs,style='js')
        bs = b'\xff\xfe\xee\x95'
        byts2chnum(bs,encode = 'utf_16')
        bs = b'\xee\x95'
        chnum = byts2chnum(bs,encode = 'utf_16_le')
        chnum
        chr(chnum)
    '''
    chstr = decode_chbyts(bs,**kwargs)
    return(ord(chstr))
    

#decode_bytstrm       decode-bytes-stream (to string)
#bytstrm2str          decode-bytes-stream (to string)
#unpack_bytstrm       decode-bytes-stream (to string)

def decode_bytstrm(bs,**kwargs):
    '''
        bs = b'O`Y}T\x17'
        decode_bytstrm(bs)
        bs = b'O`Y}T\x17'
        decode_bytstrm(bs,style='js')
        bs = b'\\u4f60\\u597d\\u5417'
        decode_bytstrm(bs,style='py')
        bs = b'O`Y}T\x17'
        decode_bytstrm(bs,encode='utf_16_be')
        bs = b'\xff\xfe\x00\x00`O\x00\x00}Y\x00\x00\x17T\x00\x00'
        decode_bytstrm(bs,encode='utf_32')
        bs = b'\xe4\xbd\xa0\xe5\xa5\xbd\xe5\x90\x97'
        decode_bytstrm(bs,encode='utf_8')
    '''
    bs = remove_bom(bs)
    s = decode_chbyts(bs,**kwargs)
    return(s)

bytstrm2str = decode_bytstrm
unpack_bytstrm = decode_bytstrm


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



#pack_str                pack-string
#encode_str              pack-string
#str2bytstrm             pack-string

def pack_str(s,**kwargs):
    '''
        s = '你好吗'
        pack_str(s)
        pack_str(s,style='js')
        pack_str(s,style='py')
        pack_str(s,encode='utf_16_be')
        pack_str(s,encode='utf_32')
        pack_str(s,encode='utf_8')
    '''
    return(pack_chstr(s,**kwargs))

encode_str = pack_str
str2bytstrm = pack_str


#str2hex                 string-in-hex
#hex2str                 hex-to-string
def str2hex(s,**kwargs):
    '''
        bs = b'O`N\xecY}\xd85\xdcR'
        s = bs.decode('utf_16_be')
        s
        str2hex(s,slashx=True)
        str2hex(s,slashx=False)
    '''
    bs = str2bytstrm(s,**kwargs)
    hs = bytstrm2hex(bs,**kwargs)
    return(hs)

def hex2str(hs,**kwargs):
    '''
        hs = '4f604eec597dd835dc52'
        hex2str(hs,style='js')
        hs = '\\x4f\\x60\\x4e\\xec\\x59\\x7d\\xd8\\x35\\xdc\\x52'
        hex2str(hs,style='js')
        hs = '\\x5c\\x75\\x34\\x66\\x36\\x30\\x5c\\x75\\x34\\x65\\x65\\x63\\x5c\\x75\\x35\\x39\\x37\\x64\\x5c\\x55\\x30\\x30\\x30\\x31\\x64\\x34\\x35\\x32'
        hex2str(hs,style='py')
        hs = '\\xe4\\xbd\\xa0\\xe4\\xbb\\xac\\xe5\\xa5\\xbd\\xf0\\x9d\\x91\\x92'
        hex2str(hs,encode='utf_8')
    '''
    bs = hex2bytstrm(hs,**kwargs)
    s = bytstrm2str(bs,**kwargs)
    return(s)

#str2chnums              string-to-char-numbers
#chnums2str              char-numbers-to-string
def str2chnums(s,**kwargs):
    '''
        s = '你好吗'
        cns = str2chnums(s)
        cns
    '''
    arr = list(s)
    cns = elel.array_map(arr,ord)
    return(cns)

def chnums2str(cns,**kwargs):
    '''
        cns = [20320, 22909, 21527]
        chnums2str(cns)
    '''
    arr = elel.array_map(cns,chr)
    s = elel.join(arr,'')
    return(s)


#str2bytnums             string-to-byte-numbers
#bytnums2str             byte-numbers-to-string
def str2bytnums(s,**kwargs):
    '''
        s = '你们好'
        str2bytnums(s)
        str2bytnums(s,style='js')
        str2bytnums(s,encode='utf_16_be')
        str2bytnums(s,style='py')
        str2bytnums(s,encode='raw_unicode_escape')
        str2bytnums(s,encode='utf_8')
    '''
    bs = str2bytstrm(s,**kwargs)
    bns = strm2bytnums(bs)
    return(bns)

def bytnums2str(bns,**kwargs):
    '''
        bns = [79, 96, 78, 236, 89, 125]
        bytnums2str(bns)
        bns = [79, 96, 78, 236, 89, 125]
        bytnums2str(bns,style='js')
        bns = [79, 96, 78, 236, 89, 125]
        bytnums2str(bns,encode='utf_16_be')
        bns = [92, 117, 52, 102, 54, 48, 92, 117, 52, 101, 101, 99, 92, 117, 53, 57, 55, 100]
        bytnums2str(bns,style='py')
        bns = [92, 117, 52, 102, 54, 48, 92, 117, 52, 101, 101, 99, 92, 117, 53, 57, 55, 100]
        bytnums2str(bns,encode='raw_unicode_escape')
        bns = [228, 189, 160, 228, 187, 172, 229, 165, 189]
        bytnums2str(bns,encode='utf_8')
    '''
    bs = bytnums2strm(bns)
    s = bytstrm2str(bs,**kwargs)
    return(s)

#str2us                  string-to-slashus
def str2us(s,**kwargs):
    '''
        bs = b'O`N\xecY}\xd85\xdcR'
        s = bs.decode('utf_16_be')
        s
        us = str2us(s,style='js')
        us
        slash_show(us,style='js')
        bs = b'\\u4f60\\u4eec\\u597d\\U0001d452'
        bs = b'\x5c\x75\x34\x66\x36\x30\x5c\x75\x34\x65\x65\x63\x5c\x75\x35\x39\x37\x64\x5c\x55\x30\x30\x30\x31\x64\x34\x35\x32'
        bs
        
        #上面两种格式的bytes 定义是一样的，只是显示方式不同
        #>>>bs = b'\x5c\x75\x34\x66\x36\x30\x5c\x75\x34\x65\x65\x63\x5c\x75\x35\x39\x37\x64\x5c\x55\x30\x30\x30\x31\x64\x34\x35\x32'
        #>>> bs
        #b'\\u4f60\\u4eec\\u597d\\U0001d452'
        
        s = bs.decode('raw_unicode_escape')
        s
        us = str2us(s,style='py')
        us
        slash_show(us,style='py')
    '''
    bs = str2bytstrm(s,**kwargs)
    us = bytstrm2us(bs,**kwargs)
    return(us)

#us2str                  slashus-to-string
def us2str(us,**kwargs):
    ''' 
        ####
        # unicode 的字面显示方式\\u \\U 总是BE 的 ，与实际存储方式无关:
            # >>> bs = '你'.encode('utf_16_le')
            # >>> bytstrm2hex(bs)
            # '\\x60\\x4f'
            # >>> bs = '你'.encode('utf_16_be')
            # >>> bytstrm2hex(bs)
            # '\\x4f\\x60'
            # >>>
        ####
        #py style
        us = '\\u4f60\\u4eec\\u597d\\U0001d452'
        s = us2str(us,style='py')
        s
        #js style
        us = '\\u4f60\\u4eec\\u597d\\ud835\\udc52'
        s = us2str(us,style='js')
        s
        ## by default ,is js style
        s = us2str(us)
        s
    '''
    if(us == ''):
        return("")
    else:
        bs = us2bytstrm(us,**kwargs)
        s = bytstrm2str(bs,**kwargs)
        return(s)




#byte-number                byte-number (number 0 -255)
#char-number                char-number  (ord(ch))
#str                        string
#bytstrm                    bytes-stream
#strmhex                    bytes-stream-in-hex
#bytnums                    byte-numbers-array (number 0-255)
#chnums                     char-numbers-array
#slashu                     unicode-in-slash ('\uxxxx' or '\Uxxxxxxxx')
#slashx                     asiic-in-slash ('\x??')

#所有转换都先转换为bytstrm

#bytstrm2hex                bytes-stream-to-stream-hex
#hex2bytstrm                stream-hex-to-bytes-stream
#strm2bytnums               bytes-stream-to-byte-numbers
#bytnums2strm               byte-numbers-to-stream
#bytstrm2chnums             bytes-stream-to-char-numbers
#chnums2bytstrm             char-numbers-to-bytes-stream
#bytstrm2us                 byte-stream-to-slashus
#us2bytstrm                 slashus-to-byte-stream


def slash_show(s,**kwargs):
    '''
        us = '\\x4f\\x60\\x59\\x7d\\x54\\x17'
        slash_show(us)
        us = '\\u4f60\\u4eec\\u597d'
        slash_show(us)
        us = '\\u4f60\\u4eec\\u597d\\U0001d452'
        slash_show(us)
        us = '\\u4f60\\u4eec\\u597d\\ud835\\udc52'
        slash_show(us,style='js')
    '''
    if('style' in kwargs):
        style = kwargs['style']
    else:
        style = 'py'
    if(style == 'py'):
        print(eval("'"+s+"'"))
    else:
        bs = us2bytstrm(us,style=style)
        s = bytstrm2str(bs)
        print(s)

def bytstrm2hex(bs,**kwargs):
    '''
        bs = b'O`Y}T\x17'
        hs = bytstrm2hex(bs)
        hs
        eval("'"+hs+"'")
        bytstrm2hex(bs,slashx=True)
        bytstrm2hex(bs,slashx=False)
    '''
    if('slashx' in kwargs):
        slashx = kwargs['slashx']
    else:
        slashx = True
    arr = elel.array_map(list(bs),hex)
    if(slashx):
        arr = elel.array_map(arr,str.replace,'0x','\\x')
    else:
        arr = elel.array_map(arr,str.replace,'0x','')
    h = elel.join(arr,'')
    return(h)

def hex2bytstrm(hs,**kwargs):
    '''
        hs = '4f60597d5417'
        hex2bytstrm(hs)
        hs = '\\x4f\\x60\\x59\\x7d\\x54\\x17'
        hex2bytstrm(hs)
    '''
    def cond_func(ele):
        num = int('0x'+ele,16)
        #important when ord >127 'latin-1' is different from 'utf-8'
        b = bytes(chr(num),'latin-1')
        return(b)
    hs = hs.replace('\\x','')
    arr = divide(hs,2)
    arr = elel.array_map(arr,cond_func)
    bs = elel.join(arr,b'')
    return(bs)

def strm2bytnums(bs,**kwargs):
    '''
        bs = b'O`Y}T\x17'
        bns = strm2bytnums(bs)
        bns
        elel.array_map(bns,chr)
    '''
    arr = list(bs)
    return(arr)

def bytnums2strm(bns,**kwargs):
    '''
        bns = [79, 96, 89, 125, 84, 23]
        bs = bytnums2strm(bns)
        bs
    '''
    arr = elel.array_map(bns,chr)
    s = elel.join(arr,'')
    bs = bytes(s,'latin-1')
    return(bs)

def bytstrm2chnums(bs,**kwargs):
    '''
        bs = b'O`Y}T\x17'
        cns = bytstrm2chnums(bs)
        cns
        elel.array_map(cns,chr)
        cns = bytstrm2chnums(bs,encode='utf_16_be')
        cns
        elel.array_map(cns,chr)
        cns = bytstrm2chnums(bs,style='js')
        cns
        elel.array_map(cns,chr)
        bs = b'\\u4f60\\u597d\\u5417'
        bs.__len__()
        cns = bytstrm2chnums(bs,style='py')
        cns
        elel.array_map(cns,chr)
        bs = b'\xe4\xbd\xa0\xe5\xa5\xbd\xe5\x90\x97'
        cns = bytstrm2chnums(bs,encode='utf_8')
        cns
        elel.array_map(cns,chr)
    '''
    if('encode' in kwargs):
        encode=kwargs['encode']
    else:
        if('style' in kwargs):
            style = kwargs['style']
        else:
            style = 'js'
        if(style == 'js'):
            encode = 'utf_16_be'
        elif(style == 'py'):
            encode = 'raw_unicode_escape'
        else:
            encode = 'raw_unicode_escape'
    s = bs.decode(encode)
    uarr = list(s)
    cns = elel.array_map(uarr,ord)
    return(cns)

strm2chnums = bytstrm2chnums

def chnums2bytstrm(cns,**kwargs):
    '''
        cns = [20320, 22909, 21527]
        bs = chnums2bytstrm(cns)
        bs
        
        chnums2bytstrm(cns,style='js')
        chnums2bytstrm(cns,encode='utf_16_be')
        
        
        chnums2bytstrm(cns,style='py')
        chnums2bytstrm(cns,encode='raw_unicode_escape')
        
        chnums2bytstrm(cns,encode='utf_8')
        
        
    '''
    if('encode' in kwargs):
        encode=kwargs['encode']
    else:
        if('style' in kwargs):
            style = kwargs['style']
        else:
            style = 'js'
        if(style == 'js'):
            encode = 'utf_16_be'
        elif(style == 'py'):
            encode = 'raw_unicode_escape'
        else:
            encode = 'raw_unicode_escape'
    s = chnums2str(cns,**kwargs)
    bs = str2bytstrm(s,**kwargs)
    return(bs)

chnums2strm = chnums2bytstrm

def bytstrm2us(bs,**kwargs):
    '''
        bs = b'O`N\xecY}\xd85\xdcR'
        bs.decode('utf_16_be')
        us = bytstrm2us(bs,style='js')
        us
        slash_show(us,style='js')
        bs = b'\\u4f60\\u4eec\\u597d\\U0001d452'
        bs = b'\x5c\x75\x34\x66\x36\x30\x5c\x75\x34\x65\x65\x63\x5c\x75\x35\x39\x37\x64\x5c\x55\x30\x30\x30\x31\x64\x34\x35\x32'
        bs
        #上面两种格式的bytes 定义是一样的，只是显示方式不同
        #>>>bs = b'\x5c\x75\x34\x66\x36\x30\x5c\x75\x34\x65\x65\x63\x5c\x75\x35\x39\x37\x64\x5c\x55\x30\x30\x30\x31\x64\x34\x35\x32'
        #>>> bs
        #b'\\u4f60\\u4eec\\u597d\\U0001d452'
        bs.decode('raw_unicode_escape')
        bns = list(bs)
        bns
        bytnums2hex(bns)
        us = bytstrm2us(bs,style='py')
        us
        slash_show(us,style='py')
    '''
    if('encode' in kwargs):
        encode=kwargs['encode']
    else:
        if('style' in kwargs):
            style = kwargs['style']
        else:
            style = 'js'
        if(style == 'js'):
            encode = 'utf_16_be'
        elif(style == 'py'):
            encode = 'raw_unicode_escape'
        else:
            encode = 'raw_unicode_escape'
    src = bs.__str__()
    cond1 = ('\\u' in src)
    cond2 = ('\\U' in src)
    cond = (cond1 | cond2)
    if(cond):
        us = src[2:-1]
        us=us.replace('\\\\','\\')
    else:
        if('style' in kwargs):
            style = kwargs['style']
        else:
            style = 'js'
        if(style == 'js'):
            cns = bytstrm2chnums(bs,**kwargs)
            hs = chnums2hex(cns,slashx=False)
            arr =  divide(hs,4)
            def cond_func(ele):
                return('\\u'+ele)
            arr = elel.array_map(arr,cond_func)
            us = elel.join(arr,'')
        else:
            bs = bs.decode(encode).encode('raw_unicode_escape')
            src = bs.__str__()
            us = src[2:-1]
            us=us.replace('\\\\','\\')    
    return(us)

def us2bytstrm(us,**kwargs):
    ''' 
        ####
        # unicode 的字面显示方式\\u \\U 总是BE 的 ，与实际存储方式无关:
            # >>> bs = '你'.encode('utf_16_le')
            # >>> bytstrm2hex(bs)
            # '\\x60\\x4f'
            # >>> bs = '你'.encode('utf_16_be')
            # >>> bytstrm2hex(bs)
            # '\\x4f\\x60'
            # >>>
        ####
        #py style
        us = '\\u4f60\\u4eec\\u597d\\U0001d452'
        slash_show(us)
        bs = us2bytstrm(us,style='py')
        bs
        bs.__len__()
        bytstrm2hex(bs)
        bs.decode('raw_unicode_escape')
        #js style
        us = '\\u4f60\\u4eec\\u597d\\ud835\\udc52'
        slash_show(us,style='js')
        bs = us2bytstrm(us,style='js')
        bs
        bs.__len__()
        bytstrm2hex(bs)
        bs.decode('utf_16_be')
        ## by default ,is js style
        bs = us2bytstrm(us)
        bs
        bs.__len__()
        bytstrm2hex(bs)
        decode_bytstrm(bs)
    '''
    if('encode' in kwargs):
        encode=kwargs['encode']
    else:
        if('style' in kwargs):
            style = kwargs['style']
        else:
            style = 'js'
        if(style == 'js'):
            encode = 'utf_16_be'
        elif(style == 'py'):
            encode = 'raw_unicode_escape'
        else:
            encode = 'raw_unicode_escape'
    if('style' in kwargs):
        style = kwargs['style']
    else:
        style = 'js'
    if(style == 'js'):
        us = str.lower(us)
        uarr = us.split('\\u')
        uarr.pop(0)
        barr = []
        for i in range(0,uarr.__len__()):
            tmp = divide(uarr[i],2)
            barr.extend(tmp)
        hs = elel.join(barr,'')
        bs = hex2bytstrm(hs)
    else:
        bs = bytes(us,encode)
    return(bs)



#hex 

#bytnums2hex              byte-numbers-in-hex
#hex2bytnums              hex-to-byte-numbers
def bytnums2hex(bns,**kwargs):
    '''
        bns = [92, 117, 52, 102, 54, 48, 92, 117, 52, 101, 101, 99, 92, 117, 53, 57, 55, 100, 92, 85, 48, 48, 48, 49, 100, 52, 53, 50]
        bytnums2hex(bns)
        
        bs = b'\\u4f60\\u4eec\\u597d\\U0001d452'
        bs.__len__()
        list(bs)
        #bytes  取下标 会被隐式转换
        bs[0]
        type(bs[0])
        bs[1]
        #...
        bs[27]
        
        bytnums2hex(bns,slashx=False)
        
    '''
    if('slashx' in kwargs):
        slashx = kwargs['slashx']
    else:
        slashx = True
    arr = elel.array_map(bns,hex)
    hs = elel.join(arr,'')
    hs = str.lower(hs)
    if(slashx == True):
        hs = hs.replace('0x','\\x')
    else:
        hs = hs.replace('0x','')
    return(hs)

def hex2bytnums(hs,**kwargs):
    '''
        hs = '\\x5c\\x75\\x34\\x66\\x36\\x30\\x5c\\x75\\x34\\x65\\x65\\x63\\x5c\\x75\\x35\\x39\\x37\\x64\\x5c\\x55\\x30\\x30\\x30\\x31\\x64\\x34\\x35\\x32'
        hex2bytnums(hs)
        hs = '5c75346636305c75346565635c75353937645c553030303164343532'
        hex2bytnums(hs)
    '''
    hs = str.lower(hs)
    hs = hs.replace('\\x','')
    arr = divide(hs,2)
    def cond_func(ele):
        ele='0x'+ele
        ele = int(ele,16)
        return(ele)
    arr = elel.array_map(arr,cond_func)    
    return(arr)


#chnums2hex               char-numbers-in-hex
#hex2chnums               hex-to-char-numbers

def chnums2hex(cns,**kwargs):
    '''
        cns = [20320, 20204, 22909, 119890]
        chnums2hex(cns)
        chnums2hex(cns,slashx=False)
        chnums2hex(cns,style='js')
        chnums2hex(cns,style='py')
        chnums2hex(cns,encode='raw_unicode_escape')
        chnums2hex(cns,encode='utf_8')
    '''
    if('encode' in kwargs):
        encode=kwargs['encode']
    else:
        if('style' in kwargs):
            style = kwargs['style']
        else:
            style = 'js'
        if(style == 'js'):
            encode = 'utf_16_be'
        elif(style == 'py'):
            encode = 'raw_unicode_escape'
        else:
            encode = 'raw_unicode_escape'
    if('slashx' in kwargs):
        slashx = kwargs['slashx']
    else:
        slashx = True
    hs = bytstrm2hex(chnums2bytstrm(cns,**kwargs),slashx=slashx)
    return(hs)

def hex2chnums(hs,**kwargs):
    '''
        hs = '\\x4f\\x60\\x4e\\xec\\x59\\x7d\\xd8\\x35\\xdc\\x52'
        chnums = hex2chnums(hs)
        chnums
        hs = '4f604eec597dd835dc52'
        chnums = hex2chnums(hs)
        chnums
        hs = '\\x4f\\x60\\x4e\\xec\\x59\\x7d\\xd8\\x35\\xdc\\x52'
        chnums = hex2chnums(hs,style='js')
        chnums
        hs = '\\x5c\\x75\\x34\\x66\\x36\\x30\\x5c\\x75\\x34\\x65\\x65\\x63\\x5c\\x75\\x35\\x39\\x37\\x64\\x5c\\x55\\x30\\x30\\x30\\x31\\x64\\x34\\x35\\x32'
        chnums = hex2chnums(hs,style='py')
        chnums
        hs = '\\x5c\\x75\\x34\\x66\\x36\\x30\\x5c\\x75\\x34\\x65\\x65\\x63\\x5c\\x75\\x35\\x39\\x37\\x64\\x5c\\x55\\x30\\x30\\x30\\x31\\x64\\x34\\x35\\x32'
        chnums = hex2chnums(hs,encode='raw_unicode_escape')
        chnums
        hs = '\\xe4\\xbd\\xa0\\xe4\\xbb\\xac\\xe5\\xa5\\xbd\\xf0\\x9d\\x91\\x92'
        chnums = hex2chnums(hs,encode='utf_8')
        chnums
    '''
    bs = hex2bytstrm(hs,**kwargs)
    chnums = bytstrm2chnums(bs,**kwargs)
    return(chnums)


#hex2us                   hex-to-slashus
#us2hex                   slashus-to-hex

def hex2us(hs,**kwargs):
    '''
        hs = '4f604eec597dd835dc52'
        us = hex2us(hs,style='js')
        us
        slash_show(us,style='js')
        
        hs = '\\x5c\\x75\\x34\\x66\\x36\\x30\\x5c\\x75\\x34\\x65\\x65\\x63\\x5c\\x75\\x35\\x39\\x37\\x64\\x5c\\x55\\x30\\x30\\x30\\x31\\x64\\x34\\x35\\x32'
        us = hex2us(hs,style='py')
        us
        slash_show(us,style='py')
        
    '''
    bs = hex2bytstrm(hs,**kwargs)
    us = bytstrm2us(bs,**kwargs)
    return(us)

def us2hex(us,**kwargs):
    '''
        us = '\\u4f60\\u4eec\\u597d\\ud835\\udc52'
        us2hex(us,style='js')
        us = '\\u4f60\\u4eec\\u597d\\U0001d452'
        us2hex(us,style='py')
    '''
    bs = us2bytstrm(us,**kwargs)
    hs = bytstrm2hex(bs,**kwargs)
    return(hs)


#chnums2bytnums           char-numbers-to-byte-numbers
#bytnums2chnums           byte-numbers-to-char-numbers


def chnums2bytnums(cns,**kwargs):
    '''
        cns = [20320, 22909, 21527]
        chnums2bytnums(cns)
        
        chnums2bytnums(cns,style='js')
        chnums2bytnums(cns,encode='utf_16_be')
        
        
        chnums2bytnums(cns,style='py')
        chnums2bytnums(cns,encode='raw_unicode_escape')
        
        chnums2bytnums(cns,encode='utf_8')
    '''
    bs = chnums2bytstrm(cns,**kwargs)
    bns = strm2bytnums(bs,**kwargs)
    return(bns)

def bytnums2chnums(bns,**kwargs):
    '''
        bns = [79, 96, 89, 125, 84, 23]
        bytnums2chnums(bns,style='js')
        bns = [92, 117, 52, 102, 54, 48, 92, 117, 53, 57, 55, 100, 92, 117, 53, 52, 49, 55]
        bytnums2chnums(bns,style='py')
        bns = [228, 189, 160, 229, 165, 189, 229, 144, 151]
        bytnums2chnums(bns,encode='utf_8')
    '''
    bs = bytnums2strm(bns,**kwargs)
    cns = bytstrm2chnums(bs,**kwargs)
    return(cns)

#chnums2us                char-numbers-to-slashus
#us2chnums                slashus-to-char-numbers

def chnums2us(cns,**kwargs):
    '''
        cns = [20320, 22909, 21527,119890]
        us = chnums2us(cns,style='js')
        us
        slash_show(us,style='js')
        us = chnums2us(cns,style='py')
        us
        slash_show(us,style='py')
    '''
    bs = chnums2bytstrm(cns,**kwargs)
    us = bytstrm2us(bs,**kwargs)
    return(us)

def us2chnums(us,**kwargs):
    '''
        us = '\\u4f60\\u597d\\u5417\\ud835\\udc52'
        us2chnums(us,style='js')
        us = '\\u4f60\\u597d\\u5417\\U0001d452'
        us2chnums(us,style='py')
        
    '''
    bs = us2bytstrm(us,**kwargs)
    cns = bytstrm2chnums(bs,**kwargs)
    return(cns)

#bytnums2us               byte-numbers-to-slashus
#us2bytnums               slashus-to-byte-numbers

def bytnums2us(bns,**kwargs):
    '''
        bns = [79, 96, 89, 125, 84, 23, 216, 53, 220, 82]
        us = bytnums2us(bns,style='js')
        us 
        slash_show(us,style='js')
        bns = [92, 117, 52, 102, 54, 48, 92, 117, 53, 57, 55, 100, 92, 117, 53, 52, 49, 55, 92, 85, 48, 48, 48, 49, 100, 52, 53, 50]
        us = bytnums2us(bns,style='py')
        us 
        slash_show(us,style='py')
    '''
    bs = bytnums2strm(bns,**kwargs)
    us = bytstrm2us(bs,**kwargs)
    return(us)


def us2bytnums(us,**kwargs):
    '''
        us = '\\u4f60\\u597d\\u5417\\ud835\\udc52'
        us2bytnums(us,style='js')
        us = '\\u4f60\\u597d\\u5417\\U0001d452'
        us2bytnums(us,style='py')
        
    '''
    bs = us2bytstrm(us,**kwargs)
    bns = strm2bytnums(bs,**kwargs)
    return(bns)


def str_code_points(s,**kwargs):
    '''
        bs = b'\xd85\xdcRO`N\xecY}\xd85\xdcR'
        s = bs.decode('utf_16_be')
        s
        str_code_points(s,style='js')
        bs[0:4]
        bs[0:4].decode('utf_16_be')
        bs[4:6]
        bs[4:6].decode('utf_16_be')
        bs[8:10]
        bs[8:10].decode('utf_16_be')
        bs[10:14]
        bs[10:14].decode('utf_16_be')
        #
        bs = s.encode('utf_8')
        str_code_points(s,encode='utf_8')
        bs[0:4]
        bs[0:4].decode('utf_8')
        bs[4:7]
        bs[4:7].decode('utf_8')
        bs[7:10]
        bs[7:10].decode('utf_8')
        bs[10:13]
        bs[10:13].decode('utf_8')
        bs[13:17]
        bs[13:17].decode('utf_8')
    '''
    if('encode' in kwargs):
        encode=kwargs['encode']
    else:
        if('style' in kwargs):
            style = kwargs['style']
        else:
            style = 'js'
        if(style == 'js'):
            encode = 'utf_16_be'
        elif(style == 'py'):
            encode = 'raw_unicode_escape'
        else:
            encode = 'raw_unicode_escape'
    arr = list(s)
    locs = [0]
    cursur = 0
    lngth = arr.__len__()
    for i in range(0,lngth):
        chbs = encode_chstr(arr[i],encode=encode)
        offset = chbs.__len__()
        cursur = cursur + offset
        locs.append(cursur)
    return(locs)

#
def str_jschar_points(s):
    '''
        bs = b'\xd85\xdcRO`N\xecY}\xd85\xdcR'
        s = bs.decode('utf_16_be')    
        s 
        str2jscharr(s)
    '''
    locs = str_code_points(s,encode='utf_16_be')
    locs = elel.array_map(locs,lambda ele:ele//2)
    return(locs)

def pychpoints2jscharpoints(s,pypoint):
    '''
        bs = b'\xd85\xdcRO`N\xecY}\xd85\xdcR'
        s = bs.decode('utf_16_be')    
        s 
        str2jscharr(s)
        pychpoints2jscharpoints(s,0)
        pychpoints2jscharpoints(s,1)
        pychpoints2jscharpoints(s,2)
        pychpoints2jscharpoints(s,3)
    '''
    jslocs = str_jschar_points(s)
    return(jslocs[pypoint])

def jscharpoints2pychpoints(s,jspoint):
    '''
        bs = b'\xd85\xdcRO`N\xecY}\xd85\xdcR'
        s = bs.decode('utf_16_be')    
        s 
        str2jscharr(s)
        jscharpoints2pychpoints(s,0)
        jscharpoints2pychpoints(s,2)
        jscharpoints2pychpoints(s,3)
        jscharpoints2pychpoints(s,4)
        jscharpoints2pychpoints(s,5)
        jscharpoints2pychpoints(s,7)
    '''
    jslocs = str_jschar_points(s)
    return(jslocs.index(jspoint))


def us2uarr(us,**kwargs):
    '''
        us = '\\u4f60\\u597d\\u5417\\ud835\\udc52'
        us2uarr(us,mode='prefix')
        us2uarr(us,mode='value')
        us2uarr(us)
        us = '\\u4f60\\u597d\\u5417\\U0001d452'
        us2uarr(us,mode='prefix')
        us2uarr(us,mode='value')
        us2uarr(us)
    '''
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = 'both'
    regex = re.compile('(\\\\[u|U][0-9a-fA-F]+)')
    m = regex.findall(us)
    lngth = m.__len__()
    prefixes = []
    values = []
    bothes = []
    for i in range(0,lngth):    
        pfix = m[i][:2]    
        value = m[i][2:]    
        prefixes.append(pfix)
        values.append(value)
        bothes.append((pfix,value))
    if(mode == 'prefix'):
        return(prefixes)
    elif(mode == 'value'):
        return(values)
    else:
        return(bothes)

def uarr2us(*args):
    '''
        puarr = ['\\u', '\\u', '\\u', '\\U']
        vuarr = ['4f60', '597d', '5417', '0001d452']
        uarr2us(puarr,vuarr)
        uarr = [('\\u', '4f60'), ('\\u', '597d'), ('\\u', '5417'), ('\\U', '0001d452')]
        uarr2us(uarr)
    '''
    uarr = args[0]
    lngth = list(uarr).__len__()
    if(lngth<1):
        return('')
    else:
        pass
    if(type(uarr[0])==type((0,0))):
        def cond_func(ele):
            return(ele[0]+ele[1])
        uarr = elel.array_map(uarr,cond_func)
    else:
        puarr = args[0]
        vuarr = args[1]
        def map_func(ele1,ele2):
            return(ele1+ele2)
        uarr = elel.array_map2(puarr,vuarr,map_func=map_func)
    us = elel.join(uarr,'')
    return(us)


def uarr2jscharr(*args):
    '''
        uarr = ['4f60', '4eec', '597d', 'd835', 'dc52']
        uarr2jscharr(uarr)
    '''
    uarr = args[0]
    lngth = list(uarr).__len__()
    if(lngth<1):
        return([])
    else:
        pass
    if(type(uarr[0])==type((0,0))):
        def cond_func(ele):
            return(ele[1])
        uarr = elel.array_map(uarr,cond_func)
    else:
        pass
    def cond_func(ele):
        ele = '0x'+ele    
        n = int(ele,16)    
        return(chr(n))    
    jscharr = elel.array_map(uarr,cond_func)
    return(jscharr)

def uarr2str(*uarrs,**kwargs):
    '''
        puarr = ['\\u', '\\u', '\\u', '\\U']
        vuarr = ['4f60', '597d', '5417', '0001d452']    
        uarr2str(puarr,vuarr,style='py')    
        uarr = [('\\u', '4f60'), ('\\u', '597d'), ('\\u', '5417'), ('\\U', '0001d452')]    
        uarr2str(uarr,style='py')    
    '''
    us = uarr2us(*uarrs)
    s = us2str(us,**kwargs)
    return(s)

def str2uarr(s,**kwargs):
    '''
        bs = b'\xd85\xdcRO`N\xecY}\xd85\xdcR'
        s = bs.decode('utf_16_be')
        s
        str2uarr(s,mode='both')
        str2uarr(s,mode='value')
    '''
    us = str2us(s,**kwargs)
    uarr = us2uarr(us,**kwargs)
    return(uarr)

def str2jscharr(s,**kwargs):
    '''
        bs = b'\xd85\xdcRO`N\xecY}\xd85\xdcR'
        s = bs.decode('utf_16_be')
        s
        str2jscharr(s)
    '''
    uarr = str2uarr(s,mode='both')
    jscharr = uarr2jscharr(uarr)
    return(jscharr)


#strlen                string-length

def length(s,**kwargs):
    '''
        # in python , the string-length means  unicode-char-lngth 
        # in javascript, the length means how-many 16-bit unit
        # for example:
        # run in js 
        var p = '\ud835\udc52' 
        p 
        p.length 
        p.codePointAt(0)    
        p.codePointAt(0).toString(16)
        p.charCodeAt(0).toString(16)
        p.charCodeAt(1).toString(16)
        '\ud835\udc52'
        # codePointAt(0) similiar to  ord in python
        
        chr(119890)
        ord(chr(119890))
        hex(119890)
        
        length(chr(119890))
        length(chr(119890),style='js')
    '''
    if('style' in kwargs):
        style = kwargs['style']
    else:
        style = 'py'
    if(style == 'py'):
        lngth = s.__len__()
    else:
        bs = s.encode('utf_16_be')
        q = bs.__len__() // 2
        r = bs.__len__() % 2
        if(r == 0):
            lngth = q
        else:
            lngth = q + 1
    return(lngth)

def fromCharCode(*args,**kwargs):
    '''
        #by default, the style is 'js'
        
        fromCharCode(97,98,99)
        fromCharCode(97,98,99,style='js')
        fromCharCode(97,98,99,style='py')
        
        #in javascript , only keep the low 2 bytes
        # String['fromCharCode'](270752) = String['fromCharCode'](0x421a0)
        # 0x000421a0
        # 0x    21a0 = 8608
        # So:
        # String['fromCharCode'](270752) = String['fromCharCode'](8608) = '?'
        
        fromCharCode(270752,style='js')
        fromCharCode(270752,style='py')
        fromCharCode(8608,style='js')
        fromCharCode(8608,style='py')
    '''
    if('style' in kwargs):
        style = kwargs['style']
    else:
        style = 'js'
    rslt =''
    if(style == 'py'):
        for i in range(0,args.__len__()):
            rslt = rslt + chr(args[i])
    else:
        for i in range(0,args.__len__()):
            rslt = rslt + chr(0x0000ffff & args[i])
    return(rslt)

def fromCodePoint(*args,**kwargs):
    '''
        # refer to https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/String/fromCharCode
        fromCodePoint(42)       
        fromCodePoint(65, 90)   
        fromCodePoint(0x404)    
        fromCodePoint(0x2F804)  
        fromCodePoint(194564)   
        fromCodePoint(0x1D306, 0x61, 0x1D307) 
    '''
    if('encode' in kwargs):
        encode=kwargs['encode']
    else:
        if('style' in kwargs):
            style = kwargs['style']
        else:
            style = 'js'
        if(style == 'js'):
            encode = 'utf_16_be'
        elif(style == 'py'):
            encode = 'raw_unicode_escape'
        else:
            encode = 'utf_16_be'
    def cond_func(ele,encode='utf_16_be',style='js'):
        bs = pack_chnum(ele,encode = encode,style=style)
        ckstr = bs.decode(encode)
        return(ckstr)
    args = list(args)
    arr = elel.array_map(args,cond_func,encode,style)
    s = elel.join(arr,'')
    return(s)

def charAt(s,index=0,**kwargs):
    '''
        bs = b'O`N\xecY}\xd85\xdcR'
        s = bs.decode('utf_16_be')
        s
        bytstrm2us(bs,style='js')
        #refer to js ,js 不是按照char-length 算位置的，而是按照16-bit 
        #s = '\u4f60\u4eec\u597d\ud835\udc52'
        #"你们好??"
        #s.charAt(0)
        #"你"
        #s.charAt(1)
        #"们"
        #s.charAt(2)
        #"好"
        #s.charAt(3)
        #"\ud835"
        #s.charAt(4)
        #"\udc52"
        #arr = Array.from(s)
        #Array(4) [ "你", "们", "好", "??" ]
        charAt(s,3)
        charAt(s,3,style='py')
        charAt(s,3,style='js')
        charAt(s,4,style='js')
        #by default ,index = 0
        charAt(s)
        
    '''
    if('style' in kwargs):
        style = kwargs['style']
    else:
        style = 'py'
    if(style == 'py'):
        ch = s[index]
    else:
        us = str2us(s,style='js')
        uarr = us.split('\\u')
        uarr.pop(0)
        tmp = '0x' + uarr[index]
        cn = int(tmp,16)
        ch = chr(cn)
    return(ch)

def charCodeAt(s,index=0,**kwargs):
    '''
        bs = b'O`N\xecY}\xd85\xdcR'
        s = bs.decode('utf_16_be')
        s
        bytstrm2us(bs,style='js')
        #refer to js ,js 不是按照char-length 算位置的，而是按照16-bit 
        #s = '\u4f60\u4eec\u597d\ud835\udc52'
        #"你们好??"
        #s.charCodeAt(0)
        #20320
        #s.charCodeAt(1)
        #20204
        #s.charCodeAt(2)
        #22909
        #s.charCodeAt(3)
        #55349
        #s.charCodeAt(4)
        #56402
        #arr = Array.from(s)
        #Array(4) [ "你", "们", "好", "??" ]
        charCodeAt(s,3)
        charCodeAt(s,3,style='py')
        charCodeAt(s,3,style='js')
        charCodeAt(s,4,style='js')
        #by default ,index = 0
        charCodeAt(s)
        
    '''
    if('style' in kwargs):
        style = kwargs['style']
    else:
        style = 'py'
    return(ord(charAt(s,index,**kwargs)))

def codePointAt(s,index=0,**kwargs):
    '''
        bs = b'\xd85\xdcRO`N\xecY}\xd85\xdcR'
        s = bs.decode('utf_16_be')
        s
        bytstrm2us(bs,style='js')
        #refer to js ,js 不是按照char-length 算位置的，而是按照16-bit 
        codePointAt(s,0,style='py')
        codePointAt(s,1,style='py')
        codePointAt(s,2,style='py')
        codePointAt(s,3,style='py')
        codePointAt(s,4,style='py')
        #
        codePointAt(s,0,style='js')
        codePointAt(s,1,style='js')
        codePointAt(s,2,style='js')
        codePointAt(s,3,style='js')
        codePointAt(s,4,style='js')
        codePointAt(s,5,style='js')
        codePointAt(s,6,style='js')
        #by default ,index = 0
        codePointAt(s)
        
    '''
    if('style' in kwargs):
        style = kwargs['style']
    else:
        style = 'py'
    if(style == 'py'):
        return(ord(charAt(s,index,**kwargs)))
    else:
        locs = str_code_points(s,encode='utf_16_be')
        locs = elel.array_map(locs,lambda ele:ele//2)
        uarr = str2uarr(s,**kwargs)
        jscharr = uarr2jscharr(uarr)
        if(index in locs):
            return(ord(charAt(s,locs.index(index),style='py')))
        else:
            return(ord(jscharr[index]))

###########


# String.prototype.concat()
# String.prototype.endsWith()
# String.prototype.includes()
# String.prototype.indexOf()
# String.prototype.lastIndexOf()
# String.prototype.localeCompare()
# String.prototype.match()
# String.prototype.normalize()
# String.prototype.padEnd()
# String.prototype.padStart()
# String.prototype.repeat()
# String.prototype.replace()
# String.prototype.search()
# String.prototype.split()
# String.prototype.startsWith()
# String.prototype.substr()
# String.prototype.substring()
# String.prototype.toLocaleLowerCase()
# String.prototype.toLocaleUpperCase()
# String.prototype.toLowerCase()
# String.prototype.toSource()
# String.prototype.toString()
# String.prototype.toUpperCase()
# String.prototype.trim()
# String.prototype.trimLeft()
# String.prototype.trimRight()
# String.prototype.valueOf()


#@@@@@@@@@@@@@@@@@@








#############################
















    


#str.split([separator[, limit]])
# str.split(sep=None, maxsplit=-1)
# >>> '1 2 3'.split(maxsplit=1)
# ['1', '2 3']
# seperator 支持正则
# empty seperator support 


def divide(s,interval):
    '''
        s = 'abcdefghi'
        divide(s,3)
        divide(s,2)
        divide(s,4)
    '''
    arr = elel.divide(s,interval)
    return(arr)

def slice(s,si,ei=None,**kwargs):
    '''
        # in python , the string-length means  unicode-char-lngth 
        # in javascript, the length means how-many 16-bit unit
        # for example:
        # run in js 
        bs = b'\xd85\xdcRO`N\xecY}\xd85\xdcR'
        s = bs.decode('utf_16_be')        
        s        
        bytstrm2us(bs,style='js')
        slice(s,0,1,style='py')
        slice(s,0,2,style='py')
        slice(s,0,3,style='py')
        slice(s,0,4,style='py')
        #
        slice(s,0,1,style='js')
        slice(s,0,2,style='js')
        slice(s,0,3,style='js')
        slice(s,0,4,style='js')
        slice(s,0,5,style='js')
        slice(s,0,6,style='js')
        slice(s,0,7,style='js')
    '''
    lngth = length(s,**kwargs)
    if('style' in kwargs):
        style = kwargs['style']
    else:
        style = 'py'
    if(ei == None):
        ei = lngth
    else:
        pass
    si = elel.uniform_index(si,lngth)
    ei = elel.uniform_index(ei,lngth)
    if(style == 'py'):
        part = s[si:ei]
        return(part)
    else:
        locs = str_code_points(s,encode='utf_16_be')
        locs = elel.array_map(locs,lambda ele:ele//2)
        us = str2us(s,encode = 'utf_16_be')
        uarr = us2uarr(us,mode='both')
        jscharr = uarr2jscharr(uarr)
        slb = elel.lower_bound(locs,si)
        sub = elel.upper_bound(locs,si)
        elb = elel.lower_bound(locs,ei)
        eub = elel.upper_bound(locs,ei)
        part1 = jscharr[si:sub]
        s1 = elel.join(part1,'')
        part2 = uarr[sub:elb]
        s2 = uarr2str(part2,style='js')
        part3 = jscharr[elb:ei]
        s3 = elel.join(part3,'')
        s = s1 + s2 + s3
        return(s)


# def str_indexes(s,c):
# def str_repeat(s,times):
# def str_xor_str(s1,s2):
# def str_to_bool(s,**kwargs):
# def str_lstrip(s,char,count):
# def str_rstrip(s,char,count):
# def str_prepend(s,char,n):
# def str_append(s,char,n):
# def str_at_begin_of_str(str1,str2):
# def str_at_end_of_str(str1,str2):
# def str_display_width(s):
# def str_prepend_basedon_displaywidth(s,width,**kwargs):
# def str_append_basedon_displaywidth(s,width,**kwargs):
# def str_to_ord_list(s):
# def str_to_slash_u_str(a_string,with_slash_u=1):
# def str_to_unicode_num_array(a_string):
# def str_to_unicode_hex_str(s):
# def str_tail_to_head(s, tail_len,**kwargs):
# def str_head_to_tail(s, head_len,**kwargs):

# def unshift(l,*args):
# def unsigned_right_shift(num,shift_num,**kwargs):
# def logical_or(x,y):
# def logical_and(x,y):
# def newDate_num(**kwargs):
# def clock_seconds_with_accuracy(accuracy):
# def toString(n,radix,**kwargs):
# def uint2str(ui,**kwargs):
# def str2uint(s,**kwargs):
# def fromCharCode(*args,**kwargs):
# def scinumstr2numstr(sci):
# def parseInt(nstr,radix=10,**kwargs):




