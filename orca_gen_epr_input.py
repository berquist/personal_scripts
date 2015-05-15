#!/usr/bin/env python

"""orca_gen_epr_input.py: ..."""

from __future__ import print_function


choices_functionals = [
    # This top one will be the Hartree-Fock case.
    {'functional': 'hf', 'functional_type': 'hybrid'},
    {'functional': 'hfs', 'functional_type': 'pure'},
    {'functional': 'vwn3', 'functional_type': 'pure'},
    {'functional': 'vwn5', 'functional_type': 'pure'},
    {'functional': 'pwlda', 'functional_type': 'pure'},
    {'functional': 'bp86', 'functional_type': 'pure'},
    {'functional': 'blyp', 'functional_type': 'pure'},
    {'functional': 'olyp', 'functional_type': 'pure'},
    {'functional': 'glyp', 'functional_type': 'pure'},
    {'functional': 'xlyp', 'functional_type': 'pure'},
    {'functional': 'pw91', 'functional_type': 'pure'},
    {'functional': 'mpwpw', 'functional_type': 'pure'},
    {'functional': 'mpwlyp', 'functional_type': 'pure'},
    {'functional': 'pbe', 'functional_type': 'pure'},
    {'functional': 'rpbe', 'functional_type': 'pure'},
    {'functional': 'revpbe', 'functional_type': 'pure'},
    {'functional': 'pwp', 'functional_type': 'pure'},
    {'functional': 'b1lyp', 'functional_type': 'hybrid'},
    {'functional': 'b3lyp', 'functional_type': 'hybrid'},
    {'functional': 'o3lyp', 'functional_type': 'hybrid'},
    {'functional': 'x3lyp', 'functional_type': 'hybrid'},
    {'functional': 'b1p', 'functional_type': 'hybrid'},
    {'functional': 'b3p', 'functional_type': 'hybrid'},
    {'functional': 'b3pw', 'functional_type': 'hybrid'},
    {'functional': 'pw1pw', 'functional_type': 'hybrid'},
    {'functional': 'mpw1pw', 'functional_type': 'hybrid'},
    {'functional': 'mpw1lyp', 'functional_type': 'hybrid'},
    {'functional': 'pbe0', 'functional_type': 'hybrid'},
    {'functional': 'pw6b95', 'functional_type': 'hybrid'},
    {'functional': 'bhandhlyp', 'functional_type': 'hybrid'},
    {'functional': 'tpss', 'functional_type': 'pure'},
    {'functional': 'tpssh', 'functional_type': 'hybrid'},
    {'functional': 'tpss0', 'functional_type': 'hybrid'},
    {'functional': 'm06l', 'functional_type': 'pure'},
    {'functional': 'm06', 'functional_type': 'hybrid'},
    {'functional': 'm062x', 'functional_type': 'hybrid'},
]

# RI options.
# Column 1: on/off
# Column 2: how to handle exact exchange
# Column 3: suffix for aux basis
choices_ri = {
    'pure': (
        ('nori', '', ''),
        ('ri', '', '/j'),
    ),
    'hybrid': (
        ('nori', '', ''),
        ('ri', 'rijonx', '/j'),
        ('ri', 'rijcosx', '/j'),
        ('ri', 'rijk', '/jk'),
    )
}


def getargs():
    """Gather and return command-line arguments."""

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('xyzfilename')
    parser.add_argument('--molecule-in-file',
                        action='store_true',
                        help="""Should the molecular coordinates be inserted \
                        directly into the input file?""")
    parser.add_argument('--ptchrgfile',
                        help="""An XYZ-style file where the atomic symbols are \
                        replaced with floats representing charges.""")
    parser.add_argument('--charge',
                        type=int,
                        default=0,
                        help="""total charge""")
    parser.add_argument('--mult',
                        type=int,
                        default=2,
                        help="""spin multiplicity""")
    parser.add_argument('--basis',
                        default='def2-qzvpp',
                        help="""Name of the basis set to use (if just one).""")
    parser.add_argument('--aux-basis',
                        default='def2-qzvpp/jk',
                        help="""Name of the RI basis set to use (if just one), \
                        with the RI type inferred from the name \
                        (if necessary).""")
    parser.add_argument('--ri-handle-exx',
                        choices=('rijonx', 'rijcosx', 'rijk'),
                        default='rijk',
                        help="""For density functionals that contain exchange \
                        exchange (Hartree-Fock), how do we handle it in the RI \
                        approximation?""")
    # parser.add_argument('--basis-file')
    # parser.add_argument('--aux-basis-file')
    parser.add_argument('--functional',
                        default='pbe0',
                        help="""Name of the density functional to use \
                        (if just one).""")
    parser.add_argument('--all-functionals',
                        action='store_true',
                        help="""Make an input for every possible density \
                        functional.""")
    parser.add_argument('--all-ri-flags',
                        action='store_true',
                        help="""Make an input for every possible RI option.""")
    parser.add_argument('--no-ri',
                        action='store_true',
                        help="""By default, use RI (with RI-JK for hybrids). \
                        Setting this disables it.""")
    parser.add_argument('--dry-run',
                        action='store_true',
                        help="""Don't actually write any files. Useful for \
                        debugging purposes.""")
    parser.add_argument('--debug',
                        action='store_true',
                        help="""turn on debug-level output""")

    args = parser.parse_args()

    return args


