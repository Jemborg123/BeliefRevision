from RationalityPostulatesContractions import *
import RationalityPostulatesRevision as Rev
from BeliefBase import *
import unittest

class RationalityPostulatesTest(unittest.TestCase):

    def SetupBeliefBase(self):
        B = BeliefBase()
        prep1 = p("p")
        prep2 = p("q")
        prep3 = prep1.IFF(prep2)
        B.extension(Belief(prep1,10))
        B.extension(Belief(prep3,10))
        return B, B.Cn()
        
    def test_closure_contracting_existing_belief(self):
        B, _ = self.SetupBeliefBase()
        target = B.base[0]
        self.assertTrue(Closure(B, target))

    def test_closure_on_empty_base(self):
        B = BeliefBase()
        phi = Belief(p("p"), 10)
        self.assertTrue(Closure(B, phi))

    def test_closure_after_contracting_all(self):
        B, _ = self.SetupBeliefBase()
        for b in list(B.base):
            B.contract_by_formula(b.p)
        cnb = B.Cn()
        self.assertTrue(BasesEqual(B, cnb))

    def test_closure_three_variables(self):
        B = BeliefBase()
        B.extension(Belief(p("a"), 10))
        B.extension(Belief(p("a").IMPLIES(p("b")), 10))
        B.extension(Belief(p("b").IMPLIES(p("c")), 10))
        phi = Belief(p("c"), 10)
        self.assertTrue(Closure(B, phi))

    def test_success_contracting_q(self):
        B, _ = self.SetupBeliefBase()
        self.assertTrue(Success(B, Belief(p("q"), 10)))

    def test_success_tautology(self):
        B, _ = self.SetupBeliefBase()
        taut = p("p").OR(p("p").NOT())
        self.assertTrue(Success(B, Belief(taut, 10)))

    def test_inclusion_contracting_q(self):
        B, _ = self.SetupBeliefBase()
        self.assertTrue(Inclusion(B, Belief(p("q"), 10)))

    def test_vacuity_unrelated_formula(self):
        B, _ = self.SetupBeliefBase()
        self.assertTrue(Vacuity(B, Belief(p("r"), 10)))

    def test_extensionality_pq_vs_qp(self):
        B, _ = self.SetupBeliefBase()
        phi = Belief(p("p").AND(p("q")), 10)
        psy = Belief(p("q").AND(p("p")), 10)
        self.assertTrue(Extensionality(B, phi, psy))

    def test_recovery_contracting_q(self):
        B, _ = self.SetupBeliefBase()
        self.assertTrue(Recovery(B, Belief(p("q"), 10)))
        
    def test_recovery_contracting_p(self):
        B, _ = self.SetupBeliefBase()
        self.assertTrue(Recovery(B, Belief(p("p"), 10)))

    def test_conjunctive_inclusion_antecedent_false(self):
        B = BeliefBase()
        B.extension(Belief(p("p"), 10))
        phi = Belief(p("p"), 10)
        psy = Belief(p("q"), 10)
        self.assertTrue(ConjunctiveInclusion(B, phi, psy))
        
    def test_conjunctive_inclusion_antecedent_true(self):
        B = BeliefBase()
        B.extension(Belief(p("p"), 10))
        B.extension(Belief(p("q"), 10))
        phi = Belief(p("p"), 10)
        psy = Belief(p("q"), 10)
        self.assertTrue(ConjunctiveInclusion(B, phi, psy))
        
    def test_conjunctive_inclusion_psi_unrelated(self):
        B = BeliefBase()
        B.extension(Belief(p("p"), 10))
        B.extension(Belief(p("p").IMPLIES(p("q")), 10))
        phi = Belief(p("q"), 10)
        psy = Belief(p("r"), 10)
        self.assertTrue(ConjunctiveInclusion(B, phi, psy))
        
    def test_conjunctive_inclusion_chain(self):
        B = BeliefBase()
        B.extension(Belief(p("p"), 10))
        B.extension(Belief(p("p").IMPLIES(p("q")), 10))
        B.extension(Belief(p("p").IMPLIES(p("r")), 10))
        phi = Belief(p("q"), 10)
        psy = Belief(p("r"), 10)
        self.assertTrue(ConjunctiveInclusion(B, phi, psy))

    def test_conjunctive_overlap_empty_intersection(self):
        B = BeliefBase()
        B.extension(Belief(p("p"), 10))
        phi = Belief(p("p"), 10)
        psy = Belief(p("q"), 10)
        self.assertTrue(ConjunctiveOverlap(B, phi, psy))

    def test_conjunctive_overlap_independent_facts(self):
        B = BeliefBase()
        B.extension(Belief(p("p"), 10))
        B.extension(Belief(p("q"), 10))
        B.extension(Belief(p("r"), 10))
        phi = Belief(p("p"), 10)
        psy = Belief(p("q"), 10)
        self.assertTrue(ConjunctiveOverlap(B, phi, psy))

    def test_conjunctive_overlap_psi_unrelated(self):
        B = BeliefBase()
        B.extension(Belief(p("p"), 10))
        B.extension(Belief(p("p").IMPLIES(p("q")), 10))
        phi = Belief(p("q"), 10)
        psy = Belief(p("r"), 10)
        self.assertTrue(ConjunctiveOverlap(B, phi, psy))

    def test_conjunctive_overlap_chain(self):
        B = BeliefBase()
        B.extension(Belief(p("p"), 10))
        B.extension(Belief(p("p").IMPLIES(p("q")), 10))
        B.extension(Belief(p("p").IMPLIES(p("r")), 10))
        phi = Belief(p("q"), 10)
        psy = Belief(p("r"), 10)
        self.assertTrue(ConjunctiveOverlap(B, phi, psy))
        


    def test_revision_closure(self):
        B, _ = self.SetupBeliefBase()
        self.assertTrue(Rev.Closure(B, Belief(p("r"), 10)))

    def test_revision_success_with_unrelated(self):
        B, _ = self.SetupBeliefBase()
        self.assertTrue(Rev.Success(B, Belief(p("r"), 10)))

    def test_revision_success_contradicting_existing(self):
        B, _ = self.SetupBeliefBase()
        self.assertTrue(Rev.Success(B, Belief(p("p").NOT(), 10)))

    def test_revision_inclusion_with_unrelated(self):
        B, _ = self.SetupBeliefBase()
        self.assertTrue(Rev.Inclusion(B, Belief(p("r"), 10)))

    def test_revision_inclusion_contradicting_existing(self):
        B, _ = self.SetupBeliefBase()
        self.assertTrue(Rev.Inclusion(B, Belief(p("p").NOT(), 10)))

    def test_revision_vacuity_unrelated(self):
        B, _ = self.SetupBeliefBase()
        self.assertTrue(Rev.Vacuity(B, Belief(p("r"), 10)))

    def test_revision_consistency_contradicting_existing(self):
        B, _ = self.SetupBeliefBase()
        self.assertTrue(Rev.Consistency(B, Belief(p("p").NOT(), 10)))

    def test_revision_consistency_with_unrelated(self):
        B, _ = self.SetupBeliefBase()
        self.assertTrue(Rev.Consistency(B, Belief(p("r"), 10)))

    def test_revision_extensionality_pq_vs_qp(self):
        B, _ = self.SetupBeliefBase()
        phi = Belief(p("p").AND(p("q")), 10)
        psy = Belief(p("q").AND(p("p")), 10)
        self.assertTrue(Rev.Extensionality(B, phi, psy))
    
if __name__ == '__main__':
    unittest.main()