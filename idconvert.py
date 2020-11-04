#!/usr/bin/env python 

# Basic routines to reduce and recover the snapshot power of AHF IDs.

NewP = 1e6

def AHF2Rock(hid):
   num = int(hid % 1e12)
   snap = int((hid - num)/1e12)
   return int(snap*NewP + num)

def Rock2AHF(hid):
   num = int(hid % NewP)
   snap = int((hid - num)/NewP)
   return int(snap*1e12 + num)


