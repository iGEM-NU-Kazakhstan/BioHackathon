'use strict';

chrome.tabs.onUpdated.addListener(function(tabId,changeInfo,tab){
	if (changeInfo.status === 'complete') {
		chrome.storage.sync.get("currentColor", function(data) {
			if (data["currentColor"]) {
		        chrome.tabs.executeScript(
		            tabId,
		            {code: 'document.body.style.backgroundColor = "#' + data["currentColor"] + '";'}
		        );
	        }
		});
	}
});


chrome.runtime.onInstalled.addListener(function() {

	chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
		chrome.declarativeContent.onPageChanged.addRules([{
			conditions: [new chrome.declarativeContent.PageStateMatcher({
				
			})
			],
			actions: [new chrome.declarativeContent.ShowPageAction()]
		}]);
	});
});
