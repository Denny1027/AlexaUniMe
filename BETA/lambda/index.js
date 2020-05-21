
const Alexa = require('ask-sdk-core');

const i18n = require('i18next');

const languageStrings = require('./localisation');

var persistenceAdapter = getPersistenceAdapter();


const LaunchRequestHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'LaunchRequest';
    },
    handle(handlerInput) {
        const sessionAttributes = handlerInput.attributesManager.getSessionAttributes();

        const sessionCounter = sessionAttributes['sessionCounter'];

        let speechText = !sessionCounter ? handlerInput.t('WELCOME_MSG') : handlerInput.t('WELCOME_BACK_MSG');
        speechText += handlerInput.t('HCIHY_MSG'); //come posso esserti d'aiuto? How Can I Help You?

        return handlerInput.responseBuilder
            .speak(speechText)
            .reprompt(speechText)
            .getResponse();
    }
};


//  ----------------------------------
//      LISTA DI INTENTI CUSTOM - INIZIO
//  ---------------------------------

const CosaChiedereIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'CosaChiedereIntent';
    },
    handle(handlerInput) {
        const speakOutput = handlerInput.t('WHATASK_MSG');
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(handlerInput.t(`REPROMPT_MSG`))
            .getResponse();
    }
};

const CertificatiComeRichiedereIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'CertificatiComeRichiedereIntent';
    },
    handle(handlerInput) {
        const speakOutput = handlerInput.t('CERT_HOW_REQ_MSG');
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(handlerInput.t(`REPROMPT_MSG`))
            .getResponse();
    }
};

const CertificatiChiDiplomaSupplementIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'CertificatiChiDiplomaSupplementIntent';
    },
    handle(handlerInput) {
        const speakOutput = handlerInput.t('CERT_WHO_DS_MSG');
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(handlerInput.t(`REPROMPT_MSG`))
            .getResponse();
    }
};

const CertificatiComeRichiedereDiplomaSupplementIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'CertificatiComeRichiedereDiplomaSupplementIntent';
    },
    handle(handlerInput) {
        const speakOutput = handlerInput.t('CERT_HOW_REQ_DS_MSG');
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(handlerInput.t(`REPROMPT_MSG`))
            .getResponse();
    }
};

const CertificatiCosaDiplomaSupplementIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'CertificatiCosaDiplomaSupplementIntent';
    },
    handle(handlerInput) {
        const speakOutput = handlerInput.t('CERT_WHAT_DS_MSG');
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(handlerInput.t(`REPROMPT_MSG`))
            .getResponse();
    }
};

const CertificatiDoveRitirareIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'CertificatiDoveRitirareIntent';
    },
    handle(handlerInput) {
        const speakOutput = handlerInput.t('CERT_WHERE_MSG');
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(handlerInput.t(`REPROMPT_MSG`))
            .getResponse();
    }
};

const CertificatiLaureaIngleseIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'CertificatiLaureaIngleseIntent';
    },
    handle(handlerInput) {
        const speakOutput = handlerInput.t('CERT_ENGL_GRAD_MSG');
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(handlerInput.t(`REPROMPT_MSG`))
            .getResponse();
    }
};

const CertificatiDiplomaSupplementBolloIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'CertificatiDiplomaSupplementBolloIntent';
    },
    handle(handlerInput) {
        const speakOutput = handlerInput.t('CERT_DS_STAMP_MSG');
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(handlerInput.t(`REPROMPT_MSG`))
            .getResponse();
    }
};

const CertificatiQuandoAvvalermiAutocertificazioneIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'CertificatiQuandoAvvalermiAutocertificazioneIntent';
    },
    handle(handlerInput) {
        const speakOutput = handlerInput.t('CERT_WHEN_MSG');
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(handlerInput.t(`REPROMPT_MSG`))
            .getResponse();
    }
};

// ------ IMMATRICOLAZIONI
const ImmatrEsoneriIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'ImmatrEsoneriIntent';
    },
    handle(handlerInput) {
        const speakOutput = handlerInput.t('IMM_EXON_MSG');
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(handlerInput.t(`REPROMPT_MSG`))
            .getResponse();
    }
};

const ImmatrComeIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'ImmatrComeIntent';
    },
    handle(handlerInput) {
        const speakOutput = handlerInput.t('IMM_HOW_MSG') + handlerInput.t(`IMM_WHAT_MSG`);
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(handlerInput.t(`REPROMPT_MSG`))
            .getResponse();
    }
};

const ImmatrCosaFareIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'ImmatrCosaFareIntent';
    },
    handle(handlerInput) {
        const speakOutput = handlerInput.t('IMM_WHAT_MSG');
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(handlerInput.t(`REPROMPT_MSG`))
            .getResponse();
    }
};

const ImmatrDisabilitaEsenzioneIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'ImmatrDisabilitaEsenzioneIntent';
    },
    handle(handlerInput) {
        const speakOutput = handlerInput.t('IMM_DIS_EXO_MSG');
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(handlerInput.t(`REPROMPT_MSG`))
            .getResponse();
    }
};

const ImmatrStessoNucleoIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'ImmatrStessoNucleoIntent';
    },
    handle(handlerInput) {
        const speakOutput = handlerInput.t('IMM_SAME_FAM_MSG');
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(handlerInput.t(`REPROMPT_MSG`))
            .getResponse();
    }
};

const ImmatrLaureaMagistraleIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'ImmatrLaureaMagistraleIntent';
    },
    handle(handlerInput) {
        const speakOutput = handlerInput.t('IMM_MAST_MSG');
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(handlerInput.t(`REPROMPT_MSG`))
            .getResponse();
    }
};

const ImmatrModPagamentoIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'ImmatrModPagamentoIntent';
    },
    handle(handlerInput) {
        const speakOutput = handlerInput.t('IMM_PAYMENT_MODE_MSG');
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(handlerInput.t(`REPROMPT_MSG`))
            .getResponse();
    }
};

const ImmatrPagamentoRateIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'ImmatrPagamentoRateIntent';
    },
    handle(handlerInput) {
        const speakOutput = handlerInput.t('IMM_PAYMENT_INSTALLMENT_MSG');
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(handlerInput.t(`REPROMPT_MSG`))
            .getResponse();
    }
};

const ImmatrQuantoPagareIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'ImmatrQuantoPagareIntent';
    },
    handle(handlerInput) {
        const speakOutput = handlerInput.t('IMM_HOW_MUCH_MSG');
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(handlerInput.t(`REPROMPT_MSG`))
            .getResponse();
    }
};

const ImmatrNumeroProgrammatoIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'ImmatrNumeroProgrammatoIntent';
    },
    handle(handlerInput) {
        const speakOutput = handlerInput.t('IMM_CLOSED_NUM_MSG');
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(handlerInput.t(`REPROMPT_MSG`))
            .getResponse();
    }
};

const ImmatrNonAmmessoAltroCorsoIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'ImmatrNonAmmessoAltroCorsoIntent';
    },
    handle(handlerInput) {
        const speakOutput = handlerInput.t('IMM_OTHER_COURSE_MSG');
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(handlerInput.t(`REPROMPT_MSG`))
            .getResponse();
    }
};

const ImmatrRinnovoAnniSuccIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'ImmatrRinnovoAnniSuccIntent';
    },
    handle(handlerInput) {
        const speakOutput = handlerInput.t('IMM_RENEWAL_MSG');
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(handlerInput.t(`REPROMPT_MSG`))
            .getResponse();
    }
};

// ------ ISEE
const IseeCosaIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'IseeCosaIntent';
    },
    handle(handlerInput) {
        const speakOutput = handlerInput.t('ISEE_WHAT_MSG');
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(handlerInput.t(`REPROMPT_MSG`))
            .getResponse();
    }
};

const IseeUtilitaIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'IseeUtilitaIntent';
    },
    handle(handlerInput) {
        const speakOutput = handlerInput.t('ISEE_USE_MSG');
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(handlerInput.t(`REPROMPT_MSG`))
            .getResponse();
    }
};

const IseeUniIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'IseeUniIntent';
    },
    handle(handlerInput) {
        const speakOutput = handlerInput.t('ISEE_UNI_MSG');
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(handlerInput.t(`REPROMPT_MSG`))
            .getResponse();
    }
};

const IseeAcquisizioneIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'IseeAcquisizioneIntent';
    },
    handle(handlerInput) {
        const speakOutput = handlerInput.t('ISEE_ACQUISITION_MSG');
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(handlerInput.t(`REPROMPT_MSG`))
            .getResponse();
    }
};

const IseeComeFunzionaIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'IseeComeFunzionaIntent';
    },
    handle(handlerInput) {
        const speakOutput = handlerInput.t('ISEE_HOW_WORKS_MSG') + handlerInput.t(`ISEE_ACQUISITION_MSG`) + handlerInput.t(`ISEE_NO_AVAIL_MSG`);
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(handlerInput.t(`REPROMPT_MSG`))
            .getResponse();
    }
};

const IseeNonAvvalersiIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'IseeNonAvvalersiIntent';
    },
    handle(handlerInput) {
        const speakOutput = handlerInput.t('ISEE_NO_AVAIL_MSG');
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(handlerInput.t(`REPROMPT_MSG`))
            .getResponse();
    }
};

const IseeProblemiConsensoIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'IseeProblemiConsensoIntent';
    },
    handle(handlerInput) {
        const speakOutput = handlerInput.t('ISEE_PROBLEMS_MSG');
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(handlerInput.t(`REPROMPT_MSG`))
            .getResponse();
    }
};

const IseeDopoScadenzaIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'IseeDopoScadenzaIntent';
    },
    handle(handlerInput) {
        const speakOutput = handlerInput.t('ISEE_AFTER_EXPIRE_MSG');
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(handlerInput.t(`REPROMPT_MSG`))
            .getResponse();
    }
};



//  ----------------------------------
//      LISTA DI INTENTI CUSTOM - FINE
//  ---------------------------------


//  ----------------------------------
//      INTENTI BUILT-IN - INIZIO
//  ---------------------------------

const HelpIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'AMAZON.HelpIntent';
    },
    handle(handlerInput) {
        const speakOutput = handlerInput.t('HELP_MSG');

        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(speakOutput)
            .getResponse();
    }
};
const CancelAndStopIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && (Alexa.getIntentName(handlerInput.requestEnvelope) === 'AMAZON.CancelIntent'
                || Alexa.getIntentName(handlerInput.requestEnvelope) === 'AMAZON.StopIntent');
    },
    handle(handlerInput) {
        const speakOutput = handlerInput.t('GOODBYE_MSG');
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .getResponse();
    }
};

/* *
 * SessionEndedRequest notifies that a session was ended. This handler will be triggered when a currently open 
 * session is closed for one of the following reasons: 1) The user says "exit" or "quit". 2) The user does not 
 * respond or says something that does not match an intent defined in your voice model. 3) An error occurs 
 * */
const SessionEndedRequestHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'SessionEndedRequest';
    },
    handle(handlerInput) {
        console.log(`~~~~ Session ended: ${JSON.stringify(handlerInput.requestEnvelope)}`);
        // Any cleanup logic goes here.
        return handlerInput.responseBuilder.getResponse(); // notice we send an empty response
    }
};

/* *
 * FallbackIntent triggers when a customer says something that doesn’t map to any intents in your skill
 * It must also be defined in the language model (if the locale supports it)
 * This handler can be safely added but will be ingnored in locales that do not support it yet 
 * */
const FallbackIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'AMAZON.FallbackIntent';
    },
    handle(handlerInput) {
        const speechText = handlerInput.t('FALLBACK_MSG');

        return handlerInput.responseBuilder
            .speak(speechText)
            .reprompt(handlerInput.t('REPROMPT_MSG'))
            .getResponse();
    }
};

// The intent reflector is used for interaction model testing and debugging.
// It will simply repeat the intent the user said. You can create custom handlers
// for your intents by defining them above, then also adding them to the request
// handler chain below.
const IntentReflectorHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest';
    },
    handle(handlerInput) {
        const intentName = Alexa.getIntentName(handlerInput.requestEnvelope);
        const speakOutput = `You just triggered ${intentName}`;

        return handlerInput.responseBuilder
            .speak(speakOutput)
            //.reprompt('add a reprompt if you want to keep the session open for the user to respond')
            .getResponse();
    }
};

/**
 * Generic error handling to capture any syntax or routing errors. If you receive an error
 * stating the request handler chain is not found, you have not implemented a handler for
 * the intent being invoked or included it in the skill builder below 
 * */
const ErrorHandler = {
    canHandle() {
        return true;
    },
    handle(handlerInput, error) {
        const speechText = handlerInput.t('ERROR_MSG');
        console.log(`~~~~ Error handled: ${JSON.stringify(error)}`);

        return handlerInput.responseBuilder
            .speak(speechText)
            .reprompt(handlerInput.t('REPROMPT_MSG'))
            .getResponse();
    }
};

