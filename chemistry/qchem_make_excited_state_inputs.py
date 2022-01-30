#!/usr/bin/env python

"""qchem_make_excited_state_inputs.py: For a given molecule and basis
set, generate Q-Chem inputs for most of the possible excited state
methods.
"""


import sys

# TODO: how should these be handled?
# mem_static
# mem_total
# cc_memory


def getargs():
    """Gather and return command-line arguments."""

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--dry-run", action="store_true", help="""Don't actually write any input files."""
    )
    parser.add_argument("--charge", type=int, default=0, help="""Total charge of the system.""")
    parser.add_argument("--mult", type=int, default=1, help="""Spin multiplicity of the system.""")
    parser.add_argument(
        "--basis",
        type=str,
        default="sto-3g",
        help="""Name of the basis set to use, or 'gen' for a \
                        custom basis.""",
    )
    parser.add_argument(
        "--basis-file",
        type=str,
        help="""If using a general basis ('basis = gen'), the \
                        file to read the basis set from.""",
    )
    parser.add_argument(
        "--aux-basis",
        type=str,
        help="""If performing a calculation using the RI \
                        approximation is desired, the name of the auxiliary \
                        basis for the RI expansion, or 'gen' for a custom \
                        basis.""",
    )
    parser.add_argument(
        "--aux-basis-file",
        type=str,
        help="""If using a general aux basis \
                        ('aux_basis = gen'), the file to read the aux basis \
                        set from.""",
    )
    parser.add_argument(
        "--xyzfile",
        type=str,
        help="""Path to the XYZ file containing the system's \
                        coordinates.""",
    )
    parser.add_argument(
        "--nstates", type=int, default=15, help="""Total number of excited states to compute."""
    )

    args = parser.parse_args()

    return args


def input_file(**kwargs):
    """The format of a Q-Chem input file."""
    return """$rem
{rem}
$end

$molecule
{charge} {mult}
{molecule}
$end

{basis_section}

{aux_basis_section}
""".format(
        **kwargs
    )


def key_partial_match(kp, d):
    """Find a key k in a dict d that contains a partial match kp,
    returning k.
    """
    for k in d:
        if kp in k:
            return k
    return -1


def which_ccman_string(b):
    """Is `ccman2` set to true or false? Pass a Python boolean to produce
    the proper string for the filename.
    """
    if b:
        return "ccman2"
    return "ccman1"


def method_to_name(optdict):
    """Convert the `method` to a filename. Performs mutation!

    But not all calculations use the compound `method` variable. So
    how can we name the output files? Mash together `exchange`,
    `correlation`, `eom_corr`, and whether or not we're doing
    EE/SF/something else or RI/CD.
    """

    if "method" not in optdict:
        pieces = ["eom"]

        # Handle the excitation type (EE/SF).
        eom_type = key_partial_match("states", optdict).split("_")[0]
        pieces.append(eom_type)

        # Handle the correlation type (CI/CC).
        correlation = optdict.get("correlation", "ccsd")
        eom_corr = optdict.get("eom_corr", "cisd")
        if "sdt" in eom_corr:
            if correlation == "ccsd":
                eom_corr = "cc23"
            if correlation == "ci":
                eom_corr = "cisdt"
        else:
            if correlation == "ccsd":
                eom_corr = correlation
            if correlation == "ci":
                eom_corr = eom_corr.replace("(", "_").replace(")", "")
        pieces.append(eom_corr)

        # Handle the possible two-electron integral approxmations (RI/CD).
        if "aux_basis" in optdict:
            pieces.append("ri")
        if "cholesky_tol" in optdict:
            pieces.append("cd")

        name = "-".join(pieces)

    else:
        name = optdict["method"].replace("(", "_").replace(")", "")

    # If a name is already present, it's probably for a reason, so do
    # nothing.
    if "_name" not in optdict:
        optdict["_name"] = name


def bool_to_str(b):
    if b == True:
        return "true"
    elif b == False:
        return "false"
    else:
        print("Oh no!")
        sys.exit(1)


def inpfile_params_to_rem_string(inpfile_params):
    block = []
    t = " {} = {}".format
    for k in sorted(inpfile_params.keys()):
        # Exclude 'private' keys.
        if k[0] != "_":
            v = inpfile_params[k]
            if type(v) == bool:
                v = bool_to_str(v)
            block.append(t(k, v))
    return "\n".join(block)


def dict_keys_private_to_public(d):
    for k in d:
        if k[0] == "_":
            nk = k[1:]
            d[nk] = d[k]
            del d[k]


