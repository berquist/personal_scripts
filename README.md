All my scripts jumbled together. Subfolders are machine-specific.

With the `__init__.py`, the directory is a Python module, and the
functions in each Python script can be used elsewhere.

## Python Requirements

### Newish Python standard library modules:

```
argparse
```

### External modules:

```
docopt
matplotlib
numpy
pandas
```

### External quantum chemistry modules:

```
cclib
```

### Personal repositories:

```
orcaparse
```

# Plotting in VMD

Interactive/graphical:

``` bash
# in normal terminal:
vmd_pretty_cubes.py --nsurf=1
vmd <parent XYZ filename> -e vmd.load_all_plt.vmd
# in VMD terminal:
source vmd.plot_all.vmd
# shell command, in either terminal:
./vmd.convert.bash
```

Text-only with no repositioning of the scene:

``` bash
# in normal terminal:
vmd_pretty_cubes.py --nsurf=1
cat vmd.load_all_plt.vmd vmd.plot_all.vmd > vmd.do_all.vmd
echo "quit" >> vmd.do_all.vmd
vmd <parent XYZ filename> -e vmd.do_all.vmd -dispdev text
./vmd.convert.bash
```
