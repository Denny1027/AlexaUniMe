'use strict';

//import ask-sdk-core
const Alexa = require('ask-sdk-core');
//const persistenceAdapter = require('ask-sdk-dynamodb-persistence-adapter');
const persistenceAdapter = getPersistenceAdapter(); //migliore rispetto a quello precedente! Vedere funzione
//include apiReq.js
const external = require('./apiReq.js');
//skill name
const appName = 'Denny Test';

function getPersistenceAdapter() {
    // This function is an indirect way to detect if this is part of an Alexa-Hosted skill
    function isAlexaHosted() {
        return process.env.S3_PERSISTENCE_BUCKET;
    }
    if (isAlexaHosted()) {
        const {S3PersistenceAdapter} = require('ask-sdk-s3-persistence-adapter');
        return new S3PersistenceAdapter({
            bucketName: process.env.S3_PERSISTENCE_BUCKET
        });
    } else {
        // IMPORTANT: don't forget to give DynamoDB access to the role you're using to run this lambda (via IAM policy)
        const {DynamoDbPersistenceAdapter} = require('ask-sdk-dynamodb-persistence-adapter');
        return new DynamoDbPersistenceAdapter({
            tableName: 'denny_test',
            createTable: true
        });
    }
}

//code for the handlers
const LaunchRequestHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'LaunchRequest';
    },
    handle(handlerInput) {

        const sessionAttributes = handlerInput.attributesManager.getSessionAttributes();
        const sessionCounter = sessionAttributes.sessionCounter;
        
        let speechText = sessionCounter ? `Bentornato! Accesso numero ${sessionCounter}` : `Benvenuto!`; 
        
        if(sessionAttributes.dipName){
            //se è già stato impostato il dipartimento...
            return handlerInput.responseBuilder
            .speak(speechText)
            .withSimpleCard(appName, speechText)
            .reprompt(speechText)
            .getResponse();
        }
        else{
            //altrimenti delego a registra dipartimento!.
            return handlerInput.responseBuilder
            .speak(speechText)
            .withSimpleCard(appName, speechText)
            //intent chaining
            .addDelegateDirective({
                name: 'RegistraDipartimentoIntent',
                confirmationStatus: 'NONE',
                slots: {}
            })
            .getResponse();
        }
    }
};

//implement custom handlers
const RegistraDipartimentoIntentHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
        && handlerInput.requestEnvelope.request.intent.name === 'RegistraDipartimentoIntent';
    },
    handle(handlerInput) {
        let {intent} = handlerInput.requestEnvelope.request;

        var speechText = 'Rigettato!';

        if(intent.confirmationStatus === 'CONFIRMED') {
            //const dipName = intent.slots.dip.value;
            const dipName = intent.slots.dip.resolutions.resolutionsPerAuthority[0].values[0].value.name;
            const dipId = intent.slots.dip.resolutions.resolutionsPerAuthority[0].values[0].value.id;

            /*
            una volta inserito il dipartimento, lo salviamo nel SessionHandler
            "salvataggio a breve termine!"
            */
           let sessionAttributes = handlerInput.attributesManager.getSessionAttributes();
           sessionAttributes.dipName = dipName;
           sessionAttributes.dipId = dipId;
           //sessionAttributes['dip] = dip //uguale!
           handlerInput.attributesManager.setSessionAttributes(sessionAttributes);

            speechText = `Hai selezionato ${dipName} come dipartimento!`;
        }

        return handlerInput.responseBuilder
        .speak(speechText)
        .withSimpleCard(appName, speechText)
        .reprompt(speechText)
        .getResponse();
    }
};

const EnunciaDipartimentoIntentHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
        && handlerInput.requestEnvelope.request.intent.name === 'EnunciaDipartimentoIntent';
    },
    handle(handlerInput) {
        const sessionAttributes = handlerInput.attributesManager.getSessionAttributes();
        const dipName = sessionAttributes.dipName;
        const dipId = sessionAttributes.dipId;

        let speechText = '';
        if(dipName){
            speechText = `Il tuo dipartimento è quello ${dipName} - ${dipId}`;
        } else {
            speechText = 'Mi dispiace, ma non hai impostato alcun dipartimento!';
        }

        return handlerInput.responseBuilder
        .speak(speechText)
        .reprompt(speechText)
        .getResponse();
    }
};

const NotizieIntentHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
        && handlerInput.requestEnvelope.request.intent.name === 'NotizieIntent';
    },
    async handle(handlerInput) {
        const sessionAttributes = handlerInput.attributesManager.getSessionAttributes();
        const dip = sessionAttributes.dipName;
        const newsNumber = sessionAttributes.newsNumber;
        
        let speechText = '';

        if(!newsNumber){
            speechText = 'Non hai ancora impostato quante news vuoi che ti legga.';

            return handlerInput.responseBuilder
            .speak(speechText)
            .addDelegateDirective({
                name: 'ImpostaNumeroNotizieIntent',
                confirmationStatus: 'NONE',
                slots: {}
            })
            .reprompt()
            .getResponse();
        }
        else if(dip){
            const response = await external.getNewsByDip(dip);
            
            if(newsNumber === 1){
                let temp = response.nodes[0].data;
                speechText = temp.node_title + ". " + temp.body;
            }
            else{
                speechText = '';
                
                for(let i = 0; i < newsNumber; i++){
                    let temp = response.nodes[i].data;
                    speechText += `News numero ${i+1}: ${temp.node_title}. ${temp.body}. `;
                }
            }
            
            return handlerInput.responseBuilder
            .speak(speechText)
            .reprompt()
            .getResponse();
        }
        else{
            speechText = 'Mi dispiace ma non hai impostato il tuo dipartimento';
            return handlerInput.responseBuilder
            .speak(speechText)
            .reprompt()
            .getResponse();
        }
        
    }
}

const ImpostaNumeroNotizieIntentHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
        && handlerInput.requestEnvelope.request.intent.name === 'ImpostaNumeroNotizieIntent';
    },
    handle(handlerInput) {
        let {intent} = handlerInput.requestEnvelope.request;

        let speechText = 'Non hai impostato il numero di news da visualizzare';

        if(intent.confirmationStatus === 'CONFIRMED'){
            const newsNumber = intent.slots.newsNumber.value;
            
            const sessionAttributes = handlerInput.attributesManager.getSessionAttributes();
            sessionAttributes.newsNumber = parseInt(newsNumber, 10);
            handlerInput.attributesManager.setSessionAttributes(sessionAttributes);

            
            speechText = (newsNumber === '1') ? `Ogni volta che ascolterai delle notizie, verrà riprodotta l'ultima notizia.`
                : `Ogni volta che ascolterai delle notizie, verranno riprodotte le ultime ${newsNumber} notizie.`; 
        }

        return handlerInput.responseBuilder
        .speak(speechText)
        .reprompt(speechText)
        .getResponse();
    }
}

// -------------------- Test
const EventiIntentHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
        && handlerInput.requestEnvelope.request.intent.name === 'EventiIntent';
    },
    async handle(handlerInput) {
        const sessionAttributes = handlerInput.attributesManager.getSessionAttributes();
        const dip = sessionAttributes.dipName;

        let speechText = '';

        if(dip){
            console.log("Sono dentro");
            const response = await external.getEventsByDip(dip);
            console.log("Ho caricato il JSON");

            if(response.count === 0) speechText = 'Non esistono eventi futuri per il tuo dipartimento';
            else{
                response.events.forEach( element => {
                    let date = new Date(element.node_data);
                    speechText += `${date.getDay()} ${monthName[date.getMonth()]} ${date.getFullYear()}: ${element.node_title}.`;
                })
            }

            return handlerInput.responseBuilder
            .speak(speechText)
            .reprompt()
            .getResponse();
            
        }
        else{
            console.log("Non sono dentro");
            speechText = 'Mi dispiace, ma non hai ancora impostato qual è il tuo dipartimento.';
            return handlerInput.responseBuilder
            .speak(speechText)
            .addDelegateDirective({
                name: 'RegistraDipartimentoIntent',
                confirmationStatus: 'NONE',
                slots: {}
            })
            .reprompt()
            .getResponse();
        }
        

    }
}

//----Test----
const CercaPersonaIntentHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
        && handlerInput.requestEnvelope.request.intent.name === 'CercaPersonaIntent';
    },
    async handle(handlerInput) {
        const api = await external.getRubrica();
        const nodes = api.nodes;
        let {intent} = handlerInput.requestEnvelope.request;

        let speechText = '';

            //Preparo il nome ottenuto tramite la searchQuery (non mi viene niente di meglio in mente)
            let string = intent.slots.fullName.value;
            let searchQuery = string.split(' ');
            let temp = [];
            
            searchQuery = searchQuery.forEach( element => {
                temp.push(element.charAt(0).toUpperCase() + element.slice(1));
            });

            let fullName = temp.join(" ");

            //Confronto il fullName con le combinazioni dei nomi, oppure se contiene un certo nome 
            let results = [];

            nodes.forEach( element => {
                let nome = element.data.Nome;
                let cognome = element.data.Cognome;

                if((`${nome} ${cognome}`).includes(fullName) || (`${cognome} ${nome}`).includes(fullName)){
                    results.push(element);
                }
            });

            if(results.length > 0){
                if(results.length === 1){
                    speechText = 'Ho trovato un risultato: ';
                }
                else{
                    speechText = `Ho trovato ${results.length} risultati: `
                }

                results.forEach( element => {
                    let e = element.data;
                    let tempTel = e.Telefono.replace(/\s/g, '').match(/.{1,2}/g);
                    speechText += `${e.Titolo} ${e.Nome} ${e.Cognome}; Email: ${e.Email}; Telefono: ${tempTel.join(' ')}.`;
                });
            }   
            else{
                speechText = 'Mi dispiace, ma non ho trovato dipendenti che corrispondono alla tua richiesta. ';
            }

            return handlerInput.responseBuilder
            .speak(speechText)
            .reprompt()
            .getResponse();

    }
}
//end Custom handlers

const HelpIntentHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
            && handlerInput.requestEnvelope.request.intent.name === 'AMAZON.HelpIntent';
    },
    handle(handlerInput) {
        //help text for your skill
        let speechText = '';

        return handlerInput.responseBuilder
            .speak(speechText)
            .reprompt(speechText)
            .withSimpleCard(appName, speechText)
            .getResponse();
    }
};

const CancelAndStopIntentHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
            && (handlerInput.requestEnvelope.request.intent.name === 'AMAZON.CancelIntent'
                || handlerInput.requestEnvelope.request.intent.name === 'AMAZON.StopIntent');
    },
    handle(handlerInput) {
        let speechText = 'Alla prossima!';
        return handlerInput.responseBuilder
            .speak(speechText)
            .withSimpleCard(appName, speechText)
            .getResponse();
    }
};

const SessionEndedRequestHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'SessionEndedRequest';
    },
    handle(handlerInput) {
        //any cleanup logic goes here
        return handlerInput.responseBuilder.getResponse();
    }
};

/*
    Per permettere il salvataggio su S3 in modo persistente, devo fare uso di "Interceptors".
    Questi sono dedicati alla lettura e alla scrittura dei file:
    LoadAttributesRequestInterceptor verrà eseguito solamente quando ci sarà
        una richiesta da Alexa verso la nostra skill
    SaveAttributesResponseInterceptor verrà eseguito (in questo caso quando la skill si concluderà)
    salvando tutti i SessionAttributes in modo permanente.


*/
/* *
 * Below we use async and await ( more info: javascript.info/async-await )
 * It's a way to wrap promises and waait for the result of an external async operation
 * Like getting and saving the persistent attributes
 * */
const LoadAttributesRequestInterceptor = {
    async process(handlerInput) {
        const {attributesManager, requestEnvelope} = handlerInput;
        if (Alexa.isNewSession(requestEnvelope)){ //is this a new session? this check is not enough if using auto-delegate (more on next module)
            const persistentAttributes = await attributesManager.getPersistentAttributes() || {};
            console.log('Loading from persistent storage: ' + JSON.stringify(persistentAttributes));
            //copy persistent attribute to session attributes
            attributesManager.setSessionAttributes(persistentAttributes); // ALL persistent attributtes are now session attributes
        }
    }
};

// If you disable the skill and reenable it the userId might change and you loose the persistent attributes saved below as userId is the primary key
const SaveAttributesResponseInterceptor = {
    async process(handlerInput, response) {
        if (!response) return; // avoid intercepting calls that have no outgoing response due to errors
        const {attributesManager, requestEnvelope} = handlerInput;
        const sessionAttributes = attributesManager.getSessionAttributes();
        const shouldEndSession = (typeof response.shouldEndSession === "undefined" ? true : response.shouldEndSession); //is this a session end?
        if (shouldEndSession || Alexa.getRequestType(requestEnvelope) === 'SessionEndedRequest') { // skill was stopped or timed out
            // we increment a persistent session counter here
            sessionAttributes['sessionCounter'] = sessionAttributes['sessionCounter'] ? sessionAttributes['sessionCounter'] + 1 : 1;
            // we make ALL session attributes persistent
            console.log('Saving to persistent storage:' + JSON.stringify(sessionAttributes));
            attributesManager.setPersistentAttributes(sessionAttributes);
            await attributesManager.savePersistentAttributes();
        }
    }
};

//Lambda handler function
//Remember to add custom request handlers here
exports.handler = Alexa.SkillBuilders.custom()
    .addRequestHandlers(LaunchRequestHandler,
        RegistraDipartimentoIntentHandler,
        EnunciaDipartimentoIntentHandler,
        NotizieIntentHandler,
        ImpostaNumeroNotizieIntentHandler,
        EventiIntentHandler,
        CercaPersonaIntentHandler,
                         HelpIntentHandler,
                         CancelAndStopIntentHandler,
                         SessionEndedRequestHandler)
    .addRequestInterceptors(                    //
        LoadAttributesRequestInterceptor        // 
    )                                           //
    .addResponseInterceptors(                   //
        SaveAttributesResponseInterceptor       //
    )                                           //
    .withPersistenceAdapter(persistenceAdapter)
    .lambda();


//tamarrate
const monthName = {
    1: "gennaio",
    2: "febbraio",
    3: "marzo",
    4: "aprile",
    5: "maggio",
    6: "giugno",
    7: "luglio",
    8: "agosto",
    9: "settembre",
    10: "ottobre",
    11: "novembre",
    12: "dicembre"
}
