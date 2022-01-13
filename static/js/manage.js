function fill(data){
  data = JSON.parse(data);
  if (Object.keys(data).length > 0) {
   $("#table").html("<tr><th>Movie</th><th>Checked Out</th><th>In Stock</th></tr>");
  }
  for (i of data) {
    i = JSON.parse(i);
    row = "<tr><td>" + i.movieName + "</td><td>" + i.checkouts + "</td><td>" + i.inStock + "</td><td><button class='add' id='" + i.id + "_Plus' type='button'>+</button></td><td><button class='subtract' id='" + i.id + "_Minus' type='button'>-</button></td></tr>";
    $("#table").html($("#table").html() + row);
    $(".add").on("click",function(e)
    {
      movieId = this.id.split("_")[0];
      addStock(movieId);
    })
    $(".subtract").on("click",function(e)
    {
      movieId = this.id.split("_")[0];
      removeStock(movieId);
    })
  }
}

function display(data){
  if (data.success == false) {
    $("#response").css("color", "red");
  }
  else { 
    $("#response").css("color", "black");
  }
  $("#response").html(data.message);
  getTable();
}

$(function() //ready function
{
  $("#submit").on("click",function(e) 
  {
    $("#submit").attr("disabled", true);
    movieName = $("#movieName").val().trim();
    $.post(
      "movies/",
      {"action":"addMovie","movieName":movieName},
      display
    )
  })
  getTable();
});

function getTable(){
  $("#submit").attr("disabled", false);
  $.get(
    "movies/",
    {},
    fill
  )
}

function addStock(id){
  $.post(
    "movies/",
    {"action":"addStock","movieId":id},
    getTable
  )
}

function removeStock(id){
  $.post(
    "movies/",
    {"action":"removeStock","movieId":id},
    getTable
  )
}

setInterval(function () { 
  getTable(); 
  }, 10000);