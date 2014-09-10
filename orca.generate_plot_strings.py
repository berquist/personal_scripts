#!/usr/bin/env python

"""Generate an ORCA input file specifically for plotting cube files.

Usage:
  orca.generate_plot_strings.py [options] [--canon=canon_list] [--uno=uno_list]

If canon_list or uno_list consists of two numbers, all cubes in that range
(inclusive) will be generated.

Options:
  --prefix=PREFIX  Append a prefix to all generated files.
  --eldens         Generate the electron density.
  --spindens       Generate the spin density.
  --beta           Orbital file contains separate beta spins/orbitals.
  --dim=DIM        Number of points in each dimension. [default: 40]
  --cclib=OUTFILE  Use cclib to determine occupied/virtual MO ranges from output file. Generate 2*NOcc cubes.
  --max=MAX        Don't generate any cube files after MAX orbital.
  --print_args     Print the parsed argument block.

Examples:
  orca.generate_plot_strings.py --spindens --beta --uno=0,4,5,6,7 --prefix='example' --canon=1,2,10
   outputs:
%plots
 format gaussian_cube
 dim1 40
 dim2 40
 dim3 40
 spindens("example.density.spin.cube");
 mo("example.mo.1a.cube", 1, 0);
 mo("example.mo.1b.cube", 1, 1);
 mo("example.mo.2a.cube", 2, 0);
 mo("example.mo.2b.cube", 2, 1);
 mo("example.mo.10a.cube", 10, 0);
 mo("example.mo.10b.cube", 10, 1);
 uno("example.uno.0.cube", 0);
 uno("example.uno.4.cube", 4);
 uno("example.uno.5.cube", 5);
 uno("example.uno.6.cube", 6);
 uno("example.uno.7.cube", 7);
 end
"""

from docopt import docopt


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
    ''''''
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
    through the args dictionary.'''
    if args['--prefix'] is None:
        prefix = ''
    else:
        prefix = args['--prefix'] + '.'

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
        if len(data.homos) == 2:
            # Don't set spindens by default, though
            args['--beta'] = True
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

    if args['--canon']:
        args['--canon'] = arg_to_list(args['--canon'])
        for mo_num in args['--canon']:
            block_parts.append(' ' + mo_string(prefix, mo_num, 0))
            if args['--beta']:
                block_parts.append(' ' + mo_string(prefix, mo_num, 1))

    if args['--uno']:
        args['--uno'] = arg_to_list(args['--uno'])
        for uno_num in args['--uno']:
            block_parts.append(' ' + uno_string(prefix, uno_num))

    block_parts.append(' end')

    block = '\n'.join(block_parts)

    return block


if __name__ == '__main__':

    args = docopt(__doc__)

    if args['--print_args']:
        print(args)

    block = generate_block(args)

    print(block)
