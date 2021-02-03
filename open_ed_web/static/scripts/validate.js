// client side validation for responsiveness

// validate registration fields
function validateRegistration() {
    username = document.querySelector('input[name="username"]');
    email = document.querySelector('input[name="email"]');
    password = document.querySelector('input[name="password"]');
    console.log(
        _usernameIsValid(username) &&
        _emailIsValid(email) &&
        _passwordIsValid(password)
    )
    return (
        _usernameIsValid(username) &&
        _emailIsValid(email) &&
        _passwordIsValid(password)
    );
}

function _usernameIsValid(username) {
    return (
        username.length >= 5 &&
        usernamelength <= 20
    );
}

function _emailIsValid(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function _passwordIsValid(password) {
    return (
        password.length >= 8 &&
        password.length <= 20
    );
}