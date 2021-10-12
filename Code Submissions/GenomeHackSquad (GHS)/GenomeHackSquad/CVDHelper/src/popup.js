(function(exports) {
  var site;

  /** @type {!number} */
  var activeFilterIndex = 0;

  /** @type {{type: string, severity: number} | undefined} */
  var restoreSettings = undefined;

  /**
  @const {array{string}}
  */
  var CVD_TYPES = ['PROTANOMALY','DEUTERANOMALY','TRITANOMALY'];

  /**
  @const {number}
  */
  var HIGHLIGHT_OFFSET = 7;

  /**
  @param {string} cvdType 
  */
  
  function createTestRow(type) {
    var toCssColor = function(rgb) {
      return 'rgb(' + rgb.join(',') + ')';
    };
    var row = document.createElement('label');
    row.classList.add('row');

    var button = document.createElement('input');
    button.id = 'select-' + type;
    button.name = 'cvdType';
    button.setAttribute('type', 'radio');
    button.value = type;
    button.checked = false;
    row.appendChild(button);
    button.addEventListener('change', function() {
      onTypeChange(this.value);
    });
    button.setAttribute('aria-label', type);

    var buttonText = document.createTextNode(type.charAt(0).toUpperCase() + type.slice(1).toLowerCase());
    row.appendChild(buttonText);
   
    return row;
  }

  /**
  @return {?string}
   */
  function getCvdTypeSelection(){
    var active = undefined;
    CVD_TYPES.forEach(function(str){
      if($('select-' + str).checked){
        active = str;
        return;
      }
    });
    return active;
  }

  /**
  @param {string} cvdType 
  @return {?string}
  */
  function setCvdTypeSelection(cvdType) {
    var highlight = $('row-highlight');
    highlight.hidden = true;
    CVD_TYPES.forEach(function(str) {
      var checkbox = $('select-' + str);
      if (cvdType == str) {
        checkbox.checked = true;
        var top = checkbox.parentElement.offsetTop - HIGHLIGHT_OFFSET;
        highlight.style.top = top + 'px';
        highlight.hidden = false;
      } else {
        checkbox.checked = false;
      }
    });
  }

  function updateControls() {
    if ($('flex-container').classList.contains('activated')) {
      $('enable').disabled = false;
      $('delta').disabled = false;
      $('setup').disabled = false;
    } else {
      $('enable').disabled = true;
      $('delta').disabled = true;
      $('setup').disabled = true;

      if (!getCvdTypeSelection()) {
        $('firstStep').classList.add('active');
        $('secondStep').classList.remove('active');
        $('severity').disabled = true;
        $('reset').disabled = true;
      } else {
        $('firstStep').classList.remove('active');
        $('secondStep').classList.add('active');
        $('severity').disabled = false;
        $('reset').disabled = false;
    
        onSeverityChange(parseFloat($('severity').value));
      }
    }
  }

  /**
  @return {boolean} 
   */
  function update() {
    var type = getDefaultType();
    var validType = false;
    CVD_TYPES.forEach(function(cvdType) {
      if (cvdType == type) {
        validType = true;
        return;
      }
    });

    if (!validType)
      return false;

    if (site) {
      $('delta').value = getSiteDelta(site);
    } else {
      $('delta').value = getDefaultDelta();
    }

    $('severity').value = getDefaultSeverity();

    if (!$('flex-container').classList.contains('activated'))
      setCvdTypeSelection(getDefaultType());
    $('enable').checked = getDefaultEnable();

    debugPrint('update: ' +
        ' del=' + $('delta').value +
        ' sev=' + $('severity').value +
        ' typ=' + getDefaultType() +
        ' enb=' + $('enable').checked +
        ' for ' + site
    );
    chrome.extension.getBackgroundPage().updateTabs();
    return true;
  }

  /**
  @param {number} value
  */
  function onDeltaChange(value) {
    debugPrint('onDeltaChange: ' + value + ' for ' + site);
    if (site) {
      setSiteDelta(site, value);
    }
    setDefaultDelta(value);
    update();
  }

  /**
  @param {number} value 
   */
  function onSeverityChange(value) {
    debugPrint('onSeverityChange: ' + value + ' for ' + site);
    setDefaultSeverity(value);
    update();
    var filter = window.getDefaultCvdCorrectionFilter(
        getCvdTypeSelection(), value);
    injectColorEnhancementFilter(filter);
    window.getComputedStyle(document.documentElement, null);
  }

  /**
  @param {string} value 
  */
  function onTypeChange(value) {
    debugPrint('onTypeChange: ' + value + ' for ' + site);
    setDefaultType(value);
    update();
    activeFilterType = value;
    $('severity').value = 0;
    updateControls();
  }

  /**
  @param {boolean} value
  */
  function onEnableChange(value) {
    debugPrint('onEnableChange: ' + value + ' for ' + site);
    setDefaultEnable(value);
    if (!update()) {
      $('setup').onclick();
    }
  }

  function onReset() {
    debugPrint('onReset');
    resetSiteDeltas();
    update();
  }

  function initialize() {
    var i18nElements = document.querySelectorAll('*[i18n-content]');
    for (var i = 0; i < i18nElements.length; i++) {
      var elem = i18nElements[i];
      var msg = elem.getAttribute('i18n-content');
      elem.textContent = chrome.i18n.getMessage(msg);
    }

    $('setup').onclick = function() {
      $('flex-container').classList.remove('activated');
    
      restoreSettings = {
        type: getDefaultType(),
        severity: getDefaultSeverity()
      };
    
      setCvdTypeSelection(restoreSettings.type);
      $('severity').value = restoreSettings.severity;
      updateControls();
    };

    $('delta').addEventListener('input', function() {
      onDeltaChange(parseFloat(this.value));
    });
    $('severity').addEventListener('input', function() {
      onSeverityChange(parseFloat(this.value));
    });
    $('enable').addEventListener('change', function() {
      onEnableChange(this.checked);
    });

    $('reset').onclick = function() {
      setDefaultSeverity(0);
      setDefaultType('');
      setDefaultEnable(false);
      $('severity').value = 0;
      $('enable').checked = false;
      setCvdTypeSelection('');
      updateControls();
      clearColorEnhancementFilter();
    };
    $('reset').hidden = !IS_DEV_MODE;

    var closeSetup = function() {
      $('flex-container').classList.add('activated');
      updateControls();
    };

    $('ok').onclick = function() {
      closeSetup();
    };

    $('cancel').onclick = function() {
      closeSetup();
      if (restoreSettings) {
        debugPrint(
          'restore previous settings: ' +
          'type = ' + restoreSettings.type +
           ', severity = ' + restoreSettings.severity);
        setDefaultType(restoreSettings.type);
        setDefaultSeverity(restoreSettings.severity);
      }
    };

    var swatches = $('swatches');
    CVD_TYPES.forEach(function(cvdType) {
      swatches.appendChild(createTestRow(cvdType));
    });

    chrome.windows.getLastFocused({'populate': true}, function(window) {
      for (var i = 0; i < window.tabs.length; i++) {
        var tab = window.tabs[i];
        if (tab.active) {
          site = siteFromUrl(tab.url);
          debugPrint('init: active tab update for ' + site);
          update();
          return;
        }
      }
      site = 'unknown site';
      update();
    });
  }

  exports.initializeOnLoad = function() {
    var ready = new Promise(function readyPromise(resolve) {
      if (document.readyState === 'complete') {
        resolve();
      }
      document.addEventListener('DOMContentLoaded', resolve);
    });
    ready.then(initialize);
  };
})(this);

this.initializeOnLoad();
