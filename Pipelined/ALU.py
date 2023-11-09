#ALU control unit


def updateAluControl(fn, aluop):
    aluc = 'xxx'
    if aluop=='00' or (aluop=='10' and fn=='100000'): #LW/SW add or ADD/ADDI
        aluc = '010'
    elif aluop=='01' or (aluop=='10' and fn == '100010'): #BEQ or SUB
        aluc = '110'   
    elif aluop=='10' and fn == '000010':    #MUL
        aluc = '011'    #let MUL alu control be mul     
    elif aluop=='10' and fn == '100100':   #and
        aluc = '000' 
    elif aluop=='10' and fn == '100101':   #or
        aluc = '001'
    elif aluop=='10' and fn == '101010':  #slt
        aluc = '111'
    return aluc    


def performALU(in1, in2, aluc):
    if aluc == '010':  # addi, lw, sw #add
        alu_res = in1 + in2
    elif aluc == '110':  # beq, bne #sub
        alu_res = in1 - in2
    elif aluc == '011':  #MUL   
        alu_res = in1 * in2 
    elif aluc == '000':  # and
        alu_res = in1 & in2
    elif aluc == '001':  # or
        alu_res = in1 | in2
    elif aluc == '111':  # slt
        alu_res = int(in1 < in2)    

    if alu_res == 0:   
        zero = 1   
    else:
        zero = 0  
    return alu_res, zero    

