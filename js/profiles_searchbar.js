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

function initPlayerSearchBar() {
  $.ajax({
    type: "POST",
    url: "/player_names",
    success: function(data) {
      $('#player-names').autocomplete({
        // Adapted from https://jqueryui.com/autocomplete/#folding example
        source: function(request, response) {
          // Creates a regular expression matcher object from the user input
          var matcher = new RegExp($.ui.autocomplete.escapeRegex(request.term), "i");
          // Return names which matches the regular expression directly,
          // or names which matches the regular expression after converting
          // from its diacritic equivalent. E.g. "Özil" -> "Ozil"
          response($.grep(data, function(value) {
            return matcher.test(value) || matcher.test(normalise(value));
          }));
        }
      });
    }
  });
}