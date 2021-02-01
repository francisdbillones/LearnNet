// functions for validation

function validateSearch() {
    var searchQuery = document.querySelector("input[name='search']");
    console.log(searchQuery.value)
    console.log(searchQuery.value == '')
    if (searchQuery.value == '') {
        return false;
    }
    return true;
}