#!/usr/bin/python2.7

"""
Zombit pandemic
===============

The nefarious Professor Boolean is up to his usual tricks. This time he is
using social engineering to achieve his twisted goal of infecting all the
rabbits and turning them into zombits! Having studied rabbits at length,
he found that rabbits have a strange quirk: when placed in a group,
each rabbit nudges exactly one rabbit other than itself.
This other rabbit is chosen with uniform probability. We consider two
rabbits to have socialized if either or both of them nudged the other.
(Thus many rabbits could have nudged the same rabbit, and two rabbits may
have socialized twice.) We consider two rabbits A and B to belong
to the same rabbit warren if they have socialized, or if A has socialized
with a rabbit belonging to the same warren as B.

For example, suppose there were 7 rabbits in Professor Boolean's nefarious lab.
We denote each rabbit using a number. The nudges may be as follows:

1 nudges 2
2 nudges 1
3 nudges 7
4 nudges 5
5 nudges 1
6 nudges 5
7 nudges 3

This results in the rabbit warrens {1, 2, 4, 5, 6} and {3, 7}.

Professor Boolean realized that by infecting one rabbit, eventually it would
infect the rest of the rabbits in the same warren! Unfortunately, due to
budget constraints he can only infect one rabbit, thus infecting only the
rabbits in one warren. He ponders, what is the expected maximum number of
rabbits he could infect?

Write a function answer(n), which returns the expected maximum number of
rabbits Professor Boolean can infect given n, the number of rabbits.

n will be an integer between 2 and 50 inclusive. Give the answer as a string
representing a fraction in lowest terms, in the form "numerator/denominator".
Note that the numbers may be large.

For example, if there were 4 rabbits, he could infect
a maximum of 2 (when they pair up) or 4 (when they're all socialized),
but the expected value is 106 / 27. Therefore the answer would be "106/27".
"""

from fractions import gcd
from math import factorial

def prod(x, y): return x * y

def memoize(f):
    ''' "the fastest memoization decorator in the world" '''
    class memodict(dict):
        def __init__(self, f):      self.f = f
        def __call__(self, *args):  return self[args]
        def __missing__(self, key):
            self[key] = self.f(*key)
            return self[key]
    return memodict(f) 

@memoize      
def binom(n, k):                    
    ''' memoized Pascal's binomial formula '''
    if k > n or k < 0    :  return 0   
    if k == n or k == 0  :  return 1   
    k = min(k, n-k)      ;  return (binom(n-1, k) + binom(n-1, k-1))              
              
@memoize      
def A000435(n): 
    ''' Calculates the normalized total height of all nodes in all rooted trees 
    with n labeled nodes. Fun fact, this was the first sequence added to the 
    Online Encyclopedia of Integer Sequences! '''
    return sum([binom(n,k) * (n-k)**(n-k) * k**k for k in xrange(1, n)]) / n

def rule_asc(n):
    ''' Rule based ascending integer partition composition.
    Reference: http://arxiv.org/pdf/0909.2331.pdf '''
    a = [0 for i in xrange(n+1)]
    a[1], k = n, 1
    while k > 0:
        x, y, k = a[k-1] + 1, a[k]-1, k-1
        while x <= y: a[k], y, k = x, y-x, k+1
        a[k] = x + y
        b = a[:k+1]
        if 1 not in b: yield b

def unique(n, p):                
''' The number of unique sets of n labled items for a partition scheme p '''
    return reduce(prod, [binom(n - sum(p[:i]), p[i]) for i in xrange(len(p))]) \
            / reduce(prod, map(factorial, [p.count(e) for e in set(p)]))


def simplify_fraction(n, d):
    g = gcd(n, d)
    return n / g, d / g

def answer(n):
    numerator = sum([unique(n, p) * \
            reduce(prod, map(A000435, p)) * max(p) for p in rule_asc(n)])

    denominator = (n-1)**n
    numerator, denominator = simplify_fraction(numerator, denominator)
    return '{}/{}'.format(numerator, denominator)

def main():

    for n in xrange(2, 40):
        print answer(n), n


main()
