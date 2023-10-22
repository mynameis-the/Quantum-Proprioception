import argparse
from math import acos, pi

from squidasm.run.stack.config import StackNetworkConfig
from squidasm.run.stack.run import run
from squidasm.sim.stack.common import LogManager

from application import AliceProgram2D, BobProgram2D, NDAngle
from statistics import average_fidelity_2D

parser = argparse.ArgumentParser(
                    prog='Quantum Proprioception',
                    description='Runs the quantum proprioception example in a squidasm simulation')

parser.add_argument('n1')
parser.add_argument('d1')
parser.add_argument('n2')
parser.add_argument('d2')
parser.add_argument('-N', '--num_epr', default=100)
parser.add_argument('-l', '--logfile', default='info.log')
parser.add_argument('-v', '--verbose',
                    action='store_true', default=False)
parser.add_argument('-n', '--noise',
                    action='store_true', default=False)
parser.add_argument('-f', '--finite-estimation',
                    action='store_true', default=False)


if __name__ == "__main__":
    args = parser.parse_args()
    if args.noise:
        cfg = StackNetworkConfig.from_file("generic_qdevice.yaml")
    else:
        cfg = StackNetworkConfig.from_file("perfect.yaml")

    LogManager.log_to_file(args.logfile)
    LogManager.set_log_level("INFO")

    if not args.verbose:
        # Disable logging to terminal
        logger = LogManager.get_stack_logger()
        logger.handlers = []

    angle1 = NDAngle(args.n1, args.d1)
    angle2 = NDAngle(args.n2, args.d2)

    alice_program = AliceProgram2D(angle1, args.num_epr)
    bob_program = BobProgram2D(angle2, args.num_epr, args.finite_estimation)

    alice_results, bob_results = run(config=cfg, programs={"Alice": alice_program, "Bob": bob_program}, num_times=1)

    results = bob_results[0]
    print(f"{results=}\n")

    fidelity = average_fidelity_2D(args.num_epr)
    error = acos(2*fidelity-1)

    print(f"Alice's angle is {angle1.radians} radians ({angle1.degrees:.3f} degrees).")
    print(f"Bob's angle is {angle2.radians} radians ({angle2.degrees:.3f} degrees).")
    print(f"difference in angles is estimated as {bob_results[0]['theta']:.3f} +- {error:.3f} radians ({bob_results[0]['theta']*180/pi:.3f} +- {error*180/pi:.3f} degrees).")
