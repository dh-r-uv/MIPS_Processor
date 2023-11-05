
def bintodec(bin):  #converting binary to int
    return int(bin, 2)

def hextobin(hex):
    hex_int = int(hex[2:], 16)  
# Convert the integer to binary using bitwise operators  
    bin_str = format(hex_int, 'b')  
    if(len(bin_str)<32):    #sign extend to 32 bits
            bin_str = '0' *(32-len(bin_str)) + bin_str
    return bin_str