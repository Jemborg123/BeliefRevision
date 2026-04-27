# main.py
from Modified_Beliefbase import p, Belief, BeliefBase
'''
def run_tests():
    print("==================================================")
    print("   STARTING BELIEF REVISION ENGINE TESTS")
    print("==================================================\n")

    # ---------------------------------------------------------
    # TEST 1: LOGICAL ENTAILMENT (PL-RESOLUTION)
    # ---------------------------------------------------------
    print("--- TEST 1: Logical Entailment (Modus Ponens) ---")
    kb1 = BeliefBase()
    
    A = p("A")
    B = p("B")
    
    # Premise 1: A implies B (Priority 10)
    rule_ab = Belief(A.IMPLIES(B), 10.0)
    # Premise 2: A is True (Priority 20)
    fact_a = Belief(A, 20.0)
    
    kb1.extension(rule_ab)
    kb1.extension(fact_a)
    
    print("Current KB1:")
    kb1.print_base()
    
    print("\nQuery 1: Does KB1 entail B? (Expected: True)")
    print(f"Result: {kb1.is_entailed(B)}")
    
    print("Query 2: Does KB1 entail (NOT B)? (Expected: False)")
    print(f"Result: {kb1.is_entailed(B.NOT())}\n")


    # ---------------------------------------------------------
    # TEST 2: CASCADING CONTRACTION (TRUTH MAINTENANCE)
    # ---------------------------------------------------------
    print("--- TEST 2: Cascading Contraction ---")
    kb2 = BeliefBase()
    
    P = p("P")
    Q = p("Q")
    R = p("R")
    
    # Create two independent core beliefs
    belief_p = Belief(P, 50.0)
    belief_q = Belief(Q, 50.0)
    
    # Create a derived belief (R) that depends on BOTH P and Q to exist
    belief_r = Belief(R, 25.0, parents=[belief_p, belief_q])
    
    # Manually link the children to the parents (Simulating the agent's deduction process)
    belief_p.add_entailment(belief_r)
    belief_q.add_entailment(belief_r)
    
    kb2.extension(belief_p)
    kb2.extension(belief_q)
    kb2.extension(belief_r)
    
    print("Before Contraction (P, Q, and R should be here):")
    kb2.print_base()
    
    print("\nAction: Contracting 'P'...")
    kb2.contract(belief_p)
    
    print("\nAfter Contraction (P should be gone. R should ALSO be gone because it lost a parent!):")
    kb2.print_base()
    print("\n")


    # ---------------------------------------------------------
    # TEST 3: REVISION (LEVI IDENTITY)
    # ---------------------------------------------------------
    print("--- TEST 3: Belief Revision (Levi Identity) ---")
    kb3 = BeliefBase()
    
    Rain = p("Rain")
    
    # The agent strongly believes it is NOT raining
    no_rain = Belief(Rain.NOT(), 100.0)
    kb3.extension(no_rain)
    
    print("Initial Belief:")
    kb3.print_base()
    
    # The agent looks out the window and realizes it IS raining
    yes_rain = Belief(Rain, 100.0)
    
    print("\nAction: Revising base with 'Rain'...")
    kb3.revision(yes_rain)
    
    print("\nAfter Revision (NOT Rain should be deleted, Rain should be added):")
    kb3.print_base()
    
    print("\n==================================================")
    print("   ALL TESTS COMPLETED")
    print("==================================================")

if __name__ == "__main__":
    run_tests()
'''

