## Denny Test Skill
Questa skill è stata creata per eseguire dei test su nuove funzionalità, senza intaccare direttamente la skill principale.


# Obiettivi
* **Abilitare l'Account Linking alla Skill "Chiedi ad Unime":** ogni utente in questa maniera può autenticarsi ed avere una esperienza modellata sulla propria persona e carriera universitaria. Per abiltiarlo, sono necessari:
  * WEB Authorization URI
  * Access Token URI
  * Client ID
  * Secret ID
  * Scopes*
  * Domain List*
  * Default Access Token Expiration Time
* **Definire degli obiettivi per l'uso di algoritmi di machine learning in ambito universitario:** Questa fase si divide in 3 parti:
  * Definizione degli obiettivi: trovare le domande a cui rispondere con il machine learning
  * Analisi: individuare le metodologie di machine learning da applicare
  * Ottenimento dei dati: attraverso uno strumento dedicato, ottenere in modo automatizzato le informazioni necessarie per il training (e il testing) degli algoritmi di machine learning pre-definiti
  * Testing e distribuzione nel server (vedi passo successivo): creazione package e distribuzione
* **Creare un server per la definizione di API REST neccessarie per l'ottenimento di informazioni derivanti dagli algoritmi di machine learning sopra citati:** l'idea è quella di utilizzare Python per la creazione di questo server, più nello specifico usando il framework `fastAPI` (https://fastapi.tiangolo.com/). La creazione del server può avvenire esclusivamente nel momento in cui gli algoritmi di machine learning sono già pronti per l'uso.
* **Creare delle skill Alexa che utilizzino le API appena create**

