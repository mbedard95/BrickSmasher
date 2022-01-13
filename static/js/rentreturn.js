user_email = "";

function fillStock(data){
  data = JSON.parse(data);
  if (Object.keys(data).length > 0) {
   $("#stockTable").html("<tr><th>Movie</th><th>In Stock</th></tr>");
  }
  else {
    $("#stockTable").html("There are no movies in stock.");
  }
  for (i of data) {
    i = JSON.parse(i);
    row = "<tr><td>" + i.movieName + "</td><td>" + i.inStock + "</td><td><button class='rent' id='" + i.id + "_Rent' type='button'>Rent</button></td></tr>";
    $("#stockTable").html($("#stockTable").html() + row);
  }
  $(".rent").on("click",function(e)
    {
      $(".rent").attr("disabled", true);
      movieId = this.id.split("_")[0];
      addCheckout(user_email, movieId);
    })
}

function fillCheckout(data){
  data = JSON.parse(data);
  console.log(data);
  if (Object.keys(data).length == 0) {
    $("#rentTable").html("This user has no movies rented");
  }
  else {
    $("#rentTable").html("<tr><th>Movie</th></tr>");
    for (i of data) {
      i = JSON.parse(i);
      row = "<tr><td>" + i.movieName + "</td><td><button class='return' id='" + i.id + "_Return' type='button'>Return</button></td></tr>";
      $("#rentTable").html($("#rentTable").html() + row);
    }
  }
  $(".return").on("click",function(e)
    {
      $(".return").attr("disabled", true);
      movieId = this.id.split("_")[0];
      returnCheckout(user_email, movieId);
    })
}

function movieDisplay(data){
  $("#submit").attr("disabled", false);
  if (data.success == false) {
    $("#response").css("color", "red");
    $("#response").html(data.message);
    $("#display").html("");
    $("#stockTable").html("");
    $("#rentMessage").html("");
  }
  else { 
    $("#response").html("");
    $("#rentMessage").html("");
    $("#display").css("color", "black");
    $("#display").html("Displaying results for " + data.first + " " + data.last + ":");
    user_email = data.email
    getCheckouts(user_email);
    getStock();
  }
}

function checkoutDisplay(data){
  $(".rent").attr("disabled", false);
  if (data.success == false) {
    $("#rentMessage").css("color", "red");
  }
  else { 
    $("#rentMessage").css("color", "black");
  }
  $("#rentMessage").html(data.message);
  getCheckouts(user_email);
  getStock()
}

$(function() //ready function
{
  $("#submit").on("click",function(e) 
  {
    $("#submit").attr("disabled", true);
    email = $("#email").val().trim();
    $.get(
      "users/",
      {"email":email},
      movieDisplay
    )
  })
});

function getStock(){
  $.get(
    "movies/",
    {},
    fillStock
  )
}

function getCheckouts(){
  $.get(
    "checkouts/",
    {"email":user_email},
    fillCheckout
  )
}

function addCheckout(email,movieId){
  $.post(
    "checkouts/",
    {"action":"add","email":email,"movieId":movieId},
    checkoutDisplay
  )
}

function returnCheckout(email,movieId){
  $.post(
    "checkouts/",
    {"action":"delete","email":email,"movieId":movieId},
    checkoutDisplay
  )
}