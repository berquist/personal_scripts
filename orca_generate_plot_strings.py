#!/usr/bin/env python

'''Generate an ORCA input file specifically for plotting cube files.

Usage:
  orca_generate_plot_strings.py [options] [--canon=canon_list] [--uno=uno_list]

If canon_list or uno_list consists of two numbers, all cubes in that range
(inclusive) will be generated. [NOT IMPLEMENTED YET]

Options:
  --prefix=PREFIX  Append a prefix to all generated files.
  --eldens         Generate the electron density.
  --spindens       Generate the spin density.
  --beta           Orbital file contains separate beta spins/orbitals.
  --dim=DIM        Number of points in each dimension. [default: 40]
  --cclib=OUTFILE  Use cclib to determine occupied/virtual MO ranges from output file. Generate 2*NOcc cubes.
  --max=MAX        Don't generate any cube files after MAX orbital. Takes highest precedence.
  --print_args     Print the parsed argument block.

Examples:
  orca_generate_plot_strings.py --spindens --beta --uno=0,4,5,6,7 --prefix='example' --canon=1,2,10
   outputs:
%plots
 format gaussian_cube
 dim1 40
 dim2 40
 dim3 40
 spindens("example.density.spin.cube");
 uno("example.uno.0.cube", 0);
 uno("example.uno.4.cube", 4);
 uno("example.uno.5.cube", 5);
 uno("example.uno.6.cube", 6);
 uno("example.uno.7.cube", 7);
 mo("example.mo.01a.cube", 1, 0);
 mo("example.mo.01b.cube", 1, 1);
 mo("example.mo.02a.cube", 2, 0);
 mo("example.mo.02b.cube", 2, 1);
 mo("example.mo.10a.cube", 10, 0);
 mo("example.mo.10b.cube", 10, 1);
 end
'''

from __future__ import print_function

from vmd_templates import *


def mo_string(prefix, mo_num, op_num):
    '''Create the string for generating a cube of a molecular orbital.'''
    if op_num == 0:
        spin = 'a'
    elif op_num == 1:
        spin = 'b'
    else:
        return
    # pylint: disable=C0301
    return 'mo("{prefix}mo.{mo_num}{spin}.cube", {mo_num}, {op_num});'.format(prefix=prefix,
                                                                              mo_num=mo_num,
                                                                              op_num=op_num,
                                                                              spin=spin)


def uno_string(prefix, uno_num):
    '''Create the string for generating a cube of a UHF natural orbital.'''
    return 'uno("{prefix}uno.{uno_num}.cube", {uno_num});'.format(prefix=prefix,
                                                                  uno_num=uno_num)


def eldens_string(prefix):
    '''Create the string for generating a cube of the electron density.'''
    return 'eldens("{prefix}density.el.cube");'.format(prefix=prefix)


def spindens_string(prefix):
    '''Create the string for generating a cube of the spin density.'''
    return 'spindens("{prefix}density.spin.cube");'.format(prefix=prefix)

def arg_to_list(arg):
    '''Convert the given argument to a list of a single element if it's an atom,
    '''
    if isinstance(arg, str):
        newarg = eval(arg)
        if isinstance(newarg, int):
            newarg = [newarg]
        return newarg
    elif isinstance(arg, list):
        return arg
    else:
        # we might be trouble if this ever gets reached...
        return list(arg)

def generate_block(args):
    '''Create the %plots block based upon command-line arguments passed in
    through the args dictionary.
    '''
    # Handle the file prefix first.
    if args['--prefix'] is None:
        prefix = ''
    else:
        prefix = args['--prefix'] + '.'

    # The "block" will be formed by generating bunch of strings,
    # appending them to this list, then calling list.join once
    # everything's done.
    block_parts = ['%plots']

    block_parts.append(' format gaussian_cube')
    block_parts.append(' dim1 {}'.format(args['--dim']))
    block_parts.append(' dim2 {}'.format(args['--dim']))
    block_parts.append(' dim3 {}'.format(args['--dim']))

    # If we desire to use cclib and automate some things...
    if args['--cclib']:
        from cclib.parser import ccopen
        job = ccopen(args['--cclib'])
        data = job.parse()
        plot_range = data.homos[0] * 2
        # cclib-discovered values take precedence
        if args['--canon']:
            args['--canon'] = list(range(plot_range))
        if args['--uno']:
            args['--uno'] = list(range(plot_range))

    if args['--eldens']:
        block_parts.append(' ' + eldens_string(prefix))
    if args['--spindens'] and args['--beta']:
        block_parts.append(' ' + spindens_string(prefix))

    # Limit the number of orbitals we're going to generate.
    if args['--max']:
        maxorb = int(args['--max'])
        if args['--canon']:
            args['--canon'] = [i for i in args['--canon'] if i <= maxorb]
        if args['--uno']:
            args['--uno'] = [i for i in args['--uno'] if i <= maxorb]

    # Plot the UNOs first due to an 'operator' bug in ORCA.
    if args['--uno']:
        args['--uno'] = pad_left_zeros_l(arg_to_list(args['--uno']))
        for uno_num in args['--uno']:
            block_parts.append(' ' + uno_string(prefix, uno_num))

    if args['--canon']:
        args['--canon'] = pad_left_zeros_l(arg_to_list(args['--canon']))
        for mo_num in args['--canon']:
            block_parts.append(' ' + mo_string(prefix, mo_num, 0))
            if args['--beta']:
                block_parts.append(' ' + mo_string(prefix, mo_num, 1))

    block_parts.append(' end')

    block = '\n'.join(block_parts)

    return block


if __name__ == '__main__':

    from docopt import docopt

    args = docopt(__doc__)

    if args['--print_args']:
        print(args)

    block = generate_block(args)

    print(block)
