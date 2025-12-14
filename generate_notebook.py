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

nb.add_markdown("""# 🌌 Viaggio al Centro del Qubit: Dalle Porte Logiche all'Algoritmo di Deutsch

Benvenuto nella versione estesa del nostro laboratorio quantistico!
Qui non solo imparerai le basi, ma esploreremo come questi mattoncini fondamentali possono essere combinati per fare cose impossibili per i computer classici.

**Il nostro percorso:**
1.  **I Fondamentali**: Qubit, Sfera di Bloch e Porte Base (X, H).
2.  **La Danza delle Fasi**: Ruotare senza cambiare bit (Z, S, T).
3.  **Il Parco Giochi**: Porte a più Qubit (SWAP, Toffoli).
4.  **La Magia Nera**: L'Algoritmo di Deutsch e il "Phase Kickback".

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
    result = sim_statevector.run(qc).result()
    state = result.get_statevector()
    display(plot_bloch_multivector(state))

print("✅ Laboratorio Quantistico Attivato!")""")

# --- PARTE 1: IL QUBIT ---

nb.add_markdown("""---
## 1. Il Qubit e la Sfera di Bloch

Ricordiamo brevemente:
*   **Polo Nord ($|0\\rangle$)**: Stato 0.
*   **Polo Sud ($|1\\rangle$)**: Stato 1.
*   **Equatore**: Sovrapposizione ($|+\\rangle$ o $|-\\rangle$).

Vediamo il nostro qubit appena nato.
""")

nb.add_code("""qc = QuantumCircuit(1)
visualize_circuit_and_state(qc, "Qubit Iniziale (|0>)")""")

# --- PARTE 2: X e H ---

nb.add_markdown("""---
## 2. Le Porte Fondamentali: X e H

### La Porta X (Il Salto Mortale)
La porta X ruota di 180° attorno all'asse X.
Se siamo a Nord, finiamo a Sud.
""")

nb.add_code("""qc.x(0)
visualize_circuit_and_state(qc, "Dopo Porta X (Not)")""")

nb.add_markdown("""### La Porta H (La Sovrapposizione)
Resettiamo il qubit a 0 e applichiamo H.
La porta H ci porta all'equatore.
""")

nb.add_code("""qc_h = QuantumCircuit(1)
qc_h.h(0)
visualize_circuit_and_state(qc_h, "Dopo Porta H (Sovrapposizione)")""")

