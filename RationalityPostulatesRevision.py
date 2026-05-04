from BeliefBase import *
from inference import InferenceEngine
from RationalityPostulatesContractions import BasesEqual, BaseSubsetEqual

def Closure(B:BeliefBase, phi:Belief):
    B_revised = B.copy()
    B_revised.revision(phi)
    return BasesEqual(B_revised, B_revised.Cn())

def Success(B:BeliefBase, phi:Belief):
    B_revised = B.copy()
    B_revised.revision(phi)
    return B_revised.is_entailed(phi.p)

def Inclusion(B:BeliefBase, phi:Belief):
    B_revised = B.copy()
    B_revised.revision(phi)
    B_expanded = B.copy()
    B_expanded.extension(phi)
    return BaseSubsetEqual(B_revised, B_expanded)

def Vacuity(B:BeliefBase, phi:Belief):
    if B.is_entailed(phi.p.NOT()):
        return True
    B_revised = B.copy()
    B_revised.revision(phi)
    B_expanded = B.copy()
    B_expanded.extension(phi)
    return BasesEqual(B_revised, B_expanded)

def Consistency(B:BeliefBase, phi:Belief):
    if InferenceEngine.entails([], phi.p.NOT()):
        return True
    B_revised = B.copy()
    B_revised.revision(phi)
    return not (B_revised.is_entailed(phi.p) and B_revised.is_entailed(phi.p.NOT()))

def Extensionality(B:BeliefBase, phi:Belief, psy:Belief):
    if not InferenceEngine.entails([], phi.p.IFF(psy.p)):
        return True
    B_phi = B.copy()
    B_psy = B.copy()
    B_phi.revision(phi)
    B_psy.revision(psy)
    return BasesEqual(B_phi, B_psy)
