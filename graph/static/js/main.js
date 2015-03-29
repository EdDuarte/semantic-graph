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
        serviceUrl: '/web/suggestSubject'
    });

    $('#predicateField').devbridgeAutocomplete({
        minChars: 1,
        width: 300,
        triggerSelectOnValidInput: false,
        preventBadQueries: false,
        lookup: predicates
    });

    $('#objectField').devbridgeAutocomplete({
        minChars: 1,
        width: 300,
        triggerSelectOnValidInput: false,
        preventBadQueries: false,
        serviceUrl: '/web/suggestObject'
    });

    $("#searchform").submit(function(event) {
        event.preventDefault();

        search($("#subjectField").val(), $("#predicateField").val(), $("#objectField").val())
    });

    $("#load").hide();
    $("#clearFacet").hide();

});

var lastSearchRequest;

function search(subject) {
    $("#clearFacet").hide();
    $("#load").hide();
    $('#subjectField').val(subject);

    $('#results').html(
        '<div style="text-align: center; margin-top: 50px; ">' +
        '<span class="glyphicon glyphicon-refresh glyphicon-refresh-animate">' +
        '</span>' +
        '</div>'
    );

    // The operations below create a JSON object that will be converted
    // into a edduarte.airi.assignment03.rest.SearchRequest.java object

    // collects selected fields on config window
    var fieldNames = [];

    if($("#medicine_name").is(':checked')){
        fieldNames.push("medicine_name");
    }

    if($("#file_path").is(':checked')){
        fieldNames.push("file_path");
    }

    if($("#text").is(':checked')){
        fieldNames.push("text");
    }

    if($("#secondary_effects").is(':checked')){
        fieldNames.push("secondary_effects");
    }

    lastSearchRequest = {
        "subject":subject,
        "startAt":0,
        "fieldNames":fieldNames,
        "facetQueries":[]
    };

    $.ajax({
        type: "POST",
        url: "/web/search",
        data: JSON.stringify(lastSearchRequest),
        contentType: "application/json",
        dataType: "html",
        success: function (response) {
            parseResponse(response);
        }
    });
}

function mlt(file, fieldName) {
    $("#clearFacet").hide();
    $("#load").hide();

    $('#results').html(
        '<div style="text-align: center; margin-top: 50px; ">' +
        '<span class="glyphicon glyphicon-refresh glyphicon-refresh-animate">' +
        '</span>' +
        '</div>'
    );

    var request = {
        "file":file,
        "fieldName":fieldName
    };

    $.ajax({
        type: "POST",
        url: "/web/mlt",
        data: JSON.stringify(request),
        contentType: "application/json",
        dataType: "html",
        success: function (response) {
            parseMlt(response);
        }
    });
}

function continueSearch() {

    lastSearchRequest = {
        "subject":lastSearchRequest.subject,
        "startAt":lastSearchRequest.startAt + 10,
        "fieldNames":lastSearchRequest.fieldNames,
        "facetQueries":lastSearchRequest.facetQueries
    };

    $.ajax({
        type: "POST",
        url: "/web/search",
        data: JSON.stringify(lastSearchRequest),
        contentType: "application/json",
        dataType: "html",
        success: function (response) {
            if(response == null) {
                resultsContainer.html('<div class="span3" style="padding-left:25px;">' +
                '<br/><br/>The inserted search query is invalid.</div>');

            } else {
                var searchResponse = JSON.parse(response);
                if (searchResponse.results.length > 0) {
                    searchResponseToHtml(searchResponse);
                    $("#load").show();
                } else {
                    $("#load").hide();
                }
            }
        }
    });
}

function facetSearch(facetQuery) {

    $("#load").hide();
    $("#clearFacet").hide();

    $('#results').html(
        '<div style="text-align: center; margin-top: 50px; ">' +
        '<span class="glyphicon glyphicon-refresh glyphicon-refresh-animate">' +
        '</span>' +
        '</div>'
    );

    // The operations below create a JSON object that will be converted
    // into a edduarte.airi.assignment03.rest.SearchRequest.java object

    // collects selected fields on config window
    var fieldNames = [];

    if($("#medicine_name").is(':checked')){
        fieldNames.push("medicine_name");
    }

    if($("#file_path").is(':checked')){
        fieldNames.push("file_path");
    }

    if($("#text").is(':checked')){
        fieldNames.push("text");
    }

    if($("#secondary_effects").is(':checked')){
        fieldNames.push("secondary_effects");
    }

    lastSearchRequest.facetQueries.push(facetQuery);

    lastSearchRequest = {
        "subject":lastSearchRequest.subject,
        "startAt":0,
        "fieldNames":fieldNames,
        "facetQueries":lastSearchRequest.facetQueries
    };

    $.ajax({
        type: "POST",
        url: "/web/search",
        data: JSON.stringify(lastSearchRequest),
        contentType: "application/json",
        dataType: "html",
        success: function (response) {
            parseResponse(response);
            $("#clearFacet").unbind('click').click(function(){
                search(lastSearchRequest.subject);
            }).show();
        }
    });
}

