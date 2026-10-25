# Glossario e guida alla lettura

> Il documento ha sei parti: **A** (Competizioni oggi) racconta come funzionano oggi campionati e coppe in OpenSWOS, nel gioco DOS originale e nel Mod; **B** (Proposta del motore) propone un motore delle competizioni separato dal gioco; **C** (Moduli e catalogo) spiega come aggiungere o togliere campionati e coppe ed elenca tutte le regole; **D** (Strategia di test) dice come si verifica tutto questo; **E** (Lezioni dal Mod) elenca i bug veri del Mod e come il motore li evita; **F** (Linee guida AI) dice come devono lavorare le sessioni AI. Chi conosce il calcio ma non il codice può leggere B, C ed E saltando i riferimenti `file:riga`, che servono solo a chi apre i sorgenti.

## I progetti e le persone

| Nome | Chi o cosa |
|---|---|
| **SWOS 96/97** | Sensible World of Soccer 96/97, il gioco originale per DOS (1996) |
| **il Mod** | la modifica di SWOS 96/97 curata da Davide Lorigliola (aminta/swos-9697-mod, sito worldofswos.com): mondi di carriera storici e il Mondo 2026-27 con le competizioni reali |
| **versioni del Mod** | 3.x = mondi storici (Europa 1984-85, stagioni storiche); 4.0 = Mondo 2026-27 (22/10/2026); 4.0.1 = la prima correzione (25/10/2026); 4.0.2 = la prossima |
| **OpenSWOS** | il rifacimento in C, open source (GPL), della versione Amiga di SWOS, di Ben Baker; usa i dati della copia del gioco del giocatore |
| **Ben Baker** | autore e maintainer di OpenSWOS |
| **Playaveli** | responsabile del progetto SWOS 2020 (che OpenSWOS continua), l'interlocutore di Davide sulla convergenza |
| **Zlatko Karakaš** | autore di SWOS++ e della ricostruzione del codice della versione DOS, la fonte principale per capire il gioco originale |
| **Pietro, Angelo, Marco** | giocatori del Mod che hanno segnalato bug o mandato dati |
| **DaniSwos** | autore del database 1984-85 usato dal Mod |
| **sessioni di lavoro AI** | le conversazioni con Claude che sviluppano il Mod (Regia, Integratore, Serie C, Coppe nazionali...) |

## Termini tecnici

