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

# --- Parte 1: Intro e Fondamentali ---

nb.add_markdown("""# Benvenuti nel Mondo Quantistico! 🌌

Ciao! Sei pronto a scoprire come funziona l'informatica del futuro?
Oggi non useremo i soliti bit (0 e 1) che conosci. Entreremo nel mondo dei **Qubit**, dove le regole della logica classica vengono stravolte.

In questa lezione imparerai:
1.  Cosa rende "strano" e potente un computer quantistico.
2.  Come usare le **Porte Quantistiche** per manipolare l'informazione.
3.  Concetti chiave come **Sovrapposizione** e **Entanglement** (non preoccuparti se sembrano paroloni, li renderemo semplicissimi!).

Useremo **Qiskit**, il framework di IBM, per simulare i nostri esperimenti direttamente qui su Google Colab.

### 🚀 Preparazione dell'Ambiente
Per prima cosa, installiamo gli strumenti necessari. Esegui la cella qui sotto.
""")

nb.add_code("""!pip install qiskit[visualization] qiskit-aer pylatexenc matplotlib""")

nb.add_markdown("""Ora importiamo le librerie che ci serviranno. Non preoccuparti di capire tutto il codice ora, ci torneremo man mano.""")

nb.add_code("""from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator, StatevectorSimulator
from qiskit.visualization import plot_histogram, plot_bloch_multivector
import matplotlib.pyplot as plt
import numpy as np

# Impostiamo i simulatori
sim_statevector = StatevectorSimulator() # Per vedere lo stato del qubit (la sfera)
sim_counts = AerSimulator()       # Per simulare le misure (i grafici a barre)

print("Tutto pronto! Possiamo iniziare.")""")

nb.add_markdown("""---
## 1. Il Qubit: Più di un semplice interruttore

Immagina un bit classico come un interruttore della luce: può essere solo **ACCESO** (che chiamiamo 1) o **SPENTO** (che chiamiamo 0).

Un **Qubit** (Quantum Bit) è molto più interessante. Immaginalo come una **sfera**.
*   Il Polo Nord della sfera rappresenta lo **0** (lo scriviamo come $|0\\rangle$).
*   Il Polo Sud della sfera rappresenta l'**1** (lo scriviamo come $|1\\rangle$).

La cosa magica? Un Qubit può puntare in **qualsiasi direzione** sulla sfera, non solo al Nord o al Sud! Questa sfera si chiama **Sfera di Bloch**.

### La Notazione di Dirac (Bra-ket)
Quei simboli strani $|0\\rangle$ e $|1\\rangle$ si chiamano **ket**. È solo un modo elegante che i fisici usano per dire "vettore di stato".
*   $|0\\rangle = \\begin{pmatrix} 1 \\\\ 0 \\end{pmatrix}$
*   $|1\\rangle = \\begin{pmatrix} 0 \\\\ 1 \\end{pmatrix}$

Non faremo calcoli con queste matrici oggi, ma è utile sapere che esistono!

Proviamo a creare il nostro primo circuito quantistico con 1 Qubit. Di default, i qubit partono sempre da $|0\\rangle$ (Polo Nord).
""")

nb.add_code("""# Creiamo un circuito con 1 qubit e 1 bit classico (per misurare il risultato)
qc = QuantumCircuit(1, 1)

# Disegniamo il circuito
qc.draw('mpl')""")

nb.add_markdown("""Vediamo dove si trova il nostro qubit sulla sfera. Dovrebbe essere al Polo Nord ($|0\\rangle$).""")

nb.add_code("""# Eseguiamo il circuito sul simulatore di stato
job = sim_statevector.run(qc)
result = job.result()
state = result.get_statevector()

# Visualizziamo la sfera di Bloch
plot_bloch_multivector(state)""")

nb.add_markdown("""Come vedi, la freccia punta in alto. È un perfetto $|0\\rangle$.

---
## 2. La Porta X: Il "NON" Quantistico

Nei computer classici, la porta **NOT** inverte il valore del bit:
*   0 $\\rightarrow$ 1
*   1 $\\rightarrow$ 0

Nel mondo quantistico, l'equivalente è la **Porta Pauli-X** (o semplicemente **X**).
Cosa fa geometricamente? Ruota la sfera di 180 gradi ($\\pi$ radianti) attorno all'asse X.

Se partiamo dal Polo Nord ($|0\\rangle$) e ruotiamo di 180 gradi, dove finiamo? Esatto, al Polo Sud ($|1\\rangle$)!

Proviamolo.
""")