def main(args):
    """If called from the command line, the main routine."""

    # Handle parameters that will be common to all inputs, like
    # charge, spin multiplicity, XYZ coordinates, basis sets(s)...
    inpfile_default_params = dict()

    if not args.xyzfile:
        print("Specify an XYZ file!")
        sys.exit(1)
    else:
        with open(args.xyzfile) as xyzfile:
            inpfile_default_params["_molecule"] = "".join(xyzfile.readlines()[2:])

    inpfile_default_params["_charge"] = args.charge
    inpfile_default_params["_mult"] = args.mult

    # Handle the standard basis set.
    inpfile_default_params["basis"] = args.basis
    inpfile_default_params["_basis_section"] = ""
    if args.basis == "gen":
        inpfile_default_params["purecart"] = "1111"
        blocks_basis = ["$basis"]
        with open(args.basis_file) as basis_file:
            blocks_basis.append(basis_file.read())
        blocks_basis.append("$end")
        inpfile_default_params["_basis_section"] = "\n".join(blocks_basis)

    # Can't completely handle the aux_basis here, need to wait until
    # the main loop. We can fail early, though.
    if args.aux_basis == "gen":
        if not args.aux_basis_file:
            print("Specify an aux_basis file!")
            sys.exit(1)

    STATES = args.nstates

    # Default settings shared by all calculations.
    default_settings_all = {
        "scf_convergence": 8,
        "thresh": 14,
        "scf_algorithm": "gdm",
        "scf_max_cycles": 1000,
        "symmetry": "false",
        "sym_ignore": "true",
        "chelpg": "false",
        "xc_grid": "000100000302",
    }

    # Default settings shared by drvman/cdman calculations.
    default_settings_noteom = {
        "cis_n_roots": STATES,
        "cis_convergence": 7,
    }

    # Default settings shared by ccman1/ccman2 calculations.
    default_settings_eom = {
        "ccman2": False,
        "cc_max_iter": 300,
        "cc_symmetry": "false",
        "eom_davidson_maxvectors": 120,
        "eom_davidson_max_iter": 200,
        "eom_davidson_convergence": 7,
        "eom_davidson_threshold": 10007,
        "eom_nguess_singles": STATES + 5,
        "eom_nguess_doubles": STATES + 5,
        "eom_preconv_sd": 60,
    }

    # Default settings shared by adcman calculations.
    default_settings_adc = {
        "cc_symmetry": "false",
        "state_analysis": "false",
        "adc_davidson_maxiter": 200,
        "adc_davidson_conv": 7,
        "adc_davidson_thresh": 14,
        "adc_nguess_singles": STATES + 5,
        "adc_nguess_doubles": STATES + 5,
    }

    # Input file option is [0], string for filename is [1].
    if args.mult > 1:
        choices_unrestricted = (("true", "uhf"), ("false", "rohf"))
    else:
        choices_unrestricted = ("false", "rhf")

    # Input file option is [0], string for filename is [1].
    choices_frozen_core = (("fc", "fc"), ("0", "nofc"))

    # All cdman and TDDFT methods go here.
    choices_method_noteom = [
        {
            "_needs_aux_basis": False,
            "method": "pbe",
        },
        {
            "_needs_aux_basis": False,
            "method": "pbe0",
        },
        {
            "_needs_aux_basis": False,
            "method": "cis",
        },
        {
            "_needs_aux_basis": False,
            "method": "cis(d)",
        },
        {
            "_needs_aux_basis": True,
            "method": "ricis(d)",
        },
        {
            "_needs_aux_basis": True,
            "method": "soscis(d)",
        },
        {
            "_needs_aux_basis": True,
            "method": "soscis(d0)",
        },
        {
            "_needs_aux_basis": True,
            "method": "soscis(d)",
            "sos_ufactor": 140,
            "_name": "soscis_d_factor_d0",
        },
        {
            "_needs_aux_basis": True,
            "method": "soscis(d0)",
            "sos_ufactor": 151,
            "_name": "soscis_d0_factor_d",
        },
    ]

    # All CI- or CC-based EOM methods go here.
    choices_method_eom = [
        {
            "_needs_aux_basis": False,
            "exchange": "hf",
            "sf_states": STATES,
            "correlation": "ci",
            "eom_corr": "cis",
        },
        {
            "_needs_aux_basis": False,
            "exchange": "hf",
            "sf_states": STATES,
            "correlation": "ci",
            "eom_corr": "cis(d)",
        },
        {
            "_needs_aux_basis": False,
            "exchange": "hf",
            "sf_states": STATES,
            "correlation": "ci",
            "eom_corr": "cisd",
        },
        {
            "_needs_aux_basis": False,
            "exchange": "hf",
            "sf_states": STATES,
            "correlation": "ci",
            "eom_corr": "sdt",
        },
        {
            "_needs_aux_basis": False,
            "exchange": "hf",
            "ee_states": STATES,
            "correlation": "ci",
            "eom_corr": "cis",
        },
        {
            "_needs_aux_basis": False,
            "exchange": "hf",
            "ee_states": STATES,
            "correlation": "ci",
            "eom_corr": "cis(d)",
        },
        {
            "_needs_aux_basis": False,
            "exchange": "hf",
            "ee_states": STATES,
            "correlation": "ci",
            "eom_corr": "cisd",
        },
        {
            "_needs_aux_basis": False,
            "exchange": "hf",
            "ee_states": STATES,
            "correlation": "ci",
            "eom_corr": "sdt",
        },
        {
            "_needs_aux_basis": False,
            "exchange": "hf",
            "ee_states": STATES,
            "correlation": "ccsd",
            "eom_corr": "sdt",
        },
        {
            "_needs_aux_basis": False,
            "exchange": "hf",
            "ee_states": STATES,
            "correlation": "ccsd",
            "ccman2": False,
        },
        {
            "_needs_aux_basis": False,
            "exchange": "hf",
            "ee_states": STATES,
            "correlation": "ccsd",
            "ccman2": True,
        },
        {
            "_needs_aux_basis": False,
            "exchange": "hf",
            "ee_states": STATES,
            "correlation": "ccsd",
            "ccman2": True,
            "cholesky_tol": 3,
        },
        # For now, we ignore the spin-flip variants of EOM-CCSD.
    ]

    # All ADC methods go here.
    choices_method_adc = [
        {
            "ee_states": STATES,
            "_needs_aux_basis": False,
            "method": "adc(0)",
        },
        {
            "ee_states": STATES,
            "_needs_aux_basis": False,
            "method": "adc(1)",
        },
        {
            "ee_states": STATES,
            "_needs_aux_basis": False,
            "method": "adc(2)",
        },
        {
            "ee_states": STATES,
            "_needs_aux_basis": False,
            "method": "adc(2)x",
        },
        {
            "ee_states": STATES,
            "_needs_aux_basis": False,
            "method": "sosadc(2)",
        },
        {
            "ee_states": STATES,
            "_needs_aux_basis": False,
            "method": "sosadc(2)x",
        },
        {
            "ee_states": STATES,
            "_needs_aux_basis": False,
            "method": "adc(3)",
        },
    ]

    options_jobs_cdman = []
    options_jobs_ccman = []
    options_jobs_adcman = []

    # Add default settings to specific job types.
    for c in choices_method_noteom:
        d = dict()
        d.update(default_settings_all)
        d.update(default_settings_noteom)
        d.update(c)
        options_jobs_cdman.append(d)
    for c in choices_method_eom:
        d = dict()
        d.update(default_settings_all)
        d.update(default_settings_eom)
        d.update(c)
        options_jobs_ccman.append(d)
    for c in choices_method_adc:
        d = dict()
        d.update(default_settings_all)
        d.update(default_settings_adc)
        d.update(c)
        options_jobs_adcman.append(d)

    options_jobs = options_jobs_cdman + options_jobs_ccman + options_jobs_adcman

    # A giant loop over all possible options! Oh boy!
    for choice_unrestricted in choices_unrestricted:
        do_unrestricted, unrestricted_str = choice_unrestricted
        for choice_frozen_core in choices_frozen_core:
            do_fc, fc_str = choice_frozen_core

            for options in options_jobs:
                inpfile_params = options.copy()

                inpfile_params["unrestricted"] = do_unrestricted
                inpfile_params["n_frozen_core"] = do_fc

                inpfile_params["_aux_basis_section"] = ""
                if inpfile_params["_needs_aux_basis"]:
                    inpfile_params["aux_basis"] = args.aux_basis
                    if args.aux_basis == "gen":
                        # If aux_basis = gen, how do we set purecart?
                        blocks_aux_basis = ["$aux_basis"]
                        with open(args.aux_basis_file) as aux_basis_file:
                            blocks_aux_basis.append(aux_basis_file.read())
                        blocks_aux_basis.append("$end")
                        inpfile_params["_aux_basis_section"] = "\n".join(blocks_aux_basis)

                method_to_name(inpfile_params)
                method_str = inpfile_params["_name"]

                if "ccman2" in inpfile_params:
                    name = "{}_{}_{}_{}".format(
                        method_str,
                        unrestricted_str,
                        fc_str,
                        which_ccman_string(inpfile_params["ccman2"]),
                    )
                else:
                    name = "{}_{}_{}".format(method_str, unrestricted_str, fc_str)

                inpfile_params.update(inpfile_default_params)
                inpfile_params["rem"] = inpfile_params_to_rem_string(inpfile_params)

                # Convert all 'private' keys into 'public' keys.
                dict_keys_private_to_public(inpfile_params)

                inpfile_contents = input_file(**inpfile_params)
                if not args.dry_run:
                    filename = ".".join([name, "in"])
                    print(filename)
                    with open(filename, "w") as inpfile:
                        inpfile.write(inpfile_contents)

    return locals()


if __name__ == "__main__":
    args = getargs()
    main_locals = main(args)
