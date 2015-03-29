$(document).ready(function() {

    var predicates = [
        { value: 'belongs_to', data: 'belongs_to' },
        { value: 'is_type', data: 'is_type' }
    ];

    $('#subjectField').devbridgeAutocomplete({
        minChars: 1,
        width: 300,
        triggerSelectOnValidInput: false,
        preventBadQueries: false,
        serviceUrl: '/suggestSubject/'
    });

    $('#predicateField').devbridgeAutocomplete({
        minChars: 0,
        width: 300,
        triggerSelectOnValidInput: false,
        preventBadQueries: false,
        lookup: predicates
    });

    $('#objectField').devbridgeAutocomplete({
        minChars: 0,
        width: 300,
        triggerSelectOnValidInput: false,
        preventBadQueries: false,
        serviceUrl: '/suggestObject/'
    });

    $("#searchform").submit(function(event) {
        event.preventDefault();
        search($("#subjectField").val(), $("#predicateField").val(), $("#objectField").val())
    });

    //$("#load").hide();
    $("#clearFacet").hide();

});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
var lastSearchRequest;

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function search(subject, predicate, object) {
    if(subject === ""){
        subject = null
    }
    if(predicate === ""){
        predicate = null
    }
    if(object === ""){
        object = null
    }

    $("#clearFacet").hide();
    //$("#load").hide();
    $('#subjectField').val(subject);
    $('#predicateField').val(predicate);
    $('#objectField').val(object);

    $('#results').html(
        '<div style="text-align: center; margin-top: 50px; ">' +
        '<span class="glyphicon glyphicon-refresh glyphicon-refresh-animate">' +
        '</span>' +
        '</div>'
    );

    lastSearchRequest = {
        "subject":subject,
        "predicate":predicate,
        "object":object
    };

    $.ajax({
        type: "POST",
        url: "/search/",
        data: JSON.stringify(lastSearchRequest),
        contentType: "application/json",
        dataType: "html",
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (response) {
            parseResponse(response);
        }
    });
}

function parseResponse(rawResponse) {
    if(rawResponse == null || !rawResponse) {
        resultsContainer.html('<div class="span3" style="padding-left:25px;">' +
        '<br/><br/>The inserted search query is invalid.</div>');

    } else {

        //var encodedResponse = btoa(encodeURI(rawResponse));
        //$('#results').html("<br><br><br><br>").append(encodedResponse);

        var img = new Image();
        img.src = 'data:image/png;base64,' + rawResponse;
        $('#results').html("<br><br><br><br>").append(img);
    }
}