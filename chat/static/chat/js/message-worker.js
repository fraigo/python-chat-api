var i=0;
var currentContact = null
var currentUser = null
var API_ENDPOINT = null
var API_HEADERS = {}

function timedCall() {
    console.log("message-worker",i, currentContact)
    i=i+1;
    if (API_ENDPOINT!=null && currentContact!=null){
        apiCall("Message/get/"+currentUser+ "/" +currentContact,function(data){
            postMessage(data);
        })
    }
    setTimeout(timedCall, 10000);
}

onmessage = function(e) {
    API_ENDPOINT=e.data.endpoint
    currentContact=e.data.contact
    currentUser=e.data.user
    API_HEADERS=e.data.headers
};


function apiCall(query, callback){
    var url= "";
    var config = {
        headers: API_HEADERS,
        method: "GET"
    }
    fetch(API_ENDPOINT + query, config)
      .then(function(response) {
          return response.json();
      })
      .then(function(myJson) {
          if (callback){
              callback(myJson)
          }
      });
  }

timedCall();