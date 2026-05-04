"""
Test suite for Belief Revision Agent
Tests AGM postulates and contraction/revision operations
"""

from BeliefBase import p, Belief, BeliefBase
from inference import InferenceEngine

def test_contraction_vacuity():
    """Vacuity: If φ not entailed, contraction does nothing"""
    print("\n=== Test 1: Vacuity ===")
    A = p(name="A")
    C = p(name="C")  # C is not in the base
    bb = BeliefBase()
    bb.extension(Belief(A, priority=1.0))
    original_size = len(bb.base)
    bb.contract_by_formula(C)  # genuinely not entailed
    assert len(bb.base) == original_size, "Vacuity failed: base changed when φ not entailed"
    print("✓ Vacuity test passed")

def test_contraction_success():
    """Success: After contracting φ, φ should NOT be entailed"""
    print("\n=== Test 2: Success ===")
    
    A = p(name="A")
    B = p(name="B")
    
    bb = BeliefBase()
    bb.extension(Belief(A, priority=1.0))
    bb.extension(Belief(B, priority=2.0))
    bb.extension(Belief(A.AND(B), priority=3.0))
    
    assert bb.is_entailed(A.AND(B)), "Precondition failed: A∧B should be entailed"
    
    bb.contract_by_formula(A.AND(B))
    
    assert not bb.is_entailed(A.AND(B)), "Success failed: φ still entailed after contraction"
    print("✓ Success test passed")

def test_contraction_inclusion():
    """Inclusion: Contracted base is subset of original base"""
    print("\n=== Test 3: Inclusion ===")
    
    A = p(name="A")
    
    bb = BeliefBase()
    bb.extension(Belief(A, priority=1.0))
    
    original_beliefs = set(bb.base)
    bb.contract_by_formula(A)
    
    assert set(bb.base).issubset(original_beliefs), "Inclusion failed: new beliefs appeared"
    print("✓ Inclusion test passed")

def test_revision_consistency():
    """Consistency: Revised base should be consistent"""
    print("\n=== Test 4: Revision Consistency ===")
    
    A = p(name="A")
    B = p(name="B")
    
    bb = BeliefBase()
    bb.extension(Belief(A, priority=1.0))
    
    # Revise with ¬A should remove A and add ¬A
    bb.revision(Belief(A.NOT(), priority=2.0))
    
    # Check consistency: should not entail both A and ¬A
    assert not (bb.is_entailed(A) and bb.is_entailed(A.NOT())), "Consistency failed: base is inconsistent"
    print("✓ Consistency test passed")

def test_multiple_contractions():
    """Test contracting complex formulas"""
    print("\n=== Test 5: Multiple Contractions ===")
    
    A = p(name="A")
    B = p(name="B")
    C = p(name="C")
    
    bb = BeliefBase()
    bb.extension(Belief(A, priority=1.0))
    bb.extension(Belief(B, priority=2.0))
    bb.extension(Belief(C, priority=3.0))
    bb.extension(Belief(A.AND(B).IMPLIES(C), priority=1.5))
    
    print("Initial base:")
    bb.print_base()
    
    # Contract C
    print("\nContracting C...")
    bb.contract_by_formula(C)
    
    print("\nAfter contracting C:")
    bb.print_base()
    
    assert not bb.is_entailed(C), "C should not be entailed anymore"

def run_all_tests():
    """Run all test cases"""
    print("=" * 50)
    print("Running AGM Postulate Tests")
    print("=" * 50)
    
    try:
        test_contraction_vacuity()
        test_contraction_success()
        test_contraction_inclusion()
        test_revision_consistency()
        test_multiple_contractions()
        
        print("\n" + "=" * 50)
        print("✓ All tests passed!")
        print("=" * 50)
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
    except Exception as e:
        print(f"\n✗ Error: {e}")

if __name__ == "__main__":
    run_all_tests()