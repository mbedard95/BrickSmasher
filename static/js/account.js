function display(data){
  if (data.success == false) {
    $("#response").css("color", "red");
  }
  else { 
    $("#response").css("color", "black");
  }
  $("#response").html(data.message);
}

$(function() //ready function
{
  $("#submit").on("click",function(e) 
  {
    first = $("#first").val().trim();
    last = $("#last").val().trim();
    email = $("#email").val().trim();
    $.post(
      "users/",
      {"first":first,"last":last,"email":email},
      display
    )
  })
});