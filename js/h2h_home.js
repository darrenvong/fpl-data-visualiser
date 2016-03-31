$(function() {
  var searchBars = new PlayerSearchBar("#player1, #player2");
  $("button[type='submit']").click(function(e) {
    searchBars.onSearch(e, ["#player1", "#player2"], true);
  });

  $("#player1_field, #player2_field").submit(function(e) {
    searchBars.onSearch(e, ["#player1", "#player2"], true);
  });

  hideErrorPrompts("#player1, #player2");
});