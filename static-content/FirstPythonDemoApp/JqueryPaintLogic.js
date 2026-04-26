
function JqueryPaintLogic() {
}

// Empty Div of all content
// Re-paint minimal, default content inside div element
// NOTE: we are given DivId(tagId) to output to on the page
JqueryPaintLogic.prototype.appendInitialDynamicDataToTag = function(divTagIdToOutput /* "#mainData" */) {
  let htmlDynamicRow = '';
  htmlDynamicRow += '<div class="row">';
  htmlDynamicRow += '<div class="col-md-6">';
  htmlDynamicRow += '<h2>Heading12</h2>';
  htmlDynamicRow += '<p><textarea id="responseFromMariaDb" name="responseFromMariaDb">abc</textarea></p>';
  htmlDynamicRow += '</div>';
  htmlDynamicRow += '<div class="col-md-6">';
  htmlDynamicRow += '<h2>Heading12</h2>';
  htmlDynamicRow += '<p><textarea id="queryChromaDb" name="queryChromaDb">def</textarea></p>';
  htmlDynamicRow += '</div>';
  htmlDynamicRow += '</div>';
  jq(divTagIdToOutput).html("");
  jq(divTagIdToOutput).append(htmlDynamicRow);
}

// When the chroma database query has returned, two items, display them on the page inside the div tag
// NOTE: we are given DivId(tagId) to output to on the page
JqueryPaintLogic.prototype.appendHtmlDynamicRowToTag = function(jsonDataSingleObject, divTagIdToOutput /* mainData */) {

  let htmlDynamicRow = '';
  htmlDynamicRow += '<div class="dynamicRow">';
  htmlDynamicRow += '  <div class="col-md-4">';
  htmlDynamicRow += '    <h2>' + jsonDataSingleObject['categoryName'] + ' - ' + jsonDataSingleObject['productName'] + '</h2>';
  htmlDynamicRow += '    <p>' + jsonDataSingleObject['brandName'] + ' - ' + jsonDataSingleObject['productDescription'] + '</p>';
  htmlDynamicRow += '    <p><a class="btn btn-secondary" href="#" role="button">View details</a></p>';
  htmlDynamicRow += '  </div>';
  htmlDynamicRow += '</div>';
  jq(divTagIdToOutput).append(htmlDynamicRow);
}
