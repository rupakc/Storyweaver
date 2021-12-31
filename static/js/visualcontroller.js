function getErrorMessage(jqXHR, exception) {
    var msg = '';
    if (jqXHR.status === 0) {
        msg = 'Not connect.\n Verify Network.';
    } else if (jqXHR.status == 404) {
        msg = 'Requested page not found. [404]';
    } else if (jqXHR.status == 500) {
        msg = 'Internal Server Error [500].';
    } else if (exception === 'parsererror') {
        msg = 'Requested JSON parse failed.';
    } else if (exception === 'timeout') {
        msg = 'Time out error.';
    } else if (exception === 'abort') {
        msg = 'Ajax request aborted.';
    } else {
        msg = 'Uncaught Error.\n' + jqXHR.responseText;
    }
    alert(msg)
}


function addListener() {
   var input = document.getElementById("search");
    input.addEventListener("keyup", function(event) {
    event.preventDefault();
       if (event.keyCode === 13) {
          document.getElementsByClassName("btn-success")[0].click();
       }
    });
}


$(document).ready(function() {
     addListener();
     $('.btn-success').click(function() {
          $("div#divLoading").addClass('show');
          $("div#divLoading").show();

          var search_term = $('#search').val();
          var pathname = window.location.pathname;
          if (pathname == '/') {
              $('#imageList').nextAll().empty().removeClass();
              $.ajax({
               type: "GET",
               url: "/search",
               data: {'search_term': search_term},
               success: function(data){
                    var imageList = data.imageList;
                    for(let i = 0; i < imageList.length; i++) {
                        $('#imageList').after("<div class='col col-md-4 thumbnail'>" +
                        " <img src=" + "'" + imageList[i] + "'" + "style='width:auto;height:260px'" + ">"
                        + "</div>")
                        console.log(imageList[i])
                    }

                    $('div#divLoading').removeClass('show');
                    $('div#divLoading').hide();
               },
               error: function (jqXHR, exception) {
                    $('div#divLoading').removeClass('show');
                    $('div#divLoading').hide();
                    getErrorMessage(jqXHR, exception);
               }
            });
          } else if (pathname == '/dissect') {
               $('#imageObjectList').nextAll().empty().removeClass();
               $.ajax({
               type: "GET",
               url: "/getobjects",
               data: {'search_term': search_term},
               success: function(data){
                    var imageObjectList = data.imageObjectList;
                    for(let i = 0; i < imageObjectList.length; i++) {
                        $('#imageObjectList').append("<div class='col col-md-1 thumbnail'>" +
                        " <img src=" + "'" + imageObjectList[i] + "'" + "style='width:auto;height:100px'" + ">"
                        + "</div>")
                        console.log(imageObjectList[i])
                    }

                    $('div#divLoading').removeClass('show');
                    $('div#divLoading').hide();
               },
               error: function (jqXHR, exception) {
                    $('div#divLoading').removeClass('show');
                    $('div#divLoading').hide();
                    getErrorMessage(jqXHR, exception);
               }
            });
          }
     });
});
