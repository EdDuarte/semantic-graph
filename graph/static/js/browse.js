/**
 * Semantic Graph v2.0.0
 * Author: Ed Duarte
 * Email: edmiguelduarte@gmail.com
 */

$(document).ready(function () {

    $('#search').devbridgeAutocomplete({
        minChars: 0,
        triggerSelectOnValidInput: false,
        preventBadQueries: false,
        serviceUrl: '/suggest_entity/'
    });

    $('#fieldForm')
        .submit(function (event) {
            event.preventDefault();
            //for (var i = 0; i <= fieldIndex; i++) {
            //    var t = {
            //        subject: $('[name="field[' + i + '].subject"]').val(),
            //        predicate: $('[name="field[' + i + '].predicate"]').val(),
            //        object: $('[name="field[' + i + '].object"]').val()
            //    };
            //    if (t.subject === "") {
            //        t.subject = null
            //    }
            //    if (t.predicate === "") {
            //        t.predicate = null
            //    }
            //    if (t.object === "") {
            //        t.object = null
            //    }
            //    triples.push(t);
            //}
            browse({entity: $("#search").val()})
        })
});

var lastBrowseRequest;

function browse(args) {
    $('#panels').hide();
    $('#loading').html(
        '<div style="text-align: center; margin-top: 50px; ">' +
        '<span class="glyphicon glyphicon-refresh glyphicon-refresh-animate">' +
        '</span>' +
        '</div>'
    );

    lastBrowseRequest = args;

    $.ajax({
        type: "POST",
        url: "/search_entity/",
        data: JSON.stringify(args),
        contentType: "application/json",
        dataType: "html",
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (response) {
            if (response == null || !response) {
                $('#loading').html('<div class="span3" style="padding-left:25px;">' +
                '<br/><br/>No results were found.</div>');

            } else {
                var jsonResponse = JSON.parse(response);
                $('#loading').html('');
                $("#subjectResults").html(jsonResponse["subjectResults"]);
                $("#objectResults").html(jsonResponse["objectResults"]);
                $('#subjectTextarea').val(jsonResponse["subjectResults"]);
                $('#objectTextarea').val(jsonResponse["objectResults"]);
                $('#panels').show();
            }
        }
    });
}