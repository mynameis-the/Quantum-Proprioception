from application import AliceProgram, BobProgram

from squidasm.run.stack.config import StackNetworkConfig
from squidasm.run.stack.run import run


cfg = StackNetworkConfig.from_file("config.yaml")

alice_program = AliceProgram()
bob_program = BobProgram()

run(config=cfg, programs={"Alice": alice_program, "Bob": bob_program}, num_times=1)