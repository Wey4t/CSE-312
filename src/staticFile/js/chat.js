function select_user(user) {
    window.location.href='/chat/'+user.id    
}
function acitve_user() {
    let posistion = window.location.href.lastIndexOf('/')
    let username =  window.location.href.slice(posistion+1)
    console.log(username)
    let user = document.getElementById(username)
    if (user.className.includes('active')) {
        user.className = user.className.replace('active',' ');
    }else{
        user.className += ' active'
    }
        
}