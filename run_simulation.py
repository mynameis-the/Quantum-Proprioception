from application import AliceProgram, BobProgram

from squidasm.run.stack.config import StackNetworkConfig
from squidasm.run.stack.run import run
from squidasm.sim.stack.common import LogManager


cfg = StackNetworkConfig.from_file("config.yaml")

# Set log level
LogManager.set_log_level("INFO")
# Disable logging to terminal
#logger = LogManager.get_stack_logger()
#logger.handlers = []
# Enable logging to file
LogManager.log_to_file("info.log")

n_epr_pairs = 2

alice_program = AliceProgram(0,n_epr_pairs)
bob_program = BobProgram(0, n_epr_pairs)

alice_results, bob_results = run(config=cfg, programs={"Alice": alice_program, "Bob": bob_program}, num_times=1)

print(f"{alice_results=}")
print(f"{bob_results=}")