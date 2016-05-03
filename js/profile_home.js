/** The top level function call (i.e. the main method) for the profiles_home page
 ** @author: Darren Vong
 **/

$(document).ready(function() {
  var searchBarSelector = '#player-names';
  var searchBar = new PlayerSearchBar(searchBarSelector);

  $("button.large-searchbar-btn").click(function(e) {
    searchBar.onSearch(e, [searchBarSelector]);
  });

  hideErrorPrompts(searchBarSelector);
});
