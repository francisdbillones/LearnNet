document.addEventListener('DOMContentLoaded', function() {
    routeButtons = document.getElementsByClassName('route-button');
    Array.prototype.map.call(routeButtons, function(routeButton) {
        routeButton.onclick = function() {
            // a button with id of edit-button will add /edit to the current location.
            window.location += '/' + routeButton.id.split('-')[0];
        };
    });
});