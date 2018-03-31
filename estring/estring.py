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

def get_chbyts_bominfo(bs,**kwargs):
    '''
        #only support utf-16 utf-32
        #LE           Little- Endian
        #BE           Big-Endian
        #OOB          Out-Of-Band (withour BOM)
        
        bs = b'\xff\xfe\x60\x4f'
        get_chbyts_bominfo(bs)
        bs = b'\x60\x4f'
        get_chbyts_bominfo(bs)
        bs = b'\xfe\xff\x4f\x60'
        get_chbyts_bominfo(bs)
        bs = b'\x4f\x60'
        get_chbyts_bominfo(bs)
        bs = b'\xff\xfe\x00\x00\x60\x4f\x00\x00'
        get_chbyts_bominfo(bs)
        bs = b'\x60\x4f\x00\x00'
        get_chbyts_bominfo(bs)
        bs = b'\x00\x00\xfe\xff\x00\x00\x4f\x60'
        get_chbyts_bominfo(bs)
        bs = b'\x00\x00\x4f\x60'
        get_chbyts_bominfo(bs)
        
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

def remove_chbyts_bom(bs,**kwargs):
    '''
        #only support utf-16 utf-32 
        
        #LE           Little- Endian
        #BE           Big-Endian
        #OOB          Out-Of-Band (withour BOM)
        
        bs = b'\xff\xfe\x60\x4f'
        remove_chbyts_bom(bs)
        bs = b'\x60\x4f'
        remove_chbyts_bom(bs)
        bs = b'\xfe\xff\x4f\x60'
        remove_chbyts_bom(bs)
        bs = b'\x4f\x60'
        remove_chbyts_bom(bs)
        bs = b'\xff\xfe\x00\x00\x60\x4f\x00\x00'
        remove_chbyts_bom(bs)
        bs = b'\x60\x4f\x00\x00'
        remove_chbyts_bom(bs)
        bs = b'\x00\x00\xfe\xff\x00\x00\x4f\x60'
        remove_chbyts_bom(bs)
        bs = b'\x00\x00\x4f\x60'
        remove_chbyts_bom(bs)
    '''
    bominfo = get_chbyts_bominfo(bs,**kwargs)
    return(bominfo[0])

def decode_chbyts(bs,encode='raw_unicode_escape',**kwargs):
    '''
        #only support utf-8 utf-16 utf-32 
        
        
        #LE           Little- Endian
        #BE           Big-Endian
        #OOB          Out-Of-Band (withour BOM)
        
        bs = b'\xff\xfe\x60\x4f'
        decode_chbyts(bs,'utf_16')
        bs = b'\x60\x4f'
        decode_chbyts(bs,'utf_16_le')
        bs = b'\xfe\xff\x4f\x60'
        decode_chbyts(bs,'utf_16_be')
        bs = b'\x4f\x60'
        decode_chbyts(bs,'utf_16_be')
        bs = b'\xff\xfe\x00\x00\x60\x4f\x00\x00'
        decode_chbyts(bs,'utf_32')
        bs = b'\x60\x4f\x00\x00'
        decode_chbyts(bs,'utf_32_le')
        bs = b'\x00\x00\xfe\xff\x00\x00\x4f\x60'
        decode_chbyts(bs,'utf_32_be')
        bs = b'\x00\x00\x4f\x60'
        decode_chbyts(bs,'utf_32_be')
    '''
    bs = remove_chbyts_bom(bs,**kwargs)
    ch = bs.decode(encode)
    return(ch)

def get_chbyts_bomtype(bs,**kwargs):
    '''
        #only support utf-16 utf-32 
        
        #LE           Little- Endian
        #BE           Big-Endian
        #OOB          Out-Of-Band (withour BOM)
        
        bs = b'\xff\xfe\x60\x4f'
        bs.decode('utf_16')
        get_chbyts_bomtype(bs)
        '\u4f60'
        bs = b'\x60\x4f'
        bs.decode('utf_16_le')
        get_chbyts_bomtype(bs)
        '\u4f60'
        bs = b'\xfe\xff\x4f\x60'
        get_chbyts_bomtype(bs)
        decode_chbyts(bs,'utf_16_be')
        '\u4f60'
        bs = b'\x4f\x60'
        bs.decode('utf_16_be')
        get_chbyts_bomtype(bs)
        '\u4f60'
        bs = b'\xff\xfe\x00\x00\x60\x4f\x00\x00'
        bs.decode('utf_32')
        get_chbyts_bomtype(bs)
        '\U00004f60'
        bs = b'\x60\x4f\x00\x00'
        bs.decode('utf_32_le')
        get_chbyts_bomtype(bs)
        '\U00004f60'
        bs = b'\x00\x00\xfe\xff\x00\x00\x4f\x60'
        decode_chbyts(bs,'utf_32_be')
        get_chbyts_bomtype(bs)
        '\U00004f60'
        bs = b'\x00\x00\x4f\x60'
        bs.decode('utf_32_be')
        get_chbyts_bomtype(bs)
        '\U00004f60'
    '''
    bominfo = get_chbyts_bominfo(bs,**kwargs)
    return(bominfo[1])



#@@@@@@@@@@@@@@@@@@@@

#chstr                        char-string
#pack_chstr                   pack-char-string (to bytes-stream)
#chstr2byts                   pack-char-string (to bytes-stream)
#encode_chstr                 pack-char-string (to bytes-stream)
#chnum                        char-number
#pack_chnum                   pack-char-number (to bytes-stream)
#chnum2byts                   pack-char-number (to bytes-stream)
#encode_chnum                 pack-char-number (to bytes-stream)

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
    '''
    chstr = chr(chnum)
    bs = pack_chstr(chstr,**kwargs)
    return(bs)

chnum2byts = pack_chnum
encode_chnum = pack_chnum


