import netsquid as ns
from netqasm.sdk.qubit import Qubit
from squidasm.sim.stack.program import Program, ProgramContext, ProgramMeta
from random import randint
import numpy as np

mu = 1
tstar = 1
c_t = np.exp(-mu*tstar)

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

        #serv1 instrucrions simulation
        # Implémentation Classique
        '''
        Serv1_A = []
        Serv1_Instructions =[]
        taux_A = []
        ch = ""
        #simulation de la V.A.R b pour calcul de probabilité
        bsimul = 0.
        #pour calculer la probavilité avec la loi des grands nombres
        produit_superieur_c_t = 0
        for i in range(100):
            Serv1_Instructions.append(np.random.exponential(mu))
            Serv1_A.append(round(1-np.exp(-mu*Serv1_Instructions[i]), 3))
            #Calcul de la probabilité que le produit soit trop élevé
            for j in range (100):
                bsimul = 1-np.exp(-mu*(np.random.exponential(mu)))
                
                produit_superieur_c_t += (1-Serv1_A[i])*(1-bsimul) >= c_t

            if produit_superieur_c_t >=50 :
                taux_A.append(1)
            else:
                taux_A.append(-1)
            ch += str(taux_A)+";"+str(Serv1_A[i])+":" 
        '''
        # Implémentation quantique
        Serv1_A = []
        Serv1_Instructions =[]
        taux_A = 0
        Alice_key = []
        ch = ""
        for i in range(100):
            Serv1_Instructions.append(np.random.exponential(mu))
            Serv1_A.append(round(1-np.exp(-mu*Serv1_Instructions[i]), 3))
            epr_qubit = epr_socket_bob.create_keep()[0]
            x = Serv1_Instructions[i]>tstar
            epr_qubit.rot_X(x,1)
            Alice_key.append("")
            
        '''
        print(f"{ns.sim_time()} ns: Hello from {self.NODE_NAME}")
        Alice_key = []
        for i in range(100):

            epr_qubit = epr_socket_bob.create_keep()[0]
            x = randint(0,1)
            epr_qubit.rot_X(x,1)
            a = epr_qubit.measure()
            yield from connection.flush()
            Alice_key.append((a,x))
            #print(f"Alice measure local EPR qubit :{result}")
        '''
        csocket_bob.send(ch)
        print("Alice sends to bob")
        '''
        message = yield from csocket_bob.recv()
        bob_key = message.split(":")
        rate = 0
        for i in range(100):
            alice = Alice_key[i]
            bob = bob_key[i]
            rate += (alice[0] ^ int(bob[0]))==(alice[1] and int(bob[1]))
        print(f"succes rate : {rate/100}")
        #création qubit
        
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

        #serv2 instrucrions simulation
        Serv2_Instructions =[]
        Serv2_B =[]
        taux_B = []
        #simulation de la V.A.R a pour calcul de probabilité
        asimul = 0.
        #pour calculer la probavilité avec la loi des grands nombres
        produit_superieur_c_t = 0
        for i in range(100):
            Serv2_Instructions.append(np.random.exponential(mu))
            Serv2_B.append(round(1-np.exp(-mu*Serv2_Instructions[i]),3))
            for j in range (100):
                asimul = 1-np.exp(-mu*(np.random.exponential(mu)))
                produit_superieur_c_t += (1-Serv2_B[i])*(1-asimul) >= c_t

            if produit_superieur_c_t >=50 :
                taux_B.append(1)
            else:
                taux_B.append(-1)
        '''
        print(f"{ns.sim_time()} ns: Hello from {self.NODE_NAME}")
        Bob_key = []
        for i in range(100):
            epr_qubit = epr_socket_alice.recv_keep()[0]
            y=randint(0,1)
            epr_qubit.rot_X((2)*y - 1 +8 ,2)
            b = epr_qubit.measure()
            yield from connection.flush()
            Bob_key.append((b,y))
            #print(f"Bob measures local EPR qubit: {result}")
        ch = ""
        for l in Bob_key:
            x = str(l[0])+str(l[1])
            ch+=x+":"
        csocket_alice.send(ch)
        print("Bob sends to Alice")
        '''
        message = yield from csocket_alice.recv()
        bob_values = message.split(":")
        rate = 0
        for i in range(100):
            l = bob_values[i]
            liste2 = l.split(";")
            if len(liste2[0])==1:
                taux_A= 1
                serv1_A = float(liste2[1])

            else:
                taux_A = -1
                serv1_A = float(liste2[1])

            if taux_A*taux_B[i]==1 and (1-serv1_A)*(1-Serv2_B[i])>=c_t:
                rate +=1
            elif taux_A*taux_B[i]==-1 and (1-serv1_A)*(1-Serv2_B[i])<c_t:
                rate +=1
        print(f'Success rate is {rate/100}')
        return {}
