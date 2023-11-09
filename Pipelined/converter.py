
def bintodec(bin, n):  #converting binary to int, making it to be signed
    if(bin[0] == '1'):  #negative int if 1 is the first bit 
        val = int(bin, 2) - (1<<n) 
    else:
        val = int(bin, 2)    
    return val

def hextobin(hex, n):
    hex_int = int(hex[2:], 16)  
    bin_str = format(hex_int, 'b')  # Convert the integer to binary using bitwise operators  
    if(len(bin_str)<n):    #sign extend to 32 bits
            bin_str = '0' *(n-len(bin_str)) + bin_str
    return bin_str

def dectohex(dec):
    val = hex(dec)
    extended_val = val[:2] + '0'*(8-(len(val)-2)) + val[2:]
    return extended_val