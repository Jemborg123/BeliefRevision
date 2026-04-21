class p:
    def __init__(self):
        pass
    
    def AND(self, q):
        return self and q
    
    def OR(self, q):
        return self or q
    
    def IMPLIES(self,q):
        return (not self) or q
    
    def IFF(self, q):
        return p == q
    
    def XOR(self, q):
        return p != q
    
    def NAND(self, q):
        return not (self.AND(q)) 
    
    def NOR(self, q):
        return not (self.OR(q))
    
    def NEG(self):
        return not self
        
    
class Belief:
    def __init__(self):
        self.prep = p
        self.entailList = []
        self.pri = 0
        self.par = None
    
    def Cn(self):
        pass
    
    
class BeliefBase:
    def __init__(self):
        self.base = []
        
    def contract(self, b:Belief):
        pass
    
    def extension(self, b:Belief):
        pass
    
    def revision(self, b:Belief):
        pass
    
    