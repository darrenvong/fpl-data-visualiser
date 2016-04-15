/* Converts diacritic input into its non-diacritic equivalent. Diacritics are accents/marks
in a letter/alphabet which stresses how words should be pronounced.
e.g. the letter "è" with the grave accent would be same as "e"
*/
function normalise(input) {
  var ret = "";
  for (var i=0; i<input.length; i++) {
    ret += accent_map[input.charAt(i)] || input.charAt(i);
  }
  return ret;
}

function capitalise(s) {
  var words = s.split(" ");
  words = words.map(function(w) {
    return w.charAt(0).toUpperCase()+w.substring(1).toLowerCase();
  });
  return words.join(" ");
}

/** Dynamically centers elements matched with respect to the context element's width by setting the
 ** element's "left" css property value.
 ** @param elements: the set of elements to center
 ** @param context: the element's width to base the centering calculation on
 **/
function centElement(elements, context) {
  var contextElementWidth = context.width();
  elements.css("left", function(i,v) {
    return ( contextElementWidth - $(this).width() ) / 2;
  });
}

function hideErrorPrompts(searchBar) {
  $(searchBar).on("input", function() {
    if ($(this).hasClass("error"))
      $(this).removeClass("error");

    var errMsg = $(".help-block.text-warning");
    if (!errMsg.hasClass("hidden")) //Error is on show, turn it off now that user is updating input
      errMsg.toggleClass("hidden");
  });
}

function addUpdateGraphHandler() {
  var start = parseInt($("#startTime").val());
  var end = parseInt($("#endTime").val());
  if (start > end) {
    toggleAlertBox(false);
    var message = ("The start game week cannot be later than the end game week. "+
      "Please check your game week time selection.");
    $(".alert-danger").html('<span class="glyphicon glyphicon-alert"></span>&nbsp;&nbsp;'+message);
    return;
  }

  return [start, end];
}

function toggleAlertBox(valid) {
  var alertBox = $(".alert-danger");

  if (valid) {
    // Item is at valid state, yet the alert is not hidden, so hide it
    if (!alertBox.hasClass("hidden"))
      alertBox.toggleClass("hidden");
  }
  else {
    if (alertBox.hasClass("hidden"))
      alertBox.toggleClass("hidden")
    else { //Invalid state, alert already shown, so highlight it for emphasis
      alertBox.effect("highlight", {color: "#a94442"});
    }
  }
}