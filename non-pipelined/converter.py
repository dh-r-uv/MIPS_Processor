
def bintodec(bin):  #converting binary to int, making it to be signed
    if(bin[0] == '1'):  #negative int if 1 is the first bit 
        val = int(bin[1:]) - 1<<16 
    else:
        val = int(bin, 2)    
    return val

def hextobin(hex):
    hex_int = int(hex[2:], 16)  
    bin_str = format(hex_int, 'b')  # Convert the integer to binary using bitwise operators  
    if(len(bin_str)<32):    #sign extend to 32 bits
            bin_str = '0' *(32-len(bin_str)) + bin_str
    return bin_str