#!/usr/bin/env python3

from __future__ import print_function
from __future__ import division

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt


# These are the choices for plots we can make.
plot_type_choices = (
    # These are plots corresponding to the files Q-Chem creates in the
    # `scratch/AIMD` directory.
    'Cost',
    'DipoleACF',
    'EComponents',
    'Energy',
    'MulMoments',
    # It doesn't make sense to plot these right now.
    # 'NucCarts',
    # 'NucForces',
    # 'NucVeloc',
    'NucVelocACF',
    'TandV',
    'Torque',
)


def make_file_iterator(filename):
    """Return an iterator over the contents of the given file name."""
    # pylint: disable=C0103
    with open(filename) as f:
        contents = f.read()
    return iter(contents.splitlines())


def getargs():
    """Get and parse command-line arguments."""

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("inputfilename",
                        help="""Path to the file we're extracting data from.""")
    parser.add_argument("plot_type",
                        choices=plot_type_choices,
                        help="""What kind of plot should we make?""")
    parser.add_argument("--normalize",
                        action="store_true",
                        help="""Should the data be normalized before plotting?""")
    parser.add_argument("--normalize-bottom",
                        type=float,
                        default=0.0,
                        help="""If normalizing data, the minimum value.""")
    parser.add_argument("--normalize-top",
                        type=float,
                        default=1.0,
                        help="""If normalizing data, the maximum value.""")
    parser.add_argument("--columns",
                        type=int,
                        nargs='+',
                        default=None,
                        help="""""")

    args = parser.parse_args()

    return args


def get_qchem_aimd_data(file_iterator, num_header_lines, num_columns, col_types):
    """Given a file iterator over a Q-Chem ..."""

    fi = file_iterator

    header_lines = []
    for _ in range(num_header_lines):
        header_lines.append(next(fi))

    data = []
    for line in fi:
        sline = line.split()[-num_columns:]
        assert len(sline) == num_columns
        lline = [t(c) for (t, c) in zip(col_types, sline)]
        data.append(lline)

    return header_lines, data


def plot_qchem_aimd_data(column_titles, data, plotfilename, plot_title, do_normalization=False, norm_bottom=0.0, norm_top=1.0):
    """Plot a bunch of data from a Q-Chem AIMD file found in
    `scratchdir/AIMD`.

    Make no assumptions about the first column of data.
    """

    xticks = range(1, len(data) + 1)

    fig, ax = plt.subplots()

    for idx, coltitle in enumerate(column_titles):
        dps = [tp[idx] for tp in data]
        if do_normalization:
            dps = normalize_data(dps, norm_bottom, norm_top)
        ax.plot(xticks, dps, label=coltitle)

    ax.set_title(plot_title)
    ax.legend(loc='best', fancybox=True, framealpha=0.50)
    fig.savefig(plotfilename, bbox_inches='tight')

    return


def plot_qchem_aimd_data_1stcol_time(column_titles, data, plotfilename, plot_title, do_normalization=False, norm_bottom=0.0, norm_top=1.0):
    """Plot a bunch of data from a Q-Chem AIMD file found in
    `scratchdir/AIMD`.

    Assume that the first column is the time step.
    """

    time = [tp[0] for tp in data]

    fig, ax = plt.subplots()

    for idx, coltitle in enumerate(column_titles, 1):
        dps = normalize_data([tp[idx] for tp in data])
        if do_normalization:
            dps = normalize_data(dps, norm_bottom, norm_top)
        ax.plot(time, dps, label=coltitle)

    ax.set_title(plot_title)
    ax.legend(loc='best', fancybox=True, framealpha=0.50)
    fig.savefig(plotfilename, bbox_inches='tight')

    return


def normalize_data(coldata, norm_bottom=0.0, norm_top=1.0):
    """Given a list that represent data for a single column, normalize it
    to be between the given bounds.

    See: http://stats.stackexchange.com/questions/70801/how-to-normalize-data-to-0-1-range
    """

    colmin, colmax = min(coldata), max(coldata)
    denom = colmax - colmin

    return [(x - colmin)/denom for x in coldata]


