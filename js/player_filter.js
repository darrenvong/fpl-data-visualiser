$(function() {

  function checkPosition() {
    if ($("#position").val() === "Midfielder" || $("#position").val() === "Forward") {
      if (!$("div.cs").hasClass("hidden"))
        $("div.cs").toggleClass("hidden");
    }
    else { // All, Def or GK selected
      if ($("div.cs").hasClass("hidden"))
        $("div.cs").toggleClass("hidden");
    }
  }

  checkPosition();
  $("#update").click(function(e) {
    var formElement = e.target.form;
    formElement.elements["num_players"].value = $("#num_players").val();
    
    // Don't submit form if user hasn't specified any filtering at all
    if ($('.filter-block input[type=checkbox]:checked').length === 0) {
      e.preventDefault();
      $(".alert-danger").html('<span class="glyphicon glyphicon-alert"></span>&nbsp;&nbsp;'+
        'Please select at least one item below before clicking "Update".');
      toggleAlertBox(false);
      if (!addUpdateGraphHandler())
        e.preventDefault();
    }
    else { //Everything is fine, about to submit change
      var csBlock = $("div.cs");
      var csCheckbox = $("input", csBlock);
      if (csBlock.hasClass("hidden") && csCheckbox.prop("checked"))
        csCheckbox.prop("checked", false);
    }
  });

  $("#position").change(checkPosition);

  $(".filter-block input[type=checkbox]").change(function() {
    toggleAlertBox(true);
  });
});