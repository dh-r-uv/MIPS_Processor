from collections import OrderedDict
import opcodes


def bintodec(bin):  #converting binary to int
    return int(bin, 2)
#Control signals
Control_Sig = OrderedDict()
Control_Sig = {"PCSrc" : 0, 
    "RegDst" : 0,
    "Jump" : 0,
    "Branch" : 0,
    "MemRead" : 0,
    "MemtoReg" : 0,
    "aluop" : '00', 
    "MemWrite" : 0,
    "ALUSrc": 0,
    "RegWrite" : 0,
    "Zero" : 0}

def updatecontrolUnit(op):    #updating control unit

    if op == opcodes.RFORMAT:
        #Control_Sig["PCSrc"] = 0
        Control_Sig["RegDst"] = 1
        Control_Sig["ALUSrc"] = 0
        Control_Sig["MemtoReg"] = 0
        Control_Sig["RegWrite"] = 1
        Control_Sig["MemRead"] = 0
        Control_Sig["MemWrite"] = 0
        Control_Sig["Branch"] = 0
        Control_Sig["aluop"] = '10'
        Control_Sig["Jump"] = 0
        
    elif op == opcodes.LW:
        #Control_Sig["PCSrc"] = 0
        Control_Sig["RegDst"] = 0
        Control_Sig["ALUSrc"] = 1
        Control_Sig["MemtoReg"] = 1
        Control_Sig["RegWrite"] = 1
        Control_Sig["MemRead"] = 1
        Control_Sig["MemWrite"] = 0
        Control_Sig["Branch"] = 0
        Control_Sig["aluop"] = '00'
        Control_Sig["Jump"] = 0

    elif op == opcodes.SW:
        #Control_Sig["PCSrc"] = 0

        Control_Sig["ALUSrc"] = 1

        Control_Sig["RegWrite"] = 0
        Control_Sig["MemRead"] = 0
        Control_Sig["MemWrite"] = 1
        Control_Sig["Branch"] = 0
        Control_Sig["aluop"] = '00'
        Control_Sig["Jump"] = 0

    elif op == opcodes.BEQ:
        #Control_Sig["PCSrc"] = 1
        Control_Sig["ALUSrc"] = 0
        Control_Sig["RegWrite"] = 0
        Control_Sig["MemRead"] = 0
        Control_Sig["MemWrite"] = 0
        Control_Sig["Branch"] = 1
        Control_Sig["aluop"] = '01'
        Control_Sig["Jump"] = 0
    #removed set less than
    elif op == opcodes.J:
        #Control_Sig["PCSrc"] = 1
        Control_Sig["RegWrite"] = 0
        Control_Sig["MemRead"] = 0
        Control_Sig["MemWrite"] = 0
        Control_Sig["Branch"] = 0
        Control_Sig["Jump"] = 1