nb.add_markdown("""La freccia punta verso di noi (asse X positivo). Questo è lo stato $|+\\rangle$.
Se misurassimo ora, avremmo 50% di probabilità per 0 e 50% per 1.

---
## 3. Navigare le Fasi: Z, S, T

Ora che siamo all'equatore, possiamo muoverci lungo la circonferenza senza cambiare latitudine.
Queste rotazioni cambiano la **Fase** dell'onda quantistica.

*   **Z**: 180° attorno all'asse Z.
*   **S**: 90° attorno all'asse Z.
*   **T**: 45° attorno all'asse Z.

Proviamo una sequenza: $H \\rightarrow T \\rightarrow S$.
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

nb.add_markdown("""Nota che la freccia è ancora all'equatore. La probabilità di misurare 0 o 1 è INVARIATA (50/50).
Ma lo stato interno è diverso. E questo sarà cruciale tra poco.

---
## 4. L'Interferenza: $H \\rightarrow Z \\rightarrow H$

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

nb.add_markdown("""**Risultato:** La freccia punta al Sud ($|1\\rangle$).
Abbiamo trasformato un ingresso 0 in un'uscita 1 con certezza assoluta, passando per il caos della sovrapposizione.

---
## 5. Il Parco Giochi: Più Qubit, Più Divertimento

Prima di affrontare l'algoritmo finale, giochiamo con porte a più qubit.

### La Porta SWAP
Fa esattamente quello che dice: scambia due qubit.
Mettiamo q0 a 1 e q1 a 0. Dopo lo SWAP, dovrebbero invertirsi.
""")

nb.add_code("""qc_swap = QuantumCircuit(2)

# Prepariamo lo stato iniziale |10> (q0=0, q1=1 attenzione qiskit usa l'ordine inverso nei ket ma visualmente q0 è q0)
# Mettiamo q0 a 1 (Sud) e q1 a 0 (Nord)
qc_swap.x(0)

print("--- PRIMA DELLO SWAP ---")
display(qc_swap.draw('mpl'))
# Nota: plot_bloch mostra q0 a sinistra e q1 a destra solitamente, o indicizzati
display(plot_bloch_multivector(sim_statevector.run(qc_swap).result().get_statevector()))

# Applichiamo SWAP
qc_swap.swap(0, 1)

print("--- DOPO LO SWAP ---")
display(qc_swap.draw('mpl'))
display(plot_bloch_multivector(sim_statevector.run(qc_swap).result().get_statevector()))""")

nb.add_markdown("""Vedi? Le frecce si sono scambiate di posto!

### La Porta Toffoli (CCNOT)
È una CNOT con DUE controlli.
Il target cambia SOLO se entrambi i controlli sono 1.
È l'equivalente quantistico della porta **AND**.

Proviamo ad attivarla.
Imposteremo Control1=1, Control2=1. Il Target (inizialmente 0) dovrebbe diventare 1.
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

nb.add_markdown("""Osserva la terza sfera (q2). Si è girata a Sud!
Prova a cambiare uno dei controlli iniziali (togliendo una X) e vedrai che q2 non girerà più.

---
## 6. L'Algoritmo di Deutsch: La Scatola Nera ⬛

Ed eccoci alla sfida finale.
Immagina di avere una funzione segreta (una "scatola nera" o **Oracolo**) che prende 1 bit e restituisce 1 bit.
$f(x) \\rightarrow y$

Ci sono solo 4 possibili funzioni, divise in due tipi:
1.  **Costanti**: Restituiscono sempre 0 o sempre 1. (L'output non dipende dall'input).
2.  **Bilanciate**: Restituiscono 0 metà delle volte e 1 l'altra metà. (Es. Identità: $f(0)=0, f(1)=1$).

**Il Problema Classico:**
Per sapere se la scatola è Costante o Bilanciata, devi interrogarla **due volte**: una con 0 e una con 1.

**La Soluzione Quantistica:**
L'algoritmo di Deutsch può scoprirlo con **UNA SOLA** interrogazione.

Come? Sfruttando il **Phase Kickback** (Ritorno di Fase).
Invece di leggere il risultato dell'oracolo, usiamo l'interferenza per leggere *come l'oracolo cambia la fase del qubit*.

### Passo 1: Preparazione
Prepariamo due qubit:
*   Qubit Input (q0): $|0\\rangle$
*   Qubit Ancilla (q1): $|1\\rangle$
""")

nb.add_code("""qc_deutsch = QuantumCircuit(2, 1) # 2 qubit, 1 bit classico per la misura finale

# Prepariamo l'ancilla a 1
qc_deutsch.x(1)

visualize_circuit_and_state(qc_deutsch, "1. Inizializzazione (|0> |1>)")""")

nb.add_markdown("""### Passo 2: Sovrapposizione
Applichiamo H a entrambi.
*   q0 diventa $|+\\rangle$ (Fase +)
*   q1 diventa $|-\\rangle$ (Fase -) perché partiva da 1.
""")

nb.add_code("""qc_deutsch.h(0)
qc_deutsch.h(1)

visualize_circuit_and_state(qc_deutsch, "2. Sovrapposizione (Input |+>, Ancilla |->)")""")

nb.add_markdown("""### Passo 3: L'Oracolo (La Scatola Nera)
Ora applichiamo la scatola nera.
Simuliamo una funzione **Bilanciata** usando una **CNOT**.
(Perché CNOT è bilanciata? Se input è 0, output non cambia. Se input è 1, output cambia. Quindi l'output dipende dall'input).

**Attenzione al trucco:**
Normalmente la CNOT cambia il Target.
MA... se il Target è nell'autostato $|-\\rangle$ (come la nostra ancilla), la CNOT lascia il target invariato e **CAMBIA LA FASE DEL CONTROLLO**.
Questo è il **Phase Kickback**.

Osserva q0 (la prima sfera) dopo questo passaggio.
""")

nb.add_code("""qc_deutsch.cx(0, 1) # Questo è il nostro Oracolo Bilanciato

visualize_circuit_and_state(qc_deutsch, "3. Dopo l'Oracolo (Osserva q0!)")""")

nb.add_markdown("""**Hai visto?**
*   L'ancilla (q1) è rimasta uguale ($|-\\rangle$).
*   L'input (q0) si è girato! È passato da $|+\\rangle$ (fronte) a $|-\\rangle$ (retro).

L'informazione "la funzione è bilanciata" è stata codificata nella fase di q0.

### Passo 4: Interferenza Finale
Ora dobbiamo leggere questa fase. Come distinguere $|+\\rangle$ da $|-\\rangle$?
Con una porta H!
*   $H |+\\rangle = |0\\rangle$
*   $H |-\\rangle = |1\\rangle$
""")

nb.add_code("""qc_deutsch.h(0)

visualize_circuit_and_state(qc_deutsch, "4. Interferenza Finale")""")

nb.add_markdown("""### Passo 5: Misura
Il qubit q0 è ora perfettamente allo stato $|1\\rangle$.
Se fosse stata una funzione costante, sarebbe finito allo stato $|0\\rangle$.

Misuriamo per confermare.
""")

nb.add_code("""qc_deutsch.measure(0, 0)

job = sim_counts.run(qc_deutsch, shots=1000)
plot_histogram(job.result().get_counts())""")

nb.add_markdown("""**Risultato 1 (100%)** $\\rightarrow$ **Bilanciata**.
Abbiamo scoperto la natura della funzione con una sola passata attraverso il circuito!

---
## Conclusione

Abbiamo percorso tanta strada.
Dalle semplici rotazioni di una sfera, siamo arrivati a sfruttare l'interferenza delle fasi per risolvere problemi computazionali in modo più efficiente dei computer classici.

L'algoritmo di Deutsch è semplice, ma contiene il seme di algoritmi più potenti come quello di Shor (per rompere la crittografia) o di Grover (per la ricerca nei database).

Ora tocca a te.
Torna indietro, cambia l'oracolo (togli la CNOT per fare una funzione Costante), e vedi se riesci a ottenere 0 come risultato finale!

Buona sperimentazione! 🚀
""")

nb.save("Lezione_Porte_Quantistiche.ipynb")
