from collections import OrderedDict
import opcodes

def updatecontrolUnit(op):    #updating control unit
    Control_Sig = {"RegDst" : 0,
    "Jump" : 0,
    "Branch" : 0,
    "MemRead" : 0,
    "MemtoReg" : 0,
    "aluop" : '00', 
    "MemWrite" : 0,
    "ALUSrc": 0,
    "RegWrite" : 0,
    "Zero" : 0}
    if op == opcodes.RFORMAT or op == opcodes.MUL:  
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
        Control_Sig["ALUSrc"] = 1
        Control_Sig["RegWrite"] = 0
        Control_Sig["MemRead"] = 0
        Control_Sig["MemWrite"] = 1
        Control_Sig["Branch"] = 0
        Control_Sig["aluop"] = '00'
        Control_Sig["Jump"] = 0

    elif op == opcodes.BEQ:
        Control_Sig["ALUSrc"] = 0
        Control_Sig["RegWrite"] = 0
        Control_Sig["MemRead"] = 0
        Control_Sig["MemWrite"] = 0
        Control_Sig["Branch"] = 1
        Control_Sig["aluop"] = '01'
        Control_Sig["Jump"] = 0

    elif op == opcodes.ADDI:
        Control_Sig["RegDst"] = 0
        Control_Sig["ALUSrc"] = 1
        Control_Sig["MemtoReg"] = 0
        Control_Sig["RegWrite"] = 1
        Control_Sig["MemRead"] = 0
        Control_Sig["MemWrite"] = 0
        Control_Sig["Branch"] = 0
        Control_Sig["aluop"] = '00'
        Control_Sig["Jump"] = 0

    elif op == opcodes.J:
        Control_Sig["RegWrite"] = 0
        Control_Sig["MemRead"] = 0
        Control_Sig["MemWrite"] = 0
        Control_Sig["Jump"] = 1

    return Control_Sig
