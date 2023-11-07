from converter import *
import opcodes
# pipelined, carry forward:
# 1)Control signals
# 2)decoded part#
# 3)register_file, updated register



IFID = {"pc": '', "curr_instr" : ''}


IDEX = {"pc" : '', "Control_Sig":{"PCSrc" : 0, "RegDst" : 0,"Jump" : 0,"Branch" : 0,"MemRead" : 0,"MemtoReg" : 0,"aluop" : '00', "MemWrite" : 0,"ALUSrc": 0,"RegWrite" : 0},
         "rd_data1" : 0, "rd_data2" : 0, "imm_val" : 0, "fn" : '', "rd" : '', "rt" : 0}


EXMEM = {"Control_Sig":{"PCSrc" : 0, "RegDst" : 0,"Jump" : 0,"Branch" : 0,"MemRead" : 0,"MemtoReg" : 0,"aluop" : '00', "MemWrite" : 0,"ALUSrc": 0,"RegWrite" : 0}, 
         "pc" : 0, "zero" : 0, "ALU_res" : 0, "rd_data2" : 0, "reg_write_data" : 0}


MEMWB = {"Control_Sig":{"PCSrc" : 0, "RegDst" : 0,"Jump" : 0,"Branch" : 0,"MemRead" : 0,"MemtoReg" : 0,"aluop" : '00', "MemWrite" : 0,"ALUSrc": 0,"RegWrite" : 0}, 
         "reg_write_data":0, "ALU_res":0, "mem_rd_data":''}

def updateIFID(pc, curr_instr):
    IFID["pc"] = pc
    IFID["curr_instr"] = curr_instr

def updateIDEX(Control_Sig, pc, rd_data1, rd_data2, imm_val, rt, rd, fn):
    IDEX["Control_Sig"] = Control_Sig
    IDEX["pc"] = pc
    IDEX["rd_data1"] = rd_data1
    IDEX["rd_data2"] = rd_data2
    IDEX["imm_val"] = imm_val
    IDEX["rt"] = rt
    IDEX["rd"] = rd
    IDEX["fn"] = fn

def updateEXMEM():
    pass

def updateMEMWB():
    pass











# class pipelined_reg:
    
#     def __init__(self):
#         self.Control_Sig = {"PCSrc" : 0, 
#             "RegDst" : 0,
#             "Jump" : 0,
#             "Branch" : 0,
#             "MemRead" : 0,
#             "MemtoReg" : 0,
#             "aluop" : '00', 
#             "MemWrite" : 0,
#             "ALUSrc": 0,
#             "RegWrite" : 0,
#             "Zero" : 0}
#         self.decoded = {"op" : '',
#             "rs" : '',
#             "rt" : '',
#             "rd" : '',
#             "imm_val" : 0,
#             "shamt" : '',
#             "fn" : '',
#             "jump_address" : 0} 
#         self.ref_file ={"rd_reg1": '',
#             "rd_reg2" : '', 
#             "wr_reg" : '', 
#             "wr_data" : '',  
#             "rd_data1" : '', 
#             "rd_data2" : ''}

#     def decode(self, curr_instr) :
#         self.decode["op"] = curr_instr[0:6] #updating control signals

#         self.decode["rs"] = curr_instr[6:11] #readreg 1
#         self.decode["rt"] = curr_instr[11:16] #readreg 2
#         self.decode["rd"] = curr_instr[16:21]
#         self.decode["shamt"] = curr_instr[21:26]
#         self.decode["fn"] = curr_instr[26:32]
#         self.decode["imm_val"] = bintodec(curr_instr[16:32]) #immediate value in lw/sw and offset in beq, note it is an integer
#         self.decode["jump_address"] =bintodec("0000"+curr_instr[6:32]+"00")   #jump address in integer format

#     def updateControl(self):
#         if self.decoded["op"] == opcodes.RFORMAT or self.decoded["op"] == opcodes.MUL:  
#             self.Control_Sig["RegDst"] = 1
#             self.Control_Sig["ALUSrc"] = 0
#             self.Control_Sig["MemtoReg"] = 0
#             self.Control_Sig["RegWrite"] = 1
#             self.Control_Sig["MemRead"] = 0
#             self.Control_Sig["MemWrite"] = 0
#             self.Control_Sig["Branch"] = 0
#             self.Control_Sig["aluop"] = '10'
#             self.Control_Sig["Jump"] = 0
        
#         elif self.decoded["op"] == opcodes.LW:
#             self.Control_Sig["RegDst"] = 0
#             self.Control_Sig["ALUSrc"] = 1
#             self.Control_Sig["MemtoReg"] = 1
#             self.Control_Sig["RegWrite"] = 1
#             self.Control_Sig["MemRead"] = 1
#             self.Control_Sig["MemWrite"] = 0
#             self.Control_Sig["Branch"] = 0
#             self.Control_Sig["aluop"] = '00'
#             self.Control_Sig["Jump"] = 0

#         elif self.decoded["op"] == opcodes.SW:

#             self.Control_Sig["ALUSrc"] = 1

#             self.Control_Sig["RegWrite"] = 0
#             self.Control_Sig["MemRead"] = 0
#             self.Control_Sig["MemWrite"] = 1
#             self.Control_Sig["Branch"] = 0
#             self.Control_Sig["aluop"] = '00'
#             self.Control_Sig["Jump"] = 0

#         elif self.decoded["op"] == opcodes.BEQ:
#             self.Control_Sig["ALUSrc"] = 0
#             self.Control_Sig["RegWrite"] = 0
#             self.Control_Sig["MemRead"] = 0
#             self.Control_Sig["MemWrite"] = 0
#             self.Control_Sig["Branch"] = 1
#             self.Control_Sig["aluop"] = '01'
#             self.Control_Sig["Jump"] = 0

#         elif self.decode["op"] == opcodes.ADDI:
#             self.Control_Sig["RegDst"] = 0
#             self.Control_Sig["ALUSrc"] = 1
#             self.Control_Sig["MemtoReg"] = 0
#             self.Control_Sig["RegWrite"] = 1
#             self.Control_Sig["MemRead"] = 0
#             self.Control_Sig["MemWrite"] = 0
#             self.Control_Sig["Branch"] = 0
#             self.Control_Sig["aluop"] = '00'
#             self.Control_Sig["Jump"] = 0

#         elif self.decoded["op"] == opcodes.J:
#             self.Control_Sig["RegWrite"] = 0
#             self.Control_Sig["MemRead"] = 0
#             self.Control_Sig["MemWrite"] = 0
#             self.Control_Sig["Jump"] = 1
        