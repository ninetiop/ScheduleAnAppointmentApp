function login(){
    var username = $('#username').val();
    var password = $('#password').val();
    var data = JSON.stringify({
        username:username,
        password:password,
    })
    $.ajax({
        url: '/login',
        method: 'POST',
        data: JSON.stringify(data),
        success: function(data){
            if(data.success){
                window.location.href = '/admin'
            }
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
            }
        })
}

$(document).ready(function() {
    $("#button").click(function(event) {
        event.preventDefault(); // Prevent the default behavior of the link
        // Add your code here to handle the click event
        login();
    });
});