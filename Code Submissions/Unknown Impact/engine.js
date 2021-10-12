var $special,
    $language = "Russian Female";
function set_UKEng() {
    $language = "UK English Female";
}
function set_USEng() {
    $language = "US English Female";
}
function set_Rus() {
    $language = "Russian Female";
}
function set_Jap() {
    $language = "Japanese Female";
}
function set_Ko() {
    $language = "Korean Female";
}
jQuery("html").hide(),
    (function (e) {
        (e.fn.removeClassWild = function (e) {
            return this.removeClass(function (a, n) {
                var t = e.replace(/\*/g, "\\S+");
                return (n.match(new RegExp("\\b" + t, "g")) || []).join(" ");
            });
        }),
            (special = {
                Reset: function () {
                    ($special = { active: 1, color: 1, font_size: 1, images: 1 }), e.cookie("special", $special, { path: "/" });
                },
                Set: function () {
                    e("html")
                        .removeClassWild("special-*")
                        .addClass("special-color-" + $special.color)
                        .addClass("special-font-size-" + $special.font_size)
                        .addClass("special-images-" + $special.images),
                        e("#special button").removeClass("active"),
                        e(".special-color button[value=" + $special.color + "]").addClass("active"),
                        e(".special-font-size button[value=" + $special.font_size + "]").addClass("active"),
                        e(".special-images button").val($special.images),
                        special.ToggleImages();
                },
                ToggleImages: function () {
                    e("img").each(function () {
                        $special.images
                            ? (e(this).data("src") && e(this).attr("src", e(this).data("src")), e(this).data("srcset") && e(this).attr("srcset", e(this).data("srcset")))
                            : (e(this).data("src", e(this).attr("src")), e(this).attr("srcset") && e(this).data("srcset", e(this).attr("srcset")), e(this).removeAttr("src"), e(this).attr("srcset") && e(this).removeAttr("srcset"));
                    });
                },
                Off: function () {
                    e("html").removeClass("special").removeClassWild("special-*"),
                        e("i.special-audio").remove(),
                        responsiveVoice.isPlaying() && responsiveVoice.cancel(),
                        e("audio").remove(),
                        e("#special").remove(),
                        e.removeCookie("special", { path: "/" }),
                        e("#specialButton").show();
                },
                On: function () {
                    e("head").append(e('<link rel="stylesheet" type="text/css" />').attr("href", "./engine-style.css")),
                        $special || special.Reset(),
                        e("#specialButton").length && (($special.active = 1), e.cookie("special", $special, { path: "/" }), e("#specialButton").hide()),
                        e("html").addClass("special"),
                        e("body").prepend(e($header)),
                        special.Set(),
                        e("#special button").on("click", function () {
                            var a = e(this).parent().attr("class").replace("special-", "");
                            if (a)
                                switch ((e("#special .special-" + a + " button").removeClass("active"), a)) {
                                    case "color":
                                        ($special.color = parseInt(e(this).val())),
                                            e(this).addClass("active"),
                                            e("html")
                                                .removeClassWild("special-" + a + "-*")
                                                .addClass("special-" + a + "-" + e(this).val()),
                                            e.cookie("special", $special, { path: "/" });
                                        break;
                                    case "font-size":
                                        ($special.font_size = parseInt(e(this).val())),
                                            e(this).addClass("active"),
                                            e("html")
                                                .removeClassWild("special-" + a + "-*")
                                                .addClass("special-" + a + "-" + e(this).val()),
                                            e.cookie("special", $special, { path: "/" });
                                        break;
                                    case "images":
                                        ($special.images = $special.images ? 0 : 1), e(this).val($special.images), special.ToggleImages(), e.cookie("special", $special, { path: "/" });
                                        break;
                                    case "audio":
                                        1 == e(this).val()
                                            ? (e("i.special-audio").remove(), responsiveVoice.isPlaying() && responsiveVoice.cancel(), e("p,h1,h2,h3,h4,h5,h6,li,dt,dd,.audiotext").off(), e(this).val(0))
                                            : (responsiveVoice.speak("Text-to-Speech Enabled.", $language),
                                              e(this).addClass("active"),
                                              e(this).val(1),
                                              e("p,h1,h2,h3,h4,h5,h6,li,dt,dd,.audiotext,a,b").on("mouseover", function () {
                                                  responsiveVoice.isPlaying() && responsiveVoice.cancel(), responsiveVoice.speak(e(this).text().trim(), $language);
                                              }));
                                        break;
                                    case "reset":
                                        special.Reset(), special.Set();
                                        break;
                                    case "quit":
                                        special.Reset(), special.Set(), special.Off();
                                }
                        });
                },
            });
    })(jQuery),
    jQuery(function (e) {
        ($version = "3.6"),
            (e.cookie.json = !0),
            ($special = e.cookie("special")),
            e("#specialButton").length ? (($subversion = "lite"), $special && $special.active && special.On(), e("#specialButton").on("click", special.On)) : (($subversion = "pro"), special.On()),
            e("html").fadeIn(1e3);
    }),
    (function (e) {
        "object" == typeof exports ? e(require("jquery")) : "function" == typeof define && define.amd ? define(["jquery"], e) : e(jQuery);
    })(function (e) {
        function a(e) {
            0 === e.indexOf('"') && (e = s.slice(1, -1).replace(/\\"/g, '"').replace(/\\\\/g, "\\"));
            try {
                return (e = decodeURIComponent(e.replace(/\+/g, " "))), t.json ? JSON.parse(e) : e;
            } catch (e) {}
        }
        function n(n, i) {
            return e.isFunction(i) ? i(t.raw ? n : a(n)) : t.raw ? n : a(n);
        }
        var t = (e.cookie = function (a, i, o) {
            if (void 0 !== i && !e.isFunction(i)) {
                if ("number" == typeof (o = e.extend({}, t.defaults, o)).expires) {
                    var l = o.expires,
                        s = (o.expires = new Date());
                    s.setTime(+s + 864e5 * l);
                }
                return (document.cookie = [
                    t.raw ? a : encodeURIComponent(a),
                    "=",
                    t.raw ? (t.json ? JSON.stringify(i) : String(i)) : encodeURIComponent(t.json ? JSON.stringify(i) : String(i)),
                    o.expires ? "; option_expires=" + o.expires.toUTCString() : "",
                    o.path ? "; option_path=" + o.path : "",
                    o.domain ? "; option_domain=" + o.domain : "",
                    o.secure ? "; option_secure" : "",
                ].join(""));
            }
            for (var c = a ? void 0 : {}, r = document.cookie ? document.cookie.split("; ") : [], u = 0, p = r.length; u < p; u++) {
                var d = r[u].split("="),
                    m = t.raw ? d.shift() : decodeURIComponent(d.shift()),
                    f = d.join("=");
                if (a && a === m) {
                    c = n(f, i);
                    break;
                }
                a || void 0 === (f = n(f)) || (c[m] = f);
            }
            return c;
        });
        (t.defaults = {}),
            (e.removeCookie = function (a, n) {
                return void 0 !== e.cookie(a) && (e.cookie(a, "", e.extend({}, n, { expires: -1 })), !e.cookie(a));
            });
    });
var ResponsiveVoice = function () {
        var e = this;
        (e.responsivevoices = [
            { name: "UK English Female", flag: "gb", gender: "f", voiceIDs: [0, 1, 2, 3, 4, 5, 6] },
            { name: "US English Female", flag: "us", gender: "f", voiceIDs: [7, 8, 9, 10, 11, 12, 13, 14] },
            { name: "Japanese Female", flag: "jp", gender: "f", voiceIDs: [15, 16, 17, 18, 19, 20, 21, 22] },
            { name: "Korean Female", flag: "kr", gender: "f", voiceIDs: [23, 24, 25, 26, 27, 28, 29] },
            { name: "Russian Female", flag: "ru", gender: "f", voiceIDs: [30, 31, 32, 33, 34, 35, 36] },
        ]),
            (e.voicecollection = [
                { name: "Agnes" },
                { name: "Google UK English Female" },
                { name: "en-AU", rate: 0.25, pitch: 1 },
                { name: "English United Kingdom" },
                { name: "Fallback en-GB Female", lang: "en-GB", fallbackvoice: !0 },
                { name: "English United Kingdom", lang: "en_GB" },
                { name: "Karen", lang: "en-AU" },
                { name: "Google US English", timerSpeed: 1 },
                { name: "English United States" },
                { name: "Vicki" },
                { name: "en-US", rate: 0.2, pitch: 1, timerSpeed: 1.3 },
                { name: "Fallback English", lang: "en-US", fallbackvoice: !0, timerSpeed: 0 },
                { name: "English United States", lang: "en_US" },
                { name: "Samantha (Enhanced)", lang: "en-US" },
                { name: "Samantha", lang: "en-US" },
                { name: "Google 日本語" },
                { name: "Google 日本人", timerSpeed: 1 },
                { name: "Kyoko Compact" },
                { name: "ja-JP", rate: 0.25 },
                { name: "Fallback Japanese", lang: "ja", fallbackvoice: !0 },
                { name: "Kyoko" },
                { name: "Japanese Japan", lang: "ja_JP" },
                { name: "Kyoko", lang: "ja-JP" },
                { name: "Google 한국의", timerSpeed: 1 },
                { name: "Narae Compact" },
                { name: "ko-KR", rate: 0.25 },
                { name: "Fallback Korean", lang: "ko", fallbackvoice: !0 },
                { name: "Korean South Korea", lang: "ko_KR" },
                { name: "Yuna" },
                { name: "Yuna", lang: "ko-KR" },
                { name: "Google русский" },
                { name: "Milena Compact" },
                { name: "Milena" },
                { name: "ru-RU", rate: 0.25 },
                { name: "Fallback Russian", lang: "ru_RU", fallbackvoice: !0 },
                { name: "Russian Russia", lang: "ru_RU" },
                { name: "Milena", lang: "ru-RU" },
            ]),
            (e.systemvoices = null),
            (e.CHARACTER_LIMIT = 100),
            (e.VOICESUPPORT_ATTEMPTLIMIT = 5),
            (e.voicesupport_attempts = 0),
            (e.fallbackMode = !1),
            (e.WORDS_PER_MINUTE = 130),
            (e.fallback_parts = null),
            (e.fallback_part_index = 0),
            (e.fallback_audio = null),
            (e.fallback_playbackrate = 1),
            (e.def_fallback_playbackrate = e.fallback_playbackrate),
            (e.fallback_audiopool = []),
            (e.msgparameters = null),
            (e.timeoutId = null),
            (e.OnLoad_callbacks = []),
            (e.useTimer = !1),
            (e.utterances = []),
            (e.default_rv = e.responsivevoices[0]),
            (e.debug = !1),
            (e.log = function (a) {
                e.debug && console.log(a);
            }),
            (e.init = function () {
                setTimeout(function () {
                    var a = setInterval(function () {
                        var n = window.speechSynthesis.getVoices();
                        0 != n.length || (null != e.systemvoices && 0 != e.systemvoices.length)
                            ? (console.log("RV: Voice support ready"), e.systemVoicesReady(n), clearInterval(a))
                            : (console.log("Voice support NOT ready"), e.voicesupport_attempts++, e.voicesupport_attempts > e.VOICESUPPORT_ATTEMPTLIMIT && (clearInterval(a), window.speechSynthesis, e.enableFallbackMode()));
                    }, 100);
                }, 100),
                    e.Dispatch("OnLoad");
            }),
            (e.systemVoicesReady = function (a) {
                (e.systemvoices = a), e.mapRVs(), null != e.OnVoiceReady && e.OnVoiceReady.call(), e.Dispatch("OnReady"), window.hasOwnProperty("dispatchEvent") && window.dispatchEvent(new Event("ResponsiveVoice_OnReady"));
            }),
            (e.enableFallbackMode = function () {
                (e.fallbackMode = !0),
                    console.log("RV: Enabling fallback mode"),
                    e.mapRVs(),
                    null != e.OnVoiceReady && e.OnVoiceReady.call(),
                    e.Dispatch("OnReady"),
                    window.hasOwnProperty("dispatchEvent") && window.dispatchEvent(new Event("ResponsiveVoice_OnReady"));
            }),
            (e.getVoices = function () {
                for (var a = [], n = 0; n < e.responsivevoices.length; n++) a.push({ name: e.responsivevoices[n].name });
                return a;
            }),
            (e.speak = function (a, n, t) {
                e.isPlaying() && (e.log("Cancelling previous speech"), e.cancel()),
                    e.fallbackMode && 0 < e.fallback_audiopool.length && e.clearFallbackPool(),
                    (a = a.replace(/[\"\`]/gm, "'")),
                    (e.msgparameters = t || {}),
                    (e.msgtext = a),
                    (e.msgvoicename = n),
                    (e.onstartFired = !1);
                var i = [];
                if (a.length > e.CHARACTER_LIMIT) {
                    for (var o = a; o.length > e.CHARACTER_LIMIT; ) {
                        var l = "";
                        if (((-1 == (c = o.search(/[:!?.;]+/)) || c >= e.CHARACTER_LIMIT) && (c = o.search(/[,]+/)), -1 == c && -1 == o.search(" ") && (c = 99), -1 == c || c >= e.CHARACTER_LIMIT))
                            for (var s = o.split(" "), c = 0; c < s.length && !(l.length + s[c].length + 1 > e.CHARACTER_LIMIT); c++) l += (0 != c ? " " : "") + s[c];
                        else l = o.substr(0, c + 1);
                        (o = o.substr(l.length, o.length - l.length)), i.push(l);
                    }
                    0 < o.length && i.push(o);
                } else i.push(a);
                if (
                    ((e.multipartText = i),
                    !0 === (c = null == n ? e.default_rv : e.getResponsiveVoice(n)).deprecated && console.warn("ResponsiveVoice: Voice " + c.name + " is deprecated and will be removed in future releases"),
                    (o = {}),
                    null != c.mappedProfile)
                )
                    o = c.mappedProfile;
                else if (((o.systemvoice = e.getMatchedVoice(c)), (o.collectionvoice = {}), null == o.systemvoice)) return void console.log("RV: ERROR: No voice found for: " + n);
                for (e.msgprofile = o, e.utterances = [], c = 0; c < i.length; c++)
                    if (e.fallbackMode) {
                        e.fallback_playbackrate = e.def_fallback_playbackrate;
                        l = e.selectBest([o.collectionvoice.pitch, o.systemvoice.pitch, 1]);
                        var r,
                            u = e.selectBest([o.collectionvoice.volume, o.systemvoice.volume, 1]);
                        null != t && ((l *= null != t.pitch ? t.pitch : 1), (u *= null != t.volume ? t.volume : 1), (r = t.extraParams || null)),
                            (l /= 2),
                            (u *= 2),
                            (l = Math.min(Math.max(l, 0), 1)),
                            (u = Math.min(Math.max(u, 0), 1)),
                            (l = e.fallbackServicePath + "?format=mp3&quality=hi&text=" + encodeURIComponent(i[c]) + "&lang=" + (o.collectionvoice.lang || o.systemvoice.lang || "en-US")),
                            r && (l += "&extraParams=" + JSON.stringify(r)),
                            ((s = document.createElement("AUDIO")).src = l),
                            (s.playbackRate = e.fallback_playbackrate),
                            (s.preload = "auto"),
                            s.load(),
                            e.fallback_parts.push(s);
                    } else
                        e.log("Using SpeechSynthesis"),
                            ((l = new SpeechSynthesisUtterance()).voiceURI = o.systemvoice.voiceURI),
                            (l.volume = e.selectBest([o.collectionvoice.volume, o.systemvoice.volume, 1])),
                            (l.rate = e.selectBest([null, o.collectionvoice.rate, o.systemvoice.rate, 1])),
                            (l.pitch = e.selectBest([o.collectionvoice.pitch, o.systemvoice.pitch, 1])),
                            (l.text = i[c]),
                            (l.lang = e.selectBest([o.collectionvoice.lang, o.systemvoice.lang])),
                            (l.rvIndex = c),
                            (l.rvTotal = i.length),
                            0 == c && (l.onstart = e.speech_onstart),
                            (e.msgparameters.onendcalled = !1),
                            null != t
                                ? ((l.voice = void 0 !== t.voice ? t.voice : o.systemvoice),
                                  c < i.length - 1 && 1 < i.length
                                      ? ((l.onend = e.onPartEnd), l.hasOwnProperty("addEventListener") && l.addEventListener("end", e.onPartEnd))
                                      : ((l.onend = e.speech_onend), l.hasOwnProperty("addEventListener") && l.addEventListener("end", e.speech_onend)),
                                  (l.onerror =
                                      t.onerror ||
                                      function (a) {
                                          e.log("RV: Unknow Error"), e.log(a);
                                      }),
                                  (l.onpause = t.onpause),
                                  (l.onresume = t.onresume),
                                  (l.onmark = t.onmark),
                                  (l.onboundary = t.onboundary || e.onboundary),
                                  (l.pitch = null != t.pitch ? t.pitch : l.pitch),
                                  (l.rate = (null != t.rate ? t.rate : 1) * l.rate),
                                  (l.volume = null != t.volume ? t.volume : l.volume))
                                : (e.log("No Params received for current Utterance"),
                                  (l.voice = o.systemvoice),
                                  (l.onend = e.speech_onend),
                                  (l.onboundary = e.onboundary),
                                  (l.onerror = function (a) {
                                      e.log("RV: Unknow Error"), e.log(a);
                                  })),
                            e.utterances.push(l),
                            0 == c && (e.currentMsg = l),
                            console.log(l),
                            e.tts_speak(l);
                e.fallbackMode && ((e.fallback_part_index = 0), e.fallback_startPart());
            }),
            (e.startTimeout = function (a, n) {
                var t = e.msgprofile.collectionvoice.timerSpeed;
                null == e.msgprofile.collectionvoice.timerSpeed && (t = 1), 0 >= t || ((e.timeoutId = setTimeout(n, e.getEstimatedTimeLength(a, t))), e.log("Timeout ID: " + e.timeoutId));
            }),
            (e.checkAndCancelTimeout = function () {
                null != e.timeoutId && (clearTimeout(e.timeoutId), (e.timeoutId = null));
            }),
            (e.speech_timedout = function () {
                e.cancel(), (e.cancelled = !1), e.speech_onend();
            }),
            (e.speech_onend = function () {
                e.checkAndCancelTimeout(),
                    !0 === e.cancelled
                        ? (e.cancelled = !1)
                        : (e.log("on end fired"),
                          null != e.msgparameters && null != e.msgparameters.onend && 1 != e.msgparameters.onendcalled && (e.log("Speech on end called  -" + e.msgtext), (e.msgparameters.onendcalled = !0), e.msgparameters.onend()));
            }),
            (e.speech_onstart = function () {
                e.onstartFired ||
                    ((e.onstartFired = !0),
                    e.log("Speech start"),
                    e.useTimer && (e.fallbackMode || e.startTimeout(e.msgtext, e.speech_timedout)),
                    (e.msgparameters.onendcalled = !1),
                    null != e.msgparameters && null != e.msgparameters.onstart && e.msgparameters.onstart());
            }),
            (e.isFallbackAudioPlaying = function () {
                var a;
                for (a = 0; a < e.fallback_audiopool.length; a++) if (!e.fallback_audiopool[a].paused) return !0;
                return !1;
            }),
            (e.fallback_finishPart = function (a) {
                e.isFallbackAudioPlaying()
                    ? (e.checkAndCancelTimeout(), (e.timeoutId = setTimeout(e.fallback_finishPart, 1e3 * (e.fallback_audio.duration - e.fallback_audio.currentTime))))
                    : (e.checkAndCancelTimeout(), e.fallback_part_index < e.fallback_parts.length - 1 ? (e.fallback_part_index++, e.fallback_startPart()) : e.speech_onend());
            }),
            (e.cancel = function () {
                e.checkAndCancelTimeout(), e.fallbackMode ? (null != e.fallback_audio && e.fallback_audio.pause(), e.clearFallbackPool()) : ((e.cancelled = !0), speechSynthesis.cancel());
            }),
            (e.voiceSupport = function () {
                return "speechSynthesis" in window;
            }),
            (e.OnFinishedPlaying = function (a) {
                null != e.msgparameters && null != e.msgparameters.onend && e.msgparameters.onend();
            }),
            (e.setDefaultVoice = function (a) {
                null != (a = e.getResponsiveVoice(a)) && (e.default_rv = a);
            }),
            (e.mapRVs = function () {
                for (var a = 0; a < e.responsivevoices.length; a++)
                    for (var n = e.responsivevoices[a], t = 0; t < n.voiceIDs.length; t++) {
                        var i = e.voicecollection[n.voiceIDs[t]];
                        if (1 == i.fallbackvoice) {
                            n.mappedProfile = { systemvoice: {}, collectionvoice: i };
                            break;
                        }
                        var o = e.getSystemVoice(i.name);
                        if (null != o) {
                            n.mappedProfile = { systemvoice: o, collectionvoice: i };
                            break;
                        }
                    }
            }),
            (e.getMatchedVoice = function (a) {
                for (var n = 0; n < a.voiceIDs.length; n++) {
                    var t = e.getSystemVoice(e.voicecollection[a.voiceIDs[n]].name);
                    if (null != t) return t;
                }
                return null;
            }),
            (e.getSystemVoice = function (a) {
                var n = String.fromCharCode(160);
                if (((a = a.replace(new RegExp("\\s+|" + n, "g"), "")), void 0 === e.systemvoices || null === e.systemvoices)) return null;
                for (var t = 0; t < e.systemvoices.length; t++) if (0 === e.systemvoices[t].name.replace(new RegExp("\\s+|" + n, "g"), "").localeCompare(a)) return e.systemvoices[t];
                return null;
            }),
            (e.getResponsiveVoice = function (a) {
                for (var n = 0; n < e.responsivevoices.length; n++)
                    if (e.responsivevoices[n].name == a)
                        return !0 === e.responsivevoices[n].mappedProfile.collectionvoice.fallbackvoice || !0 === e.fallbackMode ? ((e.fallbackMode = !0), (e.fallback_parts = [])) : (e.fallbackMode = !1), e.responsivevoices[n];
                return null;
            }),
            (e.Dispatch = function (a) {
                if (e.hasOwnProperty(a + "_callbacks") && null != e[a + "_callbacks"] && 0 < e[a + "_callbacks"].length) {
                    for (var n = e[a + "_callbacks"], t = 0; t < n.length; t++) n[t]();
                    return !0;
                }
                var i = a + "_callbacks_timeout",
                    o = a + "_callbacks_timeoutCount";
                return (
                    e.hasOwnProperty(i) ||
                        ((e[o] = 10),
                        (e[i] = setInterval(function () {
                            --e[o], (e.Dispatch(a) || 0 > e[o]) && clearTimeout(e[i]);
                        }, 50))),
                    !1
                );
            }),
            (e.AddEventListener = function (a, n) {
                e.hasOwnProperty(a + "_callbacks") || (e[a + "_callbacks"] = []), e[a + "_callbacks"].push(n);
            }),
            (e.addEventListener = e.AddEventListener),
            (e.isPlaying = function () {
                return e.fallbackMode ? null != e.fallback_audio && !e.fallback_audio.ended && !e.fallback_audio.paused : speechSynthesis.speaking;
            }),
            (e.clearFallbackPool = function () {
                for (var a = 0; a < e.fallback_audiopool.length; a++) null != e.fallback_audiopool[a] && (e.fallback_audiopool[a].pause(), (e.fallback_audiopool[a].src = ""));
                e.fallback_audiopool = [];
            }),
            "complete" === document.readyState
                ? e.init()
                : document.addEventListener("DOMContentLoaded", function () {
                      e.init();
                  }),
            (e.selectBest = function (e) {
                for (var a = 0; a < e.length; a++) if (null != e[a]) return e[a];
                return null;
            }),
            (e.pause = function () {
                e.fallbackMode ? null != e.fallback_audio && e.fallback_audio.pause() : speechSynthesis.pause();
            }),
            (e.resume = function () {
                e.fallbackMode ? null != e.fallback_audio && e.fallback_audio.play() : speechSynthesis.resume();
            }),
            (e.tts_speak = function (a) {
                setTimeout(function () {
                    (e.cancelled = !1), speechSynthesis.speak(a);
                }, 0.01);
            }),
            (e.setVolume = function (a) {
                if (e.isPlaying())
                    if (e.fallbackMode) {
                        for (var n = 0; n < e.fallback_parts.length; n++) e.fallback_parts[n].volume = a;
                        for (n = 0; n < e.fallback_audiopool.length; n++) e.fallback_audiopool[n].volume = a;
                        e.fallback_audio.volume = a;
                    } else for (n = 0; n < e.utterances.length; n++) e.utterances[n].volume = a;
            }),
            (e.onPartEnd = function (a) {
                null != e.msgparameters && null != e.msgparameters.onchuckend && e.msgparameters.onchuckend(), e.Dispatch("OnPartEnd"), (a = e.utterances.indexOf(a.utterance)), (e.currentMsg = e.utterances[a + 1]);
            }),
            (e.onboundary = function (a) {
                e.log("On Boundary"), !e.onstartFired && e.speech_onstart();
            }),
            (e.numToWords = function (a) {
                var n = function (e, a) {
                        if (Array.isArray(e)) return e;
                        if (Symbol.iterator in Object(e)) {
                            var n = [],
                                t = !0,
                                i = !1,
                                o = void 0;
                            try {
                                for (var l, s = e[Symbol.iterator](); !(t = (l = s.next()).done) && (n.push(l.value), !a || n.length !== a); t = !0);
                            } catch (e) {
                                (i = !0), (o = e);
                            } finally {
                                try {
                                    !t && s.return && s.return();
                                } finally {
                                    if (i) throw o;
                                }
                            }
                            return n;
                        }
                        throw new TypeError("Invalid attempt to destructure non-iterable instance");
                    },
                    t = function (e) {
                        return 0 === e.length;
                    },
                    i = function (e) {
                        return function (a) {
                            return a.slice(0, e);
                        };
                    },
                    o = function (e) {
                        return function (a) {
                            return function (n) {
                                return e(a(n));
                            };
                        };
                    },
                    l = "one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split(" "),
                    s = "twenty thirty forty fifty sixty seventy eighty ninety".split(" "),
                    c = "thousand million billion trillion quadrillion quintillion sextillion septillion octillion nonillion".split(" ");
                return "number" == typeof a
                    ? e.numToWords(String(a))
                    : "0" === a
                    ? "zero"
                    : o(
                          (function e(a) {
                              return function (n) {
                                  return t(n)
                                      ? []
                                      : [i(a)(n)].concat(
                                            (function (e) {
                                                if (Array.isArray(e)) {
                                                    for (var a = 0, n = Array(e.length); a < e.length; a++) n[a] = e[a];
                                                    return n;
                                                }
                                                return Array.from(e);
                                            })(
                                                e(a)(
                                                    (function (e) {
                                                        return function (a) {
                                                            return a.slice(e);
                                                        };
                                                    })(a)(n)
                                                )
                                            )
                                        );
                              };
                          })(3)
                      )(function (e) {
                          return e.slice(0).reverse();
                      })(Array.from(a))
                          .map(function (e) {
                              e = (t = n(e, 3))[0];
                              var a = t[1],
                                  t = t[2];
                              return [0 === (Number(t) || 0) ? "" : l[t] + " hundred ", 0 === (Number(e) || 0) ? s[a] : (s[a] && s[a] + "-") || "", l[a + e] || l[e]].join("");
                          })
                          .map(function (e, a) {
                              return "" === e ? e : e + " " + c[a];
                          })
                          .filter(
                              o(function (e) {
                                  return !e;
                              })(t)
                          )
                          .reverse()
                          .join(" ")
                          .trim();
            }),
            (e.getWords = function (a) {
                for (var n = a.split(/\s+/), t = 0; t < n.length; t++)
                    null != (a = n[t].toString().match(/\d+/)) &&
                        (n.splice(t, 1),
                        e
                            .numToWords(+a[0])
                            .split(/\s+/)
                            .map(function (e) {
                                n.push(e);
                            }));
                return n;
            }),
            (e.getEstimatedTimeLength = function (a, n) {
                var t = e.getWords(a),
                    i = 0,
                    o = e.fallbackMode ? 1300 : 700;
                (n = n || 1),
                    t.map(function (e, a) {
                        i += (e.toString().match(/[^ ]/gim) || e).length;
                    });
                var l = t.length,
                    s = (60 / e.WORDS_PER_MINUTE) * n * 1e3 * l;
                return 5 > l && (s = n * (o + 50 * i)), e.log("Estimated time length: " + s + " ms, words: [" + t + "], charsCount: " + i), s;
            });
    },
    responsiveVoice = new ResponsiveVoice(),
    $header =
        '<div id="special"><div class="special-panel"><div class="special-font-size"><span>Font: </span> <button title="Small Font" value="1"><i>F</i></button> <button title="Middle Font" value="2"><i>F</i></button> <button title="Large Font" value="3"><i>F</i></button></div><div class="special-color"><span>Color: </span> <button title="Black on White" value="1"><i>C</i></button> <button title="White on Black" value="2"><i>C</i></button> <button title="Blue on Cyan" value="3" i=""><i>C</i></button><button title="Brown on Milk" value="4" i=""><i>C</i></button><button title="Green on Brown" value="5" i=""><i>C</i></button></div><div class="special-images"><span>Images: </span> <button title="Disable/Enable Images"><i></i></button></div><div class="special-audio"><span>Text-to-Speech: </span> <button title="Enable/Disable Text-to-Speech" value="0"><i></i></button></div><div class="special-reset"><span>Default Settings: </span> <button title="Default Settings"><i></i></button></div><div class="special-quit"><span>Standard Version: </span> <button title="Standard Version"><i></i></button></div><div class="special-language"><span>Language: </span> <button title="UK English" onclick="set_UKEng();"><i>UK</i></button><button title="US English" onclick="set_USEng();"><i>US</i></button><button title="Russian" onclick="set_Rus();"><i>RU</i></button><button title="Japanese" onclick="set_Jap();"><i>JP</i></button><button title="Korean" onclick="set_Ko();"><i> KR</i></button></div></div></div>';
