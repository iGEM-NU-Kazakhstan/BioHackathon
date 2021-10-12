const defaultFilters = [
    "*://*.doubleclick.net/*",
    "*://partner.googleadservices.com/*",
    "*://*.googlesyndication.com/*",
    "*://*.google-analytics.com/*",
    "*://creative.ak.fbcdn.net/*",
    "*://*.adbrite.com/*",
    "*://*.exponential.com/*",
    "*://*.vdx.tv/*",
    "*://*.quantserve.com/*",
    "*://*.scorecardresearch.com/*",
    "*://*.zedo.com/*",
    "*://*.101xp.com/*", 
    "*://*.ekod.info/*", 
    "*://*.rarenok.biz/*", 
    "*://*.post.rmbn.net/*", 
    "*://*.cityadspix.com/*",
    "*://*.terraclicks.com/*", 
    "*://*.astdn.ru/*", 
    "*://*.wiki-weather.com/*", 
    "*://*.redichat.com/*", 
    "*://*.adnxs.com/*",  
    "*://*.kasperskiyweb.com/*",
    "*:/*.mxttrf.com/*", 
    "*://*.dnetworkperformance.com/*", 
    "*://megapopads.com/*",
    "*://*.superinterstitial.com/*",
    "*://*.hipersushiads.com/*",
    "*://*.regpole.com/*",
    "*://*.welcomegames/*",
    "*://*.gamesfortuna/*",
    "*://*.serving-sys.com/*",
    "*://*.rutarget.ru/*"
]


chrome.webRequest.onBeforeRequest.addListener(
    function(details){
        return {
            cancel: true
        }
    },
    {
       urls: defaultFilters 
    },
       ["blocking"] 
)