nb.add_code("""qc_x = QuantumCircuit(1, 1)

# Applichiamo la porta X
qc_x.x(0)

qc_x.draw('mpl')""")

nb.add_markdown("""Ora guardiamo la sfera:""")

nb.add_code("""# Visualizziamo lo stato dopo la porta X
job = sim_statevector.run(qc_x)
state = job.result().get_statevector()
plot_bloch_multivector(state)""")

nb.add_markdown("""La freccia punta in basso ($|1\\rangle$). Niente di troppo strano finora, vero? È come un computer classico.

Ma ora... preparati alla vera magia. ✨

---
## 3. La Porta H (Hadamard): Benvenuti nella Sovrapposizione

Questa è la porta più importante e famosa. La porta **Hadamard (H)**.

Se applichiamo una porta H a uno stato $|0\\rangle$, il qubit non va a 1. E non resta a 0.
Va all'**equatore** della sfera!

In questo stato, il qubit è in **Sovrapposizione**.
$$ H|0\\rangle = |+\\rangle = \\frac{|0\\rangle + |1\\rangle}{\\sqrt{2}} $$

Cosa significa? Significa che il qubit è, in un certo senso, **sia 0 che 1 contemporaneamente**.
È come una moneta che gira vorticosamente sul tavolo. Non è né testa né croce, è in uno stato intermedio.

Vediamolo sulla sfera.
""")

nb.add_code("""qc_h = QuantumCircuit(1, 1)

# Applichiamo la porta H
qc_h.h(0)

qc_h.draw('mpl')""")

nb.add_code("""# Visualizziamo lo stato di sovrapposizione
job = sim_statevector.run(qc_h)
state = job.result().get_statevector()
plot_bloch_multivector(state)""")

nb.add_markdown("""Vedi? La freccia punta lungo l'asse X positivo. Questo stato si chiama $|+\\rangle$.

### Dio gioca a dadi? 🎲
Ora arriva la parte sconvolgente. Cosa succede se chiediamo al qubit: "Sei 0 o sei 1?" (cioè se facciamo una **Misura**).

Quando misuriamo, costringiamo la Natura a scegliere. La "moneta quantistica" smette di girare e cade.
*   Con il 50% di probabilità otterremo 0.
*   Con il 50% di probabilità otterremo 1.

Il risultato è **puramente casuale**. Non è che non sappiamo il risultato perché ci mancano informazioni; è la natura stessa a essere probabilistica. Einstein odiava questa idea ("Dio non gioca a dadi"), ma gli esperimenti gli hanno dato torto.

Verifichiamolo! Eseguiamo il circuito 1024 volte e contiamo i risultati.
""")

nb.add_code("""# Aggiungiamo la misura al circuito
qc_h.measure(0, 0)

# Eseguiamo la simulazione 1024 volte (shots)
job = sim_counts.run(qc_h, shots=1024)
result = job.result()
counts = result.get_counts()

# Disegniamo l'istogramma
plot_histogram(counts)""")

nb.add_markdown("""Dovresti vedere due barre quasi uguali. Circa il 50% delle volte è uscito 0, e il 50% delle volte è uscito 1.

Se avessimo misurato lo stato $|0\\rangle$ (senza porta H), avremmo ottenuto il 100% delle volte 0.
La porta H crea l'incertezza fondamentale.

---
### 🏆 Challenge #1: Crea lo stato "Meno"

Abbiamo visto che $H$ applicato a $|0\\rangle$ crea lo stato $|+\\rangle$ (freccia su asse X positivo).
Esiste anche lo stato $|-\\rangle$ (freccia su asse X negativo, "dietro" la sfera).

Questo stato si ottiene applicando H allo stato $|1\\rangle$.

**La tua missione:**
1.  Crea un circuito con 1 qubit.
2.  Porta il qubit nello stato $|1\\rangle$ (usa la porta che abbiamo visto prima!).
3.  Applica la porta H.
4.  Visualizza la sfera di Bloch per confermare che la freccia punti nella direzione opposta a $|+\\rangle$.
""")

nb.add_code("""# Scrivi qui il tuo codice per la Challenge #1
qc_challenge1 = QuantumCircuit(1)

# ... aggiungi le porte ...

# job = sim_statevector.run(qc_challenge1)
# plot_bloch_multivector(job.result().get_statevector())
""")

