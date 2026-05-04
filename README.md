# BeliefRevision

DTU 02180 Intro to AI, SP25
Belief Revision Assignment
Due: May 4th, 2026 at 23:59

## Requirements

Python 3.8 or later. No external packages are required; the implementation
uses only the Python standard library (`unittest` for the test runner).

## Files

- `BeliefBase.py` — propositional formulas (`p`), beliefs, and the belief
  base with contraction, expansion, and revision operations
- `inference.py` — CNF conversion and resolution-based entailment
- `RationalityPostulatesContractions.py` — AGM contraction postulates
- `RationalityPostulatesRevision.py` — AGM revision postulates
- `RationalityPostulatesTest.py` — unittest suite for both postulate sets
- `test_belief_revision.py` — additional integration tests for revision
- `inference_test.py` — integration tests covering CNF conversion,
  deep entailment chains, and cascading contraction
- `main.py` — short demo showing typical usage

## Running

Demo:

    python3 main.py

Postulate test suite (28 tests):

    python3 -m unittest RationalityPostulatesTest

Integration tests:

    python3 inference_test.py
    python3 test_belief_revision.py