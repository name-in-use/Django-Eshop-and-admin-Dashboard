function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

var UserDeleteBtns = document.getElementsByClassName('update-users')

for (var i = 0; i < UserDeleteBtns.length; i++) {

    UserDeleteBtns[i].addEventListener('click', function() {
        console.log('Delete user clicked')
        var userId = this.dataset.user
        DeleteUser(userId)

    })

}

function DeleteUser(userID) {
    var url = '/adminpanel/deleteUsers/'

    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'userID': userID })
        })
        .then((response) => {
            return response.json()
        })

    .then((data) => {
        console.log('data:', data)
        location.reload()
    })
}