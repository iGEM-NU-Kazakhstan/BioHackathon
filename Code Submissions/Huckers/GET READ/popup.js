document.addEventListener('DOMContentLoaded', function() {
	chrome.tabs.executeScript( null, {"code": "window.getSelection().toString()"}, function(selection) {
		  var result = selection;
		  document.getElementById("hidden").innerHTML = result;
		});
});