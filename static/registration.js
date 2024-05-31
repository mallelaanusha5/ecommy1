function validateForm(){

    const usernameRegex=/^[a-zA-Z0-9_]{2,}$/;
    const emailRegex=/^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    //                    name      +@ gmail       +. com     com/ac/etc...//
    const phoneRegex=/^\d{10}$/;
    const passwordRegex=/^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/;
    //                     digits    a-z      A-Z         min 8 digits ; we give dot(.) to seperate the type//

    const username=document.getElementById("username").value;
    const email=document.getElementById("email").value;
    const phoneNo=document.getElementById("phoneNo").value;
    const password=document.getElementById("password").value;
    const confirmPassword=document.getElementById("confirmPassword").value;


    resetErrorMessage();

    if(!usernameRegex.test(username)){
        document.getElementById("usernameError").innerText="Invalid Username";
        // alert("invalid username");
        return;
    }
    if(!emailRegex.test(email)){
        document.getElementById("emailError").innerText="Invalid Email";
        // alert("invalid  2");
        return;
    }
    if(!phoneRegex.test(phoneNo)){
        document.getElementById("phoneError").innerText="Invalid Phone Number";
        // alert("invalid 3 ");
        return;
    }
    if(!passwordRegex.test(password)){
        document.getElementById("passwordError").innerText="Password must contain atleast 8 characters and contain atleast one digit, one lowercase letter, one uppercase letter";
        // alert("invalid 4");
        return;
    }
    if(password !== confirmPassword){
        document.getElementById("confirmPasswordError").innerText="Passwords don't match";
        // alert("invalid 5");
        return;
    }

    alert("Form submitted successfully");
    // event.preventDefault()
    console.log("username", username,"</br>");
    console.log("email", email,"</br>");
    console.log("phoneNo", phoneNo,"</br>");
    console.log("password", password,"</br>");
    console.log("confirmPassword", confirmPassword,"</br>");  
}
     
   
function resetForm(){
    document.getElementById("registrationForm").reset();
    resetErrorMessage();
}

function resetErrorMessage(){
    const errorMessages=document.querySelectorAll(".error-message");
    errorMessages.forEach(message=>message.innerText="");
}



