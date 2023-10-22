from squidasm.run.stack.config import StackNetworkConfig
from squidasm.run.stack.run import run
from squidasm.sim.stack.common import LogManager
import argparse

from application import AliceProgram2D, BobProgram2D

parser = argparse.ArgumentParser(
                    prog='Quantum Proprioception',
                    description='Runs the quantum proprioception example in a squidasm simulation')

parser.add_argument('angle1', default=0)
parser.add_argument('angle2', default=0)
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

    alice_program = AliceProgram2D(args.angle1, args.num_epr)
    bob_program = BobProgram2D(args.angle2, args.num_epr, args.finite_estimation)

    alice_results, bob_results = run(config=cfg, programs={"Alice": alice_program, "Bob": bob_program}, num_times=1)

    print(f"{alice_results=}")
    print(f"{bob_results=}")
