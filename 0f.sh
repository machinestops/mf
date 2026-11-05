#!/usr/bin/ysh


#abandoned

# 0f - machineforth stage 0, written in oil shell
# this is a simple program that is halfway between a monitor and an assembler.
# this is not yet a forth.
# syntax:
# \ - comment
# $FF - hex digit
# 'words - string literal
# :word - define callable subroutine
# %macro - define literal expansion/immediate
# %% - close macro definition

var D = {} #dict
var M = {} #macro dict
var B = "" # compiled buffer, hex string of bytes

var macroing = false
var wording = false

proc parse (; w) {
    case (w) {
        %% {
            setglobal macroing = false
        }
        :* {
            setvar w = w.trim(':')
            if (macroing) {
                write "$w: defining labels/words is not valid in macro mode"
            } else {
                setglobal D[w] = len(B) // 2
            }
        }
        %* { 
            setglobal macroing = w.trim('%')
            setglobal M[macroing] = ""
        }
        / '$'.* / {
            # we need to attempt to parse a hex number here
            #setvar w = w.trim('$')
            var hv = / %start '$' [a-f A-F 0-9]+ %end /  
        
            if (w ~ hv and ((len(w)-1) % 2) === 0) {
                if (macroing) {
                    setglobal M[macroing] = M[macroing] ++ " " ++ w
                } else {
                    setglobal B = B ++ w.trim('$')
                }
            } else {
                write "$w: not a valid hex digit"
            }
        
        }
        (else) {
            if (macroing and w not in M) {
                setglobal M[macroing] = M[macroing] ++ " " ++ w
            } else {
                if (w in M) {
                    for m in (M[w].split(" ")) {
                        parse (m)
                    }
                } elif (w in D) {
                    write "insert a call here"
                }
            }
            # if not macroing (defining)
            # lookup word
            # if macro, parse macro contents now
            # if word, insert call inst
            # else report not valid name
            # this means macros arent actually syntax checked until theyre called
        }
    }
}

read --all
for l in (_reply.split(u'\n') ) {
    if (l ~ / %start u'\\' dot * %end /) {
        true
    } else {
        for w in (l.split(/ space+ /)) {
            parse (w)
        }
    }
    
}

write -- $B
#json write (M)
#json write (D)
