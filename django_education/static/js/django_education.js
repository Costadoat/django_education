// ajax call on your button click
var url = $( '/resultats/' ).attr( 'action' );
$("selection-button").click(function(e) {
    e.preventDefault();
    $.ajax({
        type: "GET",
        url: url,
        data: {
            id: $('#etudiant').val();
            },
        success: function(result) {
            alert('ok');
        },
        error: function(result) {
            alert('error');
        }
    });
});
