# Task 03: Higher-Order Functions, Currying & Composition

from functools import partial

raw_events = (
    {"user": "  ADA ", "role": "data",    "spend": 200.0, "bot": False},
    {"user": "  bob ", "role": "guest",   "spend": 150.0, "bot": False},
    {"user": "  cara", "role": "systems", "spend": -10.0, "bot": False},
    {"user": "  dan ", "role": "data",    "spend": 300.0, "bot": True},
    {"user": "  eve ", "role": "systems", "spend": 400.0, "bot": False},
)

# Part A - Pipeline & Predicate Combinator Helpers:

def pipe(* fns):
    def run(x):
        for fn in fns:
            x = fn(x)
        return x
    return run

def all_of(* preds):
    return lambda x: all(p(x) for p in preds)

def any_of(* preds):
    return lambda x: any(p(x) for p in preds)

def negate(pred):
    return lambda x: not pred(x)

def none_of(* preds):
    return negate(any_of(* preds))

def col_satisfies(key: str, pred):
    return lambda row: key in row and pred(row[key])

# Part B - Composable Data Quality Validator:

is_data_or_systems = lambda n: (isinstance(n, str) and n == 'data') or (isinstance(n, str) and n == 'systems')

is_positive_spend = lambda n: isinstance(n, (int, float)) and n > 0

is_bot = lambda n: n

is_valid_event = all_of(
    col_satisfies('role', any_of(is_data_or_systems)),
    col_satisfies('spend', is_positive_spend),
    col_satisfies('bot', negate(is_bot))
)

# Part C - Point-Free Normalizer (pipe + partial):

def strip_and_lowercase(key, row):
    return {**row, key: row[key].strip().lower()}

def spend_with_tax(key, row):
    return {**row, 'spend_with_tax': round(row[key] * 1.1, 2)}

def add_verified(key, row):
    return {**row, key: True}

normalize_event = pipe(partial(strip_and_lowercase, "user"), partial(spend_with_tax, "spend"), partial(add_verified, "verified"))

# Part D - Lazy Execution & Test Assertions:

filtered_raw_events = filter(is_valid_event, raw_events)

results = tuple(map(normalize_event, filtered_raw_events))
print(results)

# 1. Test Predicate Combinators (Valid vs. Invalid records)
assert is_valid_event({"user": "ADA", "role": "data", "spend": 200.0, "bot": False}) is True
assert is_valid_event({"user": "bob", "role": "guest", "spend": 150.0, "bot": False}) is False
assert is_valid_event({"user": "dan", "role": "data", "spend": 300.0, "bot": True}) is False

# 2. Test Point-Free Normalization & Immutability
sample_event = {"user": "  ADA ", "role": "data", "spend": 200.0, "bot": False}
normalized_sample = normalize_event(sample_event)
assert normalized_sample["user"] == "ada"
assert normalized_sample["spend_with_tax"] == 220.0
assert normalized_sample["verified"] is True
assert "spend_with_tax" not in sample_event  # Proves sample_event was not mutated!

# 3. Test End-to-End Pipeline Output
assert len(results) == 2
assert results[0]["user"] == "ada" and results[0]["spend_with_tax"] == 220.0
assert results[1]["user"] == "eve" and results[1]["spend_with_tax"] == 440.0

print("All test assertions passed!")
