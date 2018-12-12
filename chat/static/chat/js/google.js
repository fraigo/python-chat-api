function fakeUser(){
  var loggedUser={
    id: 123123123,
    name: "Fake User",
    imageUrl: "http://localhost:8000/client/images/messages-120.png",
    email: "fake@user.com",
    idToken: "fakeuser123456abcdefg",
    authToken: "afastw45wfgdsadgf"
  }
  onRegisterUser(loggedUser)
}

function onSignIn(googleUser) {
    // Useful data for your client-side scripts:
    console.log(googleUser.getAuthResponse());
    var profile = googleUser.getBasicProfile();
    var loggedUser={
      id: profile.getId(),
      name: profile.getName(),
      imageUrl: profile.getImageUrl(),
      email: profile.getEmail(),
      idToken: googleUser.getAuthResponse().id_token,
      authToken: googleUser.getAuthResponse().access_token
    }

    onRegisterUser(loggedUser);

  };

  function signIn(){
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signIn().then(function (user) {
      onSignIn(user)
    });
  }
  
  function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
      console.log('User signed out.');
    });
  }
