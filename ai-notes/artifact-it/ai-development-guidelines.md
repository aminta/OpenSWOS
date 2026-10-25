# Linee guida per lo sviluppo con AI

> Come devono lavorare le sessioni AI nel nuovo progetto: prima l'architettura e la specifica, poi i test, solo dopo il codice; pull request piccole e revisionate da una persona; niente patch di binari né reverse engineering senza una domanda precisa; tutto deterministico; documentazione aggiornata nello stesso commit del codice; appunti di contesto in `ai-notes/` per non ricaricare tutto a ogni sessione.

Stato: proposta, 25/10/2026. Vale per il lavoro sul motore delle competizioni e sui data pack. Le regole di OpenSWOS in `.claude/CLAUDE.md` (compilano entrambi i target, i panic sono segnali, struct tipizzate, salvataggi a campi con nome) valgono per intero in aggiunta a queste.

## 1. Ordine di lavoro: architettura, specifica, test, codice

1. **Prima il contratto.** Ogni modifica parte dallo schema, dall'header dell'API o dal documento di progetto che tocca. Se il contratto non copre la modifica, la prima pull request cambia il contratto (documento + schema + validatore) e viene revisionata da sola.
2. **Il test prima del codice**: un frammento di specifica + seme + risultato atteso (golden file o asserzione). Una regola di formato è "fatta" solo quando senza di essa un test fallisce.
3. **Poi il codice**, il minimo che fa passare il test, dentro il modulo a cui l'architettura lo assegna (motore della fase, valutatore dei criteri di parità, motore dei sorteggi, risolutore dei link...). Nessun ramo per nazione: una particolarità di una nazione è un dato, oppure una regola nuova *con un nome* usabile da tutte.

## 2. Pull request piccole e revisionate

- Un argomento per pull request (una regola, un tipo di fase, un data pack, un refactor). Obiettivo: meno di ~400 righe di codice cambiate; i data pack possono essere più grandi ma non contengono codice.
- Ogni pull request dice: quale contratto implementa, quali test lo dimostrano, quali golden file cambiano e perché. Un golden file non cambia mai "per caso".
- Una persona revisiona e fa il merge. Le sessioni AI non pushano mai su branch condivisi, non fanno merge, non aprono pull request o issue upstream senza l'ok esplicito del maintainer in quella sessione.

## 3. Niente patch di binari, niente reverse engineering senza limiti

- Il motore si scrive dalla sua specifica, in C, nell'albero dei sorgenti. Niente patch esadecimali, niente spazi liberi nel codice, niente accesso alle strutture per offset di byte, niente trucchi "questa etichetta è l'etichetta successiva".
- Il reverse engineering del gioco originale è ammesso solo come **ricerca delimitata** con una domanda e una risposta scritta: "quali criteri di parità usava il gioco del 1996?" diventa una nota con i riferimenti a `SWOS2.s` / `swos.asm`, poi una specifica. Il port fedele resta il riferimento per il comportamento originale; il nuovo motore non imita mai un layout di byte.
- I formati reali vengono da fonti citate (regolamenti, documenti delle federazioni, pagine Wikipedia con la loro revisione), registrate accanto ai dati.

## 4. Il determinismo è una regola rigida

- Niente orologio, niente `rand()`, niente virgola mobile nelle decisioni, niente iterazione su contenitori senza ordine o per ordine di puntatore. La casualità passa solo dal generatore del motore, con uno scopo dichiarato (flusso separato).
- Stesse specifiche + stesso seme + stessi risultati = uscita della stagione identica byte per byte su ogni target (SDL 32/64 bit, Amiga). L'integrazione continua esegue i golden test su almeno due target.
- I comportamenti che dipendono dai risultati si testano **forzando** i risultati con il fornitore automatico, mai rigiocando con semi diversi sperando nel caso giusto (regola del Mod, CONVENTIONS 15).

## 5. Documentazione allineata

- Una modifica di comportamento aggiorna, nello stesso commit: lo schema o il documento dell'API, il testo della regola per i giocatori (generato da `swc-explain` dove possibile) e il registro delle modifiche. I documenti per sviluppatori stanno in `docs/`; gli appunti di lavoro per le sessioni AI in `ai-notes/`, che non sostituiscono mai `docs/`.
- Ogni termine nuovo si definisce al primo uso. Ogni documento ha una riga di stato datata (la convenzione di `docs/INDEX.md` di OpenSWOS) ed è elencato in `docs/INDEX.md`.

## 6. Disciplina del contesto per le sessioni AI

- Si parte da `ai-notes/README.md`: elenca lo stato attuale, le decisioni prese e le domande aperte in poche centinaia di righe, così una sessione non rilegge tutto il codice.
- Il codice si legge in modo mirato (grep, letture puntuali); ogni fatto nuovo che vale la pena tenere diventa una riga in `ai-notes/` con il suo `percorso:riga` e il commit in cui era vero.
- Alla fine di un blocco di lavoro si aggiorna `ai-notes/` (stato, prossimo passo) prima di fermarsi, così la sessione successiva riparte dalla nota e non dalla trascrizione.

## 7. Definizione di "fatto" (lista per ogni pull request)

- Il contratto (schema / API / documento) copre la modifica, aggiornato in questa pull request se serve
- Il validatore accetta i dati nuovi e rifiuta un esempio rotto (test incluso)
- Test unitari e golden file passano sulle build SDL e Amiga; i golden cambiati sono spiegati
- Nessuna nazione, competizione o club nuovo cablato nel codice del motore
- Niente virgola mobile, orologio o iterazione senza ordine nei percorsi di decisione
- Documenti (`docs/`) e appunti (`ai-notes/`) aggiornati; documento nuovo elencato in `docs/INDEX.md`
- Licenza e fonte di ogni dato nuovo registrate nel file dei crediti del pack
