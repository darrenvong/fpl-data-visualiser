/** The top level function call (i.e. the main method) for the player filter page
 ** @author: Darren Vong
 **/

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
    
    // Uncheck the "Clean sheets" checkbox if it is hidden
    var csBlock = $("div.cs");
    var csCheckbox = $("input", csBlock);
    if (csBlock.hasClass("hidden") && csCheckbox.prop("checked"))
      csCheckbox.prop("checked", false);

    // Don't submit form if user hasn't specified any filtering at all
    if ($('.filter-block input[type=checkbox]:checked').length === 0) {
      let message = 'Please select at least one item below before clicking "Update".';
      inactiveError(e, message);
      return;
    }
    else if (!checkGameweek()) // Don't submit form if start game week is later than end game week
      e.preventDefault();
  });

  $("#position").change(checkPosition);

  $(".filter-block input[type=checkbox]").change(function() {
    toggleAlertBox(true);
  });
});
