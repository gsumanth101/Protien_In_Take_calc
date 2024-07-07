// Your web app's Firebase configuration
var firebaseConfig = {
    apiKey: "AIzaSyAsDcPOwwQg9-w--5JF68fjfJfPsv8grqk",
    authDomain: "protien-6103b.firebaseapp.com",
    databaseURL: "https://protien-6103b-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "protien-6103b",
    storageBucket: "protien-6103b.appspot.com",
    messagingSenderId: "770802861333",
    appId: "1:770802861333:web:2c6b9bb53538d1e8e1551c",
    measurementId: "G-QR7B0VXN24"
  };
  // Initialize Firebase
  firebase.initializeApp(firebaseConfig);
  
  function login() {
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
  
    firebase.auth().signInWithEmailAndPassword(email, password)
      .then((userCredential) => {
        userCredential.user.getIdToken().then((token) => {
          fetch('/login', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify({ token: token })
          }).then(response => {
            if (response.ok) {
              window.location.href = '/model'; 
            } else {
              alert('Login failed');
            }
          });
        });
      })
      .catch((error) => {
        var errorCode = error.code;
        var errorMessage = error.message;
        alert(errorMessage);
      });
  }
  