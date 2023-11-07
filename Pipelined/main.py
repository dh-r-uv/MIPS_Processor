
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
    #jump_address=bintodec("0000"+curr_instr[6:32]+"00")   #jump address in integer format
    
    update_reg_file(rs, rt)

    updateIDEX(Control_Sig, IFID["pc"], Register_File["rd_data1"], Register_File["rd_data2"], imm_val, rt, rd, fn)
#Instruction Decode ends       

#Instruction Execute
def EX():
    fn = IDEX["fn"]
    Cntrl_sig = IDEX["Control_Sig"]
    aluc = updateAluControl(fn, Cntrl_sig["aluop"]) #updating alucontrol signals

    in1 = Register_File["rd_data1"]
    in2 = imm_val if (Control_Sig["ALUSrc"]>0) else Register_File["rd_data2"]
    performALU(in1, in2)    #performing ALU operations ALU is updated

    #performing mux1
    if(Control_Sig["Branch"] and ALU["zero"]):
        pc += 4*imm_val
    #performing mux2
    if(Control_Sig["Jump"]):
        pc = jump_address
#Instruction Execute ends

#Memory Access
rd_data_from_mem = ''
def MEM():
    global rd_data_from_mem
    if(Control_Sig["MemWrite"]==1):
        addr = ALU["res"]
        data_to_be_written = Register_File["rd_data2"]
        data_mem[addr] = data_to_be_written

    if(Control_Sig["MemRead"]==1):
        addr_to_read_from = ALU["res"]
        rd_data_from_mem = data_mem[addr_to_read_from]
#Memory Access ends

#WriteBack
data_write_back = ''
def WB():
    global data_write_back
    if(Control_Sig["MemtoReg"]):
        data_write_back = rd_data_from_mem
    else:
        data_write_back = ALU["res"]    

    if(Control_Sig["RegWrite"]):
        write_into_reg(data_write_back)
#WriteBack ends

def Create_Instr_set():
    global num_lines, strt_add
    strt_add = pc
    in_file=open("Factorial.txt","r")
    instr_list = in_file.readlines()
    num_lines = len(instr_list)
    for line in instr_list:
        instr_mem[strt_add] = '0x'+line.rstrip('\n')
        strt_add+=4

def pipelined_mips():
        cycle_count=0
        pc=0x00400000   #set pc, stored as int only
        instr = []  #instruction queue
        while(True):
            if(pc not in instr_mem.keys()):
                break



def main(): #main
    Create_Instr_set()

    pipelined_mips()  

if __name__ == "__main__":
    main()