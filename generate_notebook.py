import json

class NotebookGenerator:
    def __init__(self):
        self.cells = []
        self.metadata = {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.5"
            }
        }

    def add_markdown(self, source):
        self.cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [line + "\n" for line in source.split("\n")]
        })

    def add_code(self, source):
        self.cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [line + "\n" for line in source.split("\n")]
        })

    def save(self, filename):
        notebook = {
            "cells": self.cells,
            "metadata": self.metadata,
            "nbformat": 4,
            "nbformat_minor": 4
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=1, ensure_ascii=False)

nb = NotebookGenerator()

# --- INTRODUZIONE ---

nb.add_markdown(r"""# 🌌 Viaggio al Centro del Qubit: Corso Completo

Benvenuto! Questo è il laboratorio definitivo dove esploreremo l'informatica quantistica da zero fino agli algoritmi di ricerca avanzati.
Non useremo matematica complessa, ma ci affideremo all'intuizione visiva e agli esperimenti pratici.

**Il Programma del Corso:**
1.  **I Fondamentali**: Qubit, Sfera di Bloch e Porte Base (X, H).
2.  **La Danza delle Fasi**: Ruotare senza cambiare bit (Z, S, T).
3.  **L'Interferenza**: Cancellare le probabilità sbagliate.
4.  **Il Parco Giochi**: Porte a più Qubit (SWAP, Toffoli).
5.  **L'Algoritmo di Deutsch**: Scoprire le funzioni segrete.
6.  **SAT Solver Quantistico**: Risolvere problemi di logica.
7.  **L'Algoritmo di Grover**: Trovare un ago in un pagliaio.

---
### 🛠️ 0. Preparazione del Laboratorio
""")

nb.add_code("""!pip install qiskit[visualization] qiskit-aer pylatexenc matplotlib""")

nb.add_code("""from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator, StatevectorSimulator
from qiskit.visualization import plot_histogram, plot_bloch_multivector
import matplotlib.pyplot as plt
import numpy as np

# Simulatori
sim_statevector = StatevectorSimulator()
sim_counts = AerSimulator()

def visualize_circuit_and_state(qc, title="Stato del Qubit"):
    "Funzione di comodo per disegnare circuito e sfera insieme"
    print(f"--- {title} ---")
    display(qc.draw('mpl'))
    try:
        # Nota: Statevector funziona bene per pochi qubit.
        result = sim_statevector.run(qc).result()
        state = result.get_statevector()
        display(plot_bloch_multivector(state))
    except Exception as e:
        print(f"Non posso visualizzare la sfera (forse c'è una misura intermedia o troppi qubit?): {e}")

print("✅ Laboratorio Quantistico Attivato!")""")

# --- PARTE 1 ---

nb.add_markdown(r"""---
## 1. Il Qubit e la Sfera di Bloch

Dimentica gli 0 e gli 1 digitali. Pensa alla Terra.
*   **Polo Nord ($|0\rangle$)**: Stato 0.
*   **Polo Sud ($|1\rangle$)**: Stato 1.

Un **Qubit** può essere un punto qualsiasi sulla superficie della Terra!
Vediamo il nostro qubit appena nato (Polo Nord).
""")

nb.add_code("""qc = QuantumCircuit(1)
visualize_circuit_and_state(qc, "Qubit Iniziale (|0>)")""")

nb.add_markdown(r"""---
## 2. Le Porte Fondamentali: X e H

### La Porta X (Il Salto Mortale)
La porta X ruota di 180° attorno all'asse X.
Se siamo a Nord, finiamo a Sud.
""")

nb.add_code("""qc.x(0)
visualize_circuit_and_state(qc, "Dopo Porta X (Not)")""")

nb.add_markdown(r"""### La Porta H (La Sovrapposizione)
Resettiamo il qubit a 0 e applichiamo H.
La porta H ci porta all'**Equatore** della sfera.

La freccia punta verso di noi (asse X positivo). Questo è lo stato $|+\rangle$.
Se misurassimo ora, avremmo 50% di probabilità per 0 e 50% per 1.
""")

