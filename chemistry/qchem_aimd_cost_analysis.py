#!/usr/bin/env python3


from qchem_aimd_tools import get_qchem_aimd_data, make_file_iterator


def qchem_get_time_step(filename, searchstr, idx_cpu, idx_wall):
    """Get the CPU and wall times for each step."""

    fi = make_file_iterator(filename)

    times_cpu = []
    times_wall = []

    for line in fi:
        if searchstr in line:
            sline = line.split()
            times_cpu.append(float(sline[idx_cpu]))
            times_wall.append(float(sline[idx_wall]))

    return times_cpu, times_wall


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("costfile", help="""""")
    parser.add_argument("outputfile", help="""""")
    parser.add_argument("--dump-cost", action="store_true")
    parser.add_argument("--try-extrap-fock-analysis", action="store_true")

    args = parser.parse_args()

    fi_cost = make_file_iterator(args.costfile)
    fi_output = make_file_iterator(args.outputfile)

    for line in fi_output:
        if "threads for integral computing" in line:
            nthreads = int(line.split()[1])
            break

    header_lines, costdata = get_qchem_aimd_data(
        fi_cost, num_header_lines=1, num_columns=3, col_types=[int, float, float]
    )

    time_step = list(range(1, len(costdata) + 1))
    scf_cycles = [p[0] for p in costdata]
    cpu_time_sec = [p[1] for p in costdata]

    strtemplate = "{:4d} {:3d} {:8.2f}".format
    if args.dump_cost:
        for ts, nscf, cts in zip(time_step, scf_cycles, cpu_time_sec):
            print(strtemplate(ts, nscf, cts))

    searchstr = "Time for this dynamics step:"
    times_cpu_dynamics_step, times_wall_dynamics_step = qchem_get_time_step(
        args.outputfile, searchstr, 5, 8
    )
    searchstr = "SCF time:"
    times_cpu_scf_step, times_wall_scf_step = qchem_get_time_step(args.outputfile, searchstr, 3, 6)
    searchstr = "Gradient time:"
    times_cpu_gradient_step, times_wall_gradient_step = qchem_get_time_step(
        args.outputfile, searchstr, 3, 6
    )

    # print(len(times_cpu_dynamics_step))
    # print(len(times_cpu_scf_step))
    # print(len(times_cpu_gradient_step))

    # There's a force calculation that occurs before entering the AIMD
    # portion.
    total_dynamics_time_wall = sum(times_wall_dynamics_step)
    total_force_time_wall = sum(times_wall_scf_step[1:]) + sum(times_wall_gradient_step[1:])
    total_dynamics_time_cpu = sum(times_cpu_dynamics_step)
    total_force_time_cpu = sum(times_cpu_scf_step[1:]) + sum(times_cpu_gradient_step[1:])

    print("Total dynamics time       (wall, seconds): {:f}".format(total_dynamics_time_wall))
    print("Total SCF + gradient time (wall, seconds): {:f}".format(total_force_time_wall))
    print("Total dynamics time         (wall, hours): {:f}".format(total_dynamics_time_wall / 3600))
    print("Total SCF + gradient time   (wall, hours): {:f}".format(total_force_time_wall / 3600))

    print("Total dynamics time        (cpu, seconds): {:f}".format(total_dynamics_time_cpu))
    print("Total SCF + gradient time  (cpu, seconds): {:f}".format(total_force_time_cpu))
    print("Total dynamics time          (cpu, hours): {:f}".format(total_dynamics_time_cpu / 3600))
    print("Total SCF + gradient time    (cpu, hours): {:f}".format(total_force_time_cpu / 3600))

    speedup_force = total_force_time_cpu / total_force_time_wall
    print("speedup        : {:>5.2f}".format(speedup_force))
    print("pct efficiency : {:>5.2f}".format((speedup_force / nthreads) * 100))

    if args.try_extrap_fock_analysis:

        fi_output = make_file_iterator(args.outputfile)
        for line in fi_output:
            if "fock_extrap_order" in line.lower():
                fock_extrap_order = int(line.split()[-1])
            if "fock_extrap_points" in line.lower():
                fock_extrap_points = int(line.split()[-1])
