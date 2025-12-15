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

nb.add_markdown(r"""# 🌌 Viaggio al Centro del Qubit: Risolvere Problemi Logici

Benvenuto nella versione completa del laboratorio!
Oggi useremo tutto ciò che abbiamo imparato (sovrapposizione, porte logiche) per risolvere un vero problema di logica booleana.

**Il nostro percorso:**
1.  **I Fondamentali**: Qubit, Sfera di Bloch e Porte Base.
2.  **La Danza delle Fasi**: Ruotare senza cambiare bit.
3.  **Il Parco Giochi**: SWAP e Toffoli.
4.  **L'Algoritmo di Deutsch**: Scoprire le funzioni segrete.
5.  **SAT Solver Quantistico**: Trovare la soluzione a una formula logica complessa.

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
        # Se ci sono troppi qubit, statevector potrebbe essere grande.
        # Qui assumiamo pochi qubit per scopo didattico.
        result = sim_statevector.run(qc).result()
        state = result.get_statevector()
        display(plot_bloch_multivector(state))
    except Exception as e:
        print(f"Non posso visualizzare la sfera (forse c'è una misura intermedia?): {e}")

print("✅ Laboratorio Quantistico Attivato!")""")

# --- PARTE 1-4 ---

nb.add_markdown(r"""---
## 1. Il Qubit e la Sfera di Bloch

Ricordiamo brevemente:
*   **Polo Nord ($|0\rangle$)**: Stato 0.
*   **Polo Sud ($|1\rangle$)**: Stato 1.
*   **Equatore**: Sovrapposizione ($|+\rangle$ o $|-\rangle$).

Vediamo il nostro qubit appena nato.
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
La porta H ci porta all'equatore.
""")

nb.add_code("""qc_h = QuantumCircuit(1)
qc_h.h(0)
visualize_circuit_and_state(qc_h, "Dopo Porta H (Sovrapposizione)")""")

