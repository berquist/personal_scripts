# Copyright (c) 2008 Robert L. Campbell
# make_pov.py                                                                                       
# Do "run make_pov.py" from within pymol and then execute the script                                
# with "make_pov('povray.inp')" to create the povray.inp file.                                      
#                                                                                                   
 
from pymol import cmd
 
def make_pov(file, meta=True):
        f1, f2 = file, file[:-4] + '.inc'
 
        (header,data) = cmd.get_povray()
        povfile = open(f1,'w')
        if meta: povfile.write(header)
        povview = cmd.get_view()
 
        povfile.write("""\n
// Uncomment the following lines if you have the pymolmacro.inc include file and want to use it.
/*
#include \"pymolmacro.inc\"
PYMOL_VIEW( %10.5f, %10.5f, %10.5f,
            %10.5f, %10.5f, %10.5f,
            %10.5f, %10.5f, %10.5f,
            %10.5f, %10.5f, %10.5f,
            %10.5f, %10.5f, %10.5f,
            %10.5f, %10.5f, %10.5f )
*/
 
""" % povview)
        povfile.write('#include "%s"\n\n' % f2)
        povfile.close()
        povfile = open(f2,'w')
        povfile.write(data)
        povfile.close()
 
cmd.extend('make_pov',make_pov)
