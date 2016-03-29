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
 **/
PlayerSearchBar.prototype.onSearch = function(e, selectors) {
  for (let i=0; i < selectors.length; i++) {
    let inputVal = capitalise( normalise( $(selectors[i]).val().trim() ) );
    if (inputVal === "")
      e.preventDefault();
    else if (!this.playerNames.includes(inputVal)) {
      e.preventDefault();
      var errMsg = $(".help-block.text-warning");
      if (errMsg.hasClass("hidden"))
        $(".help-block.text-warning").toggleClass("hidden"); // Reveals error message

      var bar = $(selectors[i]);
      if (!bar.hasClass("error"))
        $(selectors[i]).toggleClass("error"); // Makes the search box border glow in red
    }
  }
};