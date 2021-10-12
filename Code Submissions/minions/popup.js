document.body.addEventListener('click', function(e) {
    let target = e.target;
    if (target.nodeName === 'BUTTON') {
        if (target.name === 'reset') {
            chrome.storage.sync.clear(function(data){
                chrome.tabs.query({active: true, currentWindow: true}, function(tab) {
                    chrome.tabs.reload(tab[0].id);
                });
            });
        }
        changeBG(target.name);
    }
    e.stopPropagation();
});
function changeBG(color) {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.executeScript(
            tabs[0].id,
            {code: 'document.body.style.backgroundColor = "#' + color + '";'}
        );
    });
    var el = document.getElementsByTagName("*");
    for (var i=0; i < el.length; i++) 
    {    
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            chrome.tabs.executeScript(
                tabs[0].id,
                {code: 'document.body.style.color = "#' + color + '";'}
            );
        });
        
    }
     storeColor(color);
               
}


function storeColor(bgColor) {
    chrome.storage.sync.set({currentColor: bgColor});
}
