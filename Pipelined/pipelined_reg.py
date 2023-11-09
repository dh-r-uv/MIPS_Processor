from converter import *
import opcodes
# pipelined, carry forward:
# 1)Control signals
# 2)decoded part#
# 3)register_file, updated register



IFID = {"pc": '', "curr_instr" : ''}

IDEX = {"pc" : '', "Control_Sig":{"PCSrc" : 0, "RegDst" : 0,"Jump" : 0,"Branch" : 0,"MemRead" : 0,"MemtoReg" : 0,"aluop" : '00', "MemWrite" : 0,"ALUSrc": 0,"RegWrite" : 0},
         "rd_data1" : 0, "rd_data2" : 0, "imm_val" : 0, "fn" : '', "rs" : '', "rd" : '', "rt" : 0, "jump_address":0}

EXMEM = {"Control_Sig":{"PCSrc" : 0, "RegDst" : 0,"Jump" : 0,"Branch" : 0,"MemRead" : 0,"MemtoReg" : 0,"aluop" : '00', "MemWrite" : 0,"ALUSrc": 0,"RegWrite" : 0}, 
         "pc" : 0, "zero" : 0, "ALU_res" : 0, "rd_data2" : 0, "reg_write_data" : '', "jump_address":0}

MEMWB = {"Control_Sig":{"PCSrc" : 0, "RegDst" : 0,"Jump" : 0,"Branch" : 0,"MemRead" : 0,"MemtoReg" : 0,"aluop" : '00', "MemWrite" : 0,"ALUSrc": 0,"RegWrite" : 0}, 
         "reg_write_data":'', "ALU_res":0, "mem_rd_data":''}

def updateIFID(reg):
    IFID["pc"] = reg[0]
    IFID["curr_instr"] = reg[1]


def updateIDEX(reg):
    IDEX["Control_Sig"] = reg[0]
    IDEX["pc"] = reg[1]
    IDEX["rd_data1"] = reg[2]
    IDEX["rd_data2"] = reg[3]
    IDEX["imm_val"] = reg[4]
    IDEX["rs"] = reg[5]
    IDEX["rt"] = reg[6]
    IDEX["rd"] = reg[7]
    IDEX["fn"] = reg[8]
    IDEX["jump_address"] = reg[9]

def updateEXMEM(reg):
    EXMEM["Control_Sig"] = reg[0]
    EXMEM["pc"] = reg[1]
    EXMEM["zero"] = reg[2]
    EXMEM["ALU_res"] = reg[3]
    EXMEM["rd_data2"] = reg[4]
    EXMEM["reg_write_data"] = reg[5]
    EXMEM["jump_address"] = reg[6]

def updateMEMWB(reg):
    MEMWB["Control_Sig"] = reg[0]
    MEMWB["reg_write_data"] = reg[1]
    MEMWB["ALU_res"] = reg[2]
    MEMWB["mem_rd_data"] = reg[3]


def update_pipelined(Reg_update):
    if(0 in Reg_update.keys()):
        updateIFID(Reg_update[0])
    if(1 in Reg_update.keys()):
        updateIDEX(Reg_update[1])    
    if(2 in Reg_update.keys()):
        updateEXMEM(Reg_update[2])
    if(3 in Reg_update.keys()):
        updateMEMWB(Reg_update[3])


def flushIFID():
    IFID["pc"] = ''
    IFID["curr_instr"] = ''

def flushIDEX():
    IDEX["Control_Sig"] = {"PCSrc" : 0, "RegDst" : 0,"Jump" : 0,"Branch" : 0,"MemRead" : 0,"MemtoReg" : 0,"aluop" : '00', "MemWrite" : 0,"ALUSrc": 0,"RegWrite" : 0}
    IDEX["pc"] = 0
    IDEX["rd_data1"] = 0
    IDEX["rd_data2"] = 0
    IDEX["imm_val"] = 0
    IDEX["rs"] = ''
    IDEX["rt"] = ''
    IDEX["rd"] = ''
    IDEX["fn"] = ''
    IDEX["jump_address"] = 0

def flushEXMEM():
    EXMEM["Control_Sig"] = {"PCSrc" : 0, "RegDst" : 0,"Jump" : 0,"Branch" : 0,"MemRead" : 0,"MemtoReg" : 0,"aluop" : '00', "MemWrite" : 0,"ALUSrc": 0,"RegWrite" : 0}
    EXMEM["pc"] = 0
    EXMEM["zero"] = 0
    EXMEM["ALU_res"] = 0
    EXMEM["rd_data2"] = 0
    EXMEM["reg_write_data"] = ''
    EXMEM["jump_address"] = 0
