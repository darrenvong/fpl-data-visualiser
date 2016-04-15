$(function() {
  if ($("#position").val() === "Goalkeeper" || $("#position").val() === "Defender") {
      if ($("div.cs").hasClass("hidden")) // i.e. it is hidden
        $("div.cs").removeClass("hidden");
  }

  $("#update").click(function(e) {
    var formElement = e.target.form;
    formElement.elements["num_players"].value = $("#num_players").val();
    if (!addUpdateGraphHandler()) {
      e.preventDefault();
    }
    // Don't submit form if user hasn't specified any filtering at all
    if ($('.filter-block input[type=checkbox]:checked').length === 0) {
      e.preventDefault();
      $(".alert-danger").html('<span class="glyphicon glyphicon-alert"></span>&nbsp;&nbsp;'+
        'Please select at least one item below before clicking "Update".');
      toggleAlertBox(false);
    }
  });

  $("#position").change(function() {
    if ($(this).val() === "Goalkeeper" || $(this).val() === "Defender") {
      if ($("div.cs").hasClass("hidden")) // i.e. it is hidden
        $("div.cs").toggleClass("hidden");
    }
    else { // Forward, Midfielder or All selected
      if (!$("div.cs").hasClass("hidden"))
        $("div.cs").toggleClass("hidden");
    }
  });

  $(".filter-block input[type=checkbox]").change(function() {
    toggleAlertBox(true);
  });
});