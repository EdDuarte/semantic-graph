/**
 * Semantic Graph v2.0.0
 * Author: Ed Duarte
 * Email: edmiguelduarte@gmail.com
 */

$(document).ready(function () {



});

var lastSearchRequest;

function search(args) {
    $('#results').html(
        '<div style="text-align: center; margin-top: 50px; ">' +
        '<span class="glyphicon glyphicon-refresh glyphicon-refresh-animate">' +
        '</span>' +
        '</div>'
    );

    lastSearchRequest = args;

    $.ajax({
        type: "POST",
        url: "/search/",
        data: JSON.stringify(args),
        contentType: "application/json",
        dataType: "html",
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (rawResponse) {
            if (rawResponse == null || !rawResponse) {
                $('#results').html('<div class="span3" style="padding-left:25px;">' +
                '<br/><br/>No results were found.</div>');

            } else {
                //var encodedResponse = btoa(encodeURI(rawResponse));
                //$('#results').html("<br><br><br><br>").append(encodedResponse);

                //var img = new Image();
                //img.src = 'data:image/png;base64,' + rawResponse;
                //$('#results').html("<br/><br/>").append(img);
            }
        }
    });
}