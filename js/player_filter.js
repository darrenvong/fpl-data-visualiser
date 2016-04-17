$(function() {
  if ($("#position").val() !== "Midfielder" || $("#position").val() !== "Forward") { // i.e. All, Def or GK selected
      if ($("div.cs").hasClass("hidden"))
        $("div.cs").toggleClass("hidden");
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
    if ($(this).val() === "Midfielder" || $(this).val() === "Forward") {
      if (!$("div.cs").hasClass("hidden")) // not hidden
        $("div.cs").toggleClass("hidden");
    }
    else { // Goalkeeper, Defender or All selected
      if ($("div.cs").hasClass("hidden")) // hidden
        $("div.cs").toggleClass("hidden");
    }
  });

  $(".filter-block input[type=checkbox]").change(function() {
    toggleAlertBox(true);
  });
});