nb.add_markdown(r"""La freccia punta verso di noi (asse X positivo). Questo è lo stato $|+\rangle$.
Se misurassimo ora, avremmo 50% di probabilità per 0 e 50% per 1.

---
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

---
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

nb.add_markdown(r"""Vedi? Le frecce si sono scambiate di posto!

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

nb.add_markdown(r"""Osserva la terza sfera (q2). Si è girata a Sud!
Prova a cambiare uno dei controlli iniziali (togliendo una X) e vedrai che q2 non girerà più.

---
## 6. L'Algoritmo di Deutsch: La Scatola Nera ⬛

Ed eccoci alla sfida finale.
Immagina di avere una funzione segreta (una "scatola nera" o **Oracolo**) che prende 1 bit e restituisce 1 bit.
$f(x) \rightarrow y$

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
*   Qubit Input (q0): $|0\rangle$
*   Qubit Ancilla (q1): $|1\rangle$
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
Ora applichiamo la scatola nera.
Simuliamo una funzione **Bilanciata** usando una **CNOT**.
(Perché CNOT è bilanciata? Se input è 0, output non cambia. Se input è 1, output cambia. Quindi l'output dipende dall'input).

**Attenzione al trucco:**
Normalmente la CNOT cambia il Target.
MA... se il Target è nell'autostato $|-\rangle$ (come la nostra ancilla), la CNOT lascia il target invariato e **CAMBIA LA FASE DEL CONTROLLO**.
Questo è il **Phase Kickback**.

Osserva q0 (la prima sfera) dopo questo passaggio.
""")

nb.add_code("""qc_deutsch.cx(0, 1) # Questo è il nostro Oracolo Bilanciato

visualize_circuit_and_state(qc_deutsch, "3. Dopo l'Oracolo (Osserva q0!)")""")

nb.add_markdown(r"""**Hai visto?**
*   L'ancilla (q1) è rimasta uguale ($|-\rangle$).
*   L'input (q0) si è girato! È passato da $|+\rangle$ (fronte) a $|-\rangle$ (retro).

L'informazione "la funzione è bilanciata" è stata codificata nella fase di q0.

### Passo 4: Interferenza Finale
Ora dobbiamo leggere questa fase. Come distinguere $|+\rangle$ da $|-\rangle$?
Con una porta H!
*   $H |+\rangle = |0\rangle$
*   $H |-\rangle = |1\rangle$
""")

nb.add_code("""qc_deutsch.h(0)

visualize_circuit_and_state(qc_deutsch, "4. Interferenza Finale")""")

nb.add_markdown(r"""### Passo 5: Misura
Il qubit q0 è ora perfettamente allo stato $|1\rangle$.
Se fosse stata una funzione costante, sarebbe finito allo stato $|0\rangle$.

Misuriamo per confermare.
""")

nb.add_code("""qc_deutsch.measure(0, 0)

job = sim_counts.run(qc_deutsch, shots=1000)
plot_histogram(job.result().get_counts())""")

nb.add_markdown(r"""**Risultato 1 (100%)** $\rightarrow$ **Bilanciata**.
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

# --- PARTE 7: SAT Solver ---

nb.add_markdown(r"""---
## 7. Risolvere un Problema Logico (SAT) 🧩

Ecco la sfida che mi hai lanciato. Dobbiamo trovare la configurazione di due bit ($q_1, q_0$) che soddisfa questa formula:

$$ \Phi(x) = (q_1 \lor q_0) \land (\neg q_0) $$

Dove:
*   $\lor$ significa **OR** (o l'uno o l'altro).
*   $\land$ significa **AND** (tutti e due).
*   $\neg$ significa **NOT** (il contrario).

### Analisi Classica (Il "Penna e Carta")
Prima di costruire il circuito, ragioniamo come Sherlock Holmes.
La formula richiede che siano vere DUE cose contemporaneamente (c'è una AND in mezzo):
1.  $(q_1 \lor q_0)$ deve essere VERO.
2.  $(\neg q_0)$ deve essere VERO.

Analizziamo la parte 2: se $(\neg q_0)$ è vero, allora **$q_0$ deve essere 0**.
Ora guardiamo la parte 1: se $q_0$ è 0, allora per rendere vero $(q_1 \lor 0)$, **$q_1$ deve essere 1**.

Quindi la soluzione dovrebbe essere: **$q_1=1, q_0=0$**. (Stato $|10\rangle$).

Ma noi vogliamo che sia il Computer Quantistico a trovarla!

### Costruzione del Circuito Quantistico
Per implementare questa logica in modo reversibile (regola d'oro quantistica), useremo 3 Qubit:
*   $q_0$: Input 0
*   $q_1$: Input 1
*   $q_{out}$: Qubit di output dove scriveremo il risultato (1 se vero, 0 se falso).

#### Semplificazione Logica
La formula è: $(q_1 \lor q_0) \land (\neg q_0)$.
In logica, possiamo semplificarla.
$(A \lor B) \land \neg B$ è equivalente a $A \land \neg B$.
(Perché? Se $B$ è falso, $A \lor B$ è vero solo se $A$ è vero).

Quindi dobbiamo implementare: **$q_1$ AND (NOT $q_0$)**.

#### I Passaggi:
1.  **Sovrapposizione**: Mettiamo $q_0$ e $q_1$ in stato $H$. Così il computer testerà TUTTE le combinazioni (00, 01, 10, 11) simultaneamente.
2.  **Logica NOT**: Applichiamo una porta **X** su $q_0$. (Ora $q_0$ rappresenta $\neg q_0$).
3.  **Logica AND**: Usiamo una porta **Toffoli (CCNOT)**.
    *   Controllo 1: $q_1$
    *   Controllo 2: $q_0$ (che ora è girato)
    *   Target: $q_{out}$
    *   Risultato: $q_{out}$ si gira se e solo se $q_1=1$ e $q_0(girato)=1$ (cioè $q_0(originale)=0$).
4.  **Pulizia (Uncomputation)**: Riapplichiamo la **X** su $q_0$ per riportarlo al suo stato originale. È buona norma lasciare gli input come li abbiamo trovati.

Proviamolo!
""")

nb.add_code("""# Creiamo il circuito con 3 qubit (2 input + 1 output) e 3 bit classici
qc_sat = QuantumCircuit(3, 3)

# 1. Inizializzazione: Mettiamo gli input in Sovrapposizione
qc_sat.h(0) # q0
qc_sat.h(1) # q1
# q2 (output) lo lasciamo a 0

visualize_circuit_and_state(qc_sat, "1. Input in Sovrapposizione (Testiamo tutto!)")

# 2. Implementiamo NOT q0
qc_sat.x(0)
# (Visualmente vedremo q0 ruotare)

# 3. Implementiamo AND (Toffoli) tra q1 e il q0 negato, scrivendo su q2
qc_sat.ccx(0, 1, 2)
# Nota: qiskit usa l'ordine (control1, control2, target).
# Qui controlliamo q0 (che ha la X) e q1. Target è q2.

# 4. Pulizia: Togliamo il NOT su q0 per ripristinare la variabile
qc_sat.x(0)

visualize_circuit_and_state(qc_sat, "2. Dopo la Logica (Soluzione calcolata su q2)")

# 5. Misura
qc_sat.measure([0,1,2], [0,1,2]) # Misuriamo tutto
""")

nb.add_markdown(r"""### Interpretazione dei Risultati
Ora eseguiamo il circuito.
Cosa ci aspettiamo?
Poiché abbiamo testato tutte le combinazioni in parallelo, otterremo una distribuzione statistica.
Dobbiamo cercare i casi in cui l'**Output (q2)** è **1**.
Quello ci dirà quali input ($q_1, q_0$) hanno soddisfatto la formula.

Nota su Qiskit: L'ordine dei bit nei grafici è $q_2, q_1, q_0$ (dal basso in alto, o sinistra destra nelle stringhe).
Quindi cerchiamo stringhe che iniziano con 1 (es. `1xx`).
""")

nb.add_code("""job = sim_counts.run(qc_sat, shots=1024)
counts = job.result().get_counts()
plot_histogram(counts)""")

nb.add_markdown(r"""### Analisi del Grafico
Guarda le barre.
Dovresti vedere 4 barre, ciascuna circa al 25% (perché abbiamo 4 combinazioni possibili in ingresso e nessuna interferenza che le cancelli).

Le combinazioni sono (leggendo da destra a sinistra q2, q1, q0):
*   `000`: Input 00, Output 0 (Falso)
*   `001`: Input 01, Output 0 (Falso)
*   `011`: Input 11, Output 0 (Falso) -> Aspetta, q1=1, q0=1. Formula $(1 \lor 1) \land (\neg 1) = 1 \land 0 = 0$. Corretto.
*   **`110`**: Input $q_1=1, q_0=0$. **Output (il primo bit a sinistra) è 1!**

**Vittoria!** 🎉
L'unica barra che ha il bit più a sinistra a 1 è quella corrispondente a $q_1=1, q_0=0$.
Abbiamo trovato la soluzione sfruttando il Parallelismo Quantistico.

(Nota: Se usassimo l'algoritmo di Grover, potremmo amplificare questa barra per farla diventare il 100% della probabilità, ma questa è una storia per la prossima lezione!)
""")

nb.save("Lezione_Porte_Quantistiche.ipynb")