def run_complex_tests():
    print("==================================================")
    print("   STARTING MASTER TEST SUITE - BELIEF REVISION")
    print("==================================================\n")

    # ---------------------------------------------------------
    # TEST 1: COMPLEX OPERATORS AND TAUTOLOGIES
    # ---------------------------------------------------------
    print("--- TEST 1: Complex Operators and Tautologies ---")
    kb1 = BeliefBase() # Empty base!
    
    A = p("A")
    B = p("B")
    
    # Build complex formulas
    # 1. Tautology: A OR (NOT A) -> Must ALWAYS be true, even if the base is empty
    tautology = A.OR(A.NOT())
    
    # 2. XOR: If A is true and B is false, (A XOR B) must be true.
    formula_xor = A.XOR(B)
    
    print(f"Generated Tautology formula: {tautology}")
    print(f"Generated XOR formula: {formula_xor}")
    
    print(f"\nDoes empty KB entail (A OR NOT A)? -> Expected: True")
    print(f"Result: {kb1.is_entailed(tautology)}")
    
    # Add A and (NOT B) to test XOR
    kb1.extension(Belief(A, 10))
    kb1.extension(Belief(B.NOT(), 10))
    print(f"Does KB with A and (NOT B) entail (A XOR B)? -> Expected: True")
    print(f"Result: {kb1.is_entailed(formula_xor)}\n")


    # ---------------------------------------------------------
    # TEST 2: DEEP CHAIN INFERENCE (SYLLOGISM)
    # ---------------------------------------------------------
    print("--- TEST 2: Deep Chain Inference ---")
    kb2 = BeliefBase()
    
    P1 = p("P1")
    P2 = p("P2")
    P3 = p("P3")
    P4 = p("P4")
    
    # P1 -> P2 -> P3 -> P4
    kb2.extension(Belief(P1.IMPLIES(P2), 10))
    kb2.extension(Belief(P2.IMPLIES(P3), 10))
    kb2.extension(Belief(P3.IMPLIES(P4), 10))
    
    # Base fact: P1 is true
    kb2.extension(Belief(P1, 50))
    
    print("The base contains P1 and a chain of rules up to P4.")
    print("Does KB entail P4? (The engine must make 3 logical jumps) -> Expected: True")
    print(f"Result: {kb2.is_entailed(P4)}\n")


    # ---------------------------------------------------------
    # TEST 3: MULTI-LEVEL CASCADING CONTRACTION (TMS)
    # ---------------------------------------------------------
    print("--- TEST 3: TMS and Cascading Contraction ---")
    kb3 = BeliefBase()
    
    # Core Beliefs
    b_water = Belief(p("Water"), 100)
    b_sun = Belief(p("Sun"), 100)
    b_soil = Belief(p("Soil"), 100)
    
    # Level 1: Plant (Derived from Water AND Sun)
    b_plant = Belief(p("Plant"), 50, parents=[b_water, b_sun])
    b_water.add_entailment(b_plant)
    b_sun.add_entailment(b_plant)
    
    # Level 2: Fruit (Derived from Plant AND Soil)
    b_fruit = Belief(p("Fruit"), 25, parents=[b_plant, b_soil])
    b_plant.add_entailment(b_fruit)
    b_soil.add_entailment(b_fruit)
    
    # Populate the base
    for b in [b_water, b_sun, b_soil, b_plant, b_fruit]:
        kb3.extension(b)
        
    print("Initial KB State (Everything present):")
    kb3.print_base()
    
    print("\nAction: Contracting 'Water'...")
    print("Expected: 'Water' falls -> 'Plant' falls -> 'Fruit' falls. 'Sun' and 'Soil' survive.")
    kb3.contract(b_water)
    
    print("\nKB State After Contraction:")
    kb3.print_base()
    print("\n")


    # ---------------------------------------------------------
    # TEST 4: ROBUSTNESS AND DEFENSIVE PROGRAMMING
    # ---------------------------------------------------------
    print("--- TEST 4: Error Handling (Defensive Programming) ---")
    try:
        print("Trying to create a Belief passing a string 'hello' instead of a list of parents...")
        bad_belief = Belief(p("Error"), 10, parents="hello")
        print("FAILED: The code allowed the creation! Check your validation checks.")
    except ValueError as e:
        print(f"SUCCESS: The program correctly blocked the error.")
        print(f"Caught error message: '{e}'")

    print("\n==================================================")
    print("   ALL MASTER TESTS COMPLETED")
    print("==================================================")

if __name__ == "__main__":
    run_complex_tests()