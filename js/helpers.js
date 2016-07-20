/** A set of common utility functions that are useful across all pages of the system
 ** @author: Darren Vong
 **/

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

function checkGameweek() {
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

/**
 ** Event handling function (logic) for when the "Update graph" button is clicked.
 ** @param e: the button click event fired upon clicking the update graph button
 ** @param control: the element which contains the interface for controlling how to update the graph on the page
 ** @param graph: reference to the page's graph object
 **/
function updateGraphHandler(e, control, graph) {
  if ($("input[type=checkbox]:checked").length === 0) { // Don't update if no "Active" boxes are checked
    let message = 'Please tick one of the checkboxes above before clicking "Update graph" again.';
    inactiveError(e, message);
  }
  else { // Don't update if the start game week is later than end game week
    let gameWeekEndPoints = checkGameweek();
    if (gameWeekEndPoints)
      graph.update(gameWeekEndPoints[0], gameWeekEndPoints[1]);
  }
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

/**
 ** Prompt to display to user when no "Active" checkboxes have been checked before trying to update the graph or player filter search
 ** @param e: the button click event fired upon clicking the update (graph) button
 ** @param msg: the message to display
 **/
function inactiveError(e, msg) {
  e.preventDefault();
  $(".alert-danger").html('<span class="glyphicon glyphicon-alert"></span>&nbsp;&nbsp;'+msg);
  toggleAlertBox(false);
}
