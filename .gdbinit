tui new-layout n regs 1 status 0 cmd 1
tui layout n

define ap
 set $len = sizeof($arg0)
 set $val = (unsigned long long)($arg0)
 while $len-- > 0
   set $char = $val & 0xff
   if $char >= 0x20 && $char <= 0x7e
     printf "%c", $char
   else
     printf "\\x%02x", $char
   end
   set $val >>= 8
 end
 printf "\n"
end
display/i $pc
starti
record
