# Minimal script for center-justified text
import sys
r=sys.argv[1:]
fill, txt = ( (' ',r[0]) if len(r)<2 else (r[0],r[1]) )
print(("{:"+fill+"^80}").format(' '+txt+' '))
