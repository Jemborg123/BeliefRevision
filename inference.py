from Beliefbase import p, Belief, BeliefBase

class InferenceEngine:

    def move_nots_inwards(node: p):
        if node is None or node.name:
            return node
        
        if node.op == "NOT":
            inner = node.left
            if inner.name:
                return node
            
            if inner.op == "NOT":
                return InferenceEngine.move_nots_inwards(inner.left)
            
            if inner.op == "AND":
                left_neg = InferenceEngine.move_nots_inwards(inner.left.NOT())
                right_neg = InferenceEngine.move_nots_inwards(inner.right.NOT())
                return left_neg.OR(right_neg)

            if inner.op == "OR":
                left_neg = InferenceEngine.move_nots_inwards(inner.left.NOT())
                right_neg = InferenceEngine.move_nots_inwards(inner.right.NOT())
                return left_neg.AND(right_neg) 
            
        left_child = InferenceEngine.move_nots_inwards(node.left) if node.left else None
        right_child = InferenceEngine.move_nots_inwards(node.right) if node.right else None
        return p(op=node.op, left=left_child, right=right_child)
    
    def distribute_or_over_and(node: p):
        if node is None or node.name or node.op == "NOT":
            return node
        
        if node.op == "AND":
            left_dist = InferenceEngine.distribute_or_over_and(node.left)
            right_dist = InferenceEngine.distribute_or_over_and(node.right)
            return left_dist.AND(right_dist) 
        
        if node.op == "OR":
            left = InferenceEngine.distribute_or_over_and(node.left)
            right = InferenceEngine.distribute_or_over_and(node.right)
            
            if left.op == "AND":
                dist_left = InferenceEngine.distribute_or_over_and(left.left.OR(right))
                dist_right = InferenceEngine.distribute_or_over_and(left.right.OR(right))
                return dist_left.AND(dist_right)
            
            if right.op == "AND":
                dist_left = InferenceEngine.distribute_or_over_and(left.OR(right.left))
                dist_right = InferenceEngine.distribute_or_over_and(left.OR(right.right))
                return dist_left.AND(dist_right)

            return p(op="OR", left=left, right=right)
        
        return node
    
    def to_cnf(node: p):
        step1 = InferenceEngine.move_nots_inwards(node)
        step2 = InferenceEngine.distribute_or_over_and(step1)
        return step2
    
    def extract_clauses(cnf_node: p):
        if cnf_node is None:
            return set()
        
        if cnf_node.op == "AND":
            return InferenceEngine.extract_clauses(cnf_node.left) | InferenceEngine.extract_clauses(cnf_node.right)
        
        clause = set()

        def collect_literals(node: p):
            if node.name:
                clause.add(("POS", node.name))
            elif node.op == "NOT":
                clause.add(("NEG", node.left.name))
            elif node.op == "OR":
                collect_literals(node.left)
                collect_literals(node.right)
        
        collect_literals(cnf_node)
        return {frozenset(clause)}
    
    def pl_resolve(ci: frozenset, cj: frozenset):
        '''
        Resolves two clauses and returns the resulting set of new clauses.
        '''
        resolvents = set()

        for literal in ci:
            sign, name = literal
            complement = ("NEG", name) if sign == "POS" else ("POS", name)

            if complement in cj:
                new_clause = set(ci) | set(cj)
                new_clause.remove(literal)
                new_clause.remove(complement)
                if InferenceEngine._is_tautology(new_clause):
                    continue
                resolvents.add(frozenset(new_clause))

        return resolvents

    def entails(kb_formulas: list['p'], query: 'p'):
        '''
        Returns True if KB|=query, False otherwise.
        '''
        clauses = set()

        for formula in kb_formulas:
            cnf_formula = InferenceEngine.to_cnf(formula)
            clauses |= InferenceEngine.extract_clauses(cnf_formula)

        negated_query = query.NOT()
        cnf_neg_query = InferenceEngine.to_cnf(negated_query)
        clauses |= InferenceEngine.extract_clauses(cnf_neg_query)
        clauses = {c for c in clauses if not InferenceEngine._is_tautology(c)}

        new_clauses = set()

        while True:
            clauses_list = list(clauses)
            n = len(clauses_list)

            for i in range(n):
                for j in range(i + 1, n):
                    resolvents = InferenceEngine.pl_resolve(clauses_list[i], clauses_list[j])

                    if frozenset() in resolvents:
                        return True
                    
                    new_clauses |= resolvents

            if new_clauses.issubset(clauses):
                return False
            
            clauses |= new_clauses

    def _is_tautology(clause):
        names_pos = {n for s, n in clause if s == "POS"}
        names_neg = {n for s, n in clause if s == "NEG"}
        return bool(names_pos & names_neg)