| Termine | Significato |
|---|---|
| **API** | l'elenco delle funzioni che il motore offre al gioco, con i loro ingressi e uscite |
| **access list** | la tabella che dice quanti posti in una coppa continentale ha ogni federazione e per quali posizioni |
| **backtracking** | ricerca che, quando una scelta porta a un vicolo cieco, torna indietro all'ultima scelta valida (come in un sudoku) |
| **branch, commit, merge, push** | una linea di lavoro separata; una modifica registrata; l'unione di due linee; l'invio delle modifiche al repository online |
| **byte, offset, esadecimale** | un byte = un numero da 0 a 255; offset = la posizione contata dall'inizio di un blocco; esadecimale = numeri scritti in base 16 (`0x50` = 80) |
| **C, C99** | il linguaggio in cui è scritto OpenSWOS; C99 è la sua versione standard del 1999, compilabile anche per Amiga |
| **callback** | una funzione che il gioco presta al motore, per rispondere alle sue domande (es. "che risultato ha fatto questa partita?") |
| **CONVENTIONS N** | il punto N delle regole del Mod, nel file `notes/CONVENTIONS.md` |
| **data pack / modulo** | una cartella di dati (competizioni, club, nomi) che si aggiunge a un mondo |
| **deterministico** | che dà sempre lo stesso risultato a partire dagli stessi dati e dallo stesso seme |
| **dichiarativo** | descritto con dati che dicono *cosa vale* (squadre, turni, regole), lasciando a un programma unico il *come* |
| **end-to-end** | test che fa girare il gioco intero, come lo usa un giocatore |
| **fornitore automatico / scritto a mano** | il primo inventa risultati plausibili dal seme e dal numero della partita (per i golden file); il secondo impone esattamente i risultati di uno scenario |
| **GPL, MIT/BSD, LGPL, CC BY-SA** | licenze: GPL obbliga a distribuire il codice dei derivati con la stessa licenza; MIT/BSD permettono quasi tutto citando l'autore; LGPL è una via di mezzo per le librerie; CC BY-SA chiede attribuzione e stessa licenza |
| **golden file** | l'uscita attesa di una simulazione, salvata e confrontata a ogni modifica: se cambia, va spiegato perché |
| **harness** | il programma che guida il gioco da solo (tasti, lettura della memoria) e controlla i risultati |
| **hash** | un calcolo che da un dato produce sempre lo stesso numero; usato per riconoscere versioni e per risultati di prova riproducibili |
| **hook** | punto in cui si aggancia codice nuovo a un passaggio del gioco |
| **integrazione continua (CI)** | i test girano da soli a ogni modifica inviata al repository |
| **JSON, YAML, JSON Schema** | formati di testo per dati strutturati, leggibili da persone e programmi (YAML è più leggibile); uno JSON Schema descrive quali campi un file JSON può avere |
| **league phase (sistema svizzero)** | classifica unica in cui ogni squadra incontra solo alcune avversarie sorteggiate (Champions League dal 2024-25) |
| **libreria** | codice riusabile da più programmi |
| **macchina a stati** | la parte del motore che sa a che punto della stagione si è e cosa viene dopo |
| **panic** | arresto volontario del gioco con un codice di errore, quando trova uno stato impossibile |
| **patch, stub** | modifiche inserite direttamente nell'eseguibile; lo stub è un piccolo pezzo di codice macchina messo in uno spazio libero |
| **poke, `*_FORCE`** | trucchi del Mod per forzare un caso nei test: scrivere direttamente nella memoria del gioco, o compilare un exe speciale |
| **porta** | un'uscita con nome di un modulo (es. `mex.liga-mx:apertura.champion`) che altri moduli possono leggere |
| **primitiva** | una regola del motore con un nome, campi JSON, test e un testo che la spiega |
| **pull request** | una proposta di modifica che una persona rivede prima di accettarla |
| **record** | il blocco di dati a struttura fissa con cui il gioco del 1996 descrive una competizione |
| **runtime** | mentre il gioco sta girando |
| **scenario** | un piccolo file di test che impone una situazione e dice cosa deve succedere |
| **seme (seed)** | il numero di partenza del generatore casuale: stesso seme, stessi sorteggi |
| **test unitario / di proprietà** | il primo controlla una sola regola con dati fissi; il secondo genera molti casi casuali e verifica che certe condizioni valgano sempre |
| **upstream** | il repository originale (qui: benbaker76/OpenSWOS), da cui il fork di Davide deriva |
| **validatore** | lo strumento che controlla i dati prima di giocare (porte, conteggi, piramide, calendario, nomi) |

## Sigle di competizioni e leghe

| Sigla | Significato |
|---|---|
| UCL, UEL, UECL | UEFA Champions League, Europa League, Conference League |
| ACL | AFC Champions League (Asia) |
| CCC | CONCACAF Champions Cup (Nord e Centro America) |
| CONMEBOL, CONCACAF, AFC, CAF, OFC | confederazioni di Sud America, Nord e Centro America, Asia, Africa, Oceania |
| EFL | English Football League (Championship, League One, League Two) |
| LPF | Liga Profesional de Fútbol (Argentina) |
| CPL | Canadian Premier League |
| MLS | Major League Soccer (USA e Canada) |
| Reducido | il play-off promozione della Primera Nacional argentina |
| cuadrangulares | i gironi finali da quattro squadre del campionato colombiano |
| liguilla | la fase finale a eliminazione del campionato messicano |
| promedio | la media punti delle ultime stagioni usata in Argentina per le retrocessioni |
