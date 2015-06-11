from __future__ import print_function

import collections
import itertools

from copy import deepcopy


# Basic scalar relativistic method
flags_rel_method = ('dkh', 'zora', 'iora', 'ioramm', 'zora_ri', 'iora_ri', 'ioramm_ri', 'nesc')
# Choice of the model potential for ALL methods
# Only use the ZORA/IORA and DKH defaults here.
flags_rel_modelpot = ('1,1,1,1', '1,0,0,0')
# This variable determines the type of fitted atomic density that
# enters the model potential
flags_rel_modeldens = ('rhodkh', 'rhozora', 'rhohf')
# Order of DKH treatment
flags_rel_order = ('1', '2')
# Use point charges or gaussians to represent nuclei?
# Only implemented for DKH (not ZORA) (or so it says).
flags_rel_finitenuc = ('false', 'true')
# Picture change for properties. Default is false.
flags_rel_picturechange = ('false', '1', 'true')
# Include the magnetic field in the free-particle Foldy-Wouthuysen
# transformation of the DKH Hamiltonian? Default is true.
flags_rel_fpfwtrafo = ('true', 'false')

default_settings_dkh = {
    '_name': 'dkh',
    'rel': {
        'method': 'dkh',
        'modelpot': '1,0,0,0',
        'modeldens': 'rhodkh',
        'order': '2',
    },
}

default_settings_zora = {
    '_name': 'zora',
    'rel': {
        'method': 'zora',
        'modelpot': '1,1,1,1',
        'modeldens': 'rhozora',
    },
}

default_settings_soc = {
    '_name': 'none',
    'rel': {
        'soctype': '3',
        'socflags': '1,2,3,0',
    },
}

flags_rel_soctype = ('1', '3', '4')

options_socflags = list(itertools.product(
    range(1+1),
    range(4+1),
    range(4+1),
    range(1+1)
))

flags_rel_socflags_curated = (
    '1,1,3,0',
    '1,2,3,0',
    '1,2,3,1',
    '1,3,3,0',
    '1,3,3,1',
    '1,4,4,0',
    '1,4,4,1',
)

flags_simple_decontract = ('decontract', 'nodecontract')

default_settings_all = deepcopy(default_settings_soc)


def update(d, u):
    """Update a dictionary d by recursively traversing dictionary u."""
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            r = update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


def add_flags_to_list_of_dicts(block_title, option, flags, list_of_dicts):
    new_list_of_dicts = []
    for flag in flags:
        for d in list_of_dicts:
            nd = deepcopy(d)
            if block_title not in nd:
                nd[block_title] = dict()
            nd[block_title][option] = flag
            new_list_of_dicts.append(nd)
    return new_list_of_dicts


def make_comma_sep_flags(l):
    """Given a list of numbers or strings, turn them into a
    comma-separated string suitable for use as an ORCA option
    argument.
    """
    return ','.join(map(str, l))


def make_block(block_name, d):
    """Form an ORCA input block given the block's name/header and a
    dictionary where the key-value pairs will become the options and their
    settings.
    """

    block = []

    block.append('%{}'.format(block_name))

    for (k, v) in d.items():
        block.append(' {} {}'.format(k, v))

    block.append(' end')

    return '\n'.join(block)


def make_basis_block(method):
    return """%basis
 basis qzv_{method}
 end""".format(method=method)


def inpfile(**kwargs):
    # First, convert all possible option dictionaries into ORCA option
    # blocks.
    c = dict()
    for k in kwargs:
        if k[0:6] == 'block_':
            c[k] = kwargs[k]
        else:
            if isinstance(kwargs[k], dict):
                c['block_{}'.format(k)] = make_block(k, kwargs[k])
    return """! uks pbe0 def2-qzvpp nori verytightscf noautostart grid7 nofinalgrid printbasis kdiis {block_simple}

%scf
 maxiter 1000
 end

%method
 specialgridatoms 29;
 specialgridintacc 10;
 end

{block_basis}

{block_rel}

* xyz +2 2
Cu 0.000000 0.000000 0.000000
*

%eprnmr
 ori centerofelcharge
 gtensor 1
 nuclei = all Cu {{ aiso, adip, aorb, fgrad, rho }}
 printlevel 4
 end
""".format(**c)


def getargs():
    """Gather and return command-line arguments."""

    import argparse

    parser = argparse.ArgumentParser()

    ### The reason these arguments don't have defaults is because we
    ### want setting them to take precedence over all other options.

    parser.add_argument('--rel-soctype', choices=flags_rel_soctype)
    parser.add_argument('--rel-socflags')

    parser.add_argument('--rel-method', choices=flags_rel_method)
    parser.add_argument('--rel-modelpot', choices=flags_rel_modelpot)
    parser.add_argument('--rel-modeldens', choices=flags_rel_modeldens)
    parser.add_argument('--rel-dkh-order', choices=flags_rel_order)
    parser.add_argument('--rel-finitenuc', choices=flags_rel_finitenuc)
    parser.add_argument('--rel-picturechange', choices=flags_rel_picturechange)
    parser.add_argument('--rel-dkh-fpfwtrafo', choices=flags_rel_fpfwtrafo)

    ### Flags for performing 'all' options of certain flags.

    # Every option, even if some of them are nonsense.
    parser.add_argument('--all', action='store_true')

    # All options relevant for DKH calculations.
    parser.add_argument('--all-dkh', action='store_true')
    # Does nothing for now.
    parser.add_argument('--all-zora', action='store_true')

    parser.add_argument('--all-rel-method', action='store_true')
    parser.add_argument('--all-rel-modelpot', action='store_true')
    parser.add_argument('--all-rel-modeldens', action='store_true')
    parser.add_argument('--all-rel-dkh-order', action='store_true')
    parser.add_argument('--all-rel-finitenuc', action='store_true')
    parser.add_argument('--all-rel-picturechange', action='store_true')
    parser.add_argument('--all-rel-dkh-fpfwtrafo', action='store_true')
    parser.add_argument('--all-rel-socflags', action='store_true')
    parser.add_argument('--all-rel-socflags-curated', action='store_true')

    parser.add_argument('--dry-run',
                        action='store_true',
                        help="""Don't actually write any files. Useful for \
                        debugging purposes.""")
    parser.add_argument('--debug',
                        action='store_true',
                        help="""turn on debug-level output""")

    args = parser.parse_args()

    return args


