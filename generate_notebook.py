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

nb.add_markdown("""# 🌌 Viaggio al Centro del Qubit: Una Lezione Interattiva

Benvenuto! Se sei qui, significa che sei pronto a mettere in discussione tutto ciò che sai sui computer.
Nei computer classici (quello che stai usando ora), tutto è certezza: un bit è 0 oppure 1. Bianco o nero. Acceso o spento.

Nel **Quantum Computing**, entriamo in un regno di sfumature, probabilità e connessioni invisibili.
Questa non è solo una lezione di informatica, è una lezione di filosofia naturale applicata.

**Obiettivi di oggi:**
1.  Capire visivamente i Qubit (non useremo formule complicate!).
2.  Sperimentare le "Porte Quantistiche" e vedere come ruotano la realtà.
3.  Toccare con mano i fenomeni "assurdi": Sovrapposizione, Interferenza ed Entanglement.

---
### 🛠️ 0. Preparazione del Laboratorio

Prima di iniziare, dobbiamo assemblare il nostro banco di lavoro digitale. Useremo **Qiskit**, il software di IBM per programmare computer quantistici reali.
""")

nb.add_code("""!pip install qiskit[visualization] qiskit-aer pylatexenc matplotlib""")

nb.add_markdown("""Importiamo gli strumenti. Immagina queste librerie come il tuo set di cacciaviti, oscilloscopi e generatori di particelle.""")

nb.add_code("""from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator, StatevectorSimulator
from qiskit.visualization import plot_histogram, plot_bloch_multivector
import matplotlib.pyplot as plt
import numpy as np

# Questo simulatore ci permette di vedere il qubit come una sfera (ideale per imparare)
sim_statevector = StatevectorSimulator()

# Questo simulatore replica un vero esperimento con misure ripetute (ideale per vedere le probabilità)
sim_counts = AerSimulator()

print("✅ Laboratorio Quantistico Attivato!")""")

# --- PARTE 1: IL QUBIT ---

nb.add_markdown("""---
## 1. Il Qubit e la Sfera di Bloch

Dimentica per un attimo gli 0 e gli 1 digitali. Pensa alla Terra.
*   Il **Polo Nord** rappresenta lo stato **0** (o $|0\\rangle$).
*   Il **Polo Sud** rappresenta lo stato **1** (o $|1\\rangle$).

Un bit classico può essere solo al Polo Nord o al Polo Sud.
Un **Qubit**, invece, può essere un punto qualsiasi sulla superficie della Terra! Può essere all'equatore, in Italia, in Australia...

Questa rappresentazione si chiama **Sfera di Bloch**.

### 👀 Guardiamo un Qubit "appena nato"
Di default, quando creiamo un Qubit, questo nasce nello stato $|0\\rangle$ (Polo Nord). Verifichiamolo.
""")

nb.add_code("""# Creiamo un circuito con 1 qubit
qc_base = QuantumCircuit(1)

# Eseguiamo la simulazione per vedere lo stato
job = sim_statevector.run(qc_base)
state = job.result().get_statevector()

# Visualizziamo!
plot_bloch_multivector(state)""")

nb.add_markdown("""La freccia blu punta dritta in alto. Questo è lo stato fondamentale. È "sicuramente 0".

---
## 2. La Porta X: Il salto mortale

La prima porta che incontriamo è la **Pauli-X**.
Nel mondo classico, la chiamiamo porta **NOT**. Se entra 0, esce 1.

Nel mondo quantistico, la porta X è una **rotazione di 180 gradi** attorno all'asse X.
Immagina di prendere la sfera e capovolgerla.

❓ **DOMANDA PRELIMINARE:**
Se partiamo dal Polo Nord ($|0\\rangle$) e ruotiamo di 180 gradi, dove finiremo?
*(Pensaci un attimo prima di scorrere)*
""")

nb.add_code("""qc_x = QuantumCircuit(1)
qc_x.x(0)  # Applichiamo la porta X
qc_x.draw('mpl')""")

nb.add_markdown("""Ora vediamo il risultato sulla sfera.""")

nb.add_code("""state_x = sim_statevector.run(qc_x).result().get_statevector()
plot_bloch_multivector(state_x)""")

