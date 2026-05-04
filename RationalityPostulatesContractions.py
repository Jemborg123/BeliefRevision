from BeliefBase import *
from inference import InferenceEngine

def Closure(B:BeliefBase,phi:Belief):
    B.contract_by_formula(phi.p)
    cnb = B.Cn()
    return BasesEqual(B,cnb)

def BasesEqual(B1:BeliefBase,B2:BeliefBase):
    left = [b.p for b in B1.base]
    right = [b.p for b in B2.base]
    for b in B1.base:
        if not InferenceEngine.entails(right, b.p): return False
    for b in B2.base:
        if not InferenceEngine.entails(left, b.p): return False
    return True

def BaseSubsetEqual(B1:BeliefBase,B2:BeliefBase):
    right = [b.p for b in B2.base]
    for b in B1.base:
        if not InferenceEngine.entails(right, b.p): return False
    return True

def Success(B:BeliefBase,phi:Belief):
    formula = phi.p
    if InferenceEngine.entails([], formula):
        return True
    B.contract_by_formula(formula)
    return not B.is_entailed(formula)

def Inclusion(B:BeliefBase,phi:Belief):
    original = list(B.base)
    B.contract_by_formula(phi.p)
    return all(b in original for b in B.base)

def Vacuity(B:BeliefBase,phi:Belief):
    if B.is_entailed(phi.p):
        return True
    original = list(B.base)
    B.contract_by_formula(phi.p)
    return B.base == original

def Extensionality(B:BeliefBase,phi:Belief,psy:Belief):
    if not InferenceEngine.entails([], phi.p.IFF(psy.p)):
        return True
    B_phi = B.copy()
    B_psy = B.copy()
    B_phi.contract_by_formula(phi.p)
    B_psy.contract_by_formula(psy.p)
    return BasesEqual(B_phi, B_psy)

def Recovery(B:BeliefBase,phi:Belief):
    B_copy = B.copy()
    B_copy.contract_by_formula(phi.p)
    B_copy.extension(phi)
    return BaseSubsetEqual(B,B_copy)

def ConjunctiveInclusion(B:BeliefBase,phi:Belief,psy:Belief):
    B_Cpp = B.copy()
    B_Cpp.contract_by_formula(p(op="AND",left=phi.p,right=psy.p))
    B_Cp = B.copy()
    B_Cp.contract_by_formula(phi.p)
    if not B_Cpp.is_entailed(phi.p):
        return BaseSubsetEqual(B_Cpp,B_Cp)
    return True
        

def ConjunctiveOverlap(B:BeliefBase,phi:Belief,psy:Belief):
    B_Cphipsy = B.copy()
    B_Cphipsy.contract_by_formula(p(op="AND",left=phi.p,right=psy.p))
    B_Cphi = B.copy()
    B_Cphi.contract_by_formula(phi.p)
    B_Cpsy = B.copy()
    B_Cpsy.contract_by_formula(psy.p)
    B_intersect = BeliefBase()
    for b in B_Cphi.base:
        if b in B_Cpsy.base:
            B_intersect.extension(b)
    return BaseSubsetEqual(B_intersect,B_Cphipsy)