# --- Parte 2: Fase e Interferenza ---

nb.add_markdown("""---
## 4. Rotazioni e Fase: Le porte Z, S, T, Y

Oltre a ribaltare (X) e creare sovrapposizione (H), possiamo ruotare il qubit attorno ad altri assi.

*   **Porta Z**: Ruota di 180 gradi attorno all'asse Z (l'asse verticale).
    *   Se siamo in $|0\\rangle$, ruotare attorno a Z non cambia nulla (la freccia è già sull'asse Z!).
    *   Ma se siamo in sovrapposizione (sull'equatore, come $|+\\rangle$), la porta Z ci sposta a $|-\\rangle$.
    *   Questo cambio si chiama **Fase**. Non cambia la probabilità di misurare 0 o 1 (che dipende dall'altezza sulla sfera), ma cambia la "direzione" interna del qubit.

*   **Porta Y**: Ruota attorno all'asse Y.
*   **Porta S**: Ruota di 90 gradi attorno a Z (metà di una Z).
*   **Porta T**: Ruota di 45 gradi attorno a Z (metà di una S).

Le porte S e T sono cruciali per algoritmi complessi, ma oggi ci concentreremo sulla Z per vedere un fenomeno incredibile: l'interferenza.

---
## 5. L'Interferenza Quantistica: Quando le probabilità si cancellano

Abbiamo detto che la porta H crea casualità (50/50).
Quindi, se applico H due volte di fila ($H \\rightarrow H$), cosa mi aspetto?
1.  Parto da 0.
2.  Prima H $\\rightarrow$ Random.
3.  Seconda H $\\rightarrow$ Ancora più Random?

La logica classica direbbe: se lancio una moneta e poi la rilancio, il risultato è sempre casuale.
La logica quantistica dice: **NO!**

Proviamo: $H \\rightarrow Z \\rightarrow H$.
""")

nb.add_code("""qc_interf = QuantumCircuit(1, 1)

# Passo 1: Creiamo sovrapposizione
qc_interf.h(0)

# Passo 2: Applichiamo Z (cambiamo la fase)
qc_interf.z(0)

# Passo 3: Riapplichiamo H
qc_interf.h(0)

qc_interf.draw('mpl')""")

nb.add_markdown("""Ora misuriamo. Secondo l'intuizione classica, dovremmo avere un miscuglio casuale.
Vediamo cosa succede.""")

nb.add_code("""qc_interf.measure(0, 0)

job = sim_counts.run(qc_interf, shots=1024)
plot_histogram(job.result().get_counts())""")

nb.add_markdown("""Sorpresa! Otteniamo **100% risultato 1** (o quasi, a parte piccoli errori di simulazione). È tornato deterministico!

**Cosa è successo?**
Le "onde" di probabilità si sono combinate.
1.  La prima H crea due onde: una per lo 0 e una per l'1.
2.  La Z inverte la fase dell'onda dell'1 (la capovolge).
3.  La seconda H fa scontrare queste onde.
    *   Per lo stato 0, le onde si sono cancellate (**interferenza distruttiva**).
    *   Per lo stato 1, le onde si sono sommate (**interferenza costruttiva**).

È esattamente come nelle cuffie a cancellazione di rumore: suono + suono opposto = silenzio.
Qui: probabilità + probabilità opposta = impossibilità.

Questo è il segreto della velocità dei computer quantistici: manipolano le fasi per cancellare le risposte sbagliate e amplificare quella giusta!

---
## 6. Multi-Qubit e Entanglement: "Azione Spettrale a Distanza" 👻

Finora abbiamo giocato con un solo qubit. Ora usiamone due.
Il nostro nuovo circuito avrà 2 linee orizzontali.

### La Porta CNOT (Controlled-NOT)
Questa è una porta condizionale (come un IF).
*   Il primo qubit è il **Controllo**.
*   Il secondo qubit è il **Target**.

Se il Controllo è 0, al Target non succede nulla.
Se il Controllo è 1, al Target viene applicata una X (si inverte).

Vediamo la "Tabella di Verità":
*   $|00\\rangle \\rightarrow |00\\rangle$
*   $|01\\rangle \\rightarrow |01\\rangle$
*   $|10\\rangle \\rightarrow |11\\rangle$ (Il controllo è 1, quindi il target 0 diventa 1)
*   $|11\\rangle \\rightarrow |10\\rangle$ (Il controllo è 1, quindi il target 1 diventa 0)

Ma cosa succede se il qubit di controllo è in **sovrapposizione**?
Se il controllo è "un po' 0 e un po' 1", allora il target diventa "un po' non girato e un po' girato".

Si crea l'**Entanglement** (Intreccio).
I due qubit smettono di essere due oggetti separati e diventano un unico oggetto indissolubile.

Creiamo lo **Stato di Bell**, lo stato più entangled possibile.
""")

