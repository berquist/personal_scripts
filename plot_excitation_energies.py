#!/usr/bin/env python

from __future__ import print_function

from cclib.parser.utils import convertor


def orca_get_cis_ex_energies(inputfile):
    state_energies = []
    line = ''
    while 'STATE' not in line:
        line = next(inputfile)
    while list(set(line.strip())) != ['-']:
        if 'STATE' in line:
            state_energies.append(float(line.split()[3]))
    return state_energies


def qchem_get_cis_energies(inputfile, unrestricted=True):
    multiplicity_map = {
        'Singlet': 0.0,
        'Doublet': 0.75,
        'Triplet': 2.0,
        'Quartet': 3.75,
    }
    state_energies = []
    state_spins = []
    state_strengths = []
    line = ''
    while 'Excited state' not in line:
        line = next(inputfile)
    while list(set(line.strip())) != ['-']:
        if 'Total energy for state' in line:
            state_energies.append(float(line.split()[-1]))
        if '<S**2>' in line:
            state_spins.append(float(line.split()[-1]))
        if 'Multiplicity' in line:
            state_spins.append(multiplicity_map[line.split()[1]])
        if 'Strength' in line:
            state_strengths.append(float(line.split()[-1]))
        line = next(inputfile)
    if not unrestricted:
        while 'Excited state' not in line:
            line = next(inputfile)
        while 'Timing summary' not in line:
            if 'Total energy for state' in line:
                state_energies.append(float(line.split()[-1]))
            if 'Multiplicity' in line:
                state_spins.append(multiplicity_map[line.split()[1]])
            if 'Strength' in line:
                state_strengths.append(float(line.split()[-1]))
            line = next(inputfile)
    return state_energies


def qchem_get_cisd_energies(inputfile, energy_gs):
    state_energies = []
    line = ''
    while 'CIS(D) excitation energy' not in line:
        line = next(inputfile)
    while list(set(line.strip())) != ['-']:
        if 'CIS(D) excitation energy' in line:
            # Stupid Q-Chem!
            energy_es = energy_gs + convertor(float(line.split()[-2]), 'eV', 'hartree')
            state_energies.append(energy_es)
        line = next(inputfile)
    return state_energies


def qchem_get_ricisd_energies(inputfile):
    state_energies = []
    line = ''
    while 'Excited state' not in line:
        line = next(inputfile)
    while list(set(line.strip())) != ['-']:
        if 'Total energy for state' in line:
            state_energies.append(float(line.split()[-2]))
        line = next(inputfile)
    return state_energies


def qchem_get_eom_energies_ccman1(inputfile):
    state_energies = []
    line = ''
    while 'Excitation energies, hartree' not in line:
        line = next(inputfile)
    while 'Analysis of SCF Wavefunction' not in line:
        if 'hartree (Ex Ene' in line:
            sline = line.split()
            state_energies.append(float(sline[5][4:]))
        line = next(inputfile)
    return state_energies


def qchem_get_eom_energies_ccman2(inputfile):
    state_energies = []
    line = ''
    while 'EOMEE-CCSD transition' not in line:
        line = next(inputfile)
    while 'Analysis of SCF Wavefunction' not in line:
        if 'Total energy' in line:
            state_energies.append(float(line.split()[3]))
        line = next(inputfile)
    return state_energies


def getargs():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', nargs='+')
    parser.add_argument('--actually-plot', action='store_true', help="""Do we actually want to make plots and save them to file(s)?""")
    parser.add_argument('--correlated-gs-energy', action='store_true')
    args = parser.parse_args()
    return args


