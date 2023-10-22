from typing import List
from enum import Enum, auto
from math import acos, pi
from dataclasses import dataclass

from netqasm.sdk.classical_communication.socket import Socket
from netqasm.sdk.connection import BaseNetQASMConnection
from netqasm.sdk.epr_socket import EPRSocket

from squidasm.sim.stack.common import LogManager
from squidasm.sim.stack.program import Program, ProgramContext, ProgramMeta


@dataclass
class NDAngle:
    n: int
    d: int

    @property
    def radians(self):
        return self.n*pi/2**self.d

    @property
    def degrees(self):
        return self.radians*180/pi

class Messages(Enum):
    STATE_CREATED = auto()


class AliceProgram2D(Program):
    PEER_NAME = "Bob"

    def __init__(self, angle: NDAngle, n_epr_pairs: int):
        self.angle = angle
        self.n_epr_pairs = n_epr_pairs

    @property
    def meta(self) -> ProgramMeta:
        return ProgramMeta(
            name="alice_program",
            csockets=[self.PEER_NAME],
            epr_sockets=[self.PEER_NAME],
            max_qubits=1,
        )

    def run(self, context: ProgramContext):
        csocket = context.csockets[self.PEER_NAME]
        epr_socket = context.epr_sockets[self.PEER_NAME]
        connection = context.connection

        logger = LogManager.get_stack_logger("AliceProgram")

        for i in range(self.n_epr_pairs):
            q = epr_socket.create_keep(1)[0]
            # turn |00> + |11> into |01> - |10>
            q.Z()
            q.X()
            # simulate angle
            q.rot_X(self.angle.n, self.angle.d)
            # wait for confirmation
            csocket.send(Messages.STATE_CREATED)
            message = yield from csocket.recv()
            assert message == Messages.STATE_CREATED
            # measure
            m = q.measure()
            yield from connection.flush()
            csocket.send(str(m.value))

        logger.info("Finished")
        return {}


class BobProgram2D(Program):
    PEER_NAME = "Alice"

    def __init__(self, angle: NDAngle, n_epr_pairs: int, finite_estimation: bool = False):
        self.angle = angle
        self.n_epr_pairs = n_epr_pairs
        self.finite_estimation = finite_estimation

    @property
    def meta(self) -> ProgramMeta:
        return ProgramMeta(
            name="bob_program",
            csockets=[self.PEER_NAME],
            epr_sockets=[self.PEER_NAME],
            max_qubits=1,
        )

    def run(self, context: ProgramContext):
        csocket = context.csockets[self.PEER_NAME]
        epr_socket = context.epr_sockets[self.PEER_NAME]
        connection = context.connection

        logger = LogManager.get_stack_logger("BobProgram")

        a = []
        b = []
        for i in range(self.n_epr_pairs):
            q = epr_socket.recv_keep(1)[0]
            # turn |00> + |11> into |01> - |10>
            q.Z()
            q.X()
            # simulate angle
            q.rot_X(self.angle.n, self.angle.d)
            # wait for confirmation
            csocket.send(Messages.STATE_CREATED)
            message = yield from csocket.recv()
            assert message == Messages.STATE_CREATED
            # measure
            m = q.measure()
            yield from connection.flush()
            am = yield from csocket.recv()
            a.append(int(am))
            b.append(m.value)

        logger.info(f"Received measurements: {a}")
        logger.info(f"Measured qubits: {b}")

        N = self.n_epr_pairs

        # eq (4)
        Nd = 0
        for i in range(N):
            if b[i] != a[i]:
                Nd += 1
        qN = 1 - 2 * Nd / N
        if self.finite_estimation:
            # eq (21)
            theta = acos(N/(N+2)*qN)
        else:
            # eq (8)
            theta = acos(qN)

        logger.info(f"Calculated difference in angles: {theta=}")

        logger.info("Finished")
        return {"correlation": qN, "theta": theta}
