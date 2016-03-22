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
  return s.charAt(0).toUpperCase() + s.substring(1).toLowerCase();
}