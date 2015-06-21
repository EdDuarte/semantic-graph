/**
 * Semantic Graph v2.0.0
 * Author: Ed Duarte
 * Email: edmiguelduarte@gmail.com
 */

$(document).ready(function () {

    $.ajax({
        type: "GET",
        url: "/is_ready/",
        contentType: "application/json",
        dataType: "html",
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (rawResponse) {
            var jsonResponse = JSON.parse(rawResponse);
            if (jsonResponse.state === "success" && jsonResponse.result) {
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
        .submit(function (event) {
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
                beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                success: function (rawResponse) {
                    var jsonResponse = JSON.parse(rawResponse);
                    if (jsonResponse.state === "success") {
                        $('#upload-modal').modal('hide');
                        $('#upload-alert').hide();
                        $('#ready-alert').show();
                        $('#error-alert').hide();
                    } else {
                        $('#upload-modal').modal('hide');
                        $('#error-message').html(jsonResponse.message);
                        $('#upload-alert').hide();
                        $('#ready-alert').hide();
                        $('#error-alert').show();
                    }
                    $('#addSubmit').removeAttr("disabled");
                }
            });
        });

    $('#removeForm')
        .submit(function (event) {
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
                beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                success: function (rawResponse) {
                    var jsonResponse = JSON.parse(rawResponse);
                    if (jsonResponse.state === "success") {
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
        .submit(function (event) {
            event.preventDefault();

            if (files) {
                var file = files[0];
                $('#uploadSubmit').attr("disabled", true);

                var reader = new FileReader();
                var formatVal = $("input:radio[name ='uploadFormatRadio']:checked").val();

                reader.onload = function (readerEvt) {
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
                        beforeSend: function (xhr, settings) {
                            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                            }
                        },
                        success: function (rawResponse) {
                            var jsonResponse = JSON.parse(rawResponse);
                            if (jsonResponse.state === "success") {
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
        .submit(function (event) {
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
                beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                success: function (response) {
                    if (formatVal == "pretty-xml") {
                        formatVal = "xml";
                    }
                    download("export." + formatVal, response);
                    $('#exportSubmit').removeAttr("disabled");
                }
            });
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

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function inferTypes() {

    $('#inference-modal').modal('hide');

    $.ajax({
        type: "GET",
        url: "/infer_types/",
        contentType: "application/json",
        dataType: "html",
        beforeSend: function (xhr, settings) {
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
        beforeSend: function (xhr, settings) {
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