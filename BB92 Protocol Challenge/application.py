import netsquid as ns
from netqasm.sdk.qubit import Qubit
from squidasm.sim.stack.program import Program, ProgramContext, ProgramMeta


class AliceProgram(Program):
    NODE_NAME = "Alice"
    PEER_BOB = "Bob"

    @property
    def meta(self) -> ProgramMeta:
        return ProgramMeta(
            name=f"program_{self.NODE_NAME}",
            csockets=[self.PEER_BOB],
            epr_sockets=[self.PEER_BOB],
            max_qubits=6,
        )

    def run(self, context: ProgramContext):
        # get classical sockets
        csocket_bob = context.csockets[self.PEER_BOB]
        # get EPR sockets
        epr_socket_bob = context.epr_sockets[self.PEER_BOB]
        # get connection to QNPU
        connection = context.connection

        print(f"{ns.sim_time()} ns: Hello from {self.NODE_NAME}")
        Alice_key = []
        for i in range(100):

            epr_qubit = epr_socket_bob.create_keep()[0]
            epr_qubit.H()
            result = epr_qubit.measure()
            yield from connection.flush()
            Alice_key.append(result)
            #print(f"Alice measure local EPR qubit :{result}")
        rate = 0
        message = yield from csocket_bob.recv()
        for i in range(50):

            rate += (message[i]==str(Alice_key[i]))
        print(f"Quantum Bit Error Rate (QBER)  : {1.-(rate/50)}")

        #création qubit
        '''
        local_qubit_tab = [[Qubit(connection), Qubit(connection)] for i in range(self.max_qubits//2)]
        for l in local_qubit_tab:
            l[0].H()
            l[0].cnot(l[1])
        
            epr_qubit = epr_socket_bob.create_keep()[0]
            yield from connection.flush()
    
        

        r0 = local_qubit0.measure()
        r1 = local_qubit1.measure()
        yield from connection.flush()
        print(f"Circuit_result :{r0} , {r1}")
        '''
        return {}
    


class BobProgram(Program):
    NODE_NAME = "Bob"
    PEER_ALICE = "Alice"

    @property
    def meta(self) -> ProgramMeta:
        return ProgramMeta(
            name=f"program_{self.NODE_NAME}",
            csockets=[self.PEER_ALICE],
            epr_sockets=[self.PEER_ALICE],
            max_qubits=6,
        )

    def run(self, context: ProgramContext):
        # get classical sockets
        csocket_alice = context.csockets[self.PEER_ALICE]
        # get EPR sockets
        epr_socket_alice = context.epr_sockets[self.PEER_ALICE]
        # get connection to QNPU
        connection = context.connection

        print(f"{ns.sim_time()} ns: Hello from {self.NODE_NAME}")
        Bob_key = []
        for i in range(100):
            epr_qubit = epr_socket_alice.recv_keep()[0]
            epr_qubit.H()
            result = epr_qubit.measure()
            yield from connection.flush()
            Bob_key.append(result)
            #print(f"Bob measures local EPR qubit: {result}")
        ch = ""
        for i in Bob_key[:50]:
            ch+=str(i)
        csocket_alice.send(ch)
        print("Bob bits were sent to Alice")

        return {}
