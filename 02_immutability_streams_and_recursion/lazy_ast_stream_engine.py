# Task 02: Immutability, Lazy Streams & Recursion
# Write your solution here!

raw_servers = [
    {"server": "db-prod-1",  "env": "prod", "costs": {"compute": 120, "storage": {"ssd": 40, "backup": 20}}},
    {"server": "web-dev-1",  "env": "dev",  "costs": {"compute": 30,  "storage": 10}},
    {"server": "etl-prod-1", "env": "prod", "costs": {"compute": 80,  "spark": {"driver": 30, "workers": {"w1": 50, "w2": 50}}}},
    {"server": "api-prod-1", "env": "prod", "costs": {"compute": 60,  "storage": 20}},
]

def sum_costs(node):
    if isinstance(node, int):
        return node
    return sum(sum_costs(child) for child in node.values())

def enrich_server(row):
    total_cost = sum_costs(row['costs'])
    return {**row, 'total_cost': total_cost }

prod_servers = (row for row in raw_servers if row['env'] == 'prod')

enriched_prod = (enrich_server(row) for row in prod_servers)

over_budget = (row for row in enriched_prod if row['total_cost'] >= 150)

summary = tuple((r["server"], r["total_cost"]) for r in over_budget)


# 1. Test Structural Recursion (Leaf, 1-level dict, 3-level nested dict)
assert sum_costs(50) == 50
assert sum_costs({"compute": 30, "storage": 10}) == 40
assert sum_costs({"a": 10, "b": {"c": 20, "d": {"e": 30}}}) == 60

# 2. Test Purity & Immutability (Original record is NEVER mutated in place)
sample_row = {"server": "test-1", "env": "prod", "costs": {"compute": 100}}
enriched_row = enrich_server(sample_row)
assert enriched_row["total_cost"] == 100
assert "total_cost" not in sample_row  # Proves sample_row was not mutated!

# 3. Test Lazy Pipeline Output
assert summary == (("db-prod-1", 180), ("etl-prod-1", 210))

print("All test assertions passed!")
