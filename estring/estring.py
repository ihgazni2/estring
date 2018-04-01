import struct
import elist.elist as elel

#strlen                string-length

def length(s,**kwargs):
    '''
        # in python , the string-length means  unicode-char-length 
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

#@@@@@@@@@@@@@@@@@@@
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

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
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
    bs = bytes(s,'utf_8')
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
    '''

def us2bytstrm(us,**kwargs):
    ''' 
        ####
        # unicode 的字面显示方式\\u \\U 总是BE 的 ，与实际存储方式无关:
            >>> bs = '你'.encode('utf_16_le')
            >>> bytstrm2hex(bs)
            '\\x60\\x4f'
            >>> bs = '你'.encode('utf_16_be')
            >>> bytstrm2hex(bs)
            '\\x4f\\x60'
            >>>
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


#str2chnums               string-to-char-numbers
#chnums2str               char-numbers-to-string

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


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

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
    



###########


def unpack_twobytes_using_unicode(two_bytes):
    '''
        >>> unpack_twobytes_using_unicode(b'\x00a')
        'a'
        >>> unpack_twobytes_using_unicode(b'\x95\xee')
        '问'
        >>> print('\u0061')
        a
        >>> print('\u95ee')
        问
        >>>
    '''
    h,l = struct.unpack('BB',two_bytes)
    h = '{0:0>2}'.format(hex(h).lstrip('0x'))
    l = '{0:0>2}'.format(hex(l).lstrip('0x'))
    u = ''.join(('\\u',h,l))
    u = bytes(u,'utf-8')
    s = u.decode('raw_unicode_escape')
    return(s)

def unpack_fourbytes_using_unicode(four_bytes):
    '''
    '''
    one,two,three,four = struct.unpack('BBBB',four_bytes)
    one = '{0:0>2}'.format(hex(one).lstrip('0x'))
    two = '{0:0>2}'.format(hex(two).lstrip('0x'))
    three = '{0:0>2}'.format(hex(three).lstrip('0x'))
    four = '{0:0>2}'.format(hex(four).lstrip('0x'))
    u = ''.join(('\\U',one,two,three,four))
    u = bytes(u,'utf-8')
    s = u.decode('raw_unicode_escape')
    return(s)

def slash_u_str_to_char(slash_u_str):
    '''
        >>> slash_u_str_to_char('\\u4f60')
        '你'
        >>> slash_u_str_to_char('4f60')
        '你'
        >>>
    '''
    if(slash_u_str[:2]=='\\u'):
        slash_u_str = slash_u_str[2:]
        one = chr(int(slash_u_str[0:2],16))
        two = chr(int(slash_u_str[2:],16))
        pk = ''.join((one,two))
        bs = bytes(pk,'latin-1')
    elif(slash_u_str[:2]=='\\U'):
        slash_u_str = slash_u_str[2:]
        one = chr(int(slash_u_str[0:2],16))
        two = chr(int(slash_u_str[2:4],16))
        three = chr(int(slash_u_str[4:6],16))
        four = chr(int(slash_u_str[6:8],16))
        pk = ''.join((one,two,three,four))
        bs = bytes(pk,'latin-1')
    else:
        if(slash_u_str.__len__() == 4):
            one = chr(int(slash_u_str[0:2],16))
            two = chr(int(slash_u_str[2:],16))
            pk = ''.join((one,two))
            bs = bytes(pk,'latin-1')
        else:
            one = chr(int(slash_u_str[0:2],16))
            two = chr(int(slash_u_str[2:4],16))
            three = chr(int(slash_u_str[4:6],16))
            four = chr(int(slash_u_str[6:8],16))
            pk = ''.join((one,two,three,four))
            bs = bytes(pk,'latin-1')
    if(bs.__len__() == 2):
        return(unpack_twobytes_using_unicode(bs))
    else:
        return(unpack_fourbytes_using_unicode(bs))

def unicode_num_to_char_str(unicode_num):
    '''
        >>> unicode_num_to_char_str(97)
        'a'
        >>> unicode_num_to_char_str(20320)
        '你'
        >>>
        in javascript , only keep the low 2 bytes
        String['fromCharCode'](270752) = String['fromCharCode'](0x421a0)
        0x000421a0
        0x    21a0 = 8608
        So:
        String['fromCharCode'](270752) = String['fromCharCode'](8608) = '?'
    '''
    h = hex(unicode_num)
    h = h[2:]
    if(h.__len__()<=4):
        prepend = "0" * (4 - h.__len__())
    else:
        prepend = "0" * (8 - h.__len__())
    h = ''.join((prepend,h))
    ch = slash_u_str_to_char(h)
    return(ch)

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
            rslt = rslt + unicode_num_to_char_str(args[i])
    else:
        for i in range(0,args.__len__()):
            rslt = rslt + unicode_num_to_char_str(0x0000ffff & args[i])
    return(rslt)

#@@@@@@@@@@@@@@@@@@








#############################














# def char_to_slash_u_str(ch,**kwargs):
    # '''
        # >>> char_to_slash_u_str('a')
        # '\\u0061'
        # >>> char_to_slash_u_str('你')
        # '\\u4f60'
    # '''
    # if('with_slash_u' in kwargs):
        # with_slash_u=kwargs['with_slash_u']
    # else:
        # with_slash_u=1
    # if('encode' in kwargs):
        # encode=kwargs['encode']
    # else:
        # encode='raw_unicode_escape'
    # if(ord(ch)<256):
        # bs = hex(ord(ch)).replace('0x','\\u00')
        # if(with_slash_u):
            # return(bs)
        # else:
            # return(bs[2:])
    # else:
        # bs = ch.encode(encode)
        # if(encode == 'raw_unicode_escape'):
            # if(with_slash_u):
                # return(bs.__str__()[3:-1])
            # else:
                # return(bs.__str__()[5:-1])
        # elif(encode == 'utf-8'):
        # elif(encode == 'utf-16'):
        # else:

    


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



