function PlayerSearchBar(selector) {
  this.playerNames = [];
  var thisClass = this;
  $.ajax({
    type: "POST",
    url: "/player_names",
    success: function(data) {
      thisClass.playerNames = data;
      $(selector).autocomplete({
        // Adapted from https://jqueryui.com/autocomplete/#folding example
        source: function(request, response) {
          // Creates a regular expression matcher object from the user input
          var matcher = new RegExp($.ui.autocomplete.escapeRegex(normalise(request.term)), "i");
          // Return names which matches the regular expression directly,
          // or names which matches the regular expression after converting
          // from its diacritic equivalent. E.g. "Özil" -> "Ozil"
          response($.grep(data, function(value) {
            return matcher.test(value);
          }));
        }
      });
    }
  });
}

/** Event handling logic at the point when the user has confirmed search
 ** (pressed enter/clicked search on the input they typed in) using the player search bar
 ** @param selectors: An array list containing the selectors for each input field
 ** @param e: The event being fired upon clicking the submit button/Pressing Enter on the keyboard
 ** @param multipleFields (optional): a boolean flag indicating whether the search bar consists of multiple fields
 **/
PlayerSearchBar.prototype.onSearch = function(e, selectors, multipleFields) {
  var hasErrors;
  for (let i=0; i < selectors.length; i++) {
    let inputVal = capitalise( normalise( $(selectors[i]).val().trim() ) );
    if (inputVal === "") {
      e.preventDefault();
      hasErrors = true;
    }
    else if (!this.playerNames.includes(inputVal)) {
      e.preventDefault();
      var errMsg = $(".help-block.text-warning");
      if (errMsg.hasClass("hidden"))
        $(".help-block.text-warning").toggleClass("hidden"); // Reveals error message

      var bar = $(selectors[i]);
      if (!bar.hasClass("error"))
        $(selectors[i]).toggleClass("error"); // Makes the search box border glow in red
      hasErrors = true;
    }
  }

  hasErrors = hasErrors || false;
  if (!hasErrors && multipleFields) { //No errors found, search bar has multiple fields
    //Call insertQueryValues to do something
    this.insertQueryValues(e);
  }
};

/** A fix on the search bars on the head-to-head comparator page since the submit button
 ** and the input fields are not in the same form.
 ** @param selectors: An array list containing the selectors for each input field
 **/
PlayerSearchBar.prototype.insertQueryValues = function(e) {
  var formElement = e.target;
  if (formElement.id.startsWith("player1")) { // Event came from player1 field
    formElement.elements["player2"].value = $("#player2").val();
  }
  else if (formElement.id.startsWith("player2"))
    formElement.elements["player1"].value = $("#player1").val();
  else { // Event came from button click, so formElement is the actual button
    formElement = formElement.parentElement;
    formElement.elements["player1"].value = $("#player1").val();
    formElement.elements["player2"].value = $("#player2").val();
  }
};