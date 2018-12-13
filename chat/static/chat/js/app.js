var app = new Vue({
    el: '#app',
    data: {
        contacts:[],
        messages:[],
        user: {
            contacts:[]
        },
        hash: '',
        actions:[
            { title:"Contacts", click: "viewContacts", icon: 'contact_mail'},
            { title:"Profile", click: "viewProfile", icon: 'account_circle' },
            { title:"Login", click: "signIn", icon: 'account_circle', guest:true },
            { title:"Logout", click: "signOut", icon: 'account_circle'},
        ],
        menu: false,
        dialog: false,
        valid:false,
        newMessage:{
            contact: null
        },
        currentContact:{},
        dialogTitle:"New",
        rules:{
            email : [function(v){ return !v || v.indexOf("@")>0 || 'Invalid email' }],
            message : [function(v){ return !v || v.length<200 || 'Maximum length : 200 characters' }]
        }
    },
    methods:{
        viewContacts: function(){
            var self=this
            this.hash = "#contacts"
            apiCall("Sender/get/"+this.user.email+"/",function(data){
                self.contacts = data;
                self.currentContact=self.findContact(self.currentContact.email);
                if (!self.currentContact.email && data.length>0){
                    self.contactClick(data[0])
                }
                setTimeout(function(){
                    var list=document.getElementById("messageList")
                    list.scrollTop = list.scrollHeight;
                },500)
            })
        },
        viewMessages: function(email){
            var self=this
            this.hash = "#contacts"
            apiCall("Message/get/"+this.user.email+"/"+email,function(data){
                self.messages = data;
            })
        },
        messageContent(message){
            return 
        },
        findContact(email){
            if (email==this.user.email){
                return this.user
            }
            return this.findItem("contacts","email",email,{})
        },
        imageUrl(url){
            if (url==null || url==""){
                return "images/user-icon.png"
            }
            return url
        },
        findItem(name,field,value,def){
            var items=this[name]
            for(var i=0;i<items.length;i++){
                if (items[i][field]==value){
                    return items[i]
                }
            }
            return def
        },
        viewProfile: function(){
            var self=this
            this.hash = "#profile"

        },
        signOut(){
            this.user = {
                contacts:[]
            }
            this.contacts=[]
            this.messages=[]
            this.currentContact={}
            API_HEADERS={}
            contactWorker({})
            messageWorker({})
            signOut()
        },
        signIn(){
            signIn()
        },
        newContact(){
            this.newMessage.email="@gmail.com"
            this.newMessage.message=""
            this.dialogTitle = "New Contact message"
            if (this.currentContact.email && this.hash=="#contacts"){
                this.newMessage.email=this.currentContact.email;
                this.dialogTitle = "New Message"
            }
            this.dialog=true;
        },
        sendContact(){
            if (!this.newMessage || this.newMessage.email.trim().length==0){
                return;
            }
            if (!this.newMessage || this.newMessage.message.trim().length==0){
                return;
            }
            var self=this
            this.dialog = false
            var message=encodeURIComponent(this.newMessage.message)
            var url="Message/push/"+this.user.email.trim().toLowerCase()+"/?to="+this.newMessage.email.trim().toLowerCase()+"&message="+message;
            //console.log(JSON.stringify(self.newMessage));
            apiCall(url,function(data){
                self.currentContact.email=self.newMessage.email
                self.viewContacts()
                self.newMessage.email="@gmail.com"
                self.newMessage.message=""
                self.newMessage.contact=null
            })
        },
        newContactSelected(contact){
            //console.log(contact);
            document.getElementById("messageText").focus();
        },
        isVisible:function(item){
            if (item.guest){
                return !this.isLogged
            }
            return this.isLogged
        },
        timeAgo(time){
            var current = new Date();
            var currentTime = current.getTime();
            var date=new Date(time*1000)
            var diff=(current - date)/1000;
            if (diff<5){
                return "Now"
            }
            if (diff<60){
                return Math.round(diff) + " seconds ago"
            }
            if (diff<120){
                return "1 minute ago"
            }
            if (diff<3600){
                return Math.round(diff/60) + " minutes ago"
            }
            if (diff<3600*24){
                return Math.round(diff/3600) + " hours ago"
            }
            if (diff<3600*24*30){
                return Math.round(diff/(3600*24)) + " days ago"
            }
            return date.toISOString();
        },
        contactClick(item){
            //console.log("item",item)
            var self=this
            this.currentContact = item
            self.messages = []
            this.viewMessages(item.email)
            messageWorker({
                endpoint: API_ENDPOINT,
                contact : item.email,
                user: this.user.email
            },function(data){
                self.messages = data
            })
        },
        messageClick(item){
            console.log(item)
            
        },
        menuClick(item){
            this[item.click]()
            this.menu=false
        },
        autoCompleteContact(ev){
            
        },
        ctChange(ev){
            console.log("Change", ev)
        },
        ctKeydown(ev){
            console.log("KeyDown", ev)
            this.newMessage.email = ""
            if(typeof(this.newMessage.contact)=="string"){
                var email=this.newMessage.contact;
                if (email.match(/.+@.+/)){
                    this.newMessage.contact={
                        name: ev,
                        email: ev
                    }
                    this.newMessage.email = ""
                    this.newContactSelected(this.newMessage.contact)
                }
            }
        }
    },
    mounted:function(){
        this.$el.style.display="";
        startWorkers();
    },
    computed:{
        isLogged:function(){
            return this.user && this.user.email!=null;
        },
        allContacts:function(){
            return this.contacts.concat(this.user.contacts)
        }
    }
})
    
