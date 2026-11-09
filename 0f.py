#!/usr/bin/env python3

# 0f - machineforth stage 0, written in python
# this is a simple program that is halfway between a monitor and an assembler.
# this is not yet a forth.
# syntax:
# \ - comment
# $FF - hex digit
# $FFFE - bytes are inserted in order. so, use LE as appropriate
# :word - define callable subroutine
# %macro - define literal expansion/immediate
# %% - close macro definition
# $$ insert source location

import sys

org = 0x400000
D = {} # dictionary
M = {} # macros
L = {} # fill in later
B = bytearray()

def parse(w, B):
    if w == '!here':
        # insert source location
        B += (org + len(B)).to_bytes(8, 'little')
    elif w == '!size':
         L[len(B)] = 'size'
         B += 0xdeadbeefdeadbeef.to_bytes(8, 'little')
    elif w.startswith('$'):
        # hex literal
        B += (bytes.fromhex(w[1:]))
        
    elif w.startswith(':'):
        # define a label/word
        D[w[1:]] = len(B)
    elif w != '%%' and w.startswith('%'):
        M[n := w[1:]] = []
        while (w := next(I)) != ';':
            M[n].append(w)
    elif w.startswith('&'):
        # take the address and fill it in later
        L[len(B)] = w[1:]
        B += 0xdeadbeefdeadbeef.to_bytes(8, 'little')
    else:
        if w in M:
            for n in M[w]:
                parse(n, B) # can't get too metaprogrammy

I = " ".join(filter(lambda x: not x.startswith("\\"), sys.stdin.readlines())).replace('\n',' ').split()
I = iter(I)
for w in I:
    parse(w,B)

for k in L:
    if L[k] == "size":
        z = len(B)
    else:
        z = org + D[L[k]]
     
    B = B[:k] + z.to_bytes(8, 'little')  + B[k+8:]
    

print(L)
print(D)
print(len(B))

open("a.out", 'wb').write(B)
