#ALU control unit
aluc = 'xxx'

def updateAluControl(fn, aluop):
    global aluc
    if aluop=='00' or (aluop=='10' and fn=='100000'): #LW/SW add or ADD/ADDI
        aluc = '010'
    elif aluop=='01' or (aluop=='10' and fn == '100010'): #VEQ or SUB
        aluc = '110'
    elif aluop=='10' and fn == '100100':   #and
        aluc = '000' 
    elif aluop=='10' and fn == '100101':   #or
        aluc = '001'
    elif aluop=='10' and fn == '101010':  #slt
        aluc = '111'

#ALU
ALU = {"in1":'', "in2":'', "aluc":aluc, "zero":0, "res":''}

def performALU(in1, in2):
    ALU["in1"] = in1
    ALU["in2"] = in2
    if aluc == '010':  # addi, lw, sw #add
        ALU["res"] = in1 + in2
    elif aluc == '110':  # beq, bne #sub
        ALU["res"] = in1 - in2
    elif aluc == '000':  # and
        ALU["res"] = in1 & in2
    elif aluc == '001':  # or
        ALU["res"] = in1 | in2
    elif aluc == '111':  # slt
        ALU["res"] = in1 << in2

    if ALU["res"] == 0:   
        ALU["zero"] = 1   