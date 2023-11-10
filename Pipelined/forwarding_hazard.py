from pipelined_reg import *



def updateforwading_sig(rs,rt):
    cntrlA, cntrlB = '00', '00' #from IDEX, no forwarding

    if(MEMWB["reg_write_data"] == rs and MEMWB["Control_Sig"]["RegWrite"]==1 and MEMWB["reg_write_data"]!='' and (EXMEM["reg_write_data"] != rs or EXMEM["Control_Sig"]['RegWrite'] == 0 or EXMEM["Control_Sig"]["MemtoReg"])):
        cntrlA = '01'   #from EXMEM, forwarding
    elif(EXMEM["reg_write_data"] == rs and EXMEM["Control_Sig"]["RegWrite"]==1 and EXMEM["reg_write_data"]!=''):
        cntrlA = '10'   #from MEMWB, forwarding


    #if(EXMEM["reg_write_data"] == rt and EXMEM["Control_Sig"]["RegWrite"] and EXMEM["reg_write_data"]!=0):
    #    cntrlB = '10'
    elif(MEMWB["reg_write_data"] == rt and MEMWB["Control_Sig"]["RegWrite"]==1 and MEMWB["reg_write_data"]!='' and (EXMEM["reg_write_data"] != rt or EXMEM["Control_Sig"]['RegWrite'] == 0)or EXMEM["Control_Sig"]["MemtoReg"]):
        cntrlB = '01'  
    if(EXMEM["reg_write_data"] == rt and EXMEM["Control_Sig"]["RegWrite"]==1 and EXMEM["reg_write_data"]!=''):
        cntrlB = '10'        

    return cntrlA, cntrlB

def forward_mul(cntrlsig, rd_data):
    if(cntrlsig == '10'):   
        rd_data = EXMEM["ALU_res"]
    elif(cntrlsig == '01'):
        if(MEMWB["Control_Sig"]["MemtoReg"]==1):
            rd_data = MEMWB["mem_rd_data"]
        else:    
            rd_data = MEMWB["ALU_res"]
    return rd_data     



#hazard

def FOWD():
    fowA, fowB = updateforwading_sig(IDEX["rs"], IDEX["rt"])
    IDEX["rd_data1"] = forward_mul(fowA, IDEX["rd_data1"])
    IDEX["rd_data2"] = forward_mul(fowB, IDEX["rd_data2"])
