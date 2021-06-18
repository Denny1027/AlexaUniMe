Moduli installati per il funzionamento del server

pip3 install [module]

- fastapi
- uvicorn[standard]
- python-multipart (already installed)

Moduli installati per il funzionamento degli algoritmi ML/DL

-pandas
-tensorflow
-numpy
-scipy
-sklearn
-scikit-learn

Per credenziali di accesso alle API, per impostare le credenziali per l'accesso a queste API e per impostare
il path assoluto dove si vanno a cercare i moduli e i dataset sono definiti in config.yaml.
-----------------
!IMPORTANTE!
-----------------
Configurare il file config.yaml:
PATH: Percorso assoluto dove caricare le informazioni necessarie agli algoritmi creati.

S3_CRED: username e password per usare API S3 UNIME

SERVER_CRED: definire username e password per l'accesso ai servizi offerti dal server.

COME AVVIARE IL SERVER

da console, scrivere
    uvicorn main:app --reload

-----
CAMBIARE HOST E PORT DEL SERVER
	guarda nel file main.py
