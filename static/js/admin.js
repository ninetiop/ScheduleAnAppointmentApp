$(document).ready(function(){
	// Activate tooltip
	var currentDate = new Date();  
	var formattedDate = currentDate.getFullYear() + "-" + ("0" + (currentDate.getMonth() + 1)).slice(-2) + "-" + ("0" + currentDate.getDate()).slice(-2);
	$('#date').val(formattedDate)
});


$("#date").on('change', function(){
    val = $(this).val()
    if (is_date_valid(val)){
        get_appointments(val);
    }
    else{
        $('#fieldset-slot').hide().change();
        $('#datepicker').val('dd/mm/yyyy').change();
    }
});

$(".btn-success").on('click', function(){
    var row = $(this).closest("tr");
    var lastname = row.find("td:eq(0)").text(); // Get the value of the first <td> element
    var firstname = row.find("td:eq(1)").text(); // Get the value of the second <td> element
    var date = $('#date').val() + ' ' +row.find("td:eq(2)").text() + ':00' // Get the value of the third <td> element
	var action = 'archiver';
    var data = JSON.stringify({
        lastname:lastname,
        firstname:firstname,
        date:date,
        action:action
    });
    $.ajax({
        url: '/admin',
        method: 'POST',
        data: JSON.stringify(data),
        success: function(data){
            row.remove();
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
            }
        })
	
})

$(".btn-danger").on('click', function(){
    var row = $(this).closest("tr");
    var lastname = row.find("td:eq(0)").text(); // Get the value of the first <td> element
    var firstname = row.find("td:eq(1)").text(); // Get the value of the second <td> element
    var date = $('#date').val() + ' ' +row.find("td:eq(2)").text() + ':00' // Get the value of the third <td> element
	var action = 'supprimer';
    var data = JSON.stringify({
        lastname:lastname,
        firstname:firstname,
        date:date,
        action:action
    });
    $.ajax({
        url: '/admin',
        method: 'POST',
        data: JSON.stringify(data),
        success: function(data){
            row.remove();
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
            }
        })
	
})

function is_date_valid(date){
    if (String(date).includes('y'))
        return false
    if (String(date).includes('m'))
        return false
    if (String(date).includes('d'))
        return false
    return true
}

function get_appointments(date){
	var data = JSON.stringify({
		date:date,
        action:'get_appointment'
	});
	$.ajax({
        url: '/admin',
        method: 'POST',
        data: JSON.stringify(data),
        success: function(data){
			clean_table();
            if (data['appointments'].length > 0){
				data['appointments'].forEach((element) => {
                	var newRow = $("<tr>");
					var lastname = $("<td>").text(element.lastname);
					newRow.append(lastname);
					var firstname = $("<td>").text(element.firstname);
					newRow.append(firstname);
					var date = $("<td>").text(element.date);
					newRow.append(date);
					var td_btn = $("<td>").addClass("td-btn");
					var button_archive = $("<button>").text("Archives");
					button_archive.addClass("btn btn-success")
					var button_delete = $("<button>").text("Supprimer");
					button_delete.addClass("btn btn-danger")
					td_btn.append(button_archive);
					td_btn.append(button_delete);
					newRow.append(td_btn);
					$("#table").append(newRow);
				});
            }
        },
        error: function(xhr, status, error) {
        	console.error('Error:', error);
        }
    })

}

function clean_table(){
	$('#table tbody tr').empty();
}