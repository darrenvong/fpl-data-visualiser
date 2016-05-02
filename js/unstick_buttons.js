/** Ensures when buttons are clicked, they are not remained in focus (i.e. stuck)
 ** @author: Darren Vong
 **/

$(document).ready(function() {
  $("button, .navbar-nav>li>a").click(function() {
    $(this).blur();
  });
});
