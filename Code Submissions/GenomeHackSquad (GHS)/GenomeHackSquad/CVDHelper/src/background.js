 function injectContentScripts() {
  chrome.windows.getAll({'populate': true}, function(windows) {
    for (var i = 0; i < windows.length; i++) {
      var tabs = windows[i].tabs;
      for (var j = 0; j < tabs.length; j++) {
        var url = tabs[j].url;
        if (isDisallowedUrl(url)) {
          continue;
        }
        chrome.tabs.executeScript(
            tabs[j].id,
            {file: 'src/common.js'});
        chrome.tabs.executeScript(
            tabs[j].id,
            {file: 'src/cvd.js'});
      }
    }
  });
}


function updateTabs() {
  chrome.windows.getAll({'populate': true}, function(windows) {
    for (var i = 0; i < windows.length; i++) {
      var tabs = windows[i].tabs;
      for (var j = 0; j < tabs.length; j++) {
        var url = tabs[j].url;
        if (isDisallowedUrl(url)) {
          continue;
        }
        var msg = {
          'delta': getSiteDelta(siteFromUrl(url)),
          'severity': getDefaultSeverity(),
          'type': getDefaultType(),
          'simulate': getDefaultSimulate(),
          'enable': getDefaultEnable()
        };
        debugPrint('updateTabs: sending ' + JSON.stringify(msg) + ' to ' +
            siteFromUrl(url));
        chrome.tabs.sendRequest(tabs[j].id, msg);
      }
    }
  });
}


(function initialize() {
  injectContentScripts();
  updateTabs();

  chrome.extension.onRequest.addListener(
      function(request, sender, sendResponse) {
        if (request['init']) {
          var delta = getDefaultDelta();
          if (sender.tab) {
            delta = getSiteDelta(siteFromUrl(sender.tab.url));
          }

          var msg = {
            'delta': delta,
            'severity': getDefaultSeverity(),
            'type': getDefaultType(),
            'simulate': getDefaultSimulate(),
            'enable': getDefaultEnable()
          };
          sendResponse(msg);
        }
      });



  document.addEventListener('storage', function(evt) {
    updateTabs();
  }, false);
})();
