from typing import List
from enum import Enum, auto
from math import acos

from netqasm.sdk.classical_communication.socket import Socket
from netqasm.sdk.connection import BaseNetQASMConnection
from netqasm.sdk.epr_socket import EPRSocket

from squidasm.sim.stack.common import LogManager
from squidasm.sim.stack.program import Program, ProgramContext, ProgramMeta


class Messages(Enum):
    STATE_CREATED = auto()


class AliceProgram2D(Program):
    PEER_NAME = "Bob"

    def __init__(self, angle: float, n_epr_pairs: int):
        self.angle = angle
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

        a = []
        for i in range(self.n_epr_pairs):
            q = epr_socket.create_keep(1)[0]
            # turn |00> + |11> into |01> - |10>
            q.Z()
            q.X()
            # wait for confirmation
            csocket.send(Messages.STATE_CREATED)
            message = yield from csocket.recv()
            assert message == Messages.STATE_CREATED
            # measure
            m = q.measure()
            yield from connection.flush()
            a.append(m)

        logger.info(f"Measured qubits: {a}")

        csocket.send(a)
        logger.info(f"Sent measurements: {a}")

        logger.info("Finished")
        return {}


class BobProgram2D(Program):
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
            max_qubits=self.n_epr_pairs,
        )

    def run(self, context: ProgramContext):
        csocket = context.csockets[self.PEER_NAME]
        epr_socket = context.epr_sockets[self.PEER_NAME]
        connection = context.connection

        logger = LogManager.get_stack_logger("BobProgram")

        b = []
        for i in range(self.n_epr_pairs):
            q = epr_socket.recv_keep(1)[0]
            # turn |00> + |11> into |01> - |10>
            q.Z()
            q.X()
            # wait for confirmation
            csocket.send(Messages.STATE_CREATED)
            message = yield from csocket.recv()
            assert message == Messages.STATE_CREATED
            # measure
            b.append(q.measure())
            yield from connection.flush()

        logger.info(f"Measured qubits: {b}")

        # receive measurements from alice
        a = yield from csocket.recv()
        logger.info(f"Received measurements: {a}")

        N = self.n_epr_pairs

        # eq (4)
        Nd = 0
        for i in range(N):
            if b[i] != a[i]:
                Nd += 1
        qN = 2*Nd/N - 1

        # eq (21)
        theta = acos(N/(N+2)*qN)

        logger.info(f"Calculated difference in angles: {theta=}")

        logger.info("Finished")
        return {"theta": theta}
