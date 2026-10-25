# Lezioni dal Mod: bug veri e come il motore li impedisce

> I bug e le trappole veri incontrati dal Mod SWOS 96/97 tra settembre e ottobre 2026 (segnalazioni dei giocatori, note di rilascio, note tecniche e messaggi di Davide in 53 sessioni di lavoro AI del Mod) e, per ognuno: perché è successo, quale regola o controllo del motore lo rende impossibile, e quale test lo blocca per sempre. La maggior parte nasce da un'unica causa: la regola stava nell'ordine del codice o in un limite nascosto dell'exe, invece che in un dato dichiarato e controllato.

Stato: piano, 25/10/2026. Fonti: `release/notes-4.0.md` e `notes-4.0.1.md` del Mod (limiti noti e correzioni), `release/notes-world-2026-27.md`, `notes/CONVENTIONS.md` (insidie 18-19), `notes/domestic-schedule.md`, `notes/sa401-exact-designs.md`, i file di passaggio di consegne in `internal/handoff/` e i messaggi di Davide nelle sessioni SWOS (segnalazioni di giocatori come Pietro, le loro carriere con Siracusa e Mestre, le carriere di prova di Davide). Le primitive rimandano alla parte C (Moduli e catalogo), i livelli di test alla la parte D (Strategia di test).

## 1. Logica delle competizioni

| # | Cosa è successo (Mod) | Perché | Come lo impedisce il motore | Test |
|---|---|---|---|---|
| 1 | Il Milan ha vinto Serie A e Conference League, poi ha giocato l'Europa League (Pietro, 4.0.1) | il posto della vincitrice della Conference è stato applicato dopo, e sopra, quello della campionessa | diritti + un'unica precedenza + garanzie (§3.12) | scenario L3 `league-champion-beats-uecl-winner`; invariante L2 "diritto migliore" |
| 2 | In alcune stagioni un posto europeo andava a un club della federazione sbagliata (limite noto della 4.0) | liste dei posti riempite da più percorsi di codice (un caso precedente nel 1984-85: una lista senza terminatore faceva prendere a una nazione l'ultimo posto di un'altra) | access list risolte tutte insieme; garanzia "posti per federazione = access list" controllata a ogni fine stagione | stagioni casuali L2; golden L4 Mondo 2026-27 |
| 3 | Un club promosso non entrava nella coppa della nuova divisione (Mestre in C senza Coppa Italia di C); la Coppa Italia del Siracusa non partiva dopo la promozione | iscritti delle coppe congelati alla lista 2026-27 | `cup.entrants_from_current_divisions` (§3.13) | scenario L3 promozione + coppa su 2 stagioni |
| 4 | Un club promosso dalla D finiva nel girone A di C invece che nel C (Siracusa) | la promossa prendeva il posto della retrocessa, senza guardare la geografia | `groups.geographic_move` con la mappa `area` dei club; il validatore controlla che ogni club abbia un'area | scenario L3 per area; invariante L2 "club nel girone della sua area" |
| 5 | Un club di Serie D vedeva le competizioni di C e la Coppa Italia; uno di C vedeva la Coppa Italia di A/B | la carriera mostrava tutte le competizioni della nazione | `visibility.real_only` (§3.10) | test L5 delle schermate di carriera |
| 6 | Nei gironi dispari di Serie D il club che riposava all'ultima giornata saltava il suo play-off, deciso per simulazione; una correzione successiva bloccava il fine stagione ed è stata ritirata | il play-off veniva costruito per club dopo la "sua" ultima partita | le fasi finiscono quando finisce la *fase*, non per club (`stage.starts_after`); i gironi dispari sono previsti dall'origine (`round_robin.odd_rest`) | dimensioni dispari L2; L3 "riposo all'ultima giornata" |
| 7 | Argentina: il Clausura è partito mentre si giocavano i play-off dell'Apertura | settimane non riservate alla fase finale | `stage.starts_after` + validatore del calendario (nessun club con due partite in una settimana) | validatore L0; invariante di calendario L2 |
| 8 | Play-off a gara secca mostravano date di ripetizione | posti per le ripetizioni riservati per difetto | `calendar.no_phantom_replays` | L1 generatore di calendario |
| 9 | Finale della Copa do Brasil ai supplementari; la regola vera è rigori subito (dalla 3.2) | un modo di decidere predefinito ereditato | `decider.required`: niente valori predefiniti | il validatore L0 rifiuta un turno senza modo di decidere |
| 10 | CONCACAF Champions Cup: il gioco fa gol in trasferta e poi rigori, la regola vera 2026 è gol in trasferta, supplementari, rigori | un insieme fisso di modi di decidere | `decider` è una lista ordinata | casi L1 dei modi di decidere |
| 11 | Campione di Apertura, Trofeo de Campeones, vincitore dei play-off MLS, doppio vincitore a Malta non visibili da nessuna parte | i titoli decisi oltre la classifica non avevano un'uscita | uscita `titles` + pagina WINNERS (§3.13) | test L5 delle schermate |
| 12 | Punti azzerati a uno split o al cambio di torneo confondevano i giocatori | la schermata mostrava solo il nome del campionato | `display.stage_in_title`, testo FORMAT generato | controllo visivo (L6) |
| 13 | Zona play-off assente dalla classifica mentre "P.OFF" compariva in un angolo; legenda diversa dalle zone colorate | zone e legenda calcolate separatamente | zone e legenda generate entrambe dalle etichette degli esiti (`zones`) | L1 legenda == zone |
| 14 | Terze dei gironi di Libertadores verso lo spareggio di Sudamericana simulate e non giocate (4.0) | passaggio tra coppe fuori dal percorso giocato | porte `cross_cup`; il club in carriera gioca qualsiasi fase in cui entra | scenario L3 `q3-losers-to-sudamericana` e variante terze dei gironi |
| 15 | Nazioni senza nazionale: un montenegrino convocato dalla Jugoslavia | nazionalità associata alla squadra sbagliata | il modulo delle nazionali dichiara le nazionalità convocabili | L1 convocabilità (livello nazionali, più avanti) |
| 16 | Le seconde squadre potevano salire nel campionato della prima squadra | nessuna relazione tra club nei dati | `club.second_team` con regole per nazione | scenari L3 per nazione |

