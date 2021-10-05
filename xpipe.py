import argparse
import sys
import subprocess

parser = argparse.ArgumentParser(
    description="Batch lines from stdin and pipe it to a command."
)
parser.add_argument(
    "-n", "--batch", type=int, required=True, help="number of lines to batch."
)

parser.add_argument(
    "-c", "--command", type=str, required=True, nargs=argparse.REMAINDER
)

args = parser.parse_args()
child = None
for (i, line) in enumerate(sys.stdin):
    if i % args.batch == 0:
        if child:
            child.stdin.close()
            child.wait()
            child = None
        child = subprocess.Popen(
            args.command, stdin=subprocess.PIPE, text=True, shell=True
        )

    child.stdin.write(line)

if child:
    child.stdin.close()
    child.wait()
