function PlayerSearchBar() {
  this.playerNames = [];
}

PlayerSearchBar.prototype.init = function() {
  var thisClass = this;
  $.ajax({
    type: "POST",
    url: "/player_names",
    success: function(data) {
      thisClass.playerNames = data;
      $('#player-names').autocomplete({
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
};

PlayerSearchBar.prototype.onSearch = function(e) {
  var inputVal = capitalise( normalise( $('#player-names').val().trim() ) );
  if (inputVal === "")
    e.preventDefault(); //prevents search if user types in nothing!
  else if (!this.playerNames.includes(inputVal)) {
      e.preventDefault();
      alert("Player not found!");      
  }
}
