var https = require('https');

var getNewsByDip = (dip) => {
      return new Promise(((resolve, reject) => {
    var options = {
        host: 'unimeapp-data.unime.it',
        port: 443,
        path:  `/api/v1/news/${dip}/all`,
        method: 'GET',
    };
    
    const request = https.request(options, (response) => {
      response.setEncoding('utf8');
      let returnData = '';

      response.on('data', (chunk) => {
        returnData += chunk;
      });

      response.on('end', () => {
        resolve(JSON.parse(returnData));
      });

      response.on('error', (error) => {
        reject(error);
      });
    });
    request.end();
  }));
}

var getEventsByDip = (dip) => {
      return new Promise(((resolve, reject) => {
    var options = {
        host: 'unimeapp-data.unime.it',
        port: 443,
        path:  `/api/v1/evento/${dip}/all?_format=json`,
        method: 'GET',
    };
    
    const request = https.request(options, (response) => {
      response.setEncoding('utf8');
      let returnData = '';

      response.on('data', (chunk) => {
        returnData += chunk;
      });

      response.on('end', () => {
          console.log("JSON -> " + returnData);
        resolve(cleanJSONFromToday(returnData));
      });

      response.on('error', (error) => {
        reject(error);
      });
    });
    request.end();
  }));
}

/*
    Ottengo un JSON contenente tutti i dati contenuti in rubrica
*/
var getRubrica = () => {
    return new Promise(((resolve, reject) => {
        var options = {
            host: 'unimeapp-data.unime.it',
            port: 443,
            path:  `/api/v1/persona/all?_format=json`,
            method: 'GET',
        };
    
    const request = https.request(options, (response) => {
        response.setEncoding('utf8');
        let returnData = '';

        response.on('data', (chunk) => {
            returnData += chunk;
        });

        response.on('end', () => {
            resolve(JSON.parse(returnData));
      });

      response.on('error', (error) => {
        reject(error);
      });
    });
    request.end();
    }));
}


exports.getNewsByDip = getNewsByDip;
exports.getEventsByDip = getEventsByDip;
exports.getRubrica = getRubrica;

/**
 * Funzioni private
 */
 function cleanJSONFromToday(json){
     let todayString = new Date().toDateString();
     
     let retArray = [];
    console.log(JSON.parse(json));
    JSON.parse(json).nodes.forEach( element => {
        //se la data dell'evento è del giorno corrente o successiva, allora copia in retArray!
        if(compareDates(element.data.node_data)) {
            retArray.push(element.data);
        }
    });
    
    let toReturn = {
        "events": retArray,
        "count": retArray.length
    }
    return toReturn;
}

//la data deve essere una stringa della forma "YYYY-MM-DD HH:mm:ss" o simili
function compareDates(date) {
    let today = new Date();
    let toCompare = new Date(date);
    
    return toCompare >= today;
}
 
 
 