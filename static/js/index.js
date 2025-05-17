// get appointments available
function get_data(){
    var nom = $('#nom').val();
    var prenom = $('#prenom').val();
    var date = $('#date').val();
    var data = JSON.stringify({
        nom:nom,
        prenom:prenom,
        date:date
    })
    if (is_date_valid(date)){
        $.ajax({
        url: '/',
        method: 'POST',
        data: JSON.stringify(data),
        success: function(data){
            if (data['slots'].length > 0){
                $('#fieldset-slot').css('display', 'block');
                data['slots'].forEach((element) => {
                    element_formatted = element.split(" ")[1];
                    element_formatted = element_formatted.substring(0, element_formatted.length - 3);
                    $('#select').append($('<option>', {
                        value: element_formatted,
                        text: element_formatted
                        }));
                });
            }
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
            }
        })
    }
    else{
        alert('La date n\'est pas valide');
    }
}

$("#date").on('change', function(){
    val = $(this).val()
    if (is_date_valid(val)){
        get_data();
    }
    else{
        $('#fieldset-slot').hide().change();
        $('#datepicker').val('dd/mm/yyyy').change();
    }
});

// submit
$(document).ready(function() {
    $('#contact-submit').on('click', function() {
        $('#alertNotif').empty()
        var nom = $('#nom').val();
        var prenom = $('#prenom').val();
        var date = $('#date').val();
        var slot = $('#select').val();
    
        var data = JSON.stringify({
            nom:nom,
            prenom:prenom,
            date:date,
            slot:slot
        })
        if (is_field_valid() && is_date_valid(date)){
            $.ajax({
                url: '/',
                method: 'POST',
                data: JSON.stringify(data),
                success: function(data){
                    if (data['success']){
                        clear_form()
                        display_notif('Votre RDV a bien été pris', data['success']);
                    }
                },
                error: function(xhr, status, error) {
                    display_notif('Votre RDV n\'a pas été pris', false);
                }
            })
        }
        else{
            alert('Remplissez tous les champs et prenez une date valide')
        }
    })
});

function clear_form(){
    $('#nom').val('');
    $('#prenom').val('');
    $('#date').val('');
    $('#select').val('');
    $('#fieldset-slot').hide();
    $('#select').empty();
    $('#datepicker').val('dd/mm/yyyy');
}

function display_notif(msg, success) {
    s = '<div class="alert alert-' + (success ? 'success' : 'danger') + ' alert-dismissible fade in" role="alert">' +
        msg + ' <strong>' + (success ? 'avec succès.' : 'malheureusement, veuillez recharger la page et réessayer.') + '</strong>' +
        '</div>';
    $('#alertNotif').html(s);
}

function is_date_valid(){
    date = $('#date').val()
    current_date = new Date();
    valid_date = new Date(date);
    current_date.setHours(0, 0, 0, 0);
    valid_date.setHours(0, 0, 0, 0);
    // Compare the time difference
    if (valid_date < current_date) {
        return false
    }
    return true
}

function is_field_valid(){
    var nom = $('#nom').val();
    var prenom = $('#prenom').val();
    var date = $('#date').val();
    var slot = $('#slot').val()
    if (prenom == ''){
        return false
    }
    if (nom == ''){
        return false    
    }
    if (date == ''){
        return false
    }
    if (String(date).includes('y'))
        return false
    if (String(date).includes('m'))
        return false
    if (String(date).includes('d'))
        return false
    if (slot == ''){
        return false    
    }
    return true
}