def main(args):
    """The main routine."""

    inputfilename = args.inputfilename
    file_iterator = make_file_iterator(inputfilename)

    plot_type = args.plot_type

    if plot_type == "Cost":
        # (1) SCF cycles (2) CPU time/sec (3) Mem Use/MB
        num_header_lines = 1
        num_columns = 3
        col_types = [int, float, float]
        column_titles = [
            "SCF cycles",
            "CPU time/sec",
        ]
        header_lines, data = get_qchem_aimd_data(file_iterator, num_header_lines, num_columns, col_types)
        plotfilename = plot_type + ".pdf"
        plot_qchem_aimd_data(column_titles,
                             data,
                             plotfilename,
                             plot_title=plot_type,
                             do_normalization=args.normalize,
                             norm_bottom=args.normalize_bottom,
                             norm_top=args.normalize_top)
    elif plot_type == "DipoleACF":
        # Dipole autocorrelation function
        # Time/fs   < u(t) u(0)>     0.00000     0.000000e+00 
        ## Look, a bug appears!
        ## Ignore me for now.
        pass
    elif plot_type == "EComponents":
        # Time/fs E(Total), V(Elec), V(One-E), V(Coul), V(Alpha Ex), V(Beta Ex), V(DFT Ex), V(DFT Corr), V(Nuc-Nuc), V(Nuc-Elec), T(Elec), T(Nuc), T(Fict)
        num_header_lines = 1
        num_columns = 14
        col_types = [float for _ in range(num_columns)]
        column_titles = [
            "E(Total)",
            "V(Elec)",
            "V(One-E)",
            "V(Coul)",
            "V(Alpha Ex)",
            "V(Beta Ex)",
            "V(DFT Ex)",
            "V(DFT Corr)",
            "V(Nuc-Nuc)",
            "V(Nuc-Elec)",
            "T(Elec)",
            "T(Nuc)",
            # Since we're doing AIMD and not ELMD, there aren't any fictious masses.
            # "T(Fict)"
        ]
        header_lines, data = get_qchem_aimd_data(file_iterator, num_header_lines, num_columns, col_types)
        plotfilename = plot_type + ".pdf"
        plot_qchem_aimd_data_1stcol_time(column_titles, data, plotfilename, plot_title=plot_type)
    elif plot_type == "Energy":
        # Time/fs   E(total) - E(prev)  E(total) - E(initial)
        num_header_lines = 1
        num_columns = 3
        col_types = [float for _ in range(num_columns)]
        column_titles = [
            "E(total) - E(previous)",
            "E(total) - E(initial)",
        ]
        header_lines, data = get_qchem_aimd_data(file_iterator, num_header_lines, num_columns, col_types)
        plotfilename = plot_type + ".pdf"
        plot_qchem_aimd_data_1stcol_time(column_titles,
                                         data,
                                         plotfilename,
                                         plot_title=plot_type,
                                         do_normalization=args.normalize,
                                         norm_bottom=args.normalize_bottom,
                                         norm_top=args.normalize_top)
    elif plot_type == "MulMoments":
        # Time/fs  Dipole + higher multipole moments (Debye*Angst**(L-1))
        num_header_lines = 1
        num_columns = 4
        col_types = [float for _ in range(num_columns)]
        column_titles = [
            "dipole (X)",
            "dipole (Y)",
            "dipole (Z)",
        ]
        header_lines, data = get_qchem_aimd_data(file_iterator, num_header_lines, num_columns, col_types)
        plotfilename = plot_type + ".pdf"
        plot_qchem_aimd_data_1stcol_time(column_titles,
                                         data,
                                         plotfilename,
                                         plot_title=plot_type,
                                         do_normalization=args.normalize,
                                         norm_bottom=args.normalize_bottom,
                                         norm_top=args.normalize_top)

    # elif plot_type == "NucCarts":
    #     pass
    # elif plot_type == "NucForces":
    #     pass
    # elif plot_type == "NucVeloc":
    #     pass
    elif plot_type == "NucVelocACF":
        # Nuclear velocity autocorrelation function
        # Time/fs   < v(t) v(0)>     0.00000     5.959529e-03 
        num_header_lines = 0
        num_columns = 2
        col_types = [float for _ in range(num_columns)]
        column_titles = [
            "<v(t).v(0)>",
        ]
        # Because of a bug in the output, do some trickery...
        next(file_iterator)
        header_lines, data = get_qchem_aimd_data(file_iterator, num_header_lines, num_columns, col_types)
        plotfilename = plot_type + ".pdf"
        plot_qchem_aimd_data_1stcol_time(column_titles,
                                         data,
                                         plotfilename,
                                         plot_title=plot_type,
                                         do_normalization=args.normalize,
                                         norm_bottom=args.normalize_bottom,
                                         norm_top=args.normalize_top)
    elif plot_type == "TandV":
        # Time/fs  V(total)  T(total)  V(t)-V(0)  T(t)-T(0)
        num_header_lines = 1
        num_columns = 5
        col_types = [float for _ in range(num_columns)]
        column_titles = [
            "V(total)",
            "T(total)",
            "V(t) - V(0)",
            "T(t) - T(0)",
        ]
        header_lines, data = get_qchem_aimd_data(file_iterator, num_header_lines, num_columns, col_types)
        plotfilename = plot_type + ".pdf"
        plot_qchem_aimd_data_1stcol_time(column_titles,
                                         data,
                                         plotfilename,
                                         plot_title=plot_type,
                                         do_normalization=args.normalize,
                                         norm_bottom=args.normalize_bottom,
                                         norm_top=args.normalize_top)
    elif plot_type == "Torque":
        # Time/fs, Torque, angular momentum, c.o.m. translational force
        num_header_lines = 1
        num_columns = 10
        col_types = [float for _ in range(num_columns)]
        column_titles = [
            "torque (X)",
            "torque (Y)",
            "torque (Z)",
            "angular momentum (X)",
            "angular momentum (Y)",
            "angular momentum (Z)",
            "c.o.m. translational force (X)",
            "c.o.m. translational force (Y)",
            "c.o.m. translational force (Z)",
        ]
        header_lines, data = get_qchem_aimd_data(file_iterator, num_header_lines, num_columns, col_types)
        plotfilename = plot_type + ".pdf"
        plot_qchem_aimd_data_1stcol_time(column_titles,
                                         data,
                                         plotfilename,
                                         plot_title=plot_type,
                                         do_normalization=args.normalize,
                                         norm_bottom=args.normalize_bottom,
                                         norm_top=args.normalize_top)
    else:
        # Meh...
        pass

    # The data we retrieve from Q-Chem AIMD single outputs is such
    # that each list in the data list is a single time step.
    # for line in header_lines:
    #     print(line)
    # for line in data:
    #     print(line)


if __name__ == "__main__":

    args = getargs()
    main_locals = main(args)
