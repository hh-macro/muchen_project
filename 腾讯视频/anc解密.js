nt = function (t) {
    function e(i) {
        var r = t.call(this) || this;
        return i && ("string" == typeof i ? r.parseKey(i) : (e.hasPrivateKeyProperty(i) || e.hasPublicKeyProperty(i)) && r.parsePropertiesFrom(i)),
            r
    }

    return rt(e, t),
        e.prototype.parseKey = function (t) {
            try {
                var e = 0
                    , i = 0
                    , r = /^\s*(?:[0-9A-Fa-f][0-9A-Fa-f]\s*)+$/.test(t) ? p(t) : d.unarmor(t)
                    , n = S.decode(r);
                if (3 === n.sub.length && (n = n.sub[2].sub[0]),
                9 === n.sub.length) {
                    e = n.sub[1].getHexStringValue(),
                        this.n = I(e, 16),
                        i = n.sub[2].getHexStringValue(),
                        this.e = parseInt(i, 16);
                    var o = n.sub[3].getHexStringValue();
                    this.d = I(o, 16);
                    var s = n.sub[4].getHexStringValue();
                    this.p = I(s, 16);
                    var a = n.sub[5].getHexStringValue();
                    this.q = I(a, 16);
                    var h = n.sub[6].getHexStringValue();
                    this.dmp1 = I(h, 16);
                    var u = n.sub[7].getHexStringValue();
                    this.dmq1 = I(u, 16);
                    var c = n.sub[8].getHexStringValue();
                    this.coeff = I(c, 16)
                } else {
                    if (2 !== n.sub.length)
                        return !1;
                    if (n.sub[0].sub) {
                        var l = n.sub[1].sub[0];
                        e = l.sub[0].getHexStringValue(),
                            this.n = I(e, 16),
                            i = l.sub[1].getHexStringValue(),
                            this.e = parseInt(i, 16)
                    } else
                        e = n.sub[0].getHexStringValue(),
                            this.n = I(e, 16),
                            i = n.sub[1].getHexStringValue(),
                            this.e = parseInt(i, 16)
                }
                return !0
            } catch (f) {
                return !1
            }
        }
        ,
        e.prototype.getPrivateBaseKey = function () {
            var t = {
                array: [new tt.asn1.DERInteger({
                    int: 0
                }), new tt.asn1.DERInteger({
                    bigint: this.n
                }), new tt.asn1.DERInteger({
                    int: this.e
                }), new tt.asn1.DERInteger({
                    bigint: this.d
                }), new tt.asn1.DERInteger({
                    bigint: this.p
                }), new tt.asn1.DERInteger({
                    bigint: this.q
                }), new tt.asn1.DERInteger({
                    bigint: this.dmp1
                }), new tt.asn1.DERInteger({
                    bigint: this.dmq1
                }), new tt.asn1.DERInteger({
                    bigint: this.coeff
                })]
            };
            return new tt.asn1.DERSequence(t).getEncodedHex()
        }
        ,
        e.prototype.getPrivateBaseKeyB64 = function () {
            return c(this.getPrivateBaseKey())
        }
        ,
        e.prototype.getPublicBaseKey = function () {
            var t = new tt.asn1.DERSequence({
                array: [new tt.asn1.DERObjectIdentifier({
                    oid: "1.2.840.113549.1.1.1"
                }), new tt.asn1.DERNull]
            })
                , e = new tt.asn1.DERSequence({
                array: [new tt.asn1.DERInteger({
                    bigint: this.n
                }), new tt.asn1.DERInteger({
                    int: this.e
                })]
            })
                , i = new tt.asn1.DERBitString({
                hex: "00" + e.getEncodedHex()
            });
            return new tt.asn1.DERSequence({
                array: [t, i]
            }).getEncodedHex()
        }
        ,
        e.prototype.getPublicBaseKeyB64 = function () {
            return c(this.getPublicBaseKey())
        }
        ,
        e.wordwrap = function (t, e) {
            if (!t)
                return t;
            var i = "(.{1," + (e = e || 64) + "})( +|$\n?)|(.{1," + e + "})";
            return t.match(RegExp(i, "g")).join("\n")
        }
        ,
        e.prototype.getPrivateKey = function () {
            var t = "-----BEGIN RSA PRIVATE KEY-----\n";
            return t += e.wordwrap(this.getPrivateBaseKeyB64()) + "\n",
                t += "-----END RSA PRIVATE KEY-----"
        }
        ,
        e.prototype.getPublicKey = function () {
            var t = "-----BEGIN PUBLIC KEY-----\n";
            return t += e.wordwrap(this.getPublicBaseKeyB64()) + "\n",
                t += "-----END PUBLIC KEY-----"
        }
        ,
        e.hasPublicKeyProperty = function (t) {
            return (t = t || {}).hasOwnProperty("n") && t.hasOwnProperty("e")
        }
        ,
        e.hasPrivateKeyProperty = function (t) {
            return (t = t || {}).hasOwnProperty("n") && t.hasOwnProperty("e") && t.hasOwnProperty("d") && t.hasOwnProperty("p") && t.hasOwnProperty("q") && t.hasOwnProperty("dmp1") && t.hasOwnProperty("dmq1") && t.hasOwnProperty("coeff")
        }
        ,
        e.prototype.parsePropertiesFrom = function (t) {
            this.n = t.n,
                this.e = t.e,
            t.hasOwnProperty("d") && (this.d = t.d,
                this.p = t.p,
                this.q = t.q,
                this.dmp1 = t.dmp1,
                this.dmq1 = t.dmq1,
                this.coeff = t.coeff)
        }
        ,
        e
}
st = function () {
    function t(t) {
        void 0 === t && (t = {}),
            t = t || {},
            this.default_key_size = t.default_key_size ? parseInt(t.default_key_size, 10) : 1024,
            this.default_public_exponent = t.default_public_exponent || "010001",
            this.log = t.log || !1,
            this.key = null
    }

    return t.prototype.setKey = function (t) {
        this.log && this.key && console.warn("A key was already set, overriding existing."),
            this.key = new nt(t)
    }
        ,
        t.prototype.setPrivateKey = function (t) {
            this.setKey(t)
        }
        ,
        t.prototype.setPublicKey = function (t) {
            this.setKey(t)
        }
        ,
        t.prototype.decrypt = function (t) {
            try {
                return this.getKey().decrypt(l(t))
            } catch (e) {
                return !1
            }
        }
        ,
        t.prototype.encrypt = function (t) {
            try {
                return c(this.getKey().encrypt(t))
            } catch (e) {
                return !1
            }
        }
        ,
        t.prototype.sign = function (t, e, i) {
            try {
                return c(this.getKey().sign(t, e, i))
            } catch (r) {
                return !1
            }
        }
        ,
        t.prototype.verify = function (t, e, i) {
            try {
                return this.getKey().verify(t, l(e), i)
            } catch (r) {
                return !1
            }
        }
        ,
        t.prototype.getKey = function (t) {
            if (!this.key) {
                if (this.key = new nt,
                t && "[object Function]" === {}.toString.call(t))
                    return void this.key.generateAsync(this.default_key_size, this.default_public_exponent, t);
                this.key.generate(this.default_key_size, this.default_public_exponent)
            }
            return this.key
        }
        ,
        t.prototype.getPrivateKey = function () {
            return this.getKey().getPrivateKey()
        }
        ,
        t.prototype.getPrivateKeyB64 = function () {
            return this.getKey().getPrivateBaseKeyB64()
        }
        ,
        t.prototype.getPublicKey = function () {
            return this.getKey().getPublicKey()
        }
        ,
        t.prototype.getPublicKeyB64 = function () {
            return this.getKey().getPublicBaseKeyB64()
        }
        ,
        t.version = void 0,
        t
}();

// 实例化 RSA 对象
const rsa = new st();

// 生成密钥（默认1024位）
rsa.getKey();

// 获取 Base64 格式的公钥
const publicKeyB64 = rsa.getPublicKeyB64();
console.log("Public Key (Base64):", publicKeyB64);

// 获取 PEM 格式的公钥（如果支持）
const publicKeyPEM = rsa.getPublicKey();
console.log("Public Key (PEM):", publicKeyPEM);