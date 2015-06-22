/**
 * Semantic Graph v2.0.0
 * Author: Ed Duarte
 * Email: edmiguelduarte@gmail.com
 */

$(document).ready(function () {

    $("#menu-toggle").click(function (e) {
        e.preventDefault();
        $(".wrapper").toggleClass("toggled");
        $("#menu-toggle-icon").toggleClass("fa-arrow-right")
    });

    $('[name="field[0].subject"]').devbridgeAutocomplete({
        width: 340,
        minChars: 0,
        triggerSelectOnValidInput: false,
        preventBadQueries: false,
        serviceUrl: '/suggest_subject/'
    });

    $('[name="field[0].predicate"]').devbridgeAutocomplete({
        width: 340,
        minChars: 0,
        triggerSelectOnValidInput: false,
        preventBadQueries: false,
        serviceUrl: '/suggest_predicate/',
        noCache: true
    });

    $('[name="field[0].object"]').devbridgeAutocomplete({
        width: 370,
        minChars: 0,
        triggerSelectOnValidInput: false,
        preventBadQueries: false,
        serviceUrl: '/suggest_object/'
    });

    var fieldIndex = 0;

    $('#fieldForm')
        .submit(function (event) {
            event.preventDefault();
            var triples = [];
            for (var i = 0; i <= fieldIndex; i++) {
                var t = {
                    subject: $('[name="field[' + i + '].subject"]').val(),
                    predicate: $('[name="field[' + i + '].predicate"]').val(),
                    object: $('[name="field[' + i + '].object"]').val()
                };
                if (t.subject === "") {
                    t.subject = null
                }
                if (t.predicate === "") {
                    t.predicate = null
                }
                if (t.object === "") {
                    t.object = null
                }
                triples.push(t);
            }
            search(triples)
        })
        // Add button click handler
        .on('click', '.addButton', function () {
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
                    width: 340,
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
                    width: 340,
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
                    width: 370,
                    minChars: 0,
                    autoSelectFirst: true,
                    triggerSelectOnValidInput: false,
                    preventBadQueries: false,
                    serviceUrl: '/suggest_object/'
                })
                .end();
        })
        // Remove button click handler
        .on('click', '.removeButton', function () {
            var $row = $(this).parents('.container2'),
                index = $row.attr('data-field-index');

            // Remove element containing the fields
            $row.remove();
            fieldIndex--;
        });

});

var lastSearchRequest;

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

                var img = new Image();
                img.src = 'data:image/png;base64,' + rawResponse;
                $('#results').html("<br/><br/>").append(img);
            }
        }
    });
}