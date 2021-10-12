window.addEventListener("load", () => {
        setInterval(() => {
            let arrElementDeleted = [];
            let searchElementDeleted = [
              document.querySelectorAll("#ad_unit"),
              document.querySelectorAll("#google_esf"),
              document.querySelectorAll("#ad_container"),
              document.querySelectorAll("#content .Contentid"),
              document.querySelectorAll(".ads_ad_box6"),
        
              document.querySelectorAll("lima-video"),
              document.querySelectorAll("#animation_container"),
              document.querySelectorAll(".rectangle-banner"),
              document.querySelectorAll(".trg-b-banner-block"),
              document.querySelectorAll(".mailru-visibility-check"),
              document.querySelectorAll(".promo-banner"),
              document.querySelectorAll(".root__bottom-ad"),
              document.querySelectorAll(".js-zone-container"),
              //document.querySelectorAll('.hookBlock'),
        
              document.querySelectorAll('a[href*="mail.ru/redir"]'),
              document.querySelectorAll("a[href*=google]"),
              document.querySelectorAll("a[href*=Google]"),
        
              document.querySelectorAll("script[src*=Google]"),
              document.querySelectorAll("script[src*=google]"),
        
              document.querySelectorAll("img[src*=Google]"),
              document.querySelectorAll("img[src*=google]"),
        
              document.querySelectorAll("div[class*=Google]"),
              document.querySelectorAll("div[class*=amzn]"),
              document.querySelectorAll("div[class*=google]"),
              document.querySelectorAll("div[class*=ads]"),
              //document.querySelectorAll('div[class*=ad]'),
              document.querySelectorAll("div[class*=Ads]"),
              //document.querySelectorAll('div[class*=Ad]'),
        
              document.querySelectorAll("iframe[src*=Google]"),
              document.querySelectorAll("iframe[id*=google]"),
              document.querySelectorAll("iframe[id*=Google]"),
              document.querySelectorAll("iframe[src*=google]"),
              document.querySelectorAll("iframe[src*=googleads]"),
            ];
        
            searchElementDeleted.forEach((el) => (el.length > 0 ? addInArr(el) : ""));
        
            function addInArr(htmlList) {
              htmlList.forEach((el) => arrElementDeleted.push(el));
            }
        
            if (arrElementDeleted.length > 0)
              arrElementDeleted.forEach((el) => (el.style.display = "none"));
          }, 100);

  });