function select_user(user) {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            var user_list = document.getElementsByClassName(user.className)
            for(let i = 0; i < user_list.length;++i){
                var u = user_list[i]
                u.className = u.className.replace('active',' ');
            //console.log(u.className)
            }
            if (user.className.includes('active')) {
                user.className = user.className.replace('active',' ');
            }else{
                user.className += 'active'
            }
        }
        
    };
    var name = user.id
    request.open("GET", "/chat-history/"+name);
    request.send();
    
}
