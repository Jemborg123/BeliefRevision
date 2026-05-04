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
            self._enforce_entrenchment(b)
            self.base.append(b)

    def _enforce_entrenchment(self, b: Belief):
        for existing in self.base:
            if self._is_conjunct_of(existing.p, b.p) and b.pri > existing.pri:
                b.pri = existing.pri
            elif self._is_conjunct_of(b.p, existing.p) and existing.pri > b.pri:
                existing.pri = b.pri
        
        self._enforce_dominance(b)

    def _enforce_dominance(self, b: Belief):
        if not b.par:
            return
        min_parent_pri = min(p.pri for p in b.par)
        if b.pri > min_parent_pri:
            b.pri = min_parent_pri

    def _is_conjunct_of(self, sub: p, conj: p) -> bool:
        if sub is None or conj is None:
            return False
        if self._formula_equal(sub, conj):
            return True
        if conj.op == "AND":
            return self._is_conjunct_of(sub, conj.left) or self._is_conjunct_of(sub, conj.right)
        return False

    def _formula_equal(self, f1: p, f2: p) -> bool:
        if f1 is None or f2 is None:
            return f1 is f2
        if f1.name and f2.name:
            return f1.name == f2.name
        if f1.op != f2.op:
            return False
        if f1.op in ("AND", "OR"):
            return (self._formula_equal(f1.left, f2.left) and self._formula_equal(f1.right, f2.right)) or \
                (self._formula_equal(f1.left, f2.right) and self._formula_equal(f1.right, f2.left))
        return self._formula_equal(f1.left, f2.left) and self._formula_equal(f1.right, f2.right)

    def revision(self, b: Belief):
        neg_p = b.p.NOT()
        self.contract_by_formula(neg_p)    
        self.extension(b)

    def print_base(self):
        for b in self.base:
            print(f"[Priority: {b.pri}] {b.p}")

    def is_entailed(self, query: p):
        from inference import InferenceEngine

        kb_formulas = [b.p for b in self.base]

        return InferenceEngine.entails(kb_formulas, query)
    
    def contract_by_formula(self, phi: p):
        """
        AGM contraction: remove enough beliefs so that phi is no longer entailed.
        Uses priority ordering (lower priority = removed first).
        """
        # Vacuity: if phi not entailed, nothing to do
        if not self.is_entailed(phi):
            return
        
        # Find all beliefs that are relevant to entailing phi
        # Strategy: collect minimal support sets for phi, then remove lowest priority ones
        
        # Step 1: Find all beliefs that are in the *justification* of phi
        supporting_beliefs = self._find_supporting_beliefs(phi)
        
        if not supporting_beliefs:
            # If phi is a tautology or unsupported, remove lowest priority beliefs one by one
            self._contract_by_removing_lowest_priority_until(phi)
            return
        
        # Step 2: Sort supporting beliefs by priority (lowest first)
        supporting_beliefs.sort(key=lambda b: b.pri)
        
        # Step 3: Remove from lowest priority until phi not entailed
        removed = []
        for belief in supporting_beliefs:
            if belief in self.base:
                self.contract(belief)  # uses your recursive dependency removal
                removed.append(belief)
                if not self.is_entailed(phi):
                    break
        
        return removed
    
    def Cn(self):
        from inference import InferenceEngine

        var_names = sorted(self._collect_variables())
        Consequence = BeliefBase()

        if not var_names:
            return Consequence

        rows = self._all_rows(len(var_names))

        for truth_pattern in self._all_rows(len(rows)):
            satisfying = [rows[i] for i, t in enumerate(truth_pattern) if t]
            formula = self._formula_from_models(var_names, satisfying)
            if formula is None:
                continue
            if InferenceEngine.entails([b.p for b in self.base], formula):
                Consequence.extension(Belief(formula, 0))

        return Consequence

    def _all_rows(self, n):
        if n == 0:
            return [()]
        result = []
        for i in range(2 ** n):
            row = tuple(bool((i >> (n - 1 - k)) & 1) for k in range(n))
            result.append(row)
        return result

    def _collect_variables(self):
        out = set()
        def walk(f):
            if f is None: return
            if f.name: out.add(f.name)
            walk(f.left); walk(f.right)
        for b in self.base:
            walk(b.p)
        return out

    def _formula_from_models(self, var_names, satisfying_rows):
        if not satisfying_rows:
            v = p(var_names[0])
            return v.AND(v.NOT())
        disjuncts = []
        for row in satisfying_rows:
            literals = []
            for name, val in zip(var_names, row):
                lit = p(name) if val else p(name).NOT()
                literals.append(lit)
            conj = literals[0]
            for lit in literals[1:]:
                conj = conj.AND(lit)
            disjuncts.append(conj)
        result = disjuncts[0]
        for d in disjuncts[1:]:
            result = result.OR(d)
        return result

    def copy(self):
        new_B = BeliefBase()
        for b in self.base:
            new_B.extension(b)
        return new_B
    
    def _find_supporting_beliefs(self, phi: p) -> list:
        """
        Find beliefs that are relevant to entailing phi.
        Simplified: any belief that appears in the resolution proof of phi.
        Returns list of Belief objects.
        """
        from inference import InferenceEngine
        
        supporting = set()
        
        # Get proof trace from entailment check
        # For now, simple approximation: all beliefs that contain variables in phi
        # Better: modify InferenceEngine to return which clauses were used
        
        phi_vars = self._extract_variables(phi)
        
        for belief in self.base:
            belief_vars = self._extract_variables(belief.p)
            if belief_vars & phi_vars:  # shares variables with phi
                supporting.add(belief)
        
        return list(supporting)
    
    def _extract_variables(self, formula: p) -> set:
        """Extract all variable names from a formula."""
        vars_set = set()
        
        def collect(f):
            if f.name:
                vars_set.add(f.name)
            if f.left:
                collect(f.left)
            if f.right:
                collect(f.right)
        
        collect(formula)
        return vars_set
    
    def _contract_by_removing_lowest_priority_until(self, phi: p):
        """
        Fallback: remove lowest priority beliefs one by one until phi not entailed.
        """
        sorted_beliefs = sorted(self.base, key=lambda b: b.pri)
        
        for belief in sorted_beliefs:
            if belief in self.base:
                self.contract(belief)
                if not self.is_entailed(phi):
                    break
    
    def contract_by_priority(self, phi: p):
        """
        Alternative contraction: remove minimal set of lowest-priority beliefs
        to eliminate entailment of phi.
        """
        if not self.is_entailed(phi):
            return []
        
        # Try removing combinations of low-priority beliefs
        sorted_beliefs = sorted(self.base, key=lambda b: b.pri)
        
        # Binary search on how many to remove
        low, high = 1, len(sorted_beliefs)
        best_removed = None
        
        while low <= high:
            mid = (low + high) // 2
            
            # Test removing first 'mid' lowest priority beliefs
            test_base = [b for b in self.base if b not in sorted_beliefs[:mid]]
            temp_base = BeliefBase()
            temp_base.base = test_base.copy()
            
            if not temp_base.is_entailed(phi):
                # Success, try fewer removals
                best_removed = sorted_beliefs[:mid]
                high = mid - 1
            else:
                # Need to remove more
                low = mid + 1
        
        # Apply the minimal removal found
        if best_removed:
            for belief in best_removed:
                if belief in self.base:
                    self.contract(belief)
        
        return best_removed or []