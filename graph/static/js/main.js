$(document).ready(function() {

    $.ajax({
        type: "GET",
        url: "/is_ready/",
        contentType: "application/json",
        dataType: "html",
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (rawResponse) {
            var jsonResponse = JSON.parse(rawResponse);
            if(jsonResponse.state === "success" && jsonResponse.result) {
                $('#upload-alert').hide();
                $('#ready-alert').show();
                $('#error-alert').hide();
            } else {
                $('#upload-alert').show();
                $('#ready-alert').hide();
                $('#error-alert').hide();
            }
        }
    });

    $('[name="field[0].subject"]').devbridgeAutocomplete({
        width: 200,
        minChars: 0,
        triggerSelectOnValidInput: false,
        preventBadQueries: false,
        serviceUrl: '/suggest_subject/'
    });

    $('[name="field[0].predicate"]').devbridgeAutocomplete({
        width: 200,
        minChars: 0,
        triggerSelectOnValidInput: false,
        preventBadQueries: false,
        serviceUrl: '/suggest_predicate/',
        noCache: true
    });

    $('[name="field[0].object"]').devbridgeAutocomplete({
        width: 200,
        minChars: 0,
        triggerSelectOnValidInput: false,
        preventBadQueries: false,
        serviceUrl: '/suggest_object/'
    });

    $('#addSubject').devbridgeAutocomplete({
        minChars: 0,
        triggerSelectOnValidInput: false,
        preventBadQueries: false,
        serviceUrl: '/suggest_subject/'
    });

    $('#addPredicate').devbridgeAutocomplete({
        minChars: 0,
        triggerSelectOnValidInput: false,
        preventBadQueries: false,
        serviceUrl: '/suggest_predicate/',
        noCache: true
    });

    $('#addObject').devbridgeAutocomplete({
        minChars: 0,
        triggerSelectOnValidInput: false,
        preventBadQueries: false,
        serviceUrl: '/suggest_object/'
    });

    $('#removeSubject').devbridgeAutocomplete({
        minChars: 0,
        triggerSelectOnValidInput: false,
        preventBadQueries: false,
        serviceUrl: '/suggest_subject/'
    });

    $('#removePredicate').devbridgeAutocomplete({
        minChars: 0,
        triggerSelectOnValidInput: false,
        preventBadQueries: false,
        serviceUrl: '/suggest_predicate/',
        noCache: true
    });

    $('#removeObject').devbridgeAutocomplete({
        minChars: 0,
        triggerSelectOnValidInput: false,
        preventBadQueries: false,
        serviceUrl: '/suggest_object/'
    });

    $('#addForm')
        .submit(function(event) {
            event.preventDefault();
            $('#add-modal').modal('hide');

            $('#addSubmit').attr("disabled", true);

            var addSubjectForm = $('#addSubject');
            var addPredicateForm = $('#addPredicate');
            var addObjectForm = $('#addObject');

            var params = JSON.stringify({
                subject: addSubjectForm.val(),
                predicate: addPredicateForm.val(),
                object: addObjectForm.val()
            });

            addSubjectForm.val("");
            addPredicateForm.val("");
            addObjectForm.val("");

            $.ajax({
                type: "POST",
                url: "/add/",
                data: params,
                contentType: "application/json",
                dataType: "html",
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                success: function(rawResponse) {
                    var jsonResponse = JSON.parse(rawResponse);
                    if(jsonResponse.state === "success") {
                        $('#upload-modal').modal('hide');
                        $('#upload-alert').hide();
                        $('#ready-alert').show();
                        $('#error-alert').hide();
                    } else {
                        $('#upload-modal').modal('hide');
                        $('#upload-alert').hide();
                        $('#ready-alert').hide();
                        $('#error-alert').show();
                        $('#error-message').html(jsonResponse.message);
                    }
                    $('#addSubmit').removeAttr("disabled");
                }
            });
        });

    $('#removeForm')
        .submit(function(event) {
            event.preventDefault();
            $('#remove-modal').modal('hide');

            $('#removeSubmit').attr("disabled", true);

            var removeSubjectForm = $('#removeSubject');
            var removePredicateForm = $('#removePredicate');
            var removeObjectForm = $('#removeObject');

            var params = JSON.stringify({
                subject: removeSubjectForm.val(),
                predicate: removePredicateForm.val(),
                object: removeObjectForm.val()
            });

            removeSubjectForm.val("");
            removePredicateForm.val("");
            removeObjectForm.val("");

            $.ajax({
                type: "POST",
                url: "/remove/",
                data: params,
                contentType: "application/json",
                dataType: "html",
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                success: function(rawResponse) {
                    var jsonResponse = JSON.parse(rawResponse);
                    if(jsonResponse.state === "success") {
                        $('#upload-modal').modal('hide');
                        $('#upload-alert').hide();
                        $('#ready-alert').show();
                        $('#error-alert').hide();
                    } else {
                        $('#upload-modal').modal('hide');
                        $('#upload-alert').hide();
                        $('#ready-alert').hide();
                        $('#error-alert').show();
                        $('#error-message').html(jsonResponse.message);
                    }
                    $('#removeSubmit').removeAttr("disabled");
                }
            });
        });

    var files;
    $('#uploadFile').on('change', function (event) {
        files = event.target.files;
    });

    $('#uploadForm')
        .submit(function(event) {
            event.preventDefault();

            if(files) {
                var file = files[0];
                $('#uploadSubmit').attr("disabled", true);

                var reader = new FileReader();
                var formatVal = $("input:radio[name ='uploadFormatRadio']:checked").val();

                reader.onload = function(readerEvt) {
                    var binaryString = readerEvt.target.result;
                    var uploadRequest = {
                        base: btoa(binaryString),
                        format: formatVal
                    };

                    $.ajax({
                        type: "POST",
                        url: "/upload/",
                        data: JSON.stringify(uploadRequest),
                        contentType: "application/json",
                        dataType: "html",
                        beforeSend: function(xhr, settings) {
                            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                            }
                        },
                        success: function (rawResponse) {
                            var jsonResponse = JSON.parse(rawResponse);
                            if(jsonResponse.state === "success") {
                                $('#upload-modal').modal('hide');
                                $('#upload-alert').hide();
                                $('#ready-alert').show();
                                $('#error-alert').hide();
                            } else {
                                $('#upload-modal').modal('hide');
                                $('#upload-alert').hide();
                                $('#ready-alert').hide();
                                $('#error-alert').show();
                                $('#error-message').html(jsonResponse.message);
                            }
                            $('#uploadSubmit').removeAttr("disabled");
                            files = null;
                        }
                    });
                };

                reader.readAsBinaryString(file);
            }



        });

    $('#exportForm')
        .submit(function(event) {
            event.preventDefault();
            $('#export-modal').modal('hide');

            $('#exportSubmit').attr("disabled", true);

            var formatVal = $("input:radio[name ='exportFormatRadio']:checked").val();
            var params = JSON.stringify({
                format: formatVal
            });

            $.ajax({
                type: "POST",
                url: "/export/",
                data: params,
                contentType: "application/json",
                dataType: "html",
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                success: function(response) {
                    if(formatVal == "pretty-xml"){
                        formatVal = "xml";
                    }
                    download("export."+formatVal, response);
                    $('#exportSubmit').removeAttr("disabled");
                }
            });
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
                    width: 200,
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
                    width: 200,
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
                    width: 200,
                    minChars: 0,
                    autoSelectFirst: true,
                    triggerSelectOnValidInput: false,
                    preventBadQueries: false,
                    serviceUrl: '/suggest_object/'
                })
                .end();
        })
        // Remove button click handler
        .on('click', '.removeButton', function() {
            var $row  = $(this).parents('.container2'),
                index = $row.attr('data-field-index');

            // Remove element containing the fields
            $row.remove();
            fieldIndex--;
        });

});

function download(filename, text) {
    var pom = document.createElement('a');
    pom.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    pom.setAttribute('download', filename);

    if (document.createEvent) {
        var event = document.createEvent('MouseEvents');
        event.initEvent('click', true, true);
        pom.dispatchEvent(event);
    }
    else {
        pom.click();
    }
}

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
        success: function (rawResponse) {
            if(rawResponse == null || !rawResponse) {
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

function inferTypes() {

    $('#inference-modal').modal('hide');

    $.ajax({
        type: "GET",
        url: "/infer_types/",
        contentType: "application/json",
        dataType: "html",
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        //},
        //success: function (response) {
        //    if(response.state === "success") {
        //        search(lastSearchRequest);
        //    }
        }
    });
}


function inferParents() {

    $('#inference-modal').modal('hide');

    $.ajax({
        type: "GET",
        url: "/infer_parents/",
        contentType: "application/json",
        dataType: "html",
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        //},
        //success: function (response) {
        //    if(response.state === "success") {
        //        search(lastSearchRequest);
        //    }
        }
    });
}