// greet user with "Hello, username" when user enters a valid email

console.log('greeter starting');

// current page is on http://127.0.0.1:5000/signin, this function will return http://127.0.0.1:5000
function getHostAndPort() {
    var url = window.location.href.split('/');
    url = url[0] + '//' + url[2];
    return url;
}

function ValidateEmail(email) {
    return (/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(email));
}

function getUsername(email) {
    return fetch(`${getHostAndPort()}/getusername?email=${email}`).then((response) => {
        var result = response.json();
        return result;
    }).then((result) => {
        return result.username;
    });
}

document.addEventListener('DOMContentLoaded', function() {

    const input = document.querySelector('input#email');
    const greeter = document.querySelector('legend');

    input.addEventListener('keyup', function() {
        var email = input.value
        if (ValidateEmail(email)) {
            getUsername(email).then((username) => {
                if (username != null) {
                    greeter.innerHTML = `Hello, ${username}. Please sign in.`;
                } else {
                    greeter.innerHTML = 'Hello, user. Please sign in.'
                }
            });
        }
    });
});