//  ----------------------------------
//      INTENTI BUILT-IN - FINE
//  ---------------------------------


// ----- FUNZIONI AGGIUNTIVE -----
// 


// This request interceptor will bind a translation function 't' to the handlerInput
// Additionally it will handle picking a random value if instead of a string it receives an array
const LocalisationRequestInterceptor = {
    process(handlerInput) {
        const localisationClient = i18n.init({
            lng: Alexa.getLocale(handlerInput.requestEnvelope),
            resources: languageStrings,
            returnObjects: true
        });
        localisationClient.localise = function localise() {
            const args = arguments;
            const value = i18n.t(...args);
            if (Array.isArray(value)) {
                return value[Math.floor(Math.random() * value.length)];
            }
            return value;
        };
        handlerInput.t = function translate(...args) {
            return localisationClient.localise(...args);
        }
    }
};

// This request interceptor will log all incoming requests to this lambda
const LoggingRequestInterceptor = {
    process(handlerInput) {
        console.log(`Incoming request: ${JSON.stringify(handlerInput.requestEnvelope)}`);
    }
};

// This response interceptor will log all outgoing responses of this lambda
const LoggingResponseInterceptor = {
    process(handlerInput, response) {
        console.log(`Outgoing response: ${JSON.stringify(response)}`);
    }
};
// -- PERSISTENCE ADAPTER --

function getPersistenceAdapter(tableName) {
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
            tableName: tableName,
            createTable: true
        });
    }
}

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

// The SkillBuilder acts as the entry point for your skill, routing all request and response
// payloads to the handlers above. Make sure any new handlers or interceptors you've
// defined are included below. The order matters - they're processed top to bottom.
exports.handler = Alexa.SkillBuilders.custom()
    .addRequestHandlers(
        LaunchRequestHandler,
            CosaChiedereIntentHandler,
            CertificatiComeRichiedereIntentHandler,
            CertificatiChiDiplomaSupplementIntentHandler,
            CertificatiComeRichiedereDiplomaSupplementIntentHandler,
            CertificatiCosaDiplomaSupplementIntentHandler,
            CertificatiDoveRitirareIntentHandler,
            CertificatiLaureaIngleseIntentHandler,
            CertificatiDiplomaSupplementBolloIntentHandler,
            CertificatiQuandoAvvalermiAutocertificazioneIntentHandler,
            //fine certificati - inizio immatricolazione
            ImmatrEsoneriIntentHandler,
            ImmatrComeIntentHandler,
            ImmatrCosaFareIntentHandler,
            ImmatrDisabilitaEsenzioneIntentHandler,
            ImmatrStessoNucleoIntentHandler,
            ImmatrLaureaMagistraleIntentHandler,
            ImmatrModPagamentoIntentHandler,
            ImmatrPagamentoRateIntentHandler,
            ImmatrQuantoPagareIntentHandler,
            ImmatrNumeroProgrammatoIntentHandler,
            ImmatrNonAmmessoAltroCorsoIntentHandler,
            ImmatrRinnovoAnniSuccIntentHandler,
            //fine immatricolazioni - inizio isee
            IseeCosaIntentHandler,
            IseeUtilitaIntentHandler,
            IseeUniIntentHandler,
            IseeAcquisizioneIntentHandler,
            IseeComeFunzionaIntentHandler,
            IseeNonAvvalersiIntentHandler,
            IseeProblemiConsensoIntentHandler,
            IseeDopoScadenzaIntentHandler,
            //fine isee
            //intent handlers
        HelpIntentHandler,
        CancelAndStopIntentHandler,
        FallbackIntentHandler,
        SessionEndedRequestHandler,
        IntentReflectorHandler, // make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
    )
    .addErrorHandlers(
        ErrorHandler,
    )
    .addRequestInterceptors(
        LocalisationRequestInterceptor,
        LoggingRequestInterceptor,
        LoadAttributesRequestInterceptor)
    .addResponseInterceptors(
        LoggingResponseInterceptor,
        SaveAttributesResponseInterceptor)
    .withPersistenceAdapter(persistenceAdapter)
    .withApiClient(new Alexa.DefaultApiClient())
    .lambda();
