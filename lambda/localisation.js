/*
    Attraverso questo file, è possibile creare stringhe di risposta in diversi linguaggi. Si deve aggiungere all'oggetto module.exports un altro oggetto con chiamato con l'abbreviazione della lingua
    (es. en)  con all'interno le stesse chiavi con il valore nella relativa lingua (es. WELCOME_BACK_MSG: `Welcome back!`)
*/

module.exports = {
    it: {
        translation: {
            WELCOME_MSG: `Benvenuto in "Chiedi ad ùNIME"! Di quale dipartimento fai parte? `,
            WELCOME_BACK_MSG: [`Bentornato!`,`Ciao!`,`Hey!`],
            HCIHY_MSG: [`Come posso essere d'aiuto?`,`Come posso aiutarti?`],
                //Cosa chiedere?
                WHATASK_MSG: `Io posso risponderti a domande sull'ISEE, sui Certificati e sulle Immatricolazioni.`,
                //Certificati come richiedere
                CERT_HOW_REQ_MSG: `Per richiedere un certificato, devi collegarti al sito ùNIME nella sezione studenti, in alto a destra. Successivamente bisogna cliccare su "Iscrizioni" e poi su "Modulistica e Documentazione". Li troverai il modulo di "Richiesta certificati". Tale modulo va compilato e inviato all'indirizzo email "protocollo@unime.it. "`,
                //Certificati - Chi può usufruire del diploma supplement
                CERT_WHO_DS_MSG: `Il Diploma supplement è previsto soltanto per i laureati triennali specialisti e per i laureati triennali magistrali. `,
                //Certificati - Come richiedere il diploma supplement
                CERT_HOW_REQ_DS_MSG: `Per richiedere il Diploma Supplement, devi collegarti al sito ùNIME e scaricare il modulo "Richiesta certificati". Tale modulo va compilato inserendo la dicitura “Diploma Supplement” e inviato a protocollo@unime.it. Se non sai dove trovare il modulo, chiedimi come richiedere un certificato. `,
                //Certificati - Cosa è il diploma supplement
                CERT_WHAT_DS_MSG:`Il Diploma Supplement è un documento integrativo del titolo di studio ufficiale, conseguito al termine di un corso di studi in una università o in un istituto di istruzione superiore. Il DS fornisce una descrizione della natura, del livello, del contesto, del contenuto e dello status, degli studi effettuati e completati dallo studente. `,
                //Certificati - Dove Ritirarli
                CERT_WHERE_MSG: `Potrai ritirare il certificato portando 2 marche da bollo da sedici euro, allo sportello di competenza, sito al Palazzo Mariani, in Piazza Antonello, Lunedì, Mercoledì e Venerdi dalle 8 e 30 alle 12 e 30, e il Martedì e Giovedì dalle 14 e 30 alle 16. `,
                //Certificati - laurea in lingua inglese
                CERT_ENGL_GRAD_MSG: `L’università degli Studi di Messina può rilasciare il certificato di laurea anche in lingua inglese, solo con il voto finale. Esso è soggetto all’imposta di bollo di 16 euro, sia nella richiesta che nel certificato. `,
                //Certificati - Bollo Diploma Supplement
                CERT_DS_STAMP_MSG: `Poichè il DS vieni rilasciato in carta semplice, non ha bisogno di marca da bollo. Esso non è un vero e proprio "certificato", bensì è formalmente una "relazione informativa". `,
                //Certificati - Quando avvalermi
                CERT_WHEN_MSG: `L'autocertificazione è da produrre solamente nei confronti della Pubblica Amministrazione e dei gestori di pubblici servizi. Questo modello si trova tra i certificati, oppure è possibile scaricare l'autocertificazione direttamente da ESSE 3. Se non sai dove trovare i certificati, chiedimi come richiedere i certificati. `,
                
                ///////// FINE CERTIFICATI //////////
                //Immatricolazioni - Esoneri (Unione esoneri e esoneri 100)
                IMM_EXON_MSG: `Per gli studenti che hanno conseguito in Italia il diploma di maturità nell’anno di immatricolazione la votazione di 100 o di 100 con lode, persone con disabilità, persone appartenenti allo stesso nucleo familiare, o persone che si iscrivono ad anni successivi al 1° in presenza di determinati requisiti legati al merito e al reddito, sono previsti esenzioni dal pagamento del contributo onnicomprensivo annuale. è possibile verificare tutti i prerequisiti nella sezione "No tax area" all'interno della pagina "Immatricolazioni e Iscrizioni". `,
                //Immatricolazioni - Come immatricolarsi
                IMM_HOW_MSG: `Per immatricolarsi al primo anno di corso di tutte le lauree triennali, a ciclo unico e magistrali, ad accesso libero e ad accesso programmato, bisogna collegarsi al sito web dell'università, cliccare sulla voce "Futuri Studenti", in alto a destra, cliccare su "Immatricolazione", e seguire tutti i passaggi proposti. `,
                //Immatricolazioni - cosa fare per immatricolarsi
                IMM_WHAT_MSG: `Per coloro che si iscrivono per la prima volta ad uno dei corsi di laurea dell'università degli studi di Messina, dovranno effettuare la registrazione, inserendo i propri dati personali. Dopo aver compilato tutti i campi e, dopo aver confermato l'iscrizione, è necessario concludere la fase di registrazione cliccando su "Procedi con l'autenticazione". E' possibile stampare un promemoria dell'iscrizione cliccando sull'omonimo pulsante. `,
                //Immatricolazioni - Esenzioni per persone con disabilità
                IMM_DIS_EXO_MSG: `Gli studenti con disabilità Sono esonerati dal pagamento del contributo onnicomprensivo annuale per l’anno accademico corrente. Dovranno versare, quindi, esclusivamente l’importo della tassa regionale per il diritto allo studio con marca da bollo, pari a 156 euro. `,
                //Immatricolazioni - Stesso nucleo familiare
                IMM_SAME_FAM_MSG: `Gli studenti iscritti appartenenti allo stesso nucleo familiare godranno, sul pagamento del contributo annuale onnicomprensivo, di una riduzione fino a 80 euro per il secondo componente e fino a 150 euro dal terzo componente in poi, a condizione che siano regolarmente iscritti per l’anno accademico corrente  e abbiano presentato ciascuno il proprio ISEE-U. Gli stessi saranno tenuti al pagamento della tassa regionale per il diritto allo studio. `,
                //Immatricolazioni - Laurea magistrale
                IMM_MAST_MSG: `Per accedere ad un Corso di Laurea Magistrale devi collegarti sul sito ùnime e selezionare nel menù "Didattica" la voce "Offerta Formativa". In questa pagina potrai trovare tutti i corsi offerti dall'università di Messina. Una volta scelto il corso, leggere le istruzioni sui requisiti di accesso e sull'immatricolazione. ` ,
                //Immatricolazioni - Metodo di pagamento
                IMM_PAYMENT_MODE_MSG: `è possibile pagare l'immatricolazione e tutte le altre tasse attraverso il portale esse 3. Qui si potrà scegliere se pagare attraverso il sistema PagoPA® scegliendo tra carta di creito, di debito, o prepagata, oppure attraverso un bonifico bancario. `, 
                //Immatricolazioni - Rateizzazione pagamento
                IMM_PAYMENT_INSTALLMENT_MSG: `Durante la fase di immatricolazione, potrai scegliere se rateizzare il pagamento in due o in quattro rate. `,
                //Immatricolazione - Quanto pagare
                IMM_HOW_MUCH_MSG: `L'importo standard per l'immatricolazione di tutte le categorie di studenti, consiste nel versamento complessivo di 156 euro, di cui 140 euro di tassa regionale per il diritto allo studio, e 16 euro per il bollo virtuale. `,
                //Immatricolazioni - Numero programmato
                IMM_CLOSED_NUM_MSG: `Va effettuata una pre-iscrizione, tassativamente entro i termini previsti dal relativo bando.`,
                //Immatricolazioni - Non ammesso quindi altro corso
                IMM_OTHER_COURSE_MSG: `Hai la possibilità di immatricolarti in un altro Corso di Studi ad accesso libero, magari in una classe di laurea affine, per poi riprovare i test l'anno successivo, qualora successivamente fosse ammesso , e potresti chiedere il riconoscimento degli esami già sostenuti in comune tra i due corsi.`,
                //Immatricolazioni - Rinnovo anni successivi
                IMM_RENEWAL_MSG: `Se sul portale ESSE 3, alla voce "Iscrizioni", non c'è il bottone "Modifica Ultima Iscrizione", allora si deve mandare  o la segnalazione alla Segreteria Studenti di appartenenza, oppure tramite mail a protocollo@unime.it con la propria e-mail istituzionale, indicando nome, cognome, matricola e corso di studi. `,
                
                ///////// FINE IMMATRICOLAZIONI //////////
                //ISEE - Cos'è
                ISEE_WHAT_MSG: `L'ISEE è l’Indicatore della Situazione Economica Equivalente dei soggetti che richiedono prestazioni sociali agevolate, e si ottiene combinando e valutando tre elementi : il reddito, il patrimonio, e la composizione del nucleo familiare. L'isee da utilizzare per l'università prende il nome di ISEE-U. `,
                //ISEE - Utilità
                ISEE_USE_MSG: `L’ISEE-U, o ISEE Università, serve ad usufruire delle prestazioni agevolate per il diritto allo studio universitario.`,
                //ISEE - ISEE-U Università
                ISEE_UNI_MSG: `Per ottenere l’attestazione ISEE-U, si deve compilare la Dichiarazione sostitutiva unica, o DSU integrale, comprensiva del modulo MB2, scaricabile dal sito dell’Inps. La DSU contiene informazioni sul nucleo familiare e sui redditi e patrimoni di ogni suo componente. Deve essere compilata e presentata presso il CAF, il Comune, o all'INPS, anche per via telematica. L'ente al quale è stata presentata la DSU, comunica allo studente quando l'attestazione ISEE-U è elaborata dall'INPS. Poiché per la presentazione della DSU, sono richieste informazioni relative ai patrimoni mobiliari e immobiliari, e poiché l’ottenimento delle relative attestazioni può richiedere diversi giorni, si invitano gli studenti ad adoperarsi in tempo utile per la presentazione della DSU, rivolgendosi se del caso ai CAF, che forniranno tutte le informazioni utili all’ottenimento dell’ISEE Università.`,
                //ISEE - Modalità di acquisizione
                ISEE_ACQUISITION_MSG: `Dopo aver fornito il consenso, i dati saranno migrati automaticamente dalla banca dati dell’INPS. Per poter fornire il consenso, bisogna andare su esse 3, alla voce "Segreteria" e poi a quella "Isee Università". `,
                //ISEE - Come Funziona (usufruirne)
                ISEE_HOW_WORKS_MSG: `Durante la procedura di immatricolazione/iscrizione occorre esprimere il consenso all’acquisizione dei propri dati dalla banca dati INPS. `,
                //ISEE - Non mi avvalgo
                ISEE_NO_AVAIL_MSG: `Per chi non intende avvalersi della riduzione delle tasse e che, quindi, non autorizzano l’Ateneo ad acquisire i propri dati isee dalla banca dati inps, devono spuntare il flag di "non consento" durante la procedura on-line di immatricolazione iscrizione. `,
                //ISEE - Problemi con consenso
                ISEE_PROBLEMS_MSG: `Qualora esistano dei problemi con la selezione relativa al consenso, è necessario mandare un’istanza a protocollo@unime.it al fine di segnalare l’anomalia presente. `,
                //ISEE - Dopo scadenza acquisizione
                ISEE_EXPIRE_MSG: `La scadenza viene fissata annualmente con delibera del Consiglio di Amministrazione Immatricolazioni e iscrizioni. Dopo la scadenza, è necessario pagare una tassa di revisione di 100 euro. `,
                
            REJECTED_DIP_MSG: `Ripetere il dipartimento`,
                
            FALLBACK_MSG: `Perdonami, penso di non aver capito bene. Riprova. `,
            HELP_MSG: `Il mio compito è quello di rispondere alle tue domande. Temporaneamente posso risponderti a domande relative l'ISEE, le certificazioni e le immatricolazioni. Per iniziare, fammi qualche domanda! `,
            REPROMPT_MSG: `Se non sai cosa fare, prova a chiedermi aiuto. Se vuoi uscire dalla skill dimmi pure stop. Cosa vuoi fare? `,
            
            GOODBYE_MSG: `Spero di esserti stata d'aiuto! A presto! `,
            REFLECTOR_MSG: `Hai invocato l'intento {{intent}} `,
            ERROR_MSG: `Scusa, c'è stato un errore. Riprova. `
            
        }
    }
}
