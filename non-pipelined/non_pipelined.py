
import opcodes
from memory import data_mem, instr_mem
from Registers import regmem, regmem_name
from Control import Control_Sig, updatecontrolUnit
from ALU import updateAluControl, aluc, performALU   
from Register_File import Register_File, update_reg_file

#ALU Control Signals





#important variables
cycle_count=0
pc=0x00400000   #set pc

op=''
rs=''
rt=''
rd=''
imm_val = 0
shamt=''
fn=''
offset=''
jump_address=''
btarget=''

##
def bintodec(bin):  #converting binary to int
    return int(bin, 2)
##
curr_instr = ''
#Instruction Fetch

def IF():
    global curr_instr, pc, cycle_count
    cycle_count+=1
    curr_instr = instr_mem[pc]
    pc+=4

#Instruction Fetch Ends

#Instruction Decode

def ID():
    global rs, rt, rd, op, offset, fn, jump_address, shamt, imm_val
    op = curr_instr[0:6]
    updatecontrolUnit(op) #updating control signals


    rs=curr_instr[6:11] #readreg 1
    rt=curr_instr[11:16] #readreg 2
    rd=curr_instr[16:21]
    shamt=curr_instr[21:26]
    fn=curr_instr[26:32]
    imm_val=bintodec(curr_instr[16:32]) #immediate value in lw/sw and offset in beq
    jump_address="0000"+curr_instr[6:32]+"00"

    

    # if(op=='000000'):   #R format
    #     rs=curr_instr[6:11] 
    #     rt=curr_instr[11:16] 
    #     rd=curr_instr[16:21]
    #     shamt=curr_instr[21:26]
    #     fn=curr_instr[26:32]
    #     print("Decode R type")
    # elif(op == '001000' or op=='100011' or op=='101011'):   #I format
    #     rs=curr_instr[6:11]
    #     rt=curr_instr[11:16]
    #     imm_val=bintodec(curr_instr[16:32]) 
    #     print("Decode I type non-beq")
    
    # elif(op=='000100'):   #I format beq instr
    #     rs=curr_instr[6:11]
    #     rt=curr_instr[11:16]
    #     imm_val=bintodec(curr_instr[16:32]) #this is offset
    #     print("Decode I type non-beq")

    # elif(op == '000010'):   #J format
    #     jump_address="0000"+curr_instr[6:32]+"00"
    #     print("Decode J type")

    wr_reg = rd if (Control_Sig["RegDst"]>0) else rt
    #now to update register File
    update_reg_file(rs, rt, wr_reg)

#Instruction Decode ends       

#Instruction Execute
#note : aluc is the 3 bit alucontrol sig


def EX():
    updateAluControl(fn, Control_Sig["aluop"]) #updating alucontrol signals
    ##performing ALU here
    in1 = Register_File["rd_data1"]
    in2 = imm_val if (Control_Sig["ALUSrc"]>0) else Register_File["rd_data2"]

    performALU(in1, in2)    #performing ALU operations

#Instruction Execute ends
#Memory Access
#WriteBack


def main(): #main
    pass

if __name__ == "__main__":
    main()