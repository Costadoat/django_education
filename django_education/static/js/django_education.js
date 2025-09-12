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

// Menu deroulant systemes

$(".checkbox-menu").on("change", "input[type='checkbox']", function() {
   $(this).closest("li").toggleClass("active", this.checked);
});

$(document).on('click', '.allow-focus', function (e) {
  e.stopPropagation();
});

$("question").submit(function() {
  if (window.File && window.FileReader && window.FileList && window.Blob) {
    var file = $('#id_file')[0].files[0];

    if (file && file.size > 2 * 1024 * 1024) {
      alert("File " + file.name + " of type " + file.type + " is too big");
      return false;
    }
  }
});

