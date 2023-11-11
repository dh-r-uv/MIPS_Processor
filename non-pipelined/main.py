
import opcodes                               #opcodes for all instructions
from memory import data_mem, instr_mem       #conatins both data memory and instruction memory
from Registers import regmem, regmem_name    #conatins all registers and its data
from Control import *                        #contains control signals which is later upddated while execution
from ALU import *
from Register_File import *                  #contains registers which is fetced after Instruction Decode stage
from converter import *

##implemented only the instructions available in opcodes

#important variables
cycle_count=0
pc=0x00400000                    #set pc, stored as int 

op=''                            #all possible fiels of instructions(R, I, J) are initiated as empty string
rs=''                
rt=''
rd=''
imm_val = 0                      #imm_val and jump_address are stroed as int
shamt=''
fn=''
jump_address=0

curr_instr = ''                  #this variable contains the instruction to be executed
#Instruction Fetch
def IF():
    global curr_instr, pc, cycle_count
    cycle_count+=1               #cycle_count and PC are incremented after every IF stage
    curr_instr = instr_mem[pc]   #instruction is fetched from the instruction memory(instr_mem)
    pc+=4
#Instruction Fetch Ends

#Instruction Decode
def ID():
    global rs, rt, rd, op, fn, jump_address, shamt, imm_val
    op = curr_instr[0:6]        #opcode is decoded
    updatecontrolUnit(op)       #updating control signals acc to the opcode

    rs=curr_instr[6:11]         #all fields are being assigned respective values
    rt=curr_instr[11:16] 
    rd=curr_instr[16:21]
    shamt=curr_instr[21:26]
    fn=curr_instr[26:32]
    imm_val=bintodec(curr_instr[16:32], 16)                   #immediate value in lw/sw and offset in beq, note it is an integer
    jump_address=bintodec("0000"+curr_instr[6:32]+"00", 32)   #jump address extended to 32 bits

    wr_reg = rd if (Control_Sig["RegDst"]>0) else rt          #value of wr_reg set acc to control signal
    #now to update register File
    update_reg_file(rs, rt, wr_reg)                           #updates Register_File with rs, rt, wr_reg
#Instruction Decode ends                                      #this is passed to ALU (Execute stage)

#Instruction Execute
def EX():
    global pc
    updateAluControl(fn, Control_Sig["aluop"]) #updating alucontrol signals using aluop and fn(function field)

    in1 = Register_File["rd_data1"]            #data is fetched upon which ALU performs operation
    in2 = imm_val if (Control_Sig["ALUSrc"]>0) else Register_File["rd_data2"]
    performALU(in1, in2)                       #performing ALU operations ALU is updated

    #performing mux1
    if(Control_Sig["Branch"] and ALU["zero"]):
        pc += 4*imm_val              #if condition for BEQ is satisfied, PC is updated
    #performing mux2
    if(Control_Sig["Jump"]):
        pc = jump_address            #if JUMP condition is satisfied, PC is updated
#Instruction Execute ends

#Memory Access
rd_data_from_mem = ''
def MEM():
    global rd_data_from_mem
    if(Control_Sig["MemWrite"]==1):                    #if data is to be written into the memory(sw)
        addr = ALU["res"]                              #takes address from result of ALU
        data_to_be_written = Register_File["rd_data2"]
        data_mem[addr] = data_to_be_written            #data is stored in its location

    if(Control_Sig["MemRead"]==1):                     #if data is to be read from memory(lw)
        addr_to_read_from = ALU["res"]      
        rd_data_from_mem = data_mem[addr_to_read_from] #memory is fetched
#Memory Access ends

#WriteBack
data_write_back = ''
def WB():
    global data_write_back
    if(Control_Sig["MemtoReg"]):                 #determines if data to be written back is from memory or ALU
        data_write_back = rd_data_from_mem
    else:
        data_write_back = ALU["res"]    

    if(Control_Sig["RegWrite"]):                 #write data back into register memory
        write_into_reg(data_write_back)
#WriteBack ends

def Create_Instr_set():
    global num_lines, strt_add
    strt_add = pc
    in_file=open("sorting_bin.txt","r")          #file with machine code is opened
    instr_list = in_file.readlines()             #instr_list contains each line of the machine code
    num_lines = len(instr_list)
    for line in instr_list:
        instr_mem[strt_add] = line.rstrip('\n')  #strips down hex charater and stores at appropriate PC location
        strt_add+=4                              #instr_mem used to fetc instruction in IF stage

def main(): #main
    Create_Instr_set()
    print("Data Memory is:")                         #data memory is displayed before instructions are executed
    print(data_mem)
    print("Register Memory is:")                     
    for key in regmem.keys():                        #register memory is displayed before instructions are executed
        print(f'{regmem_name[key]} : {regmem[key]}')    
    while(True):
        if(pc not in instr_mem.keys()):              #programme ends after PC exceeds all the instructions
            break
        IF()                                         #all phases are called and executed in order
        ID()
        EX()
        MEM()
        WB()
        print(f'Running inst at address : {pc} and clockcyle count: {cycle_count}')
        print("IF ID EX MEM WB")
    print(f'Time taken by processor assuming each clock cycle is 950ps is {cycle_count*950/1000: .2f} ns')    
    print("Data Memory is:")                        #data memoru os displayed after all instructions are executed
    print(data_mem)
    print("Register Memory is:")          
    for key in regmem.keys():                       #data memory is executed after all instructions are executed
        print(f'{regmem_name[key]} : {regmem[key]}')   

if __name__ == "__main__":
    main()