def main(args):

    reldicts = [dict()]

    reldicts[0]['rel'] = dict()
    if args.all_dkh:
        reldicts[0]['rel']['method'] = 'dkh'
        args.all_zora = False
    if args.all_zora:
        reldicts[0]['rel']['method'] = 'zora'
        args.all_dkh = False

    if args.all_rel_method or args.all:
        reldicts = add_flags_to_list_of_dicts('rel',
                                              'method',
                                              flags_rel_method,
                                              reldicts)
    if args.all_rel_modelpot or args.all:
        reldicts = add_flags_to_list_of_dicts('rel',
                                              'modelpot',
                                              flags_rel_modelpot,
                                              reldicts)
    if args.all_rel_modeldens or args.all:
        reldicts = add_flags_to_list_of_dicts('rel',
                                              'modeldens',
                                              flags_rel_modeldens,
                                              reldicts)
    if args.all_rel_dkh_order or args.all or args.all_dkh:
        reldicts = add_flags_to_list_of_dicts('rel',
                                              'order',
                                              flags_rel_order,
                                              reldicts)
    if args.all_rel_finitenuc or args.all or args.all_dkh:
        reldicts = add_flags_to_list_of_dicts('rel',
                                              'finitenuc',
                                              flags_rel_finitenuc,
                                              reldicts)
    if args.all_rel_picturechange or args.all:
        reldicts = add_flags_to_list_of_dicts('rel',
                                              'picturechange',
                                              flags_rel_picturechange,
                                              reldicts)
    if args.all_rel_dkh_fpfwtrafo or args.all or args.all_dkh:
        reldicts = add_flags_to_list_of_dicts('rel',
                                              'fpfwtrafo',
                                              flags_rel_fpfwtrafo,
                                              reldicts)

    # Here's some tricky business.
    # Only make *all* socflags if explicitly asked, since this will
    # otherwise create a bazillion options.
    if args.all_rel_socflags_curated or args.all:
        comma_sep_flags = flags_rel_socflags_curated
        reldicts = add_flags_to_list_of_dicts('rel',
                                              'socflags',
                                              comma_sep_flags,
                                              reldicts)
    elif args.all_rel_socflags:
        comma_sep_flags = [make_comma_sep_flags(flags)
                           for flags in options_socflags]
        reldicts = add_flags_to_list_of_dicts('rel',
                                              'socflags',
                                              comma_sep_flags,
                                              reldicts)
    else:
        pass


    if args.debug:
        print('### reldicts begin')
        for reldict in reldicts:
            print(reldict)
        print(len(reldicts))
        print('### reldicts end')

    choices_method_dkh = [
        dict(),
    ]
    choices_method_zora = [
        dict(),
    ]
    # choices_method_iora = []

    options_jobs_reldicts = []
    options_jobs_dkh = []
    options_jobs_zora = []
    # options_jobs_iora = []

    # Add default settings to specific job types.
    # For each update, slowly become more specific.
    for c in reldicts:
        d = dict()
        d = update(d, default_settings_all)
        # No intermediate update for this batch.
        d = update(d, c)
        options_jobs_reldicts.append(d)
    for c in choices_method_dkh:
        d = dict()
        d = update(d, default_settings_all)
        d = update(d, default_settings_dkh)
        d = update(d, c)
        options_jobs_dkh.append(d)
    for c in choices_method_zora:
        d = dict()
        d = update(d, default_settings_all)
        d = update(d, default_settings_zora)
        d = update(d, c)
        options_jobs_zora.append(d)

    options_jobs = options_jobs_dkh + options_jobs_zora + options_jobs_reldicts
    all_inpfile_params = options_jobs

    if args.debug:
        for inpfile_params in all_inpfile_params:
            print(inpfile_params)

    for inpfile_params in all_inpfile_params:
        inpfile_params['block_basis'] = ''
        inpfile_params['block_simple'] = ''
        inpfile_contents = inpfile(**inpfile_params)
        if '_name' in inpfile_params:
            filename = '.'.join([inpfile_params['_name'], 'in'])
        else:
            name = []
            for (k, v) in inpfile_params['rel'].items():
                name.append('{}_{}'.format(k, v.replace(',', '')))
            filename = '.'.join(['_'.join(name), 'in'])
        print(filename)
        if not args.dry_run:
            # with open(filename, 'w') as inpfile:
            #     inpfile.write(inpfile_contents)
            print(inpfile_contents)

if __name__ == '__main__':
    args = getargs()
    main_locals = main(args)
