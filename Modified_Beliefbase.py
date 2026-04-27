'''
I modified the BeliefBase code because using the boolean operators and, or, not Python will evaluate them immediatly as True or False,
not keeping track of the formula. In the assignment is written that "The engine should work for propositional logic in its symbolic form",
so maybe we should evaluate the propositions only when needed.
'''

class p:
    
    def __init__(self, name: str = None, op: str = None, left: 'p' = None, right: 'p' = None):
        self.name = name # "P", "Q", etc.
        self.op = op # "AND", "OR", "NOT"
        self.left = left # lef side of the operator
        self.right = right # right side of the operator

    def AND(self, q: 'p'):
        return p(op="AND", left=self, right=q)

    def OR(self, q: 'p'):
        return p(op="OR", left=self, right=q)

    def NOT(self):
        return p(op="NOT", left=self)
    
    def IMPLIES(self, q: 'p'):
        return p(op="OR", left=self.NOT(), right=q)
    
    def IFF(self, q: 'p'):
        impl1 = self.IMPLIES(q)
        impl2 = q.IMPLIES(self)
        return impl1.AND(impl2)
    
    def XOR(self, q: 'p'):
        return self.AND(q.NOT()).OR(self.NOT().AND(q))
    
    def NAND(self, q: 'p'):
        return self.AND(q).NOT()
    
    def NOR(self, q: 'p'):
        return self.OR(q).NOT()
    
    def __str__(self):
        if self.name: return self.name
        if self.op == "NOT": return f"(NOT {self.left})"
        return f"({self.left} {self.op} {self.right})"
    
class Belief:

    def __init__(self, proposition: p, priority: float, parents: list['Belief'] = None):
        self.p = proposition
        self.entailList = []
        self.pri = priority

        if parents is None:
            self.par = []
        elif not isinstance(parents, list):
            raise ValueError("Parents should be a list of Belief objects.")
        else:
            for item in parents:
                if not isinstance(item, Belief):
                    raise ValueError("All items in parents should be Belief objects.")
                self.par = parents
        
        self.is_core = (len(self.par) == 0)

    def Cn(self):
        return self.entailList
    
    def add_entailment(self, belief: 'Belief'):
        if belief not in self.entailList:
            self.entailList.append(belief)
    
class BeliefBase:

    def __init__(self):
        self.base = []

    def contract(self, b: Belief):
        if b in self.base:
            self.base.remove(b)
        
            for parent in b.par:
                if b in parent.entailList:
                    parent.entailList.remove(b)
            
            for consequence in list(b.entailList):
                if b in consequence.par:
                    consequence.par.remove(b)

                if not consequence.is_core:
                    self.contract(consequence) 

    def extension(self, b: Belief):
        if b not in self.base:
            self.base.append(b)

    def revision(self, b: Belief):
        neg_p = b.p.NOT()

        beliefs_to_remove = [belief for belief in self.base if str(belief.p) == str(neg_p)]

        for conflict in beliefs_to_remove:
            self.contract(conflict)
        
        self.extension(b)

    def print_base(self):
        for b in self.base:
            print(f"[Priority: {b.pri}] {b.p}")

    def is_entailed(self, query: p):
        from inference import InferenceEngine

        kb_formulas = [b.p for b in self.base]

        return InferenceEngine.entails(kb_formulas, query)