nb.add_markdown("""Esattamente al Polo Sud ($|1\\rangle$).

### 🧠 Riflessione: Doppia Negazione
Cosa succede se applichiamo **due** porte X di fila?
Classicamente: `NOT(NOT(0)) = 0`.
Quantisticamente: Una rotazione di 180° + un'altra rotazione di 180° = 360° (Giro completo).

Proviamo!
""")

nb.add_code("""qc_xx = QuantumCircuit(1)
qc_xx.x(0)
qc_xx.x(0)
plot_bloch_multivector(sim_statevector.run(qc_xx).result().get_statevector())""")

nb.add_markdown("""Siamo tornati al punto di partenza. In questo caso, l'intuizione classica e quella quantistica coincidono. Ma non durerà a lungo... 😉

---
## 3. La Porta H: Entriamo nella "Bizzarria"

Ecco la porta **Hadamard (H)**. È la porta che crea la magia.
Invece di ruotare di 180° (come la X), la porta H fa una rotazione particolare che porta il Polo Nord... all'**Equatore**!

Precisamente, punta verso l'asse X positivo (fronte a noi). Questo stato si chiama $|+\\rangle$.

$$ H|0\\rangle = |+\\rangle $$

Costruiamo il circuito.
""")

nb.add_code("""qc_h = QuantumCircuit(1)
qc_h.h(0)
qc_h.draw('mpl')""")

nb.add_markdown("""Visualizziamo la sfera.""")

nb.add_code("""state_h = sim_statevector.run(qc_h).result().get_statevector()
plot_bloch_multivector(state_h)""")

nb.add_markdown("""### 🛑 STOP & THINK: Cosa significa?
La freccia non è né su (0) né giù (1). È a metà strada.
In Fisica Quantistica, diciamo che il Qubit è in **Sovrapposizione**.

È come una moneta che sta ruotando sul tavolo. Finché ruota, è sia testa che croce.

#### Cosa succede se la misuriamo?
La misura è l'atto di "fermare la moneta". La natura **deve** decidere. Non può restituirci "metà 0 e metà 1". Deve dire 0 oppure 1.

Poiché siamo esattamente all'equatore (a metà strada tra i poli), la probabilità sarà perfettamente 50/50.

Facciamo un esperimento reale (simulato): lanciamo questa "moneta quantistica" 1000 volte.
""")

nb.add_code("""# Creiamo un circuito con misura
qc_measure = QuantumCircuit(1, 1)
qc_measure.h(0)
qc_measure.measure(0, 0) # Misura il qubit 0 e salva il risultato nel bit 0

# Eseguiamo 1000 volte
job_sim = sim_counts.run(qc_measure, shots=1000)
counts = job_sim.result().get_counts()

plot_histogram(counts)""")

nb.add_markdown("""Guarda il grafico. Dovresti vedere circa 500 volte '0' e 500 volte '1'.
Ogni volta che eseguiamo il codice, il risultato preciso cambierà leggermente (magari 490 vs 510), proprio come nel lancio di monete reali.

**Concetto Chiave:** Il determinismo è morto. A livello fondamentale, l'universo è probabilistico.

---
## 4. Navigare l'Equatore: Le Porte Z, S e T

Siamo all'equatore (stato $|+\\rangle$). Possiamo muoverci lungo l'equatore senza tornare ai poli?
Sì! Possiamo ruotare attorno all'asse Z (l'asse verticale che passa per i poli).

Queste rotazioni cambiano la **Fase** del Qubit.
Immagina la fase come la direzione in cui guarda la freccia mentre sta sull'equatore.

*   **Porta Z**: Rotazione di 180° attorno a Z. Porta dal fronte ($|+\\rangle$) al retro ($|-\\rangle$).
*   **Porta S**: Rotazione di 90° attorno a Z.
*   **Porta T**: Rotazione di 45° attorno a Z.

Proviamo a fare una "passeggiata" sull'equatore.
Partiremo da $|+\\rangle$ (dopo una H) e applicheremo una T, poi una S.
""")

