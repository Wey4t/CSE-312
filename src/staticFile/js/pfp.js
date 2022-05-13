
function able_pfp() {
    var current_image = document.getElementById('pfp_button')
    current_image.hidden = false
}

function show_profile_input() {
    var f = document.getElementById('profile_form')
    var s = document.getElementById('content_form')
    f.hidden = !f.hidden
    if(!f.hidden){
        s.hidden = true
    }
    
}

function show_content_input() {
    var f = document.getElementById('content_form')
    var s = document.getElementById('profile_form')
    f.hidden = !f.hidden
    if(!f.hidden){
        s.hidden = true
    }
    
}