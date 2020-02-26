var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            xhr.setRequestHeader("content-type", "application/json");
        }
    }
});

function showalert(message,alerttype) {

    $('#alert_placeholder').append('<div id="alertdiv" class="alert ' +  alerttype + '"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>')

    // this will automatically close the alert and remove this if the users doesnt close it in 5 secs
    setTimeout(function() { 
      $("#alertdiv").remove();
    }, 5000);
  }

function AddFileToCart(file_id, button) {
    $.ajax({
        url: "/ajax/add_to_cart/",
        type: "POST",
        dataType: "json",
        success: function(data){
            message = "The file " + data.file_name + " was addded to your download cart"
            showalert(message, "alert-success");
            button.disabled = true;
        },
    });
}

function AddCorpusToCart(corpus_id) {
    $.ajax({
        url: "/ajax/add_to_cart/",
        type: "POST",
        dataType: "json",
        data: JSON.stringify({corpus_id: corpus_id}),
        success: function(data){
            message = "All the files in the corpus " + data.corpus_name + " were addded to your download cart"
            showalert(message, "alert-success")
        },
    });
}

function AddSearchResultsToCart(search_results_file_ids) {
    $.ajax({
        url: "/ajax/add_to_cart/",
        type: "POST",
        dataType: "json",
        data: JSON.stringify({search_results_file_ids: search_results_file_ids}),
        success: function(data){
            message = "All the files from the search results were addded to your download cart"
            showalert(message, "alert-success")
        },
    });
}

function RemoveFileFromCart(file_id, button) {
    $.ajax({
        url: "/ajax/remove_from_cart/",
        type: "POST",
        dataType: "json",
        data: JSON.stringify({file_id: file_id}),
        success: function (data) {
            $(button).parents(".card").remove();
            message = "The file " + data.file_name + " was removed from your download cart"
            showalert(message, "alert-warning");
        },
    });
}

function ClearCart() {
    $.ajax({
        url: "/ajax/clear_cart/",
        type: "POST",
        dataType: "json",
        success: function (data) {
            $(".card").remove();
            $("#cart").html("Your cart is empty!")
            message = "Your download cart was emptied"
            showalert(message, "alert-warning");
        },
    })
}

$(document).ready(function(){
    $('.alert').hide();
}); 