nb.add_code("""qc_rot = QuantumCircuit(1)
qc_rot.h(0) # Andiamo all'equatore (Asse X)

# Visualizziamo dove siamo ora
print("Dopo H (Stato |+>):")
display(plot_bloch_multivector(sim_statevector.run(qc_rot).result().get_statevector()))

# Applichiamo T (45 gradi)
qc_rot.t(0)
print("Dopo T (Rotazione di 45°):")
display(plot_bloch_multivector(sim_statevector.run(qc_rot).result().get_statevector()))

# Applichiamo S (90 gradi)
qc_rot.s(0)
print("Dopo S (Ulteriore rotazione di 90°):")
display(plot_bloch_multivector(sim_statevector.run(qc_rot).result().get_statevector()))""")

nb.add_markdown("""Vedi come la freccia si sposta lungo la "cintura" della sfera?
Nota bene: l'altezza non è cambiata. Siamo sempre all'equatore.
Se misurassimo ORA, avremmo ancora 50% probabilità di 0 e 50% di 1.
La **Fase** non cambia le probabilità di misura (Z), ma è FONDAMENTALE per l'interferenza.

---
## 5. L'Interferenza: La matematica non è un'opinione (o forse sì?)

Ora facciamo l'esperimento più importante. Segui bene i passaggi.

1.  Prendiamo un qubit a 0.
2.  Applichiamo **H**. (Ora è 50/50).
3.  Applichiamo **Z**. (Ruotiamo la fase di 180°. Siamo ancora all'equatore, quindi se misurassimo ora sarebbe ancora 50/50).
4.  Applichiamo **H** di nuovo.

❓ **DOMANDA PER LO STUDENTE:**
Classicamente, se mescolo le carte (H), poi le giro (Z), e poi le rimescolo (H), dovrei avere ancora disordine, giusto?
Dovrebbe uscire ancora 50% e 50%.

Verifichiamo se l'intuizione è corretta.
""")

nb.add_code("""qc_interf = QuantumCircuit(1, 1)
qc_interf.h(0)
qc_interf.z(0)
qc_interf.h(0)

# Disegniamo per essere sicuri
qc_interf.draw('mpl')""")

nb.add_markdown("""Ora misuriamo 1000 volte.""")

nb.add_code("""qc_interf.measure(0, 0)
counts = sim_counts.run(qc_interf, shots=1000).result().get_counts()
plot_histogram(counts)""")

nb.add_markdown("""🤯 **WOW!**
Il risultato è **100% '1'**. (O quasi, escludendo errori di simulazione).
Il caso è sparito. La certezza è tornata.

**Spiegazione Intuitiva:**
Le porte quantistiche manipolano le onde di probabilità.
*   La prima H crea due onde (onda-0 e onda-1).
*   La Z inverte la cresta dell'onda-1 (la fa diventare una valle).
*   La seconda H fa scontrare le onde.
    *   Verso lo 0: Onda e Valle si cancellano (**Interferenza Distruttiva**). Risultato: 0% probabilità.
    *   Verso l'1: Valle e Valle si sommano e si invertono. Risultato: 100% probabilità.

Questo è il cuore degli algoritmi quantistici: creare interferenza distruttiva su tutte le risposte sbagliate affinché rimanga solo quella giusta!

---
## 6. Entanglement: Connessioni Spettrali

Finora abbiamo usato 1 qubit. La vera potenza esplode con 2 o più qubit.
Introduciamo la porta **CNOT (Controlled-NOT)**.

È una porta "SE":
*   SE il primo qubit (Control) è 1 $\\rightarrow$ Gira il secondo qubit (Target) con una X.
*   SE il primo qubit è 0 $\\rightarrow$ Non fare nulla.

### Esperimento A: Qubit Indipendenti
Mettiamo il primo qubit in sovrapposizione (H) e lasciamo il secondo a 0.
Non li colleghiamo.
""")

nb.add_code("""qc_indep = QuantumCircuit(2, 2)
qc_indep.h(0)       # Qubit 0 in sovrapposizione
# Nessuna CNOT qui
qc_indep.measure([0,1], [0,1])

counts = sim_counts.run(qc_indep, shots=1000).result().get_counts()
plot_histogram(counts)""")

