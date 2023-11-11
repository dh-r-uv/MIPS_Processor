from Registers import regmem

Register_File = {"rd_reg1": '',
                 "rd_reg2" : '', 
                 "wr_reg" : '', 
                 "wr_data" : '',    #inputs of File
                 "rd_data1" : '', 
                 "rd_data2" : ''}   #outputs of file

#updates register file in  ID stage
def update_reg_file(rs, rt):
    Register_File["rd_reg1"] = rs
    Register_File["rd_reg2"] = rt
    Register_File["rd_data1"] = regmem[rs]  #rd_data is int
    Register_File["rd_data2"] = regmem[rt]

#updates register file in WB stage    
def write_into_reg(wr_reg, wr_data):
    Register_File['wr_reg'] = wr_reg
    Register_File["wr_data"] = wr_data 
    regmem[Register_File["wr_reg"]] = Register_File["wr_data"]  