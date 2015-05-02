$(document).ready(function() {

    $('[name="field[0].subject"]').devbridgeAutocomplete({
        minChars: 0,
        triggerSelectOnValidInput: false,
        preventBadQueries: false,
        serviceUrl: '/suggest_subject/'
    });

    $('[name="field[0].predicate"]').devbridgeAutocomplete({
        minChars: 0,
        triggerSelectOnValidInput: false,
        preventBadQueries: false,
        serviceUrl: '/suggest_predicate/',
        noCache: true
    });

    $('[name="field[0].object"]').devbridgeAutocomplete({
        minChars: 0,
        triggerSelectOnValidInput: false,
        preventBadQueries: false,
        serviceUrl: '/suggest_object/',
        width: 200
    });

    var fieldIndex = 0;

    $('#fieldForm')
        .submit(function(event) {
            event.preventDefault();
            var triples = [];
            for(var i = 0; i <= fieldIndex; i++) {
                var t = {
                    subject: $('[name="field['+i+'].subject"]').val(),
                    predicate: $('[name="field['+i+'].predicate"]').val(),
                    object: $('[name="field['+i+'].object"]').val()
                };
                if(t.subject === ""){
                    t.subject = null
                }
                if(t.predicate === ""){
                    t.predicate = null
                }
                if(t.object === ""){
                    t.object = null
                }
                triples.push(t);
            }
            search(triples)
        })
        // Add button click handler
        .on('click', '.addButton', function() {
            fieldIndex++;
            var $template = $('#fieldTemplate'),
                $clone = $template
                    .clone()
                    .removeClass('hide')
                    .removeAttr('id')
                    .attr('data-field-index', fieldIndex)
                    .insertBefore($template);

            // Update the name attributes
            $clone
                .find('[name="subject"]')
                .attr('name', 'field[' + fieldIndex + '].subject')
                .devbridgeAutocomplete({
                    minChars: 0,
                    autoSelectFirst: true,
                    triggerSelectOnValidInput: false,
                    preventBadQueries: false,
                    serviceUrl: '/suggest_subject/'
                })
                .end()
                .find('[name="predicate"]')
                .attr('name', 'field[' + fieldIndex + '].predicate')
                .devbridgeAutocomplete({
                    minChars: 0,
                    autoSelectFirst: true,
                    triggerSelectOnValidInput: false,
                    preventBadQueries: false,
                    serviceUrl: '/suggest_predicate/',
                    noCache: true
                })
                .end()
                .find('[name="object"]')
                .attr('name', 'field[' + fieldIndex + '].object')
                .devbridgeAutocomplete({
                    minChars: 0,
                    autoSelectFirst: true,
                    triggerSelectOnValidInput: false,
                    preventBadQueries: false,
                    serviceUrl: '/suggest_object/',
                    width: 200
                })
                .end();
        })
        // Remove button click handler
        .on('click', '.removeButton', function() {
            var $row  = $(this).parents('.container4'),
                index = $row.attr('data-field-index');

            // Remove element containing the fields
            $row.remove();
            fieldIndex--;
        });

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

function search(triples) {
    $('#results').html(
        '<div style="text-align: center; margin-top: 50px; ">' +
        '<span class="glyphicon glyphicon-refresh glyphicon-refresh-animate">' +
        '</span>' +
        '</div>'
    );

    lastSearchRequest = triples;

    $.ajax({
        type: "POST",
        url: "/search/",
        data: JSON.stringify(triples),
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
        $('#results').html("<br><br>").append(img);
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
                search(lastSearchRequest);
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
                search(lastSearchRequest);
            }
        }
    });
}