function onRegisterUser(loggedUser){
    var email=loggedUser.email;
    var name=loggedUser.name;
    var imageLink=loggedUser.imageUrl;
    var idToken=loggedUser.idToken;
    var authToken=loggedUser.authToken;
    console.log(loggedUser);

    var query="User/register/{email}/?name={name}&imageUrl={imageLink}"
        .replace("{email}",email)
        .replace("{name}",name)
        .replace("{imageLink}",imageLink)
        .replace("{token}",idToken)
    API_HEADERS={
        'Authentication': 'Bearer '+idToken,
        'Client-Id': getMeta("google-signin-client_id"),
        'Auth-Token': authToken

    }
    apiFullCall("GET",query,API_HEADERS, function(data){
        console.log(data)
        app.user = data
        app.viewContacts()
        contactWorker({
            endpoint: API_ENDPOINT,
            user : data.email
        },function(data){
            app.contacts = data
        })
    })

    
}

API_ENDPOINT = document.location.protocol + '//' + document.location.host + document.location.pathname + '../../'
API_HEADERS= {}
API_ENDPOINT = document.location.protocol + '//' + document.location.host + "/";

function apiCall( query, callback){
    var header={}
    if (API_HEADERS){
        header=API_HEADERS
    }
    apiFullCall("GET", query, header, callback);
}


function apiFullCall(method, query, headers,  callback){
  var url= "";
  var config = {
      headers: headers,
      method: method
  }
  fetch(API_ENDPOINT + query, config)
    .then(function(response) {
        if(!response.ok){
            alert("Error "+response.status+" : "+ response.statusText);
            return null;
        }
        return response.json();
    })
    .then(function(myJson) {
        if (myJson && callback){
            callback(myJson)
        }
    });
}


function startWorkers() {
    if(typeof(Worker) !== "undefined") {
        if(typeof(mw) == "undefined") {
            mw = new Worker("js/message-worker.js");
        }
        if(typeof(cw) == "undefined") {
            cw = new Worker("js/contact-worker.js");
        }
    } else {
        alert("Sorry, your browser does not support Web Workers.");
    }
}

function messageWorker(data, callback){
    data.headers=API_HEADERS
    mw.onmessage = function(event) {
        if (callback) callback(event.data)
    };
    mw.postMessage(data)
}

function contactWorker(data, callback){
    data.headers=API_HEADERS
    cw.onmessage = function(event) {
        if (callback) callback(event.data)
    };
    cw.postMessage(data)
}

function stopWorker() { 
    if (mw){
        mw.terminate();
        mw = undefined;
    }
}

function getMeta(metaName) {
    const metas = document.getElementsByTagName('meta');
  
    for (let i = 0; i < metas.length; i++) {
      if (metas[i].getAttribute('name') === metaName) {
        return metas[i].getAttribute('content');
      }
    }
  
    return '';
  }