def eprfile(**kwargs):
    """A default template for running ORCA EPR calculations, finding the
    g-tensor and copper/nitrogen hyperfine/nuclear quadrupole tensors.
    """
    return """! {hf} {functional} {basis} {aux_basis} {ri_flags} noautostart verytightscf grid5 gridx5 nofinalgrid

%pal
 nprocs 8
 end

{pointcharge_line}

* {xyzflag} {charge} {multiplicity} {xyzcontents}*

%rel
 soctype 3
 socflags 1,3,3,1
 picturechange false
 end

%eprnmr
 gtensor 1
 nuclei = all N  {{ aiso, adip, aorb, fgrad, rho }}
 nuclei = all Cu {{ aiso, adip, aorb, fgrad, rho }}
 printlevel 5
 end

""".format(**kwargs)


def make_pointcharge_line(args):
    if args.ptchrgfile:
        return '%pointcharges "{}"'.format(args.ptchrgfile)
    else:
        return ''


def determine_ri_flags(args, inpfile_params):
    for choice_functional in choices_functionals:
        if choice_functional['functional'] == inpfile_params['functional']:
            if choice_functional['functional_type'] == 'pure':
                if args.no_ri:
                    return 'nori'
                else:
                    return 'ri'
            else:
                for choice_ri in choices_ri[choice_functional['functional_type']]:
                    if choice_ri[1] == args.ri_handle_exx:
                        return ' '.join([choice_ri[0], choice_ri[1]])
    # If the density functional isn't present, assume we aren't doing
    # RI.
    else:
        return 'nori'


def determine_aux_basis(args, inpfile_params):
    """
    Order of precedence:
    1. --no-ri
    2. inpfile_params['ri_type'] is already set
    3. determine from inpfile_params['functional'], with defaults:
      pure: RI
      hybrid: RI-JK
      no functional match: no RI
    4. ... (incomplete!)

    This way, we only use the --aux-basis ending as a last resort.
    """

    ri_type_aux_basis_endings = {
        'ri': '/j',
        'rijonx': '/j',
        'rijcosx': '/j',
        'rijk': '/jk',
    }

    if args.no_ri:
        return ''
    elif inpfile_params['ri_type']:
        if inpfile_params['ri_type'] == 'nori':
            return ''
        else:
            return inpfile_params['basis'] + \
                ri_type_aux_basis_endings[inpfile_params['ri_type']]
    elif inpfile_params['functional']:
        for choice_functional in choices_functionals:
            if choice_functional['functional'] == inpfile_params['functional']:
                functional_type = choice_functional['functional_type']
        # No match? Assume no RI.
        else:
            return ''
        # pure default
        if functional_type == 'pure':
            return inpfile_params['basis'] + '/j'
        # hybrid default
        if functional_type == 'hybrid':
            return inpfile_params['basis'] + '/jk'
        # shouldn't be here...
        else:
            return ''
    else:
        # finish me!
        return ''


