$(document).ready(function() {

    $('#subjectField').devbridgeAutocomplete({
        minChars: 0,
        triggerSelectOnValidInput: false,
        preventBadQueries: false,
        serviceUrl: '/suggest_subject/'
    });

    $('#predicateField').devbridgeAutocomplete({
        minChars: 0,
        noCache: true,
        triggerSelectOnValidInput: false,
        preventBadQueries: false,
        serviceUrl: '/suggest_predicate/'
    });

    $('#objectField').devbridgeAutocomplete({
        minChars: 0,
        triggerSelectOnValidInput: false,
        preventBadQueries: false,
        serviceUrl: '/suggest_object/'
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


function inferTypes() {
    $.ajax({
        type: "POST",
        url: "/infer_types/",
        contentType: "application/json",
        dataType: "html",
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (response) {
            if(response.state === "success") {
                search(
                    lastSearchRequest.subject,
                    lastSearchRequest.predicate,
                    lastSearchRequest.object
                );
            }
        }
    });
}


function inferParents() {
    $.ajax({
        type: "POST",
        url: "/infer_parents/",
        contentType: "application/json",
        dataType: "html",
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (response) {
            if(response.state === "success") {
                search(
                    lastSearchRequest.subject,
                    lastSearchRequest.predicate,
                    lastSearchRequest.object
                );
            }
        }
    });
}