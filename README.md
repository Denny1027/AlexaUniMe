## Denny Test Skill
Questa skill è stata creata per eseguire dei test su nuove funzionalità, senza intaccare direttamente la skill principale.


# Bug conosciuti
1. In `impostaNumeroNotizieIntent`, nello slot `newsNumber`, impostare il set [1,2,3] di valori inseribili. In questo momento, puoi inserire qualunque valore.

# Task list
- [ ] Risolvere bug 1
- [ ] Creare bucket su amazon S3
- [ ] Collegare bucket S3 a lambda function `denny_test_lambda`
- [ ] Creare lambda function `periodic_rubrica` che permette la creazione di un file `rubrica.json` all'interno del bucket `dennytestalexabucket`
