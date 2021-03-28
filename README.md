## Denny Test Skill
Questa skill è stata creata per eseguire dei test su nuove funzionalità, senza intaccare direttamente la skill principale.


# Bug conosciuti
1. In `impostaNumeroNotizieIntent`, nello slot `newsNumber`, impostare il set [1,2,3] di valori inseribili. In questo momento, puoi inserire qualunque valore.

# Task list
- [ ] Risolvere bug 1
- [x] Creare bucket su amazon S3
- [x] Collegare bucket S3 a lambda function `denny_test_lambda`
- [x] Creare lambda function `periodic_rubrica` che permette la creazione di un file `rubrica.json` all'interno del bucket `dennytestalexabucket`

## Risultato
La lambda function accetta esclusivamente file **.zip**, sia come upload diretto (da interfaccia Lambda), sia da un bucket **S3**, quindi non è possibile creare un bucket, inserire i singoli file e dipendenze e *linkare* il bucket alla Lambda Function, in modo da indicargli quale file caricare per primo (dovrebbe essere *index.js*). 
In questo modo, va a cadere anche l'idea di utilizzare una "Lambda" di supporto che permetta l'esecuzione periodica (mezzanotte di ogni giorno) di uno script che crei un file *.json* all'interno del bucket S3 (utilizzato dalla Lambda function della skill di Alexa), in modo di "alleggerire" il carico riguardo la richiesta all' API di **tutta** la rubrica ( 43k righe, 1.5s esecuzione).
