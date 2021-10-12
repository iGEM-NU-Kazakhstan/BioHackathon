var $special;
jQuery("html").hide(),
    (function (e) {
        (e.fn.removeClassWild = function (e) {
            return this.removeClass(function (i, t) {
                var s = e.replace(/\*/g, "\\S+");
                return (t.match(new RegExp("\\b" + s, "g")) || []).join(" ");
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
                    e("html").removeClass("special").removeClassWild("special-*"), e("i.special-audio").remove(), e("audio").remove(), e("#special").remove(), e("#specialButton").show();
                },
                On: function () {
                    e("head").append(e('<link rel="stylesheet" type="text/css" />').attr("href", "./engine-style.css")),
                        $special || special.Reset(),
                        e("#specialButton").length && (($special.active = 1), e.cookie("special", $special, { path: "/" }), e("#specialButton").hide()),
                        e("html").addClass("special"),
                        e("body").prepend(e($header)),
                        special.Set(),
                        e("#special button").on("click", function () {
                            var i = e(this).parent().attr("class").replace("special-", "");
                            if (i)
                                switch ((e("#special .special-" + i + " button").removeClass("active"), i)) {
                                    case "color":
                                        ($special.color = parseInt(e(this).val())),
                                            e(this).addClass("active"),
                                            e("html")
                                                .removeClassWild("special-" + i + "-*")
                                                .addClass("special-" + i + "-" + e(this).val()),
                                            e.cookie("special", $special, { path: "/" });
                                        break;
                                    case "font-size":
                                        ($special.font_size = parseInt(e(this).val())),
                                            e(this).addClass("active"),
                                            e("html")
                                                .removeClassWild("special-" + i + "-*")
                                                .addClass("special-" + i + "-" + e(this).val()),
                                            e.cookie("special", $special, { path: "/" });
                                        break;
                                    case "images":
                                        ($special.images = $special.images ? 0 : 1), e(this).val($special.images), special.ToggleImages(), e.cookie("special", $special, { path: "/" });
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
        function i(e) {
            0 === e.indexOf('"') && (e = s.slice(1, -1).replace(/\\"/g, '"').replace(/\\\\/g, "\\"));
            try {
                return (e = decodeURIComponent(e.replace(/\+/g, " "))), a.json ? JSON.parse(e) : e;
            } catch (e) {}
        }
        function t(t, s) {
            return e.isFunction(s) ? s(a.raw ? t : i(t)) : a.raw ? t : i(t);
        }
        var a = (e.cookie = function (i, s, l) {
            if (void 0 !== s && !e.isFunction(s)) {
                if ("number" == typeof (l = e.extend({}, a.defaults, l)).expires) {
                    var o = l.expires,
                        n = (l.expires = new Date());
                    n.setTime(+n + 864e5 * o);
                }
                return (document.cookie = [
                    a.raw ? i : encodeURIComponent(i),
                    "=",
                    a.raw ? (a.json ? JSON.stringify(s) : String(s)) : encodeURIComponent(a.json ? JSON.stringify(s) : String(value)),
                    l.expires ? "; option_expires=" + l.expires.toUTCString() : "",
                    l.path ? "; option_path=" + l.path : "",
                    l.domain ? "; option_domain=" + l.domain : "",
                    l.secure ? "; option_secure" : "",
                ].join(""));
            }
            for (var c = i ? void 0 : {}, p = document.cookie ? document.cookie.split("; ") : [], r = 0, u = p.length; r < u; r++) {
                var d = p[r].split("="),
                    v = a.raw ? d.shift() : decodeURIComponent(d.shift()),
                    h = d.join("=");
                if (i && i === v) {
                    c = t(h, s);
                    break;
                }
                i || void 0 === (h = t(h)) || (c[v] = h);
            }
            return c;
        });
        a.defaults = {};
    });
var $header =
    '<div id="special"><div class="special-panel"><div class="special-font-size"><span>Font: </span> <button title="Small Font" value="1"><i>F</i></button> <button title="Middle Font" value="2"><i>F</i></button> <button title="Large Font" value="3"><i>F</i></button></div><div class="special-color"><span>Color: </span> <button title="Black on White" value="1"><i>C</i></button> <button title="White on Black" value="2"><i>C</i></button> <button title="Blue on Cyan" value="3" i=""><i>C</i></button><button title="Brown on Milk" value="4" i=""><i>C</i></button><button title="Green on Brown" value="5" i=""><i>C</i></button></div><div class="special-images"><span>Images: </span> <button title="Disable/Enable Images"><i></i></button></div><div class="special-audio"><span>Text-to-Speech: </span> <button title="Enable/Disable Text-to-Speech" value="0"><i></i></button></div><div class="special-reset"><span>Default Settings: </span> <button title="Default Settings"><i></i></button></div><div class="special-quit"><span>Standard Version: </span> <button title="Standard Version"><i></i></button></div></div></div>';
