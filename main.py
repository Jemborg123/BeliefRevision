# main.py
from Modified_Beliefbase import p, Belief, BeliefBase
from inference import InferenceEngine

def main():
    print("=" * 50)
    print("Belief Revision Agent Demo")
    print("=" * 50)
    
    # Create propositions
    A = p(name="A")
    B = p(name="B")
    C = p(name="C")
    
    # Create belief base
    bb = BeliefBase()
    
    # Add beliefs (lower priority = more entrenched)
    print("\n1. Adding beliefs:")
    bb.extension(Belief(A, priority=1.0))
    bb.extension(Belief(A.IMPLIES(B), priority=1.0))
    bb.extension(Belief(B.IMPLIES(C), priority=2.0))
    bb.print_base()
    
    # Check entailments
    print("\n2. Checking entailments:")
    print(f"  Entails A? {bb.is_entailed(A)}")        # True
    print(f"  Entails B? {bb.is_entailed(B)}")        # True  
    print(f"  Entails C? {bb.is_entailed(C)}")        # True
    print(f"  Entails NOT B? {bb.is_entailed(B.NOT())}") # False
    
    # Contract by C
    print("\n3. Contracting by C (remove until C not entailed):")
    bb.contract_by_formula(C)
    print("\n  After contraction:")
    bb.print_base()
    print(f"  Entails C? {bb.is_entailed(C)}")
    
    # Revision example
    print("\n4. Revision example:")
    bb = BeliefBase()  # Fresh start
    bb.extension(Belief(A, priority=1.0))
    print("  Before revision:")
    bb.print_base()
    print(f"  Entails A? {bb.is_entailed(A)}")
    
    print("\n  Revising with NOT A:")
    bb.revision(Belief(A.NOT(), priority=2.0))
    print("  After revision:")
    bb.print_base()
    print(f"  Entails A? {bb.is_entailed(A)}")
    print(f"  Entails NOT A? {bb.is_entailed(A.NOT())}")

if __name__ == "__main__":
    main()