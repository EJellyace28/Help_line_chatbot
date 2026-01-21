// ========== UTILITY FUNCTIONS ========== 
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// ========== PASSWORD TOGGLE ==========
function togglePassword() {
    const passwordInput = document.getElementById('loginPassword');
    const eyeIcon = document.getElementById('eyeIcon');
    const eyeOffIcon = document.getElementById('eyeOffIcon');

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        eyeIcon.style.display = 'none';
        eyeOffIcon.style.display = 'block';
    } else {
        passwordInput.type = 'password';
        eyeIcon.style.display = 'block';
        eyeOffIcon.style.display = 'none';
    }
}

function toggleRegisterPassword(inputId, eyeId, eyeOffId) {
    const passwordInput = document.getElementById(inputId);
    const eyeIcon = document.getElementById(eyeId);
    const eyeOffIcon = document.getElementById(eyeOffId);

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        eyeIcon.style.display = 'none';
        eyeOffIcon.style.display = 'block';
    } else {
        passwordInput.type = 'password';
        eyeIcon.style.display = 'block';
        eyeOffIcon.style.display = 'none';
    }
}


// ========== LOGIN HANDLER ========== 
function handleLogin(event) {
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    let isValid = true;

    if (!validateEmail(email)) {
        document.querySelector('#loginEmail').parentElement.classList.add('error');
        isValid = false;
    } else {
        document.querySelector('#loginEmail').parentElement.classList.remove('error');
    }

    if (password.length === 0) {
        document.querySelector('#loginPassword').parentElement.classList.add('error');
        isValid = false;
    } else {
        document.querySelector('#loginPassword').parentElement.classList.remove('error');
    }

    if (isValid) {
        return true;
    } else {
        event.preventDefault();
        return false;
    }
}

// ========== REGISTRATION HANDLER ========== 
function handleRegister(event) {
    const name = document.getElementById('registerName').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const confirmPassword = document.getElementById('registerConfirmPassword').value;

    let isValid = true;

    if (name.length === 0) {
        document.querySelector('#registerName').parentElement.classList.add('error');
        isValid = false;
    } else {
        document.querySelector('#registerName').parentElement.classList.remove('error');
    }

    if (!validateEmail(email)) {
        document.querySelector('#registerEmail').parentElement.classList.add('error');
        isValid = false;
    } else {
        document.querySelector('#registerEmail').parentElement.classList.remove('error');
    }

    if (password.length < 8) {
        document.querySelector('#registerPassword').parentElement.classList.add('error');
        isValid = false;
    } else {
        document.querySelector('#registerPassword').parentElement.classList.remove('error');
    }

    if (password !== confirmPassword) {
        document.querySelector('#registerConfirmPassword').parentElement.classList.add('error');
        isValid = false;
    } else {
        document.querySelector('#registerConfirmPassword').parentElement.classList.remove('error');
    }

    if (isValid) {
        return true;
    } else {
        event.preventDefault();
        return false;
    }
}