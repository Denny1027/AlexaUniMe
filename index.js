const Alexa = require('ask-sdk-core');    //istanziazione alexa sdk 
//nel caso in cui vogliamo INTERNAZIONALIZZARE IL CODICE dobbiamo istanziare anche i18next
const i18next = require('i18next');

//SUCCESSIVAMENTE dobbiamo creare un "language strings object"

const languageStrings = {
    'us' : {
        'translation' : {
            WELCOME_MSG: "Welcome. Say Good Morning",
            MORNING_MSG: "Shit morning maaaaaan"
        }
    },
    'it' : {
        'translation' : {
            WELCOME_MSG: "Benvenuto, dici la parola Buongiorno",
            MORNING_MSG: "Buongiorno sta ceppa"
        }
    }
}
/*
    Tutti gli handler (di default o personali) si presentano sotto questa forma.
    sono tutte costanti e presentano sempre DUE METODI di base:
    canHandle(handlerInput) -> Determina se l'utente ha richiamato il giusto intento
    handle(handlerInput) -> Determina cosa c'è bisogno per rispondere alla richiesta

*/
const LaunchRequestHandler = { 
    canHandle(handlerInput) = {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'LaunchRequest';
    },
    handle(handlerInput) {
        const speakOutput = 'Benvenuto, come posso esserti daiuto?';
        /* QUESTO VALE CON L'INTERCEPTOR
        const speakOutput = handlerInput.t('WELCOME_MSG'); 
        */
        return handlerInput. responseBuilder
            .speak(speakOutput)  //aggiunta del metodo speak con il testo come argomento
            .reprompt(speakOutput) //tiene la sessione aperta e attende un input dall'utente
            .getResponse();
    }
}

/*
    Esistono Handler extra per questioni di debug
*/



/*
   REQUEST INTERCEPTOR (PER INTERNAZIONALIZZAZIONE)
*/

const LocalisationRequestInterceptor = {
    process(handlerInput) {
        i18next.init({
            lng: Alexa.getLocale(handleInput.requestEnvelope),
            resources: languageStrings  //si rifà all'oggetto creato con le traduzioni
        }).then((t) => {
            handlerInput.t = (...args) => t(...args);
        });
    }
};

// SKILL BUILDER 
exports.handler = Alexa.SkillBuilders.custom()
    .addRequestHandlers(
        LaunchRequestHandler,
        HelloWorldIntentHandler,
        HelpIntentHandler,
        CancelAndStopIntentHandler,
        SessionEndedRequestHandler,
        IntentReflectorHandler, // make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
    )
    /*              */
    .addRequestInterceptors(LocalisationRequestInterceptor) //QUESTA SOLO SE SI USA L'INTERCEPTOR
    /*              */
    .addErrorHandlers(
        ErrorHandler,
    )
    .lambda();