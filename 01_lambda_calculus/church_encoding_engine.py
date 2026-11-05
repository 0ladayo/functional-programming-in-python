# Task 01: Lambda Calculus
# Write your solution here!
# Part A - Church Booleans & Access Control Gate:

TRUE = lambda p: lambda q: p
FALSE = lambda p: lambda q: q
NOT = lambda p: p(FALSE)(TRUE)
AND = lambda p: lambda q: p(q)(p)
OR = lambda p: lambda q: p(p)(q)
to_bool = lambda p: p(True)(False)

CAN_ACCESS = lambda is_admin: lambda is_active: lambda is_banned: AND(OR(is_admin)(is_active)) (NOT(is_banned))

print(to_bool(CAN_ACCESS(FALSE)(TRUE)(FALSE)))
print(to_bool(CAN_ACCESS(FALSE)(FALSE)(FALSE)))

# Part B - Curried Price Pipeline & Church Numerals:

ZERO = lambda f: lambda x: x
SUCC = lambda n: lambda f: lambda x: f(n(f)(x))
ADD  = lambda m: lambda n: lambda f: lambda x: m(f)(n(f)(x))
MULT = lambda m: lambda n: lambda f: m(n(f))
to_int = lambda n: n(lambda k: k + 1)(0)


ONE = SUCC(ZERO)
TWO = SUCC(ONE)
THREE = SUCC(TWO)
FOUR = SUCC(THREE)

print(to_int(MULT(ADD(THREE)(ONE))(TWO)))

final_bill = lambda tax_rate: lambda shipping: lambda subtotal: ADD(MULT(subtotal)(ADD(ONE)(tax_rate)))(shipping)

us_checkout = final_bill(ONE)(TWO)

print(to_int(us_checkout(THREE)))
