#!/usr/bin/env python3

import cclib
from cclib.io import ccopen
from cclib.parser.utils import convertor


program_names = {
    cclib.parser.daltonparser.DALTON: 'DALTON',
    cclib.parser.gaussianparser.Gaussian: 'Gaussian',
    cclib.parser.gamessparser.GAMESS: 'GAMESS',
    cclib.parser.nwchemparser.NWChem: 'NWChem',
    cclib.parser.orcaparser.ORCA: 'ORCA',
    cclib.parser.psiparser.Psi: 'Psi',
    cclib.parser.qchemparser.QChem: 'Q-Chem',
}


def search_file(fh, string_to_search, fieldnum):
    for line in fh:
        if string_to_search in line:
            return line.split()[fieldnum]


def get_energy_nocclib(outputfilename, string_to_search, fieldnum):
    with open(outputfilename) as fh:
        energy = search_file(fh, string_to_search, fieldnum)
    return float(energy)


def getargs():

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('outputfilename', nargs='+')

    args = parser.parse_args()

    return args


if __name__ == '__main__':

    args = getargs()

    scfenergies = []

    for outputfilename in args.outputfilename:
        if 'cfour' in outputfilename.lower():
            program = 'CFOUR'
            scfenergy = get_energy_nocclib(outputfilename, 'E(SCF)=', 1)
        else:
            job = ccopen(outputfilename)
            program = program_names[type(job)]
            data = job.parse()
            scfenergy = convertor(data.scfenergies[0], 'eV', 'hartree')
        scfenergies.append((program, outputfilename, scfenergy))

    scfenergies = sorted(scfenergies, key=lambda x: x[2])

    for (program, outputfilename, scfenergy) in scfenergies:
        print(scfenergy, program, outputfilename)
