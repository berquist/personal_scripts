# Copyright (c) 2004 Robert L. Campbell
from pymol import cmd
import glob
import re

def load_sep(files,obj=''):
  """
  load_sep <files>, <object>

  loads multiple files (using filename globbing)
  into a multiple objects (e.g. from modelling or NMR).

  e.g. load_sep prot_*.pdb, prot
  """
  file_list = glob.glob(files)
  file_list.sort()
# find both directory prefixes and file type suffixes
  extension = re.compile( '(^.*[\/]|\.(pdb|ent|brk))' )

  if file_list:
    for i in range(len(file_list)):
      if ( obj == '' ):
        obj_name = extension.sub('',file_list[i])
      else:
        obj_name = "%s_%d" % (obj,i)

      cmd.load(file_list[i],obj_name)
  else:
    print "No files found for pattern %s" % files

cmd.extend('load_sep',load_sep)