nb.add_code("""qc_bell = QuantumCircuit(2, 2)

# 1. Mettiamo il primo qubit in sovrapposizione con H
qc_bell.h(0)

# 2. Applichiamo la CNOT con q0 come controllo e q1 come target
qc_bell.cx(0, 1)

qc_bell.draw('mpl')""")

nb.add_markdown("""Ora, ragioniamo.
*   Dopo la H, q0 è 50% $|0\\rangle$ e 50% $|1\\rangle$. q1 è ancora $|0\\rangle$.
*   La CNOT agisce.
    *   Nella realtà in cui q0 è 0, q1 resta 0. -> Stato $|00\\rangle$.
    *   Nella realtà in cui q0 è 1, q1 diventa 1. -> Stato $|11\\rangle$.

Il sistema è ora una sovrapposizione di $|00\\rangle$ e $|11\\rangle$.
Non esiste $|01\\rangle$ e non esiste $|10\\rangle$.
O sono entrambi 0, o sono entrambi 1.

Misuriamoli!
""")

nb.add_code("""qc_bell.measure([0,1], [0,1])

job = sim_counts.run(qc_bell, shots=1024)
counts = job.result().get_counts()
plot_histogram(counts)""")

nb.add_markdown("""Dovresti vedere due barre alte per 00 e 11. (Quasi) zero per 01 e 10.

Se misuro il primo qubit e trovo 0, so **istantaneamente** che anche l'altro è 0. Anche se l'altro qubit fosse su Marte!
Einstein chiamava questo fenomeno "Spooky action at a distance" (Azione spettrale a distanza). Non c'è scambio di informazioni (non possiamo mandare messaggi più veloci della luce), ma le correlazioni sono più forti di qualsiasi cosa possibile nel mondo classico.

---
### La Porta Toffoli (CCNOT)
Giusto per completezza, esiste anche la "nonna" della CNOT: la Toffoli.
Ha **due** controlli e un target.
Il target si inverte se e solo se **entrambi** i controlli sono 1.
È l'equivalente quantistico della porta classica **AND**.
""")

nb.add_code("""qc_toff = QuantumCircuit(3)
qc_toff.ccx(0, 1, 2) # q0, q1 controlli, q2 target
qc_toff.draw('mpl')""")

nb.add_markdown("""---
### 🏆 Challenge #2: L'enigma dell'Entanglement

Hai visto come creare lo stato che correla 00 e 11 (Stato di Bell $\\Phi^+$).
La tua sfida è creare un circuito che produca sempre e solo gli stati **01** e **10**.
Cioè: se il primo è 0, il secondo deve essere 1. Se il primo è 1, il secondo deve essere 0.

*Suggerimento:* Parti dallo stato di Bell che abbiamo appena fatto ($H$ su q0, $CX$ su q0,q1). Alla fine, quale porta devi aggiungere a uno dei due qubit per "invertire" il risultato? (Forse una X da qualche parte?)
""")

nb.add_code("""# Scrivi qui il tuo codice per la Challenge #2
qc_challenge2 = QuantumCircuit(2, 2)

# ... il tuo codice ...

# qc_challenge2.measure([0,1], [0,1])
# plot_histogram(sim_counts.run(qc_challenge2).result().get_counts())
""")

nb.add_markdown("""---
## Conclusione: Il futuro è qui

Hai appena toccato con mano i tre pilastri del Quantum Computing:
1.  **Sovrapposizione**: Essere in più stati contemporaneamente (grazie ad H).
2.  **Interferenza**: Usare le onde di probabilità per cancellare i risultati errati.
3.  **Entanglement**: Legare il destino di più qubit indissolubilmente.

Le porte quantistiche non sono magiche, sono fisica. Ma permettono di fare calcoli che per un computer classico richiederebbero milioni di anni.

Continua a sperimentare! Prova a combinare le porte in modi nuovi e guarda cosa succede alla sfera di Bloch.
Buon divertimento quantistico! ⚛️
""")

nb.save("Lezione_Porte_Quantistiche.ipynb")