# def unpack_twobytes_using_unicode(two_bytes):
# def unpack_fourbytes_using_unicode(four_bytes):
# def pack_str_using_unicode(str):
# def unpack_bytes_stream_using_unicode(Bs):
# def char_str_to_unicode_num(char_str):
# def unicode_num_to_char_str(unicode_num):
# def str_to_unicode_num_array(a_string):
# def unicode_num_array_to_str(num_arr):


# def str_to_unicode_hex_str(s):
# def unicode_hex_str_to_str(s):











###############################
# def pack_char_using_unicode(char_str):
# def pack_char_using_unicode(char_str):
    # '''
        # >>> print('a')
        # a
        # >>> print(ord('a'))
        # 97
        # >>> print(hex(97))
        # 0x61
        # >>> '\x00'
        # '\x00'
        # >>> print('\x61')
        # a
        # >>> print('\u0061')
        # a
        # >>> pack_char_using_unicode('a')
        # b'\x00a'
        # >>>
        # >>>
        # >>>
        # >>> print('问')
        # 问
        # >>> print(ord('问'))
        # 38382
        # >>> print(hex(38382))
        # 0x95ee
        # >>> print('\x95')
        # <95>
        # >>> print('\xee')
        # ?
        # >>> print('\u95ee')
        # 问
        # >>> pack_char_using_unicode('问')
        # b'\x95\xee'
        # >>>
    # '''
    # if('encode' in kwargs):
        # encode=kwargs['encode']
    # else:
        # encode='raw_unicode_escape'
    # u = char_str.encode(encode)
    # u = u.decode('utf-8')
    # if(u.__len__() == 1):
        # u = b'\x00' + bytes(u,'latin-1')
    # else:
        # u = u[2:]
        # uh = int(u[0:2],16)
        # ul = int(u[2:],16)
        # u = bytes((chr(uh)+chr(ul)),'latin-1')
    # return(u)