nb.add_code("""qc_h = QuantumCircuit(1)
qc_h.h(0)
visualize_circuit_and_state(qc_h, "Dopo Porta H (Sovrapposizione)")""")

# --- PARTE 2: FASI ---

nb.add_markdown(r"""---
## 3. Navigare le Fasi: Z, S, T

Ora che siamo all'equatore, possiamo muoverci lungo la circonferenza senza cambiare latitudine.
Queste rotazioni cambiano la **Fase** dell'onda quantistica.

*   **Z**: 180° attorno all'asse Z.
*   **S**: 90° attorno all'asse Z.
*   **T**: 45° attorno all'asse Z.

Proviamo una sequenza: $H \rightarrow T \rightarrow S$.
Segui la freccia rossa muoversi lungo l'equatore!
""")

nb.add_code("""qc_phase = QuantumCircuit(1)

# 1. H per andare all'equatore
qc_phase.h(0)
visualize_circuit_and_state(qc_phase, "Passo 1: H (Stato |+>)")

# 2. T (45 gradi)
qc_phase.t(0)
visualize_circuit_and_state(qc_phase, "Passo 2: Aggiunta fase T (45°)")

# 3. S (90 gradi)
qc_phase.s(0)
visualize_circuit_and_state(qc_phase, "Passo 3: Aggiunta fase S (+90° = 135° totali)")""")

nb.add_markdown(r"""Nota che la freccia è ancora all'equatore. La probabilità di misurare 0 o 1 è INVARIATA (50/50).
Ma lo stato interno è diverso. E questo sarà cruciale tra poco.
""")

# --- PARTE 3: INTERFERENZA ---

nb.add_markdown(r"""---
## 4. L'Interferenza: $H \rightarrow Z \rightarrow H$

Ripetiamo l'esperimento chiave.
Come cancellare le probabilità indesiderate?

1.  H: Crea due realtà (0 e 1).
2.  Z: Inverte la fase della realtà "1" (la freccia all'equatore gira di 180°).
3.  H: Fa scontrare le realtà.

Guardiamolo passo-passo sulla sfera.
""")

nb.add_code("""qc_int = QuantumCircuit(1)

# Passo 1: H
qc_int.h(0)
visualize_circuit_and_state(qc_int, "Dopo prima H (Stato |+>)")

# Passo 2: Z
qc_int.z(0)
visualize_circuit_and_state(qc_int, "Dopo Z (Stato |->, freccia dietro)")

# Passo 3: H finale
qc_int.h(0)
visualize_circuit_and_state(qc_int, "Dopo seconda H (Tornati deterministici!)")""")

nb.add_markdown(r"""**Risultato:** La freccia punta al Sud ($|1\rangle$).
Abbiamo trasformato un ingresso 0 in un'uscita 1 con certezza assoluta, passando per il caos della sovrapposizione.
""")

# --- PARTE 4: MULTI QUBIT ---

nb.add_markdown(r"""---
## 5. Il Parco Giochi: Più Qubit, Più Divertimento

### La Porta SWAP
Fa esattamente quello che dice: scambia due qubit.
Mettiamo q0 a 1 e q1 a 0. Dopo lo SWAP, dovrebbero invertirsi.
""")

nb.add_code("""qc_swap = QuantumCircuit(2)

# Mettiamo q0 a 1 (Sud) e q1 a 0 (Nord)
qc_swap.x(0)

print("--- PRIMA DELLO SWAP ---")
display(qc_swap.draw('mpl'))
display(plot_bloch_multivector(sim_statevector.run(qc_swap).result().get_statevector()))

# Applichiamo SWAP
qc_swap.swap(0, 1)

print("--- DOPO LO SWAP ---")
display(qc_swap.draw('mpl'))
display(plot_bloch_multivector(sim_statevector.run(qc_swap).result().get_statevector()))""")

nb.add_markdown(r"""### La Porta Toffoli (CCNOT)
È una CNOT con DUE controlli.
Il target cambia SOLO se entrambi i controlli sono 1.
È l'equivalente quantistico della porta **AND**.
""")

