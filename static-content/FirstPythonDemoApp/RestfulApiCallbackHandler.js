
function RestfulApiCallbackHandler() {
}

// clear the div (content output) to minimal, default display.
// do the ajax call (CREATE INSERT ADD_CONSTRAINT, SELECT_ALL, INGEST, DROP) and display results
RestfulApiCallbackHandler.prototype.createTablesHttpHandlerReturnBoolean = function(httpEncodedUrl, htmlIdToOutputResponse, prefix) {

  // any time we need to scrub html content to known empty state
  jqueryPaintLogic.appendInitialDynamicDataToTag("#mainData");

  jq.ajax({
      url: httpEncodedUrl,
      method: "GET",
      dataType: "text",   // expect plain text from server
      success: function (text) {
          jq(htmlIdToOutputResponse).text(prefix + " - server exited successfully. logical operation returned state = " + text);
      },
      error: function (xhr, status, error) {
          jq(htmlIdToOutputResponse).text(prefix + " - server quitted abnormally with error message = " + error);
      }
  });
}

// clear the div (content output) to minimal, default display.
// do the ajax call (QUERY CHROMA DB WITH searchTerm parameter, retrieve results and display in the div) and display results
RestfulApiCallbackHandler.prototype.queryChromaRetrieveAndDisplayHttpHandler = function(httpEncodedUrl, htmlIdToOutputResponse, prefix) {

  // any time we need to scrub html content to known empty state
  jqueryPaintLogic.appendInitialDynamicDataToTag("#mainData");

  if ($("#searchTerm").val().trim() !== "") {
//    console.log("Textbox has text");

    let searchTermTextBox = $("#searchTerm").val();
    let searchTermTextBoxEncoded = encodeURIComponent(searchTermTextBox);
    console.log(searchTermTextBoxEncoded);

    jq.ajax({
        url: httpEncodedUrl + '/' + searchTermTextBoxEncoded,
        method: "GET",
        dataType: "json",  // Expecting JSON response
        success: function (jsonData) {
            if (jsonData !== null && jsonData !== undefined) {
                if (Array.isArray(jsonData) && jsonData.length > 0) {
    //    console.log("Valid array with items");

                    let htmlStr = "";
                    for (let i = 0; i <jsonData.length; i++) {
                      htmlStr += "[" + jsonData[i]['productId'] + ";" + jsonData[i]['sku'] + ";" + jsonData[i]['brandName'] + ";" + jsonData[i]['categoryName'] + ";" + jsonData[i]['productName'] + ";" + jsonData[i]['productDescription'] + "],";
                      jqueryPaintLogic.appendHtmlDynamicRowToTag(jsonData[i], "#mainData");
                    }

                    jq(htmlIdToOutputResponse).text(prefix + " - server exited successfully. with json data processed = [" + htmlStr + "]");

    //appendHtmlDynamicRowToTag()
    //                                appendHtmlDynamicRowToTag();

                } else {
                    jq(htmlIdToOutputResponse).text(prefix + " - server quited normally but without returning any useful json data. cannot display.");
                }
            } else {
                jq(htmlIdToOutputResponse).text(prefix + " - server quited normally but without returning any useful json data. cannot display.");
            }
   //                        jq(htmlIdToOutputResponse).text(prefix + " - server exited successfully. logical operation returned state = " + text);
        },
        error: function (xhr, status, error) {
            jq(htmlIdToOutputResponse).text(prefix + " - server quited abnormally with error message = " + error);
        }
    }); // end ajax call

  } else {
    console.log('searchTerm is null or empty');
  }

}

