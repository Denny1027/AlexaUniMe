## AlexaUniMe
Progetto -> creazione skill per Alexa riguardo le Frequently Asked Question

Questo è il branch di sviluppo della skill Alexa "Chiedi ad UniMe".

# Bug conosciuti
1. Durante la fase di `<intentConfirmation>`, se si risponde "si", lo considera come una entità di uno slot (non si sa quale) e lo sovrascrive all'entità inserita in precedenza, richiedendo conferma.

# Task list
- [ ] Risolvere bug 1 
