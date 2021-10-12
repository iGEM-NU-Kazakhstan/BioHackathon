function $(id) {
  return document.getElementById(id);
}

function siteFromUrl(url) {
  var a = document.createElement('a');
  a.href = url;
  return a.hostname;
}

/**
@param {string} url The URL to check.
 */
function isDisallowedUrl(url) {
  return url.startsWith('chrome') || url.startsWith('about');
}

/**
@const {boolean}
 */
var IS_DEV_MODE = !('update_url' in chrome.runtime.getManifest());

/**
@param {*} message 
 */
function debugPrint(str) {
  if (IS_DEV_MODE)
    console.log(str);
}
