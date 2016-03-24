/** The top level function call (i.e. the main method) for the profiles_home page
 ** @author: Darren Vong
**/

$(document).ready(function() {
  var searchBar = new PlayerSearchBar();

  $("button.large-searchbar-btn").click(function(e) {
    searchBar.onSearch(e);
  });
});