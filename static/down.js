
function initializeDownloadLogic() {
    "use strict";
    var n = i("d4ec"),
        a = i("bee2"),
        r = (i("d9e2"),
            i("d3b7"),
            i("e6cf"),
            i("83c5")),
        o = i("2294"),
        s = i("6df4"),
        c = function() {
            return window.globalVue
        },
        l = function(e) {
            var t, i, n, a, r, o, s = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
            n = e.length,
            i = 0,
            t = "";
            while (i < n) {
                if (a = 255 & e.charCodeAt(i++),
                i === n) {
                    t += s.charAt(a >> 2),
                    t += s.charAt((3 & a) << 4),
                    t += "==";
                    break
                }
                if (r = e.charCodeAt(i++),
                i === n) {
                    t += s.charAt(a >> 2),
                    t += s.charAt((3 & a) << 4 | (240 & r) >> 4),
                    t += s.charAt((15 & r) << 2),
                    t += "=";
                    break
                }
                o = e.charCodeAt(i++),
                t += s.charAt(a >> 2),
                t += s.charAt((3 & a) << 4 | (240 & r) >> 4),
                t += s.charAt((15 & r) << 2 | (192 & o) >> 6),
                t += s.charAt(63 & o)
            }
            return t
        },
        d = function() {
            function e(t, i) {
                Object(n["a"])(this, e),
                this.ctx = t,
                this.sign = "",
                this.timestamp = "",
                this.vm = i
            }
            return Object(a["a"])(e, [{
                key: "getSign",
                value: function() {
                    var e = this;
                    return this.sign ? Promise.resolve() : Object(o["c"])().then((function(t) {
                        var i = t.sign1,
                            n = t.sign2,
                            a = t.sign3,
                            r = t.timestamp,
                            o = "";
                        try {
                            o = new Function("return " + n)()
                        } catch (c) {
                            throw new Error(c.message)
                        }
                        if ("function" !== typeof o)
                            throw new Error("get sign fail");
                        var s = o(a, i);
                        e.sign = l(s),
                        e.timestamp = r
                    }
                    ))
                }
            }, {
                key: "setResData",
                value: function(e) {
                    if (0 === e.errno && (e.dlink || e.list))
                        return e;
                    var t = c(),
                        i = t.$t("main.reloadMsg") + '<a class="nd-file-manage-tip__fail-link" href="javascript:window.location.reload();">' + t.$t("main.refresh") + "</a>" + t.$t("main.andRetry"),
                        n = {
                            2: t.$t("main.downloadFail"),
                            116: t.$t("main.shareNotFound"),
                            "-1": t.$t("main.illegalDownload"),
                            118: t.$t("main.noPermission"),
                            113: i,
                            112: i,
                            121: t.$t("main.toManyFiles"),
                            31326: t.$t("main.downloadFail"),
                            31426: t.$t("main.downloadFail")
                        },
                        a = e.show_msg || n[e.errno];
                    return e.show_msg = a,
                    e
                }
            }, {
                key: "getDlink",
                value: function(e) {
                    var t = this,
                        i = e.fidlist,
                        n = e.type;
                    console.log(this.getSign().then(() => console.log("Sign generated successfully:", this.sign)).catch(console.error))
                    return this.getSign().then((function() {
                        var e, a = t.sign, o = t.timestamp, l = (null === (e = c()) || void 0 === e || null === (e = e.$store) || void 0 === e ? void 0 : e.state.download.trialDownloadTestKey) > s["l"].NO_TRIAL ? 1 : 0;
                        return Object(r["a"])({
                            fidlist: i,
                            type: n,
                            vip: 2,
                            sign: a,
                            timestamp: o,
                            need_speed: l
                        }).then((function(e) {
                            const response = t.setResData(e);  // Assuming e is your response object
                            if (response && response.dlink && Array.isArray(response.dlink)) {
                                response.dlink.forEach(item => console.log(item.dlink));
                            }
                            return t.setResData(e)
                        }
                        ))
                    }
                    ))
                }
            }])
        }();
    return d;
}