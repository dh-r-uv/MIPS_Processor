
import opcodes
from memory import data_mem, instr_mem
from Registers import regmem, regmem_name
from pipelined_reg import *
from Control import *
from ALU import *
from Register_File import *
from converter import *
from forwarding_hazard import *


def Create_Instr_set(pc):
    global num_lines, strt_add
    strt_add = pc
    in_file=open("sorting.txt","r")
    instr_list = in_file.readlines()
    num_lines = len(instr_list)
    for line in instr_list:
        instr_mem[strt_add] = '0x'+line.rstrip('\n')
        strt_add+=4

#implementing it without jump first

hzd = 0 #for data hazard

#Instruction Fetch
def IF(pc):
    curr_instr = hextobin(instr_mem[pc], 32)
    pc+=4
    return pc, [pc, curr_instr]
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
    imm_val=bintodec(curr_instr[16:32], 16) #immediate value in lw/sw and offset in beq, note it is an integer
    jump_address=bintodec("0000"+curr_instr[6:32]+"00", 32)   #jump address in integer format
    update_reg_file(rs, rt)
    return [Control_Sig, IFID["pc"], Register_File["rd_data1"], Register_File["rd_data2"], imm_val, rs, rt, rd, fn, jump_address]
#Instruction Decode ends       

#Instruction Execute
def EX():
    global hzd
    #updating forwardingcontrol signals
    fowA, fowB = updateforwading_sig(IDEX["rs"], IDEX["rt"])
    fn = IDEX["fn"]
    Cntrl_sig = IDEX["Control_Sig"]
    imm_val = IDEX["imm_val"]
    pc = IDEX["pc"] 
    aluc = updateAluControl(fn, Cntrl_sig["aluop"]) #updating alucontrol signals

    #forwarding   
    inp1 = forward_mul(fowA, IDEX["rd_data1"])
    inp2 = forward_mul(fowB, IDEX["rd_data2"])

    if(fowA or fowB):
        hzd = 1

    in1 = inp1
    in2 = 0
    if(Cntrl_sig["ALUSrc"]==0):
        in2 = inp2
    else:
        in2 = imm_val

    alu_res, zero = performALU(in1, in2, aluc)    #performing ALU operations ALU is updated

    #performing mux1
    if(Cntrl_sig["Branch"] and zero):
        pc += 4*imm_val
    #performing mux2
    if(Cntrl_sig["Jump"]):
        pc = IDEX["jump_address"]

    #write_reg is updated
    reg_write_data = IDEX["rd"] if (Cntrl_sig["RegDst"]==1) else IDEX["rt"]   
    
    #jumping
    to_jump = 0
    if(Cntrl_sig["Jump"] or (Cntrl_sig["Branch"] and zero)):
        to_jump = 1
    return to_jump, pc, [Cntrl_sig, pc, zero, alu_res, inp2, reg_write_data, IDEX["jump_address"]]
#Instruction Execute ends

#Memory Access
def MEM():
    Control_Sig = EXMEM["Control_Sig"]
    address = EXMEM["ALU_res"]
    data_to_be_written = EXMEM["rd_data2"]
    rd_data_from_mem = ''
    if(Control_Sig["MemWrite"]==1):
        data_mem[address] = data_to_be_written

    if(Control_Sig["MemRead"]==1):
        rd_data_from_mem = data_mem[address]
    return [Control_Sig, EXMEM["reg_write_data"], EXMEM["ALU_res"], rd_data_from_mem]
#Memory Access ends

#WriteBack
def WB():
    Control_Sig = MEMWB["Control_Sig"]
    if(Control_Sig["MemtoReg"]):
        data_write_back = MEMWB["mem_rd_data"]
    else:
        data_write_back = MEMWB["ALU_res"]    
    if(Control_Sig["RegWrite"]):
        write_into_reg(MEMWB["reg_write_data"], data_write_back)
#WriteBack ends


def pipelined_mips(pc):
    global hzd
    cycle_count=0
    instr = [None, None, None, None, None]  #0-IF, 1-ID, 2-EX, 3-MEM, 4-WB
    global st
    st = 0

    while(True):
        if(st):
            instr.insert(2, None)
        elif(pc not in instr_mem.keys()):
            instr.insert(0, None)
        else:
            instr.insert(0, pc) #storing the current instruction
        instr.pop()
        if(instr.count(None)==5):
            break
        Reg_update = {}

        cycle_count+=1
        
        print(f'Running inst at address : {pc} and clockcyle count: {cycle_count}')
        to_jump = 0
        for i in range(4, -1, -1):
            if(instr[i] is None):
                continue
            if(i==4):
                #print("WB")
                WB()
            elif(i==3):
                #print("MEM")
                Reg_update[i] = MEM()
                if(st==1):
                    st=0
                    flushEXMEM()
                    break
            elif(i==2):
                #print("EX")
                to_jump, pc2, Reg_update[i] = EX() 
            elif(i==1):
                #print("ID")
                Reg_update[i] = ID()
            elif(i==0):
                #print("IF")
                pc, Reg_update[i] = IF(pc) 
        FOWD()  
        #updating pipelined register
        if(hzd):
            hzd = 0
            FOWD()
        update_pipelined(Reg_update)     
        #hazard detection and resolving

        if(EXMEM["Control_Sig"]["MemtoReg"] and (IDEX["rs"]==EXMEM["reg_write_data"] or IDEX["rt"]==EXMEM["reg_write_data"])):
            st = 1
            

        #end 
        #BEQ and jump start
        if(to_jump):
            to_jump = 0
            flushEXMEM()
            flushIDEX()
            flushIFID()
            pc = pc2
            instr[0] = None
            instr[1] = None

        #end
        
        print("Data Memory is:")
        print(data_mem)
        print("Register Memory is:")
        # for key in regmem.keys():
        #     print(f'{regmem_name[key]} : {regmem[key]}')   
     

def main(): #main
    pc=0x00400000   #set pc, stored as int only
    Create_Instr_set(pc)
    pipelined_mips(pc)  

if __name__ == "__main__":
    main()