nb.add_code("""qc_toff = QuantumCircuit(3)

# Prepariamo i controlli a 1
qc_toff.x(0) # Controllo 1
qc_toff.x(1) # Controllo 2
# Il target (q2) resta a 0

print("--- INPUT: |011> (q2=0, q1=1, q0=1) ---")
display(qc_toff.draw('mpl'))
display(plot_bloch_multivector(sim_statevector.run(qc_toff).result().get_statevector()))

# Applichiamo Toffoli
qc_toff.ccx(0, 1, 2)

print("--- OUTPUT: Toffoli Attivata! ---")
display(qc_toff.draw('mpl'))
display(plot_bloch_multivector(sim_statevector.run(qc_toff).result().get_statevector()))""")

# --- PARTE 5: DEUTSCH ---

nb.add_markdown(r"""---
## 6. L'Algoritmo di Deutsch: La Scatola Nera ⬛

Immagina di avere una funzione segreta (una "scatola nera" o **Oracolo**) che prende 1 bit e restituisce 1 bit.
Ci sono solo due tipi di funzioni: **Costanti** (output sempre uguale) o **Bilanciate** (0 metà delle volte, 1 l'altra metà).

**Il Problema:** Scoprire se la scatola è Costante o Bilanciata con UNA SOLA domanda.
**La Soluzione:** Usiamo il **Phase Kickback**.

### Passo 1: Preparazione
Prepariamo due qubit: q0 (Input) e q1 (Ancilla).
""")

nb.add_code("""qc_deutsch = QuantumCircuit(2, 1) # 2 qubit, 1 bit classico per la misura finale

# Prepariamo l'ancilla a 1
qc_deutsch.x(1)

visualize_circuit_and_state(qc_deutsch, "1. Inizializzazione (|0> |1>)")""")

nb.add_markdown(r"""### Passo 2: Sovrapposizione
Applichiamo H a entrambi.
*   q0 diventa $|+\rangle$ (Fase +)
*   q1 diventa $|-\rangle$ (Fase -) perché partiva da 1.
""")

nb.add_code("""qc_deutsch.h(0)
qc_deutsch.h(1)

visualize_circuit_and_state(qc_deutsch, "2. Sovrapposizione (Input |+>, Ancilla |->)")""")

nb.add_markdown(r"""### Passo 3: L'Oracolo (La Scatola Nera)
Simuliamo una funzione **Bilanciata** usando una **CNOT**.
La CNOT lascia il target invariato ma **CAMBIA LA FASE DEL CONTROLLO** perché il target è $|-\rangle$.
""")

nb.add_code("""qc_deutsch.cx(0, 1) # Oracolo Bilanciato

visualize_circuit_and_state(qc_deutsch, "3. Dopo l'Oracolo (Osserva q0!)")""")

nb.add_markdown(r"""**Hai visto?** L'input (q0) si è girato da $|+\rangle$ a $|-\rangle$.
L'informazione è stata codificata nella fase!

### Passo 4: Interferenza Finale e Misura
Per leggere la fase, usiamo H.
""")

nb.add_code("""qc_deutsch.h(0)
qc_deutsch.measure(0, 0)

visualize_circuit_and_state(qc_deutsch, "4. Interferenza Finale")

job = sim_counts.run(qc_deutsch, shots=1000)
plot_histogram(job.result().get_counts())""")

nb.add_markdown(r"""**Risultato 1 (100%)** $\rightarrow$ **Bilanciata**.
Abbiamo scoperto la natura della funzione con una sola passata!
""")

# --- PARTE 6: SAT SOLVER ---

nb.add_markdown(r"""---
## 7. Risolvere un Problema Logico (SAT) 🧩

Troviamo la configurazione di due bit ($q_1, q_0$) che soddisfa:

$$ \Phi(x) = (q_1 \lor q_0) \land (\neg q_0) $$

Analisi Logica Classica:
*   $(\neg q_0)$ vero $\rightarrow q_0 = 0$.
*   $(q_1 \lor 0)$ vero $\rightarrow q_1 = 1$.
*   Soluzione attesa: **$q_1=1, q_0=0$**.

### Costruzione del Circuito Quantistico
Implementiamo la logica semplificata: **$q_1$ AND (NOT $q_0$)**.

1.  Input in Sovrapposizione ($H$).
2.  X su $q_0$ (NOT).
3.  Toffoli (AND) su un output qubit.
4.  X su $q_0$ (Uncompute).
""")