## 2. Limiti nascosti dell'eseguibile del 1996

| # | Limite incontrato | Dove | Come lo evita il motore |
|---|---|---|---|
| 17 | 24 squadre per campionato (tabelle di coppie) | Argentina 30, MLS 30 | nessuna dimensione fissa; generatore per qualsiasi n; il validatore avvisa solo sui limiti dell'interfaccia |
| 18 | Le tabelle dispari non sono vere giornate (una squadra due volte in alcune giornate) | 15, 21 squadre; presenti anche nelle tabelle di OpenSWOS | giornate generate; invariante L2 |
| 19 | Il motore degli split del Mod tiene al massimo 64 giornate per campionato; i calendari veri da 44 giornate di Guatemala, El Salvador e Paraguay non ci sono entrati nella 4.0 | stato degli split | nessuna dimensione fissa |
| 20 | Cache di 100 squadre; salvataggio di carriera = un intervallo fisso di memoria | mondi grandi (4ª divisione inglese + league phase) | stato del motore in campi JSON con nome, niente intervalli di memoria |
| 21 | Il fine stagione controlla "80 iscritti europei" e altrimenti si blocca | fine stagione del 1996 | i conteggi vengono dalle specifiche; il validatore li dimostra prima che la stagione cominci |
| 22 | Nel calcolo della forza di una squadra, un prezzo medio dei giocatori pari a zero (club molto deboli) causava una divisione per zero e il blocco del gioco | calcolo della forza | validazione delle rose (L0); test di proprietà con rose degeneri |
| 23 | I numeri che identificano le nazioni erano gli stessi usati come numeri dei menu: con più mondi di carriera nello stesso exe entravano in conflitto | exe con più mondi | id testuali con spazio dei nomi |

## 3. Processo e test

| # | Cosa è successo | Lezione | Nel nuovo progetto |
|---|---|---|---|
| 24 | Un crash solo nelle build di rilascio (mercato estero), perché i dati di rilascio avevano pool che le build di test non avevano (CONVENTIONS 17a) | si testa sui dati che si distribuiscono | mondi golden sui pack distribuiti, non su dati di test |
| 25 | Un salvataggio fatto con una versione dei dati, rigiocato su un'altra, sembrava un blocco del gioco | le versioni dei dati devono essere esplicite | il salvataggio registra id, versione e hash del pack; se non coincidono, rifiuto con un messaggio |
| 26 | Una riscrittura di testo in un patcher ha saltato in silenzio un hook di caricamento; blocco alla terza stagione (CONVENTIONS 19) | ogni generatore controlla cosa ha cambiato | importatori e generatori di codice verificano i conteggi; il controllo del registro fallisce se manca copertura |
| 27 | Esecuzioni in serie dell'harness condividevano cache di moduli e producevano falsi errori | i test devono essere isolati | ogni test costruisce il suo mondo; nessuna cache condivisa |
| 28 | Casi rari raggiunti rigiocando stagioni, ore perse (Davide: "usa i cheat, non mille tentativi") | forzare, non ritentare | fornitore di risultati scritto a mano (L3) |
| 29 | File di dati condivisi cambiati prima del loro motore, con altri branch rotti | prima il motore, poi i dati | `module.json` dichiara la versione di motore/schema che richiede; il validatore rifiuta dati più nuovi su un motore più vecchio |
| 30 | Regole reinventate a ogni bug ("non reinventiamo la ruota ogni volta", Davide 21/10) | un unico insieme coerente di regole | registro delle primitive; una regola nuova è una pull request revisionata con i suoi test (linee guida) |
| 31 | Caratteri estranei e titoli troppo lunghi per la loro barra | i testi sono dati con dei limiti | il validatore controlla larghezze e caratteri del font |

## 4. Gli schemi dietro l'elenco

1. **Regole che dipendono dall'ordine** (1, 2, 6, 7): il risultato dipendeva da quale codice girava prima. Il motore risolve i fine stagione tutti insieme, con una precedenza dichiarata, e controlla le garanzie.
2. **Dati congelati o mancanti** (3, 4, 16): liste che andavano ricalcolate ogni stagione erano fissate alla prima, o mancava un dato (l'area geografica di un club, il legame tra prima e seconda squadra). Il motore ricava gli iscritti dallo stato attuale a ogni stagione e il validatore pretende i dati che servono.
3. **Valori predefiniti impliciti** (8, 9, 10): comportamenti che nessuno aveva scelto. Lo schema non ha valori predefiniti per le regole che cambiano da competizione a competizione.
4. **Uscite mancanti** (5, 11, 12, 13): il motore sapeva qualcosa che il giocatore non poteva vedere. Ogni titolo, zona e regola di visibilità è un'uscita della specifica, e le schermate la leggono.
5. **Limiti nascosti** (17-23): dimensioni fissate nel 1996. Il motore non ne ha; il validatore avvisa solo dove l'interfaccia ha un limite vero.
6. **Percorsi non testati** (24-28): test che giravano su altri dati o si affidavano alla fortuna. I test girano sui dati distribuiti, sono isolati e forzano i loro casi.
7. **Regole di processo** (29-31): versioni dei dati, regole reinventate, testi fuori misura. Il motore li affida al validatore e al registro delle primitive.
