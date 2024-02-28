var updateBtns = document.getElementsByClassName('update-cart')

for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var foodId = this.dataset.product
        var action = this.dataset.action
        console.log('foodId:', foodId, 'action:', action)

        console.log('USER:', user)
        if(user === 'AnonymousUser'){
            addCookieItem()
            
        } else{
            updateUserOrder(foodId, action)
        }
    })
}

function updateUserOrder(foodId, action){
    console.log('Вы вошли в систему, отправка данных..')

    var url = '/update_item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'foodId':foodId, 'action':action})
    })

    .then((response) =>{
        return response.json()
    })
    .then((data) =>{
        console.log('data:', data)
        location.reload()
    })
}