from pipelined_reg import *



def updateforwading_sig(rs,rt):
    cntrlA, cntrlB = '00', '00' #from IDEX, no forwarding
    if(EXMEM["reg_write_data"] == rs and EXMEM["Control_Sig"]["RegWrite"] and EXMEM["reg_write_data"]!=''):
        cntrlA = '10'   #from MEMWB, forwarding
    elif(MEMWB["reg_write_data"] == rs and MEMWB["Control_Sig"]["RegWrite"] and MEMWB["reg_write_data"]!='' and (EXMEM["reg_write_data"] != rs or EXMEM["Control_Sig"]['RegWrite'] == 0)):
        cntrlA = '01'   #from EXMEM, forwarding


    if(EXMEM["reg_write_data"] == rt and EXMEM["Control_Sig"]["RegWrite"] and EXMEM["reg_write_data"]!=0):
        cntrlB = '10'
    elif(MEMWB["reg_write_data"] == rt and MEMWB["Control_Sig"]["RegWrite"] and MEMWB["reg_write_data"]!=0 and (EXMEM["reg_write_data"] != rt or EXMEM["Control_Sig"]['RegWrite'] == 0)):
        cntrlB = '01'      

    return cntrlA, cntrlB

def forward_mul(cntrlsig, rd_data):
    if(cntrlsig == '10'):   
        rd_data = EXMEM["ALU_res"]
    elif(cntrlsig == '01'):
        if(MEMWB["Control_Sig"]["MemtoReg"]):
            rd_data = MEMWB["mem_rd_data"]
        else:    
            rd_data = MEMWB["ALU_res"]
    return rd_data     



#hazard
