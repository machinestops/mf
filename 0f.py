#!/usr/bin/env python3

# 0f - machineforth stage 0, written in python
# this is a simple program that is halfway between a monitor and an assembler.
# this is not yet a forth.
# syntax:
# \ - comment
# $FF - hex digit
# :word - define callable subroutine
# %macro - define literal expansion/immediate
# %% - close macro definition
# $$ insert source location

import sys

D = {} # dictionary
M = {} # macros
B = []

def parse(w):
    if w != '$$' and w.startswith('$'):
        B.append(bytes.fromhex(w[1:]))
    elif w.startswith(':'):
        D[w[1:]] = len(B)
    elif w != '%%' and w.startswith('%'):
        M[n := w[1:]] = []
        while (w := next(I)) != '%%':
            M[n].append(w)
    else:
        if w in M:
            for n in M[w]:
                parse(n)
            
        

I = " ".join(filter(lambda x: not x.startswith("\\"), sys.stdin.readlines())).replace('\n',' ').split()
I = iter(I)
for w in I:
    parse(w)
print(M)
print(D)

open("a.out", 'wb').write(b''.join(B))
