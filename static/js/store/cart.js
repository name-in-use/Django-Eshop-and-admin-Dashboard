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

function clearCart() {
    cart = {}
    location.reload()
    document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/"
}




var RecommendBtns = document.getElementsByClassName('set-recommend')

for (var i = 0; i < RecommendBtns.length; i++) {

    RecommendBtns[i].addEventListener('click', function () {
        if (user != "Guest User") {
            console.log('recommend clicked')
            var productId = this.dataset.product
            var url = 'http://127.0.0.1:8000/recommend_product/'
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({ 'productId': productId })
            })
                .then((response) => {
                    return response.json()
                })

                .then((data) => {
                    console.log('data:', data)
                    location.reload()
                })
        } else {
            alert('Please Login to recommend products')
        }
    })

}


var updateBtns = document.getElementsByClassName('update-cart')
for (var i = 0; i < updateBtns.length; i++) {

    updateBtns[i].addEventListener('click', function () {
        if (user != "Guest User") {
            var productId = this.dataset.product
            var action = this.dataset.action
            console.log('product id:', productId, 'action:', action)
            addCookieItem(productId, action)
        } else {
            alert('Please Login to purchace products')
        }

    })

}


function addCookieItem(productId, action) {
    console.log('Not logged in...')

    if (action == "add") {
        if (cart[productId] == undefined) {
            cart[productId] = { 'quantity': 1 }

        } else {
            cart[productId]['quantity'] += 1
        }
    }

    if (action == "remove") {
        cart[productId]['quantity'] -= 1

        if (cart[productId]['quantity'] <= 0) {
            console.log("remove item")
            delete cart[productId]
        }

    }
    console.log("Cart=", cart)
    location.reload()
    document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/"

}


function updateUserOrder(productId, action) {
    console.log('User is logged in, sending data..')
    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'user': currentuser, 'productId': productId, 'action': action })
    })
        .then((response) => {
            return response.json()
        })

        .then((data) => {
            console.log('data:', data)
            location.reload()
        })
}