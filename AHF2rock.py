#!/usr/bin/env python 

import os
import idconvert as ids
from math import log10

# Some AHF halo files can have tabs (\t) and blank spaces to delimit the 
# columns. Therefore, here we replace all of them by one (1) space,
# including the header to be consistent.

def convert_AHFfile(infile, outfile): 
   fin = open(infile, "r")
   line = fin.readline()
   header = " ".join(line.split()) 
   
   # Check if outfile exists:
   if os.path.exists(outfile):
      raise NameError(outfile+" already exists!")
      exit()
   fout = open(outfile, "w")
   fout.write(header+'\n')

   # Now we convert the file line by line:
   for line in fin.readlines():
      id1, id2 = line.split()[:2] 
      rest = " ".join(line.split()[2:])
      
      id1 = str(ids.AHF2Rock(int(id1)))
      id2 = str(ids.AHF2Rock(int(id2)))

      fout.write("{:s} {:s} {:s}\n".format(id1, id2, rest))

   fin.close()
   fout.close()

def convert_AHFmergerTree(infile, outfile):
   fin = open(infile, "r")
   # Check if outfile exists:
   if os.path.exists(outfile):
      raise NameError(outfile+" already exists!")
   
   fout = open(outfile, "w")
   # We process the 3 lines of the header:
   for _ in range(3):
      line = fin.readline()
      header = " ".join(line.split()) 
      fout.write(header+'\n')
   
   # And now the halos (descendant and progenitors separately):
   for line in fin.readlines():
      if (len(line.split()) > 1):
         id1, nprog = line.split()
         id1 = str(ids.AHF2Rock(int(id1)))
         fout.write("{:s} {:s}\n".format(id1, nprog))
      else:
         if line.split()[0] != "END":
            id1 = str(ids.AHF2Rock(int(line)))
            fout.write("{:s}\n".format(id1))
         else:
            fout.write(line)
         
   fin.close()
   fout.close()

# Here we read the merger tree to find the halo with the largest ID, 
# excluding the snapshot power
def get_max_AHFid(infile):
   fin = open(infile, "r")
   for _ in range(3): fin.readline()
   maxid = 0
   for line in fin.readlines():
      if (len(line.split()) > 1):
         id1, nprog = line.split()
         num = int(int(id1) % 1e12)
         if num > maxid:
            maxid = num
      else:
         pass
   fin.close()
   print("Max ID: "+str(maxid))
   return maxid

# Now the routine to process a complete directory with AHF files
def convert_AHFdir(inpath, outpath):
   
   files = os.listdir(inpath)
   files.sort()
   # get the maxID and calculate the new power:
   for f in files:
      if "MergerTree" == f[:10]:
         print("Searching for MaxID in "+inpath+"/"+f)
         maxid = get_max_AHFid(inpath+"/"+f)
         break
   ids.NewP = 10**int(log10(maxid)+1)
   print("New snapshot power: {:g}".format(float(ids.NewP)))

   # Now process the files:
   for f in files:
      if ".AHF_halos" == f[-10:]:
         print(inpath+"/"+f+" -> "+outpath+"/"+f)
         convert_AHFfile(inpath+"/"+f, outpath+"/"+f)
      if "MergerTree" == f[:10]:
         print(inpath+"/"+f+" -> "+outpath+"/"+f)
         convert_AHFmergerTree(inpath+"/"+f, outpath+"/"+f)
   fout = open(outpath+"/NewP", "w")
   fout.write(str(ids.NewP)+"\n")
   fout.close()


if __name__ == "__main__":
   import sys
   if len(sys.argv) != 3:
      print("Usage: python AHF2rock.py <in_dir> <out_dir>")
      exit()
   
   inpath, outpath = sys.argv[1], sys.argv[2]
   # Check if out_dir exists in filesystem:
   if not os.path.isdir(outpath):
      print("ERROR: "+outpath+" does not exist!")
      exit()
   
   convert_AHFdir(inpath, outpath)
   print("Done!")

