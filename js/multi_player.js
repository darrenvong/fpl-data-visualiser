$(function() {
  $("#update").click(function(e) {
    var formElement = e.target.form;
    formElement.elements["num_players"].value = $("#num_players").val();
    // Don't submit form if user hasn't specified any filtering at all
    if ($('.filter-block input[type=checkbox]:checked').length === 0)
      e.preventDefault();
  });
});