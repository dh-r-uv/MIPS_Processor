
# pipelined, carry forward:
# 1)Control signals
# 2)decoded part#
# 3)register_file, updated register

class pipelined_obj:
    
    def __init__(self):
        self.Control_Sig = {"PCSrc" : 0, 
            "RegDst" : 0,
            "Jump" : 0,
            "Branch" : 0,
            "MemRead" : 0,
            "MemtoReg" : 0,
            "aluop" : '00', 
            "MemWrite" : 0,
            "ALUSrc": 0,
            "RegWrite" : 0,
            "Zero" : 0}
        self.decoded = {"op" : '',
            "rs" : '',
            "rt" : '',
            "rd" : '',
            "imm_val" : 0,
            "shamt" : '',
            "fn" : '',
            "jump_address" : 0} 
        
        
    