nb.add_markdown("""Osserva i risultati: abbiamo circa 50% di `00` e 50% di `01`.
Il primo bit (a destra nella notazione standard qiskit) varia casualmente. Il secondo bit (a sinistra) è sempre 0.
Sono indipendenti.

### Esperimento B: Lo Stato di Bell (Entanglement)
Ora usiamo la CNOT.
Il Controllo è il qubit 0, che è in sovrapposizione (50% 0, 50% 1).
Quindi la CNOT scatta "al 50%".
""")

nb.add_code("""qc_ent = QuantumCircuit(2, 2)
qc_ent.h(0)      # Superposition
qc_ent.cx(0, 1)  # Entanglement! Se q0 è 1, gira q1.

qc_ent.draw('mpl')""")

nb.add_markdown("""❓ **PREVISIONE:**
Quali stati vedremo?
*   Se q0 era 0, la CNOT non fa nulla -> q1 resta 0. Stato finale: **00**.
*   Se q0 era 1, la CNOT inverte q1 -> q1 diventa 1. Stato finale: **11**.

Esisteranno gli stati misti (01 o 10)?
""")

nb.add_code("""qc_ent.measure([0,1], [0,1])
counts = sim_counts.run(qc_ent, shots=1000).result().get_counts()
plot_histogram(counts)""")

nb.add_markdown("""Esattamente! Vediamo solo **00** e **11**.
Le barre centrali (01 e 10) sono vuote.

**Cosa significa?**
Significa che i due qubit si sono "messi d'accordo".
Non importa quanto siano distanti: se misuro il primo e trovo 0, so **istantaneamente** che anche il secondo è 0.

Questa correlazione è più forte di qualsiasi legame classico. Einstein la chiamava "spooky action at a distance" (azione spettrale a distanza) perché sembrava violare la logica che le informazioni viaggiano al massimo alla velocità della luce. (Spoiler: non viola la relatività, perché non possiamo usare questo trucco per mandare messaggi istantanei, ma la correlazione è reale!).

---
### 🏆 Challenge Finale: Il Teletrasporto (Simulato)

Ok, non faremo un vero teletrasporto oggi (è un po' lungo), ma faremo un puzzle di entanglement.

**Obiettivo:** Crea un circuito che generi SOLO gli stati **01** e **10**.
(Ovvero: i due qubit devono essere sempre opposti).

**Indizi:**
1.  Parti dallo stato di Bell che abbiamo appena fatto (H + CNOT), che ti dà 00 e 11.
2.  Come trasformi un 00 in 01? E un 11 in 10?
3.  Ti serve una porta che inverte (X) applicata a UNO solo dei qubit, DOPO l'entanglement (o prima, se sei furbo).

Scrivi il codice qui sotto!
""")

nb.add_code("""# --- SPAZIO PER LA TUA SOLUZIONE ---
qc_challenge = QuantumCircuit(2, 2)

# 1. Crea Entanglement standard
qc_challenge.h(0)
qc_challenge.cx(0, 1)

# 2. Aggiungi la porta magica per invertire uno dei due
# ... scrivi qui ... (Suggerimento: qc_challenge.x(1) ?)

# 3. Misura
qc_challenge.measure([0,1], [0,1])

# Verifica
# counts = sim_counts.run(qc_challenge).result().get_counts()
# plot_histogram(counts)""")

nb.add_markdown("""---
## Conclusione

Oggi hai visto che il mondo microscopico non segue le regole del nostro mondo quotidiano.
*   Le cose possono essere in più stati contemporaneamente (**Sovrapposizione**).
*   Le probabilità possono cancellarsi a vicenda (**Interferenza**).
*   Oggetti separati possono comportarsi come un unico sistema (**Entanglement**).

Questi sono i mattoni con cui costruiremo i computer del futuro, capaci di simulare molecole per nuovi farmaci, ottimizzare traffico e logistica, e rompere i codici crittografici attuali.

Continua a esplorare! Prova a cambiare le rotazioni, aggiungi più qubit, rompi le cose. È il modo migliore per imparare. 🚀
""")

nb.save("Lezione_Porte_Quantistiche.ipynb")
