$(document).ready(function(){
    $("li").removeClass("active");
    var all_lists = $("li");
    var pathname = window.location.pathname; // Get pathname from url

    $.each(all_lists, function (index, child) {
            if (pathname == "/") {
                if (child.textContent === "Search") {
                    $(child).addClass("active");
                }
            }

            else if (pathname == "/dissect") {
              if (child.textContent === "Dissect") {
                    $(child).addClass("active");
                }
            }

            else if (pathname == "/weave") {
              if (child.textContent === "Weave") {
                    $(child).addClass("active");
                }
            }
    });
});
