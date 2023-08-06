#!/usr/bin/python3 -u

"""run a shell command repeatedly, or until it fails"""

# Copyright © 2018, Gregory P. Ward. All rights reserved.
# Use of this source code is governed by a BSD-style license that can
# be found in the LICENSE.txt file.

# usage:
#
# shrep [-n REPS] [-j JOBS] [-f] arg...
#
# shrep [-n REPS] [-j JOBS] [-f] -c "cmd"

import argparse
import os
import subprocess
import sys
import tempfile


def main():
    args = parse_args()
    num_failed = run_children(args)
    sys.exit(num_failed > 0)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--reps', '-n', type=int,
                        help='number of repetitions to (default: infinity)')
    parser.add_argument('--jobs', '-j', type=int, default=1,
                        help='run JOBS processes in parallel')
    parser.add_argument('--fail-early', '-f', action='store_true',
                        help='stop after the first failed process')
    parser.add_argument('--shell', '-c', action='store_true',
                        help='run /bin/sh -c CMD')
    parser.add_argument('--output', '-o', metavar='DIR',
                        help='record stdout+stderr of children in DIR')
    parser.add_argument('--keep-only-failed', '-k', action='store_true',
                        help='keep output of only failed children')
    parser.add_argument('cmd', nargs='+',
                        help='command to run')
    args = parser.parse_args()
    if args.reps is None:
        args.reps = float('+inf')
    if args.shell and len(args.cmd) > 1:
        parser.error('with --shell/-c, CMD must be a single argument')
    if args.keep_only_failed and not args.output:
        parser.error('--keep-only-failed option requires --output DIR too')
    if args.shell:
        args.cmd = ['/bin/sh', '-c', args.cmd[0]]

    return args


def run_children(args):
    if args.output and not os.path.isdir(args.output):
        os.makedirs(args.output)

    started = 0                         # total number of processes
    running = {}                        # map pid to subprocess.Popen
    num_failed = 0
    while started < args.reps:
        while started < args.reps and len(running) < args.jobs:
            child = launch_child(args.cmd, args.output)
            started += 1
            child.shrep_counter = started
            running[child.pid] = child

        failed = await_child(args, running)
        num_failed += int(failed)
        if failed and args.fail_early:
            break

    while running:
        failed = await_child(args, running)
        num_failed += int(failed)

    print('ran {} processes: {} failed'.format(started, num_failed))
    return num_failed


def launch_child(cmd, output):
    output_fn = stderr = stdout = None
    if output:
        (output_fd, output_fn) = tempfile.mkstemp(prefix='shrep.', dir=output)
        stderr = subprocess.STDOUT
        stdout = output_fd

    child = subprocess.Popen(cmd, stderr=stderr, stdout=stdout)
    child.shrep_output = output_fn
    return child


def await_child(args, running):
    (pid, status) = os.wait()
    child = running.pop(pid)
    print('run {} (child {}): exit status {}'
          .format(child.shrep_counter, pid, status))
    if args.output and child.shrep_output:
        if status == 0 and args.keep_only_failed:
            os.remove(child.shrep_output)
        else:
            new_name = os.path.join(args.output, 'shrep-{}.out'.format(pid))
            os.rename(child.shrep_output, new_name)

    return status != 0


main()
