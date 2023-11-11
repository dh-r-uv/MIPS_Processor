
import opcodes
from memory import data_mem, instr_mem
from Registers import regmem, regmem_name
from pipelined_reg import *
from Control import *
from ALU import *
from Register_File import *
from converter import *
from forwarding_hazard import *

#creating instruction dictionary
def Create_Instr_set(pc):
    global num_lines, strt_add
    strt_add = pc
    in_file=open("sorting.txt","r")
    instr_list = in_file.readlines()
    num_lines = len(instr_list)
    for line in instr_list:
        instr_mem[strt_add] = '0x'+line.rstrip('\n')
        strt_add+=4

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
    rd=curr_instr[16:21] #writereg 
    shamt=curr_instr[21:26] #shift field
    fn=curr_instr[26:32] #function field
    imm_val=bintodec(curr_instr[16:32], 16) #immediate value in lw/sw and offset in beq, note it is an integer
    jump_address=bintodec("0000"+curr_instr[6:32]+"00", 32) #jump address in integer format
    update_reg_file(rs, rt)  #updating register file
    return [Control_Sig, IFID["pc"], Register_File["rd_data1"], Register_File["rd_data2"], imm_val, rs, rt, rd, fn, jump_address]   #returning what is to be updated in IDEX
#Instruction Decode ends       

#Instruction Execute
def EX():
    #updating forwardingcontrol signals
    fowA, fowB = updateforwading_sig(IDEX["rs"], IDEX["rt"]) 
    fn = IDEX["fn"] #extracting the right vals from IDEX pipelined register
    Cntrl_sig = IDEX["Control_Sig"]
    imm_val = IDEX["imm_val"] 
    pc = IDEX["pc"] 
    aluc = updateAluControl(fn, Cntrl_sig["aluop"]) #updating alucontrol signals

    #forwarding   
    inp1 = forward_mul(fowA, IDEX["rd_data1"])  #getting the right forwarded vals depending on the forwarding control signals
    inp2 = forward_mul(fowB, IDEX["rd_data2"])

    in1 = inp1
    in2 = 0
    if(Cntrl_sig["ALUSrc"]==0): #multiplexer that handles if immediate val or rt val is to be taken
        in2 = inp2
    else:
        in2 = imm_val

    alu_res, zero = performALU(in1, in2, aluc)    #performing ALU operations ALU is updated

    #performing mux1 that updates pc if branch is to occur
    if(Cntrl_sig["Branch"] and zero):
        pc += 4*imm_val
    #performing mux2 that updates pc if jump is to occur
    if(Cntrl_sig["Jump"]):
        pc = IDEX["jump_address"]

    #write_reg is updated
    reg_write_data = IDEX["rd"] if (Cntrl_sig["RegDst"]==1) else IDEX["rt"]   
    
    #jumping or branch
    to_jump = 0 #flag that checks if pc is to be changed or not
    if(Cntrl_sig["Jump"] or (Cntrl_sig["Branch"] and zero)):
        to_jump = 1

    return to_jump, pc, [Cntrl_sig, pc, zero, alu_res, inp2, reg_write_data, IDEX["jump_address"]]  #contains list for updation of EXMEM
#Instruction Execute ends

#Memory Access
def MEM():
    Control_Sig = EXMEM["Control_Sig"]
    address = EXMEM["ALU_res"]
    data_to_be_written = EXMEM["rd_data2"]
    rd_data_from_mem = ''
    if(Control_Sig["MemWrite"]==1):     #if memtowrite is 1, then data is to be written into memory
        data_mem[address] = data_to_be_written

    if(Control_Sig["MemRead"]==1):      #if memread is 1, then data is to be read into memory
        rd_data_from_mem = data_mem[address]
    return [Control_Sig, EXMEM["reg_write_data"], EXMEM["ALU_res"], rd_data_from_mem] #returns what is to be udated in MEMWB pipelined
#Memory Access ends

#WriteBack
def WB():
    Control_Sig = MEMWB["Control_Sig"]
    if(Control_Sig["MemtoReg"]):    #if MEMtoREG then we write data read from memory
        data_write_back = MEMWB["mem_rd_data"]
    else:   #else we write alu result into it
        data_write_back = MEMWB["ALU_res"]    
    if(Control_Sig["RegWrite"]):    #if regWrite is 1 only then we write into register
        write_into_reg(MEMWB["reg_write_data"], data_write_back)
#WriteBack ends


def pipelined_mips(pc):
    cycle_count=0
    instr = [None, None, None, None, None]  #0-IF, 1-ID, 2-EX, 3-MEM, 4-WB
    global st   #maintains if stall is to be done during load dependency
    st = 0
    print("Data Memory is:")
    print(data_mem)
    print("Register Memory is:")
    for key in regmem.keys():
        print(f'{regmem_name[key]} : {regmem[key]}') 
    while(True):
        if(st):
            instr.insert(2, None)
        elif(pc not in instr_mem.keys()):
            instr.insert(0, None)
        else:
            instr.insert(0, pc) #storing the current instruction
        instr.pop()
        if(instr.count(None)==5):   #breaking if everything is none in instr queue
            break
        Reg_update = {} #dictionary that contains the updates that is to be done for each pipelined register after a clock cycle

        cycle_count+=1
        
        print(f'Running inst at address : {pc} and clockcyle count: {cycle_count}')
        to_jump = 0
        for i in range(4, -1, -1):
            if(instr[i] is None):
                continue
            if(i==4):
                print("WB", end=" ")
                WB()
            elif(i==3):
                print("MEM", end = " ")
                Reg_update[i] = MEM()
                if(st==1):  #if stall then flushexmem and break, ie dont execute EX, ID, IF
                    st=0
                    flushEXMEM()
                    break
            elif(i==2):
                print("EX", end = " ")
                to_jump, pc2, Reg_update[i] = EX() 
            elif(i==1):
                print("ID", end = " ")
                Reg_update[i] = ID()
            elif(i==0):
                print("IF", end = " ")
                pc, Reg_update[i] = IF(pc) 
        print() 

        #forwarding the right values into IDEX register depending upon the forwarding control signals       
        FOWD()
        #updating pipelined registers  
        update_pipelined(Reg_update)     

        if(EXMEM["Control_Sig"]["MemtoReg"] and (IDEX["rs"]==EXMEM["reg_write_data"] or IDEX["rt"]==EXMEM["reg_write_data"])):
            st = 1  #if EXMEM is load(ie MemtoReg ==1) and rs or rt of IDEX is same as rd in EXMEM then we stall
            print("stalling")
        #BEQ and jump start
        if(to_jump): 
            print("Flushing after jump/branch")   
            to_jump = 0
            flushEXMEM()    #flusing the pipelined registers to get rid of the the values in pipelined reg
            flushIDEX()
            flushIFID()
            pc = pc2    #updating pc
            instr[0] = None #flusing IF and ID
            instr[1] = None

        #end
    print("After executing all instructions:::") 
    print("Data Memory is:")
    print(data_mem)
    print("Register Memory is:")
    for key in regmem.keys():
        print(f'{regmem_name[key]} : {regmem[key]}')   
     

def main(): #main
    pc=0x00400000   #set pc, stored as int only
    Create_Instr_set(pc)
    pipelined_mips(pc)  

if __name__ == "__main__":
    main()