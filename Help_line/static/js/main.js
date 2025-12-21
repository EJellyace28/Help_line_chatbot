// ========== PAGE NAVIGATION ========== 
function showPage(pageId) {
    const page = document.getElementById(pageId);
    if (!page) {
        console.warn('Page element not found:', pageId);
        return;
    }
    
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    page.classList.add('active');
}

function showLanding() {
    // For multi-page Django apps, redirect instead of DOM manipulation
    if (document.getElementById('landingPage')) {
        showPage('landingPage');
    } else {
        window.location.href = '/';
    }
}

function showLogin() {
    // For multi-page Django apps, redirect instead of DOM manipulation
    if (document.getElementById('loginPage')) {
        showPage('loginPage');
    } else {
        window.location.href = '/login/';
    }
}

function showRegister() {
    // For multi-page Django apps, redirect instead of DOM manipulation
    if (document.getElementById('registerPage')) {
        showPage('registerPage');
    } else {
        window.location.href = '/register/';
    }
}

// ========== FORM VALIDATION ========== 
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// ========== CLEAR ERRORS ON INPUT ========== 
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.input, input').forEach(input => {
        input.addEventListener('input', function() {
            const inputGroup = this.closest('.input-group');
            if (inputGroup) {
                inputGroup.classList.remove('error');
            }
            if (this.parentElement) {
                this.parentElement.classList.remove('error');
            }
        });
    });
});

// ========== CSRF TOKEN FOR DJANGO ========== 
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}