
import opcodes
from memory import data_mem, instr_mem
from Registers import regmem, regmem_name
from pipelined_reg import *
from Control import *
from ALU import *
from Register_File import *
from converter import *

#implementing it without jump first


#Instruction Fetch
def IF(pc):
    curr_instr = hextobin(instr_mem[pc])
    pc+=4
    updateIFID(pc, curr_instr)
#Instruction Fetch Ends

#Instruction Decode
def ID():
    curr_instr = IFID["curr_instr"]
    op = curr_instr[0:6]
    Control_Sig = updatecontrolUnit(op) #updating control signals
    rs=curr_instr[6:11] #readreg 1
    rt=curr_instr[11:16] #readreg 2
    rd=curr_instr[16:21]
    shamt=curr_instr[21:26]
    fn=curr_instr[26:32]
    imm_val=bintodec(curr_instr[16:32]) #immediate value in lw/sw and offset in beq, note it is an integer
    jump_address=bintodec("0000"+curr_instr[6:32]+"00")   #jump address in integer format
    
    update_reg_file(rs, rt)

    updateIDEX(Control_Sig, IFID["pc"], Register_File["rd_data1"], Register_File["rd_data2"], imm_val, rt, rd, fn, jump_address)
#Instruction Decode ends       

#Instruction Execute
def EX():
    fn = IDEX["fn"]
    Cntrl_sig = IDEX["Control_Sig"]
    imm_val = IDEX["imm_val"]
    aluc = updateAluControl(fn, Cntrl_sig["aluop"]) #updating alucontrol signals

    in1 = IDEX["rd_data1"]
    if(Cntrl_sig["ALUSrc"]==0):
        in2 = IDEX["rd_data2"]
    else:
        in2 = imm_val

    # in2 = imm_val if (Control_Sig["ALUSrc"]>0) else Register_File["rd_data2"]
    alu_res, zero = performALU(in1, in2, aluc)    #performing ALU operations ALU is updated

    #performing mux1
    if(Cntrl_sig["Branch"] and zero):
        pc += 4*imm_val
    #performing mux2
    if(Cntrl_sig["Jump"]):
        pc = IDEX["jump_address"]

    #write_reg is updated
    reg_write_data = IDEX["rd"] if (Cntrl_sig["RegDst"]>0) else IDEX["rt"]    

    updateEXMEM(Cntrl_sig, pc, zero, alu_res, IDEX["rd_data2"], reg_write_data, IDEX["jump_address"])    
#Instruction Execute ends

#Memory Access
def MEM():
    Control_Sig = EXMEM["Control_Sig"]
    address = EXMEM["ALU_res"]
    data_to_be_written = EXMEM["rd_data2"]
    if(Control_Sig["MemWrite"]==1):
        data_mem[address] = data_to_be_written

    if(Control_Sig["MemRead"]==1):
        rd_data_from_mem = data_mem[address]

    updateMEMWB(Control_Sig, EXMEM["reg_write_data"], EXMEM["ALU_res"], rd_data_from_mem)    
#Memory Access ends

#WriteBack
data_write_back = ''
def WB():
    Control_Sig = MEMWB["Control_Sig"]
    if(Control_Sig["MemtoReg"]):
        data_write_back = MEMWB["mem_rd_data"]
    else:
        data_write_back = MEMWB["res"]    

    if(Control_Sig["RegWrite"]):
        write_into_reg(MEMWB["reg_write_data"], data_write_back)
        
#WriteBack ends

def Create_Instr_set(pc):
    global num_lines, strt_add
    strt_add = pc
    in_file=open("Factorial.txt","r")
    instr_list = in_file.readlines()
    num_lines = len(instr_list)
    for line in instr_list:
        instr_mem[strt_add] = '0x'+line.rstrip('\n')
        strt_add+=4

def pipelined_mips(pc):
    cycle_count=0
    instr = []  #instruction queue
    while(True):
        if(pc not in instr_mem.keys()):
            break
        
    pass



def main(): #main
    pc=0x00400000   #set pc, stored as int only
    Create_Instr_set(pc)
    pipelined_mips(pc)  

if __name__ == "__main__":
    main()