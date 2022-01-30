#!/usr/bin/env python

"""fix_molden.py

Some programs produce non-standard input files for Molden. The
sections might not be in order, the section headers might be
incorrect, partially correct, or unnecessary, the units might be off,
or maybe worse.

Molden itself can read these 'malformed' inputs, and save a new
'cleaned' file in the Molden input format that can be read by Jmol,
Avogadro, or VMD. Ideally, one would just call Molden from the command
line to generate this file, but it doesn't seem that Molden is
scriptable in this way. In addition, that brings in Molden as a
dependency. Open Babel can read/write Molden inputs, but its output is
severly truncated (no MOs!).

Attempt to fix these malformed inputs, knowing what possible section
headers/keys are and what the 'official' Molden output looks like.
"""



bfs = ('[5D]', '[5D10F]', '[7F]', '[5D7F]', '[9G]')
section_headers_no_newline = bfs + tuple('[Molden Format]')


def make_file_iterator(filename):
    """Return an iterator over the contents of the given file name."""
    # pylint: disable=C0103
    with open(filename) as f:
        contents = f.read()
    return iter(contents.splitlines())


def getargs():

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('moldeninputfilename')

    args = parser.parse_args()

    return args


def get_molden_file_sections(moldeninputfile):
    """Parse the given Molden file (iterator) for sections, which are
    specified by [SECTIONNAME].
    """

    sections_to_ignore = (
        '[Molden Format]',
        '[End of Molden output from Dalton2013]'
    )
    sections = dict()

    for line in moldeninputfile:

        # if any(section in line for section in sections_to_ignore):
        #     continue

        # If this fails, it's because we've hit a blank/empty line,
        # but we need to save it...
        try:
            if line[0] == '[':
                k = line.strip()
                sections[k] = []
                while line[0] != '[':
                    sections[k].append(line)
                    line = next(moldeninputfile)
            else:
                sections[k].append(line)
        # ...We must've already seen a section header (key), so keep
        # it there.
        except IndexError:
            sections[k].append(line)

    return sections


def cleanup_section_atoms(section_atoms, in_au=False):
    """If the coordinates are in atomic units (bohr), we must convert them
    to Angstroms.
    """

    if in_au:
        section_lines = []
        for line in section_atoms:
            chomp = line.split()
            chomp[3:] = map(lambda x: float(x) * 0.5291772109, chomp[3:])
            newline = '{:>3} {:>8} {:>3} {:>20.12f} {:>20.12f} {:>20.12f}'.format(*chomp)
            section_lines.append(newline)
    else:
        section_lines = section_atoms

    return section_lines


def cleanup_section_gto(section_gto):
    """For now, the [GTO] block doesn't require cleaning up."""
    return section_gto


def cleanup_section_mo(section_mo):
    """For now, the [MO] block doesn't require cleaning up."""
    return section_mo


def section_end(section_header):
    """Given a section header, do we terminate it with a newline or not?
    Return the correct terminator.
    """

    if section_header in section_headers_no_newline:
        return ''
    else:
        return '\n'


def main(args):
    moldeninputfile = make_file_iterator(args.moldeninputfilename)
    original_sections = get_molden_file_sections(moldeninputfile)
    print(original_sections)

    # for pair in original_sections.items():
    #     print(pair)
    # print(original_sections.keys())

    original_ordering_orca = (
        '[Molden Format]',
        '[Title]',
        '[Atoms] AU',
        '[GTO]',
        '[5D]',
        '[9G]',
        '[MO]'
    )
    original_ordering_dalton = (
        '[Molden Format]',
        '[GTO]',
        '[SCFCONV]',
        '[TITLE]',
        '[Atoms] AU',
        '[5D7F]',
        '[9G]',
        '[MO]',
        '[End of Molden output from Dalton2013]'
    )
    # TODO: get Molcas Molden keywords/ordering. Grid files and gv
    # suck!
    original_ordering_molcas = (
    )
    original_ordering_qchem = (
        '[Molden Format]',
        '[Atoms] (Angs)',
        '[GTO]',
        '[MO]',
        '[5D]'
    )
    # Cobbled together from
    # http://www.cmbi.ru.nl/molden/molden_format.html and various
    # 'official' Molden outputs.
    target_ordering = (
        '[Molden Format]',
        '[Atoms] Angs',
        '[GTO]',
        '[STO]',
        '[5D]', '[5D10F]', '[7F]', '[5D7F]', '[9G]',
        '[MO]',
        '[SCFCONV]',
        '[GEOCONV]',
        '[GEOMETRIES]',
        '[FREQ]',
        '[FR-COORD]',
        '[FR-NORM-COORD]',
        '[INT]'
    )

    if 'qchem' in args.moldeninputfilename:
        original_ordering = original_ordering_qchem
    if 'orca' in args.moldeninputfilename:
        original_ordering = original_ordering_orca
    if 'dalton' in args.moldeninputfilename:
        original_ordering = original_ordering_dalton
    if 'molcas' in args.moldeninputfilename:
        original_ordering = original_ordering_molcas
    # for section_header in original_ordering:
    #     print(section_header)
    #     print('\n'.join(original_sections[section_header]), end=section_end(section_header))

    # ???
    singular_keywords = (
    )

    new_sections = dict()
    new_sections['[Molden Format]'] = []

    for sh_original in original_sections:

        if '[Atoms]' in sh_original:
            if not any('[Atoms]' in k for k in new_sections):
                new_sh = '[Atoms] Angs'
                if 'AU' in sh_original:
                    new_sections[new_sh] = cleanup_section_atoms(original_sections[sh_original], in_au=True)
                elif 'Angs' in sh_original:
                    new_sections[new_sh] = cleanup_section_atoms(original_sections[sh_original], in_au=False)
                else:
                    # Assume we're already in Angstroms.
                    new_sections[new_sh] = cleanup_section_atoms(original_sections[sh_original], in_au=False)

        elif '[GTO]' in sh_original:
            if '[GTO]' not in new_sections:
                new_sections['[GTO]'] = cleanup_section_gto(original_sections['[GTO]'])

        elif sh_original in bfs:
            if sh_original not in new_sections:
                new_sections[sh_original] = []

        elif '[MO]' in sh_original:
            if '[MO]' not in new_sections:
                new_sections['[MO]'] = cleanup_section_mo(original_sections['[MO]'])

        # For sections that don't require cleaning up, just pass them
        # through.
        else:
            if sh_original not in new_sections:
                new_sections[sh_original] = original_sections[sh_original]

    for sh in target_ordering:
        if sh in new_sections:
            print(sh)
            print('\n'.join(new_sections[sh]), end=section_end(sh))

    return


if __name__ == '__main__':
    args = getargs()
    main(args)