def main(args):
    import os.path

    # Handle parameters that will be common to all inputs, like
    # charge, spin multiplicity, XYZ coordinates...
    inpfile_default_params = dict()

    # Are we going to insert the XYZ file directly into the input, or
    # just have a reference to its name?
    if args.molecule_in_file:
        with open(args.xyzfilename) as xyzfile:
            contents = xyzfile.readlines()[2:]
        inpfile_default_params['xyzcontents'] = ''.join(['\n'] + contents)
        inpfile_default_params['xyzflag'] = 'xyz'
    else:
        inpfile_default_params['xyzcontents'] = os.path.basename(args.xyzfilename) + ' '
        inpfile_default_params['xyzflag'] = 'xyzfile'

    inpfile_default_params['charge'] = args.charge
    inpfile_default_params['multiplicity'] = args.mult
    inpfile_default_params['pointcharge_line'] = make_pointcharge_line(args)

    all_inpfile_params = []

    name = '{functional}_{basis}_{ri_type}'.format

    if args.all_functionals and args.all_ri_flags:
        for choice_functional in choices_functionals:
            functional_type = choice_functional['functional_type']
            for choice_ri in choices_ri[functional_type]:
                inpfile_params = inpfile_default_params.copy()
                inpfile_params['hf'] = 'uks'
                inpfile_params['functional'] = choice_functional['functional']
                if inpfile_params['functional'] == 'hf':
                    inpfile_params['hf'] = ''
                    inpfile_params['functional'] = 'uhf'
                inpfile_params['basis'] = args.basis.lower()
                inpfile_params['ri_flags'] = ' '.join([choice_ri[0], choice_ri[1]])
                inpfile_params['ri_type'] = inpfile_params['ri_flags'].split()[-1]
                inpfile_params['aux_basis'] = determine_aux_basis(args, inpfile_params)
                inpfile_params['name'] = name(functional=inpfile_params['functional'],
                                              basis=inpfile_params['basis'],
                                              ri_type=inpfile_params['ri_type'])
                all_inpfile_params.append(inpfile_params)
    elif args.all_functionals:
        for choice_functional in choices_functionals:
            inpfile_params = inpfile_default_params.copy()
            inpfile_params['hf'] = 'uks'
            inpfile_params['functional'] = choice_functional['functional']
            if inpfile_params['functional'] == 'uhf':
                inpfile_params['hf'] = ''
                inpfile_params['functional'] = 'uhf'
            inpfile_params['basis'] = args.basis.lower()
            inpfile_params['ri_flags'] = determine_ri_flags(args, inpfile_params)
            inpfile_params['ri_type'] = inpfile_params['ri_flags'].split()[-1]
            inpfile_params['aux_basis'] = determine_aux_basis(args, inpfile_params)
            inpfile_params['name'] = name(functional=inpfile_params['functional'],
                                          basis=inpfile_params['basis'],
                                          ri_type=inpfile_params['ri_type'])
            all_inpfile_params.append(inpfile_params)
    elif args.all_ri_flags:
        # need to handle the HF edge case
        for choice_functional in choices_functionals:
            if args.functional.lower() == choice_functional['functional']:
                functional_type = choice_functional['functional_type']
        for choice_ri in choices_ri[functional_type]:
            inpfile_params = inpfile_default_params.copy()
            inpfile_params['hf'] = 'uks'
            inpfile_params['functional'] = args.functional.lower()
            if inpfile_params['functional'] == 'hf':
                inpfile_params['hf'] = ''
                inpfile_params['functional'] = 'uhf'
            inpfile_params['basis'] = args.basis.lower()
            inpfile_params['ri_flags'] = ' '.join([choice_ri[0], choice_ri[1]])
            inpfile_params['ri_type'] = inpfile_params['ri_flags'].split()[-1]
            inpfile_params['aux_basis'] = determine_aux_basis(args, inpfile_params)
            inpfile_params['name'] = name(functional=inpfile_params['functional'],
                                          basis=inpfile_params['basis'],
                                          ri_type=inpfile_params['ri_type'])
            all_inpfile_params.append(inpfile_params)
    else:
        inpfile_params = inpfile_default_params.copy()
        inpfile_params['hf'] = 'uks'
        inpfile_params['functional'] = args.functional.lower()
        if inpfile_params['functional'] == 'hf':
            inpfile_params['hf'] = ''
            inpfile_params['functional'] = 'uhf'
        inpfile_params['basis'] = args.basis.lower()
        inpfile_params['ri_flags'] = determine_ri_flags(args, inpfile_params)
        inpfile_params['ri_type'] = inpfile_params['ri_flags'].split()[-1]
        inpfile_params['aux_basis'] = determine_aux_basis(args, inpfile_params)
        inpfile_params['name'] = name(functional=inpfile_params['functional'],
                                      basis=inpfile_params['basis'],
                                      ri_type=inpfile_params['ri_type'])
        all_inpfile_params.append(inpfile_params)

    if args.debug:
        for inpfile_params in all_inpfile_params:
            print(inpfile_params)

    if not args.dry_run:
        for inpfile_params in all_inpfile_params:
            inpfile_contents = eprfile(**inpfile_params)
            filename = '.'.join([inpfile_params['name'], 'in'])
            print(filename)
            with open(filename, 'w') as inpfile:
                inpfile.write(inpfile_contents)

    return locals()


if __name__ == "__main__":
    args = getargs()
    main_locals = main(args)
