from typing import List
from enum import Enum, auto
from math import acos

from netqasm.sdk.classical_communication.socket import Socket
from netqasm.sdk.connection import BaseNetQASMConnection
from netqasm.sdk.epr_socket import EPRSocket

from squidasm.sim.stack.common import LogManager
from squidasm.sim.stack.program import Program, ProgramContext, ProgramMeta


class Messages(Enum):
    ALL_INITIALISED = auto()


class AliceProgram(Program):
    PEER_NAME = "Bob"

    def __init__(self, direction: float, n_epr_pairs: int):
        self.direction = direction
        self.n_epr_pairs = n_epr_pairs

    @property
    def meta(self) -> ProgramMeta:
        return ProgramMeta(
            name="alice_program",
            csockets=[self.PEER_NAME],
            epr_sockets=[self.PEER_NAME],
            max_qubits=2,
        )

    def run(self, context: ProgramContext):
        csocket = context.csockets[self.PEER_NAME]
        epr_socket = context.epr_sockets[self.PEER_NAME]
        connection = context.connection

        logger = LogManager.get_stack_logger("AliceProgram")

        # Generate epr pairs
        epr_qubits = epr_socket.create_keep(number=self.n_epr_pairs)

        # turn |00> + |11> into |01> - |10>
        for q in epr_qubits:
            q.Z()
            q.X()

        # wait for qubits to be initialised in the required state
        csocket.send(Messages.ALL_INITIALISED)
        message = yield from csocket.recv()
        assert message == Messages.ALL_INITIALISED

        # measure epr qubits
        a = [q.measure() for q in epr_qubits]

        yield from connection.flush()
        logger.info(f"Measured qubits: {a}")

        # send the measurements to bob
        csocket.send(a)
        logger.info(f"Sent measurements: {a}")

        logger.info("Finished")
        return {}


class BobProgram(Program):
    PEER_NAME = "Alice"

    def __init__(self, direction: float, n_epr_pairs: int):
        self.direction = direction
        self.n_epr_pairs = n_epr_pairs

    @property
    def meta(self) -> ProgramMeta:
        return ProgramMeta(
            name="bob_program",
            csockets=[self.PEER_NAME],
            epr_sockets=[self.PEER_NAME],
            max_qubits=2,
        )

    def run(self, context: ProgramContext):
        csocket = context.csockets[self.PEER_NAME]
        epr_socket = context.epr_sockets[self.PEER_NAME]
        connection = context.connection

        logger = LogManager.get_stack_logger("BobProgram")

        # Generate epr pairs
        epr_qubits = epr_socket.create_keep(number=self.n_epr_pairs)

        # turn |00> + |11> into |01> - |10>
        for q in epr_qubits:
            q.Z()
            q.X()

        # wait for qubits to be initialised in the required state
        csocket.send(Messages.ALL_INITIALISED)
        message = yield from csocket.recv()
        assert message == Messages.ALL_INITIALISED

        # measure epr qubits
        b = [q.measure() for q in epr_qubits]

        # receive measurements from alice
        a = yield from csocket.recv()
        logger.info(f"Bob receives measurements: {a}")

        N = self.n_epr_pairs

        # eq (4)
        Nd = 0
        for i in range(N):
            if b[i] != a[i]:
                Nd += 1

        # eq (4)
        qN = 2*Nd/N - 1

        # eq (21)
        theta = acos(N/(N+2)*qN)

        logger.info(f"Bob Calculates difference in angles: {theta=}")

        logger.info("Finished")
        return {"theta": theta}