def main(args):
    import os
    import sys
    from scripts.utils import make_file_iterator
    import cclib
    import numpy as np
    if args.actually_plot:
        import matplotlib as mpl
        mpl.use('Agg')
        import matplotlib.pyplot as plt


    matches_ccman1 = (
        'DOING EOM-CCSD CALCULATIONS',
        'GENUINE CIS CODE',
        'GENUINE CISD CODE',
        'GENUINE CISDT CODE'
    )

    matches_correlated_gs_energies_cdman = (
        # Shows up in RI-CIS(D) calculations.
        'RIMP2         total energy',
        # Shows up in SOS-CIS(D) and SOS-CIS(D0) calculations.
        'Total SOS-MP2 energy',
        # Shows up in CIS(D) calculations (without RI).
        'Total ground state energy'
    )

    if args.actually_plot:
        fig, ax = plt.subplots()
        cmap = plt.cm.get_cmap('nipy_spectral')
        njobs = len(args.inputfile)
        ax.set_color_cycle([cmap(i) for i in np.linspace(0, 1, njobs)])

    for inputfilename in args.inputfile:

        # We aren't parsing the files, since they might fail; just
        # trying to determine which program they came from for now.
        job = cclib.parser.ccopen(inputfilename)
        stub = os.path.splitext(inputfilename)[0]
        inputfile = make_file_iterator(inputfilename)
        unrestricted = True

        if type(job) == cclib.parser.qchemparser.QChem:
            print('Q-Chem:', stub)
            for line in inputfile:
                # Are we using a ROHF reference?
                if ' restricted ' in line:
                    unrestricted = False
                # This is the RHF/ROHF/UHF ground state energy.
                if 'Total energy in the final basis set' in line:
                    energy_gs = float(line.split()[-1])
                # Do we want a correlated ground state energy instead?
                # (RI-MP2, MP2, CCSD, ...)
                if args.correlated_gs_energy:
                    # Runs that call cdman will match here.
                    if any(match in line for match in matches_correlated_gs_energies_cdman):
                        energy_gs = float(line.split()[-2])
                    # Runs that call ccman/ccman2 will match here.
                    if 'ccsd total energy' in line.lower():
                        energy_gs = float(line.split()[-1])
                if 'CIS Excitation Energies' in line:
                    energies_es = qchem_get_cis_energies(inputfile, unrestricted)
                if 'TDDFT/TDA Excitation Energies' in line:
                    energies_es = qchem_get_cis_energies(inputfile, unrestricted)
                if line.strip() == 'CIS(D) Excitation Energies':
                    energies_es = qchem_get_cisd_energies(inputfile, energy_gs)
                if line.strip() == 'RI-CIS(D) Excitation Energies':
                    energies_es = qchem_get_ricisd_energies(inputfile)
                if line.strip() == 'SOS-CIS(D) Excitation Energies':
                    energies_es = qchem_get_ricisd_energies(inputfile)
                if line.strip() == 'SOS-CIS(D0) Excitation Energies':
                    energies_es = qchem_get_cis_energies(inputfile, unrestricted)
                if 'Solving for EOM-CCSD' in line:
                    energies_es = qchem_get_eom_energies_ccman2(inputfile)
                if any(line.strip() == match for match in matches_ccman1):
                    energies_es = qchem_get_eom_energies_ccman1(inputfile)

        elif type(job) == cclib.parser.orcaparser.ORCA:
            print('ORCA:', stub)
            for line in inputfile:
                if 'Total Energy' in line:
                    energy_gs = float(line.split()[3])
                if 'CIS EXCITED STATES' in line:
                    energies_es = orca_get_cis_ex_energies(inputfile)
                if 'TD-DFT/TDA EXCITED STATES' in line:
                    energies_es = orca_get_cis_ex_energies(inputfile)

        elif type(job) == cclib.parser.psiparser.Psi:
            print('Psi:', stub)
            pass

        else:
            sys.exit()

        # print('Ground state energy:')
        # print(energy_gs)
        # print('Excited state energies:')
        # print(energies_es)

        try:
            if type(job) == cclib.parser.orcaparser.ORCA:
                excitation_energies = energies_es
            else:
                excitation_energies = [convertor(energy_es - energy_gs, 'hartree', 'eV')
                                       for energy_es in energies_es]

            # print('Excitation energies:')
            # print(excitation_energies)

            nstates = len(excitation_energies)
            states = range(1, nstates + 1)

            if args.actually_plot:
                ax.plot(states, excitation_energies[:nstates], label=stub, marker='o')

        except:
            print("Something's wrong!")

    if args.actually_plot:
        ax.set_xlabel('excited state #')
        if args.correlated_gs_energy:
            ax.set_ylabel(r'$E_{\mathrm{state}} - E_{\mathrm{GS}}$ (eV)')
        else:
            ax.set_ylabel(r'$E_{\mathrm{state}} - E_{\mathrm{GS}}^{\mathrm{HF}}$ (eV)')
        ax.set_xticks(states)
        # Which one do I choose? Nobody knows! I can never remember.
        ax.set_xlim(1, nstates)
        # ax.set_xbound(1, nstates)
        ax.legend(loc='best', fancybox=True, framealpha=0.50, fontsize='x-small')
        if args.correlated_gs_energy:
            fig.savefig('plot_corr.pdf', bbox_inches='tight')
        else:
            fig.savefig('plot.pdf', bbox_inches='tight')

if __name__ == '__main__':
    args = getargs()
    main(args)