function parseResponse(response) {
    var resultsContainer = $('#results');

    if(response == null || !response) {
        resultsContainer.html('<div class="span3" style="padding-left:25px;">' +
        '<br/><br/>The inserted search query is invalid.</div>');

    } else {

        var searchResponse = JSON.parse(response);

        resultsContainer.html("");

        // info data (hits and elapsed time)
        resultsContainer.append('<div class="span3" style="padding-left:25px;">' +
        '<br/><br/>Obtained ' + searchResponse.numHits + ' results in ' +
        searchResponse.elapsedTime + '</div><br/>');

        // spellchecking
        var length = searchResponse.spellingSuggestions.length;
        if(length > 0) {
            resultsContainer.append('<div class="span3" style="padding-left:25px;">' +
            '<br/><br/><font color="red">Did you mean <span id="spells"></span>?</font></div><br/>');

            var spellContainer = $('#spells');

            for (var i = 0; i < length; i++) {
                var s = searchResponse.spellingSuggestions[i];
                spellContainer.append('<a href="#" id="spell_'+s+'">' + s + '</a>');
                spellContainer.$('#spell_'+s).unbind('click').click(function(){
                    search(s);
                });

                if((i + 2) == length) {
                    spellContainer.append(' or ');
                } else if((i + 1) < length) {
                    spellContainer.append(', ');
                }
            }
        }

        searchResponseToHtml(searchResponse);

        var facetsContainer = $('#facets').html("");
        searchResponse.medicineNameFacets.forEach(function(f){
            facetsContainer.append('<li> <a href="#" id="'+f.term+'">'+f.term+' ('+ f.count+')</a> </li>');
            $('#' + f.term).unbind('click').click(function () {
                facetSearch(f.term);
            });
        });

        if(searchResponse.results.length > 0) {
            $("#load").show();
        }
    }
}



function parseMlt(response) {
    var resultsContainer = $('#results');

    if(response == null || !response) {
        resultsContainer.html('<div class="span3" style="padding-left:25px;">' +
        '<br/><br/>The inserted "more like this" query is invalid.</div>');

    } else {

        var searchResponse = JSON.parse(response);

        resultsContainer.html("");

        // info data (hits and elapsed time)
        resultsContainer.append('<div class="span3" style="padding-left:25px;">' +
        '<br/><br/>Obtained ' + searchResponse.numHits + ' results in ' +
        searchResponse.elapsedTime + '</div><br/>');

        searchResponse.files.forEach(function(f){
            resultsContainer.append('<div class="span5" style="padding-left:15px;">' +
            '<h4>'+ f + '</h4><font size="2px">');

            resultsContainer.append('<a href="#" id="similar1_' + count + '">Similar contents</a>');
            $('#similar1_' + count).unbind('click').click(function () {
                mlt(f, "text");
            });

            resultsContainer.append('<a style="padding-left:1em;" href="#" id="similar2_' + count + '">Similar secondary effects</a>');
            $('#similar2_' + count).unbind('click').click(function () {
                mlt(f, "secondary_effects");
            });
            count++;

            resultsContainer.append('</font>');

            resultsContainer.append('</div><br/>');
        });

        var facetsContainer = $('#facets').html("");
        searchResponse.medicineNameFacets.forEach(function(f){
            facetsContainer.append('<li> <a href="#" id="'+f.term+'">'+f.term+' ('+ f.count+')</a> </li>');
            $('#' + f.term).unbind('click').click(function () {
                facetSearch(f.term);
            });
        });

        if(searchResponse.results.length > 0) {
            $("#load").show();
        }
    }
}

var count = 0;

function searchResponseToHtml(searchResponse) {

    var resultsContainer = $('#results');
    searchResponse.results.forEach(function(h){
        resultsContainer.append('<div class="span5" style="padding-left:15px;">' +
        '<h4>'+ h.file + '</h4><font size="2px">');

        resultsContainer.append('<a href="#" id="similar1_' + count + '">Similar contents</a>');
        $('#similar1_' + count).unbind('click').click(function () {
            mlt(h.file, "text");
        });

        resultsContainer.append('<a style="padding-left:1em;" href="#" id="similar2_' + count + '">Similar secondary effects</a>');
        $('#similar2_' + count).unbind('click').click(function () {
            mlt(h.file, "secondary_effects");
        });
        count++;

        resultsContainer.append('</font>');

        resultsContainer.append('<p>');
        if (typeof h.snippets !== 'undefined') {
            h.snippets.forEach(function (snippet) {
                resultsContainer.append('... ' + snippet + ' ...');
            });
        }

        resultsContainer.append('</p></div><br/>');
    });

}