nb.add_code("""qc_sat = QuantumCircuit(3, 3)
qc_sat.h(0) # q0
qc_sat.h(1) # q1

# Logica: q1 AND (NOT q0)
qc_sat.x(0)
qc_sat.ccx(0, 1, 2) # Scriviamo su q2
qc_sat.x(0)

qc_sat.measure([0,1,2], [0,1,2])

visualize_circuit_and_state(qc_sat, "Circuito SAT Completo")

job = sim_counts.run(qc_sat, shots=1024)
plot_histogram(job.result().get_counts())""")

nb.add_markdown(r"""Guarda l'istogramma.
L'unica barra che inizia con 1 (es. `110`) è quella corrispondente a $q_1=1, q_0=0$.
Abbiamo trovato la soluzione! Ma... solo con il 25% di probabilità (una scelta a caso).
""")

# --- PARTE 7: GROVER ---

nb.add_markdown(r"""---
## 8. L'Algoritmo di Grover: L'Amplificatore 📢

Come facciamo a trovare la soluzione al 100%?
Usiamo l'Algoritmo di Grover.

Ingredienti:
1.  **Oracolo di Fase**: Invece di scrivere su un output, inverte la fase della soluzione. (Usiamo il SAT solver + Phase Kickback con ancilla $|-\rangle$).
2.  **Diffusore**: Amplifica la differenza di fase.

Costruiamo il circuito completo.
""")

nb.add_code("""# Circuito di Grover (2 qubit input + 1 ancilla)
qc_grover = QuantumCircuit(3, 2) # Misureremo solo i 2 input

# 1. Inizializzazione
qc_grover.x(2)      # Ancilla a 1
qc_grover.h(2)      # Ancilla a |-> (per il Phase Kickback)
qc_grover.h([0,1])  # Input in Sovrapposizione completa

visualize_circuit_and_state(qc_grover, "1. Inizializzazione")

# 2. ORACLE (Il SAT Solver come Oracolo di Fase)
# Logica: q1 AND (NOT q0) attiva il Phase Kickback
qc_grover.x(0)         # NOT q0
qc_grover.ccx(0, 1, 2) # Phase Kickback! Inverte il segno di |10>
qc_grover.x(0)         # Uncompute NOT q0

visualize_circuit_and_state(qc_grover, "2. Dopo l'Oracolo (Fase segnata)")

# 3. DIFFUSORE (Amplificazione)
# Standard per 2 qubit: H -> X -> CZ -> X -> H
qc_grover.h([0,1])
qc_grover.x([0,1])

qc_grover.cp(np.pi, 0, 1) # Controlled-Z (inverte fase se 11)

qc_grover.x([0,1])
qc_grover.h([0,1])

visualize_circuit_and_state(qc_grover, "3. Dopo il Diffusore (Amplificazione)")

# 4. Misura
qc_grover.measure([0,1], [0,1])

job = sim_counts.run(qc_grover, shots=1024)
counts = job.result().get_counts()
plot_histogram(counts)""")

nb.add_markdown(r"""### Analisi Finale
Guarda l'istogramma!
La colonna **10** ($q_1=1, q_0=0$) dovrebbe essere dominante (vicina al 100%).

Abbiamo trasformato una probabilità del 25% in una certezza, usando l'interferenza costruttiva.

---
## Conclusione

Congratulazioni! Hai completato il corso.
Abbiamo visto che i computer quantistici non sono solo "più veloci", ma ragionano in modo diverso.
Usano lo spazio delle fasi, la sovrapposizione e l'entanglement per manipolare l'informazione in modi che la fisica classica non permette.

Continua a esplorare! 🚀
""")

nb.save("Lezione_Porte_Quantistiche.ipynb")
