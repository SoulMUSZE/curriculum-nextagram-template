function myFunction() {
  let x = document.getElementById("psw");
  // console.log(`psw element value is ${x}`)
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}


const flashMsgParent = document.querySelector('.flash-messages');
flashMsgParent.onclick = function (e) {
  let msg = e.target;
  flashMsgParent.removeChild(msg)
  // msg.parentNode.removeChild(msg)
}


let myInput = document.getElementById("psw");
let letter = document.getElementById("letter");
let capital = document.getElementById("capital");
let number = document.getElementById("number");
let length = document.getElementById("length");

show = false
// When the user clicks on the password field, toggle the showing of the message box
myInput.onclick = function () {
  if (!show) {
    document.getElementById("message").style.display = "block";
    show = !show
  }
  else {
    document.getElementById("message").style.display = "none";
    show = !show
  }
}

// When the user starts to type something inside the password field
myInput.onkeyup = function () {
  // Validate lowercase letters
  var lowerCaseLetters = /[a-z]/g;
  if (myInput.value.match(lowerCaseLetters)) {
    letter.classList.remove("invalid");
    letter.classList.add("valid");
  } else {
    letter.classList.remove("valid");
    letter.classList.add("invalid");
  }

  // Validate capital letters
  var upperCaseLetters = /[A-Z]/g;
  if (myInput.value.match(upperCaseLetters)) {
    capital.classList.remove("invalid");
    capital.classList.add("valid");
  } else {
    capital.classList.remove("valid");
    capital.classList.add("invalid");
  }

  // Validate numbers
  var numbers = /[0-9]/g;
  if (myInput.value.match(numbers)) {
    number.classList.remove("invalid");
    number.classList.add("valid");
  } else {
    number.classList.remove("valid");
    number.classList.add("invalid");
  }

  // Validate length
  if (myInput.value.length >= 8) {
    length.classList.remove("invalid");
    length.classList.add("valid");
  } else {
    length.classList.remove("valid");
    length.classList.add("invalid");
  }
}

function preview_image(event) {
  var reader = new FileReader();

  reader.onload = function () {
    var output = document.getElementById('preview-img');
    output.src = reader.result;
  }

  reader.readAsDataURL(event.target.files[0]);
}
