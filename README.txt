Progetto Tesi Danilo Montalbano

Contenuto cartelle:
	* cau_ml_tools
		
		Strumenti per la creazione di modelli e dataset necessari per allenare gli algoritmi di machine learning e deep learning utilizzati.

	* cau_rest_server

		Server API REST che permettono l'ottenimento delle informazioni derivate dagli algoritmi di machine learning. Usa il framework FastAPI

		PORTA: 8000
		HOST: localhost

		Per altre info, leggere i README di ogni cartella.

	*ml-folders-chiedi-ad-unime
		
		Cartella contenente già alcuni modelli trainati e alcuni dataset creati. Sono sufficienti per fare tutti gli esempi necessari per il corso di Informatica.

		Nei file config.yaml si dovrà specificare dove questa cartella deve andare:
		es: PATH: C:\Users\Danilo\Documents\ml-folders-chiedi-ad-unime

		Attenzione: se una cartella non è stata definita come root per la creazione delle sottocartelle (vedere in ml-folders-chiedi-ad-unime)
			gli script daranno errore. 