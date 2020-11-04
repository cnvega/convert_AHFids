#!/usr/bin/env python 

import os
import idconvert as ids
from math import log10

# These are the .list files created from AHF outputs, to be processed by CT. 
def convert_Listfile(infile, outfile): 
   fin = open(infile, "r")
   
   # Check if outfile exists:
   if os.path.exists(outfile):
      raise NameError(outfile+" already exists!")
      exit()
   fout = open(outfile, "w")

   # Now we convert the file line by line:
   for line in fin.readlines():
      id1, id2 = line.split()[:2] 
      rest = " ".join(line.split()[2:])
      
      id1 = str(ids.AHF2Rock(int(id1)))
      id2 = str(ids.AHF2Rock(int(id2)))

      fout.write("{:s} {:s} {:s}\n".format(id1, id2, rest))

   fin.close()
   fout.close()

# Here we read one file to find the halo with the largest ID: 
def get_max_id(infile):
   fin = open(infile, "r")
   if ".AHF_halos" == infile[-10:]:
      fin.readline()
   maxid = 0
   for line in fin.readlines():
      id1 = line.split()[0] 
      num = int(int(id1) % 1e12)
      if num > maxid:
         maxid = num
      else:
         pass
   fin.close()
   return maxid

# Now the routine to process a complete directory with AHF files
def convert_Listdir(inpath, outpath):
   
   files = os.listdir(inpath)
   files.sort()
   # get the maxID and calculate the new power:
   maxid = 0
   for f in files:
      if ".list" == f[-5:]:
         print("Searching for MaxID in "+inpath+"/"+f)
         tmp = get_max_id(inpath+"/"+f)
         if (tmp > maxid): maxid = tmp
   ids.NewP = 10**int(log10(maxid)+1)
   print("Max ID found: {:d}".format(maxid))
   print("New snapshot power: {:g}".format(float(ids.NewP)))

   # Now process the files:
   for f in files:
      if ".list" == f[-5:]:
         print(inpath+"/"+f+" -> "+outpath+"/"+f)
         convert_Listfile(inpath+"/"+f, outpath+"/"+f)
   fout = open(outpath+"/NewP", "w")
   fout.write(str(ids.NewP)+"\n")
   fout.close()


if __name__ == "__main__":
   import sys
   if len(sys.argv) != 3:
      print("Usage: python CTinput.py <in_dir> <out_dir>")
      exit()
   
   inpath, outpath = sys.argv[1], sys.argv[2]
   # Check if out_dir exists in filesystem:
   if not os.path.isdir(outpath):
      print("ERROR: "+outpath+" does not exist!")
      exit()
   
   convert_Listdir(inpath, outpath)
   print("Done!")

