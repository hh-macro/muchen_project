var V, q, C = [];
for (V = "0".charCodeAt(0),
         q = 0; q <= 9; ++q)
    C[V++] = q;
for (V = "a".charCodeAt(0),
         q = 10; q < 36; ++q)
    C[V++] = q;
for (V = "A".charCodeAt(0),
         q = 10; q < 36; ++q)
    C[V++] = q;

function j(t, e) {
    var i = C[t.charCodeAt(e)];
    return null == i ? -1 : i
}

function P(t) {
    var e = _();
    return e.fromInt(t),
        e
}

var Y = function () {
    function t() {
    }

    return t.prototype.nextBytes = function (t) {
        for (var e = 0; e < t.length; ++e)
            t[e] = W()
    }
        ,
        t
}();
var F = function () {
    function t() {
        this.i = 0,
            this.j = 0,
            this.S = []
    }

    return t.prototype.init = function (t) {
        var e, i, r;
        for (e = 0; e < 256; ++e)
            this.S[e] = e;
        for (i = 0,
                 e = 0; e < 256; ++e)
            i = i + this.S[e] + t[e % t.length] & 255,
                r = this.S[e],
                this.S[e] = this.S[i],
                this.S[i] = r;
        this.i = 0,
            this.j = 0
    }
        ,
        t.prototype.next = function () {
            var t;
            return this.i = this.i + 1 & 255,
                this.j = this.j + this.S[this.i] & 255,
                t = this.S[this.i],
                this.S[this.i] = this.S[this.j],
                this.S[this.j] = t,
                this.S[t + this.S[this.i] & 255]
        }
        ,
        t
}();
// H = void 0
// L = 256

var H, L, U = null;
if (null == U) {
    U = [],
        L = 0;
    var z = void 0;
    if ("undefined" != typeof window && window.crypto && window.crypto.getRandomValues) {
        var K = new Uint32Array(256);
        for (window.crypto.getRandomValues(K),
                 z = 0; z < K.length; ++z)
            U[L++] = 255 & K[z]
    }
    var G = 0
        , Z = function (t) {
        if ((G = G || 0) >= 256 || L >= 256)
            window.removeEventListener ? window.removeEventListener("mousemove", Z, !1) : window.detachEvent && window.detachEvent("onmousemove", Z);
        else
            try {
                var e = t.x + t.y;
                U[L++] = 255 & e,
                    G += 1
            } catch (i) {
            }
    };
    "undefined" != typeof window && (window.addEventListener ? window.addEventListener("mousemove", Z, !1) : window.attachEvent && window.attachEvent("onmousemove", Z))
}

function W() {
    if (null == H) {
        for (H = new F; L < 256;) {
            var t = Math.floor(65536 * Math.random());
            U[L++] = 255 & t
        }
        for (H.init(U),
                 L = 0; L < U.length; ++L)
            U[L] = 0;
        L = 0
    }
    return H.next()
}

function M(t) {
    var e, i = 1;
    return 0 != (e = t >>> 16) && (t = e,
        i += 16),
    0 != (e = t >> 8) && (t = e,
        i += 8),
    0 != (e = t >> 4) && (t = e,
        i += 4),
    0 != (e = t >> 2) && (t = e,
        i += 2),
    0 != (e = t >> 1) && (t = e,
        i += 1),
        i
}

var J = {
    md2: "3020300c06082a864886f70d020205000410",
    md5: "3020300c06082a864886f70d020505000410",
    sha1: "3021300906052b0e03021a05000414",
    sha224: "302d300d06096086480165030402040500041c",
    sha256: "3031300d060960864801650304020105000420",
    sha384: "3041300d060960864801650304020205000430",
    sha512: "3051300d060960864801650304020305000440",
    ripemd160: "3021300906052b2403020105000414"
};

function _() {
    return new k(null)
}

k = function () {
    function t(t, e, i) {
        null != t && ("number" == typeof t ? this.fromNumber(t, e, i) : null == e && "string" != typeof t ? this.fromString(t, 256) : this.fromString(t, e))
    }

    return t.prototype.toString = function (t) {
        if (this.s < 0)
            return "-" + this.negate().toString(t);
        var i;
        if (16 == t)
            i = 4;
        else if (8 == t)
            i = 3;
        else if (2 == t)
            i = 1;
        else if (32 == t)
            i = 5;
        else {
            if (4 != t)
                return this.toRadix(t);
            i = 2
        }
        var r, n = (1 << i) - 1, o = !1, s = "", a = this.t, h = this.DB - a * this.DB % i;
        if (a-- > 0)
            for (h < this.DB && (r = this[a] >> h) > 0 && (o = !0,
                s = e(r)); a >= 0;)
                h < i ? (r = (this[a] & (1 << h) - 1) << i - h,
                    r |= this[--a] >> (h += this.DB - i)) : (r = this[a] >> (h -= i) & n,
                h <= 0 && (h += this.DB,
                    --a)),
                r > 0 && (o = !0),
                o && (s += e(r));
        return o ? s : "0"
    }
        ,
        t.prototype.negate = function () {
            var e = _();
            return t.ZERO.subTo(this, e),
                e
        }
        ,
        t.prototype.abs = function () {
            return this.s < 0 ? this.negate() : this
        }
        ,
        t.prototype.compareTo = function (t) {
            var e = this.s - t.s;
            if (0 != e)
                return e;
            var i = this.t;
            if (0 != (e = i - t.t))
                return this.s < 0 ? -e : e;
            for (; --i >= 0;)
                if (0 != (e = this[i] - t[i]))
                    return e;
            return 0
        }
        ,
        t.prototype.bitLength = function () {
            return this.t <= 0 ? 0 : this.DB * (this.t - 1) + M(this[this.t - 1] ^ this.s & this.DM)
        }
        ,
        t.prototype.mod = function (e) {
            var i = _();
            return this.abs().divRemTo(e, null, i),
            this.s < 0 && i.compareTo(t.ZERO) > 0 && e.subTo(i, i),
                i
        }
        ,
        t.prototype.modPowInt = function (t, e) {
            var i;
            return i = t < 256 || e.isEven() ? new B(e) : new A(e),
                this.exp(t, i)
        }
        ,
        t.prototype.clone = function () {
            var t = _();
            return this.copyTo(t),
                t
        }
        ,
        t.prototype.intValue = function () {
            if (this.s < 0) {
                if (1 == this.t)
                    return this[0] - this.DV;
                if (0 == this.t)
                    return -1
            } else {
                if (1 == this.t)
                    return this[0];
                if (0 == this.t)
                    return 0
            }
            return (this[1] & (1 << 32 - this.DB) - 1) << this.DB | this[0]
        }
        ,
        t.prototype.byteValue = function () {
            return 0 == this.t ? this.s : this[0] << 24 >> 24
        }
        ,
        t.prototype.shortValue = function () {
            return 0 == this.t ? this.s : this[0] << 16 >> 16
        }
        ,
        t.prototype.signum = function () {
            return this.s < 0 ? -1 : this.t <= 0 || 1 == this.t && this[0] <= 0 ? 0 : 1
        }
        ,
        t.prototype.toByteArray = function () {
            var t = this.t
                , e = [];
            e[0] = this.s;
            var i, r = this.DB - t * this.DB % 8, n = 0;
            if (t-- > 0)
                for (r < this.DB && (i = this[t] >> r) != (this.s & this.DM) >> r && (e[n++] = i | this.s << this.DB - r); t >= 0;)
                    r < 8 ? (i = (this[t] & (1 << r) - 1) << 8 - r,
                        i |= this[--t] >> (r += this.DB - 8)) : (i = this[t] >> (r -= 8) & 255,
                    r <= 0 && (r += this.DB,
                        --t)),
                    0 != (128 & i) && (i |= -256),
                    0 == n && (128 & this.s) != (128 & i) && ++n,
                    (n > 0 || i != this.s) && (e[n++] = i);
            return e
        }
        ,
        t.prototype.equals = function (t) {
            return 0 == this.compareTo(t)
        }
        ,
        t.prototype.min = function (t) {
            return this.compareTo(t) < 0 ? this : t
        }
        ,
        t.prototype.max = function (t) {
            return this.compareTo(t) > 0 ? this : t
        }
        ,
        t.prototype.and = function (t) {
            var e = _();
            return this.bitwiseTo(t, i, e),
                e
        }
        ,
        t.prototype.or = function (t) {
            var e = _();
            return this.bitwiseTo(t, r, e),
                e
        }
        ,
        t.prototype.xor = function (t) {
            var e = _();
            return this.bitwiseTo(t, n, e),
                e
        }
        ,
        t.prototype.andNot = function (t) {
            var e = _();
            return this.bitwiseTo(t, o, e),
                e
        }
        ,
        t.prototype.not = function () {
            for (var t = _(), e = 0; e < this.t; ++e)
                t[e] = this.DM & ~this[e];
            return t.t = this.t,
                t.s = ~this.s,
                t
        }
        ,
        t.prototype.shiftLeft = function (t) {
            var e = _();
            return t < 0 ? this.rShiftTo(-t, e) : this.lShiftTo(t, e),
                e
        }
        ,
        t.prototype.shiftRight = function (t) {
            var e = _();
            return t < 0 ? this.lShiftTo(-t, e) : this.rShiftTo(t, e),
                e
        }
        ,
        t.prototype.getLowestSetBit = function () {
            for (var t = 0; t < this.t; ++t)
                if (0 != this[t])
                    return t * this.DB + s(this[t]);
            return this.s < 0 ? this.t * this.DB : -1
        }
        ,
        t.prototype.bitCount = function () {
            for (var t = 0, e = this.s & this.DM, i = 0; i < this.t; ++i)
                t += a(this[i] ^ e);
            return t
        }
        ,
        t.prototype.testBit = function (t) {
            var e = Math.floor(t / this.DB);
            return e >= this.t ? 0 != this.s : 0 != (this[e] & 1 << t % this.DB)
        }
        ,
        t.prototype.setBit = function (t) {
            return this.changeBit(t, r)
        }
        ,
        t.prototype.clearBit = function (t) {
            return this.changeBit(t, o)
        }
        ,
        t.prototype.flipBit = function (t) {
            return this.changeBit(t, n)
        }
        ,
        t.prototype.add = function (t) {
            var e = _();
            return this.addTo(t, e),
                e
        }
        ,
        t.prototype.subtract = function (t) {
            var e = _();
            return this.subTo(t, e),
                e
        }
        ,
        t.prototype.multiply = function (t) {
            var e = _();
            return this.multiplyTo(t, e),
                e
        }
        ,
        t.prototype.divide = function (t) {
            var e = _();
            return this.divRemTo(t, e, null),
                e
        }
        ,
        t.prototype.remainder = function (t) {
            var e = _();
            return this.divRemTo(t, null, e),
                e
        }
        ,
        t.prototype.divideAndRemainder = function (t) {
            var e = _()
                , i = _();
            return this.divRemTo(t, e, i),
                [e, i]
        }
        ,
        t.prototype.modPow = function (t, e) {
            var i, r, n = t.bitLength(), o = P(1);
            if (n <= 0)
                return o;
            i = n < 18 ? 1 : n < 48 ? 3 : n < 144 ? 4 : n < 768 ? 5 : 6,
                r = n < 8 ? new B(e) : e.isEven() ? new R(e) : new A(e);
            var s = []
                , a = 3
                , h = i - 1
                , u = (1 << i) - 1;
            if (s[1] = r.convert(this),
            i > 1) {
                var c = _();
                for (r.sqrTo(s[1], c); a <= u;)
                    s[a] = _(),
                        r.mulTo(c, s[a - 2], s[a]),
                        a += 2
            }
            var l, f, p = t.t - 1, d = !0, g = _();
            for (n = M(t[p]) - 1; p >= 0;) {
                for (n >= h ? l = t[p] >> n - h & u : (l = (t[p] & (1 << n + 1) - 1) << h - n,
                p > 0 && (l |= t[p - 1] >> this.DB + n - h)),
                         a = i; 0 == (1 & l);)
                    l >>= 1,
                        --a;
                if ((n -= a) < 0 && (n += this.DB,
                    --p),
                    d)
                    s[l].copyTo(o),
                        d = !1;
                else {
                    for (; a > 1;)
                        r.sqrTo(o, g),
                            r.sqrTo(g, o),
                            a -= 2;
                    a > 0 ? r.sqrTo(o, g) : (f = o,
                        o = g,
                        g = f),
                        r.mulTo(g, s[l], o)
                }
                for (; p >= 0 && 0 == (t[p] & 1 << n);)
                    r.sqrTo(o, g),
                        f = o,
                        o = g,
                        g = f,
                    --n < 0 && (n = this.DB - 1,
                        --p)
            }
            return r.revert(o)
        }
        ,
        t.prototype.modInverse = function (e) {
            var i = e.isEven();
            if (this.isEven() && i || 0 == e.signum())
                return t.ZERO;
            for (var r = e.clone(), n = this.clone(), o = P(1), s = P(0), a = P(0), h = P(1); 0 != r.signum();) {
                for (; r.isEven();)
                    r.rShiftTo(1, r),
                        i ? (o.isEven() && s.isEven() || (o.addTo(this, o),
                            s.subTo(e, s)),
                            o.rShiftTo(1, o)) : s.isEven() || s.subTo(e, s),
                        s.rShiftTo(1, s);
                for (; n.isEven();)
                    n.rShiftTo(1, n),
                        i ? (a.isEven() && h.isEven() || (a.addTo(this, a),
                            h.subTo(e, h)),
                            a.rShiftTo(1, a)) : h.isEven() || h.subTo(e, h),
                        h.rShiftTo(1, h);
                r.compareTo(n) >= 0 ? (r.subTo(n, r),
                i && o.subTo(a, o),
                    s.subTo(h, s)) : (n.subTo(r, n),
                i && a.subTo(o, a),
                    h.subTo(s, h))
            }
            return 0 != n.compareTo(t.ONE) ? t.ZERO : h.compareTo(e) >= 0 ? h.subtract(e) : h.signum() < 0 ? (h.addTo(e, h),
                h.signum() < 0 ? h.add(e) : h) : h
        }
        ,
        t.prototype.pow = function (t) {
            return this.exp(t, new O)
        }
        ,
        t.prototype.gcd = function (t) {
            var e = this.s < 0 ? this.negate() : this.clone()
                , i = t.s < 0 ? t.negate() : t.clone();
            if (e.compareTo(i) < 0) {
                var r = e;
                e = i,
                    i = r
            }
            var n = e.getLowestSetBit()
                , o = i.getLowestSetBit();
            if (o < 0)
                return e;
            for (n < o && (o = n),
                 o > 0 && (e.rShiftTo(o, e),
                     i.rShiftTo(o, i)); e.signum() > 0;)
                (n = e.getLowestSetBit()) > 0 && e.rShiftTo(n, e),
                (n = i.getLowestSetBit()) > 0 && i.rShiftTo(n, i),
                    e.compareTo(i) >= 0 ? (e.subTo(i, e),
                        e.rShiftTo(1, e)) : (i.subTo(e, i),
                        i.rShiftTo(1, i));
            return o > 0 && i.lShiftTo(o, i),
                i
        }
        ,
        t.prototype.isProbablePrime = function (t) {
            var e, i = this.abs();
            if (1 == i.t && i[0] <= E[E.length - 1]) {
                for (e = 0; e < E.length; ++e)
                    if (i[0] == E[e])
                        return !0;
                return !1
            }
            if (i.isEven())
                return !1;
            for (e = 1; e < E.length;) {
                for (var r = E[e], n = e + 1; n < E.length && r < D;)
                    r *= E[n++];
                for (r = i.modInt(r); e < n;)
                    if (r % E[e++] == 0)
                        return !1
            }
            return i.millerRabin(t)
        }
        ,
        t.prototype.copyTo = function (t) {
            for (var e = this.t - 1; e >= 0; --e)
                t[e] = this[e];
            t.t = this.t,
                t.s = this.s
        }
        ,
        t.prototype.fromInt = function (t) {
            this.t = 1,
                this.s = t < 0 ? -1 : 0,
                t > 0 ? this[0] = t : t < -1 ? this[0] = t + this.DV : this.t = 0
        }
        ,
        t.prototype.fromString = function (e, i) {
            var r;
            if (16 == i)
                r = 4;
            else if (8 == i)
                r = 3;
            else if (256 == i)
                r = 8;
            else if (2 == i)
                r = 1;
            else if (32 == i)
                r = 5;
            else {
                if (4 != i)
                    return void this.fromRadix(e, i);
                r = 2
            }
            this.t = 0,
                this.s = 0;
            for (var n = e.length, o = !1, s = 0; --n >= 0;) {
                var a = 8 == r ? 255 & +e[n] : j(e, n);
                a < 0 ? "-" == e.charAt(n) && (o = !0) : (o = !1,
                    0 == s ? this[this.t++] = a : s + r > this.DB ? (this[this.t - 1] |= (a & (1 << this.DB - s) - 1) << s,
                        this[this.t++] = a >> this.DB - s) : this[this.t - 1] |= a << s,
                (s += r) >= this.DB && (s -= this.DB))
            }
            8 == r && 0 != (128 & +e[0]) && (this.s = -1,
            s > 0 && (this[this.t - 1] |= (1 << this.DB - s) - 1 << s)),
                this.clamp(),
            o && t.ZERO.subTo(this, this)
        }
        ,
        t.prototype.clamp = function () {
            for (var t = this.s & this.DM; this.t > 0 && this[this.t - 1] == t;)
                --this.t
        }
        ,
        t.prototype.dlShiftTo = function (t, e) {
            var i;
            for (i = this.t - 1; i >= 0; --i)
                e[i + t] = this[i];
            for (i = t - 1; i >= 0; --i)
                e[i] = 0;
            e.t = this.t + t,
                e.s = this.s
        }
        ,
        t.prototype.drShiftTo = function (t, e) {
            for (var i = t; i < this.t; ++i)
                e[i - t] = this[i];
            e.t = Math.max(this.t - t, 0),
                e.s = this.s
        }
        ,
        t.prototype.lShiftTo = function (t, e) {
            for (var i = t % this.DB, r = this.DB - i, n = (1 << r) - 1, o = Math.floor(t / this.DB), s = this.s << i & this.DM, a = this.t - 1; a >= 0; --a)
                e[a + o + 1] = this[a] >> r | s,
                    s = (this[a] & n) << i;
            for (a = o - 1; a >= 0; --a)
                e[a] = 0;
            e[o] = s,
                e.t = this.t + o + 1,
                e.s = this.s,
                e.clamp()
        }
        ,
        t.prototype.rShiftTo = function (t, e) {
            e.s = this.s;
            var i = Math.floor(t / this.DB);
            if (i >= this.t)
                e.t = 0;
            else {
                var r = t % this.DB
                    , n = this.DB - r
                    , o = (1 << r) - 1;
                e[0] = this[i] >> r;
                for (var s = i + 1; s < this.t; ++s)
                    e[s - i - 1] |= (this[s] & o) << n,
                        e[s - i] = this[s] >> r;
                r > 0 && (e[this.t - i - 1] |= (this.s & o) << n),
                    e.t = this.t - i,
                    e.clamp()
            }
        }
        ,
        t.prototype.subTo = function (t, e) {
            for (var i = 0, r = 0, n = Math.min(t.t, this.t); i < n;)
                r += this[i] - t[i],
                    e[i++] = r & this.DM,
                    r >>= this.DB;
            if (t.t < this.t) {
                for (r -= t.s; i < this.t;)
                    r += this[i],
                        e[i++] = r & this.DM,
                        r >>= this.DB;
                r += this.s
            } else {
                for (r += this.s; i < t.t;)
                    r -= t[i],
                        e[i++] = r & this.DM,
                        r >>= this.DB;
                r -= t.s
            }
            e.s = r < 0 ? -1 : 0,
                r < -1 ? e[i++] = this.DV + r : r > 0 && (e[i++] = r),
                e.t = i,
                e.clamp()
        }
        ,
        t.prototype.multiplyTo = function (e, i) {
            var r = this.abs()
                , n = e.abs()
                , o = r.t;
            for (i.t = o + n.t; --o >= 0;)
                i[o] = 0;
            for (o = 0; o < n.t; ++o)
                i[o + r.t] = r.am(0, n[o], i, o, 0, r.t);
            i.s = 0,
                i.clamp(),
            this.s != e.s && t.ZERO.subTo(i, i)
        }
        ,
        t.prototype.squareTo = function (t) {
            for (var e = this.abs(), i = t.t = 2 * e.t; --i >= 0;)
                t[i] = 0;
            for (i = 0; i < e.t - 1; ++i) {
                var r = e.am(i, e[i], t, 2 * i, 0, 1);
                (t[i + e.t] += e.am(i + 1, 2 * e[i], t, 2 * i + 1, r, e.t - i - 1)) >= e.DV && (t[i + e.t] -= e.DV,
                    t[i + e.t + 1] = 1)
            }
            t.t > 0 && (t[t.t - 1] += e.am(i, e[i], t, 2 * i, 0, 1)),
                t.s = 0,
                t.clamp()
        }
        ,
        t.prototype.divRemTo = function (e, i, r) {
            var n = e.abs();
            if (!(n.t <= 0)) {
                var o = this.abs();
                if (o.t < n.t)
                    return null != i && i.fromInt(0),
                        void (null != r && this.copyTo(r));
                null == r && (r = _());
                var s = _()
                    , a = this.s
                    , h = e.s
                    , u = this.DB - M(n[n.t - 1]);
                u > 0 ? (n.lShiftTo(u, s),
                    o.lShiftTo(u, r)) : (n.copyTo(s),
                    o.copyTo(r));
                var c = s.t
                    , l = s[c - 1];
                if (0 != l) {
                    var f = l * (1 << this.F1) + (c > 1 ? s[c - 2] >> this.F2 : 0)
                        , p = this.FV / f
                        , d = (1 << this.F1) / f
                        , g = 1 << this.F2
                        , m = r.t
                        , b = m - c
                        , v = null == i ? _() : i;
                    for (s.dlShiftTo(b, v),
                         r.compareTo(v) >= 0 && (r[r.t++] = 1,
                             r.subTo(v, r)),
                             t.ONE.dlShiftTo(c, v),
                             v.subTo(s, s); s.t < c;)
                        s[s.t++] = 0;
                    for (; --b >= 0;) {
                        var w = r[--m] == l ? this.DM : Math.floor(r[m] * p + (r[m - 1] + g) * d);
                        if ((r[m] += s.am(0, w, r, b, 0, c)) < w)
                            for (s.dlShiftTo(b, v),
                                     r.subTo(v, r); r[m] < --w;)
                                r.subTo(v, r)
                    }
                    null != i && (r.drShiftTo(c, i),
                    a != h && t.ZERO.subTo(i, i)),
                        r.t = c,
                        r.clamp(),
                    u > 0 && r.rShiftTo(u, r),
                    a < 0 && t.ZERO.subTo(r, r)
                }
            }
        }
        ,
        t.prototype.invDigit = function () {
            if (this.t < 1)
                return 0;
            var t = this[0];
            if (0 == (1 & t))
                return 0;
            var e = 3 & t;
            return (e = (e = (e = (e = e * (2 - (15 & t) * e) & 15) * (2 - (255 & t) * e) & 255) * (2 - ((65535 & t) * e & 65535)) & 65535) * (2 - t * e % this.DV) % this.DV) > 0 ? this.DV - e : -e
        }
        ,
        t.prototype.isEven = function () {
            return 0 == (this.t > 0 ? 1 & this[0] : this.s)
        }
        ,
        t.prototype.exp = function (e, i) {
            if (e > 4294967295 || e < 1)
                return t.ONE;
            var r = _()
                , n = _()
                , o = i.convert(this)
                , s = M(e) - 1;
            for (o.copyTo(r); --s >= 0;)
                if (i.sqrTo(r, n),
                (e & 1 << s) > 0)
                    i.mulTo(n, o, r);
                else {
                    var a = r;
                    r = n,
                        n = a
                }
            return i.revert(r)
        }
        ,
        t.prototype.chunkSize = function (t) {
            return Math.floor(Math.LN2 * this.DB / Math.log(t))
        }
        ,
        t.prototype.toRadix = function (t) {
            if (null == t && (t = 10),
            0 == this.signum() || t < 2 || t > 36)
                return "0";
            var e = this.chunkSize(t)
                , i = Math.pow(t, e)
                , r = P(i)
                , n = _()
                , o = _()
                , s = "";
            for (this.divRemTo(r, n, o); n.signum() > 0;)
                s = (i + o.intValue()).toString(t).substr(1) + s,
                    n.divRemTo(r, n, o);
            return o.intValue().toString(t) + s
        }
        ,
        t.prototype.fromRadix = function (e, i) {
            this.fromInt(0),
            null == i && (i = 10);
            for (var r = this.chunkSize(i), n = Math.pow(i, r), o = !1, s = 0, a = 0, h = 0; h < e.length; ++h) {
                var u = j(e, h);
                u < 0 ? "-" == e.charAt(h) && 0 == this.signum() && (o = !0) : (a = i * a + u,
                ++s >= r && (this.dMultiply(n),
                    this.dAddOffset(a, 0),
                    s = 0,
                    a = 0))
            }
            s > 0 && (this.dMultiply(Math.pow(i, s)),
                this.dAddOffset(a, 0)),
            o && t.ZERO.subTo(this, this)
        }
        ,
        t.prototype.fromNumber = function (e, i, n) {
            if ("number" == typeof i)
                if (e < 2)
                    this.fromInt(1);
                else
                    for (this.fromNumber(e, n),
                         this.testBit(e - 1) || this.bitwiseTo(t.ONE.shiftLeft(e - 1), r, this),
                         this.isEven() && this.dAddOffset(1, 0); !this.isProbablePrime(i);)
                        this.dAddOffset(2, 0),
                        this.bitLength() > e && this.subTo(t.ONE.shiftLeft(e - 1), this);
            else {
                var o = []
                    , s = 7 & e;
                o.length = 1 + (e >> 3),
                    i.nextBytes(o),
                    s > 0 ? o[0] &= (1 << s) - 1 : o[0] = 0,
                    this.fromString(o, 256)
            }
        }
        ,
        t.prototype.bitwiseTo = function (t, e, i) {
            var r, n, o = Math.min(t.t, this.t);
            for (r = 0; r < o; ++r)
                i[r] = e(this[r], t[r]);
            if (t.t < this.t) {
                for (n = t.s & this.DM,
                         r = o; r < this.t; ++r)
                    i[r] = e(this[r], n);
                i.t = this.t
            } else {
                for (n = this.s & this.DM,
                         r = o; r < t.t; ++r)
                    i[r] = e(n, t[r]);
                i.t = t.t
            }
            i.s = e(this.s, t.s),
                i.clamp()
        }
        ,
        t.prototype.changeBit = function (e, i) {
            var r = t.ONE.shiftLeft(e);
            return this.bitwiseTo(r, i, r),
                r
        }
        ,
        t.prototype.addTo = function (t, e) {
            for (var i = 0, r = 0, n = Math.min(t.t, this.t); i < n;)
                r += this[i] + t[i],
                    e[i++] = r & this.DM,
                    r >>= this.DB;
            if (t.t < this.t) {
                for (r += t.s; i < this.t;)
                    r += this[i],
                        e[i++] = r & this.DM,
                        r >>= this.DB;
                r += this.s
            } else {
                for (r += this.s; i < t.t;)
                    r += t[i],
                        e[i++] = r & this.DM,
                        r >>= this.DB;
                r += t.s
            }
            e.s = r < 0 ? -1 : 0,
                r > 0 ? e[i++] = r : r < -1 && (e[i++] = this.DV + r),
                e.t = i,
                e.clamp()
        }
        ,
        t.prototype.dMultiply = function (t) {
            this[this.t] = this.am(0, t - 1, this, 0, 0, this.t),
                ++this.t,
                this.clamp()
        }
        ,
        t.prototype.dAddOffset = function (t, e) {
            if (0 != t) {
                for (; this.t <= e;)
                    this[this.t++] = 0;
                for (this[e] += t; this[e] >= this.DV;)
                    this[e] -= this.DV,
                    ++e >= this.t && (this[this.t++] = 0),
                        ++this[e]
            }
        }
        ,
        t.prototype.multiplyLowerTo = function (t, e, i) {
            var r = Math.min(this.t + t.t, e);
            for (i.s = 0,
                     i.t = r; r > 0;)
                i[--r] = 0;
            for (var n = i.t - this.t; r < n; ++r)
                i[r + this.t] = this.am(0, t[r], i, r, 0, this.t);
            for (n = Math.min(t.t, e); r < n; ++r)
                this.am(0, t[r], i, r, 0, e - r);
            i.clamp()
        }
        ,
        t.prototype.multiplyUpperTo = function (t, e, i) {
            --e;
            var r = i.t = this.t + t.t - e;
            for (i.s = 0; --r >= 0;)
                i[r] = 0;
            for (r = Math.max(e - this.t, 0); r < t.t; ++r)
                i[this.t + r - e] = this.am(e - r, t[r], i, 0, 0, this.t + r - e);
            i.clamp(),
                i.drShiftTo(1, i)
        }
        ,
        t.prototype.modInt = function (t) {
            if (t <= 0)
                return 0;
            var e = this.DV % t
                , i = this.s < 0 ? t - 1 : 0;
            if (this.t > 0)
                if (0 == e)
                    i = this[0] % t;
                else
                    for (var r = this.t - 1; r >= 0; --r)
                        i = (e * i + this[r]) % t;
            return i
        }
        ,
        t.prototype.millerRabin = function (e) {
            var i = this.subtract(t.ONE)
                , r = i.getLowestSetBit();
            if (r <= 0)
                return !1;
            var n = i.shiftRight(r);
            (e = e + 1 >> 1) > E.length && (e = E.length);
            for (var o = _(), s = 0; s < e; ++s) {
                o.fromInt(E[Math.floor(Math.random() * E.length)]);
                var a = o.modPow(n, this);
                if (0 != a.compareTo(t.ONE) && 0 != a.compareTo(i)) {
                    for (var h = 1; h++ < r && 0 != a.compareTo(i);)
                        if (0 == (a = a.modPowInt(2, this)).compareTo(t.ONE))
                            return !1;
                    if (0 != a.compareTo(i))
                        return !1
                }
            }
            return !0
        }
        ,
        t.prototype.square = function () {
            var t = _();
            return this.squareTo(t),
                t
        }
        ,
        t.prototype.gcda = function (t, e) {
            var i = this.s < 0 ? this.negate() : this.clone()
                , r = t.s < 0 ? t.negate() : t.clone();
            if (i.compareTo(r) < 0) {
                var n = i;
                i = r,
                    r = n
            }
            var o = i.getLowestSetBit()
                , s = r.getLowestSetBit();
            if (s < 0)
                e(i);
            else {
                o < s && (s = o),
                s > 0 && (i.rShiftTo(s, i),
                    r.rShiftTo(s, r));
                var a = function () {
                    (o = i.getLowestSetBit()) > 0 && i.rShiftTo(o, i),
                    (o = r.getLowestSetBit()) > 0 && r.rShiftTo(o, r),
                        i.compareTo(r) >= 0 ? (i.subTo(r, i),
                            i.rShiftTo(1, i)) : (r.subTo(i, r),
                            r.rShiftTo(1, r)),
                        i.signum() > 0 ? setTimeout(a, 0) : (s > 0 && r.lShiftTo(s, r),
                            setTimeout((function () {
                                    e(r)
                                }
                            ), 0))
                };
                setTimeout(a, 10)
            }
        }
        ,
        t.prototype.fromNumberAsync = function (e, i, n, o) {
            if ("number" == typeof i)
                if (e < 2)
                    this.fromInt(1);
                else {
                    this.fromNumber(e, n),
                    this.testBit(e - 1) || this.bitwiseTo(t.ONE.shiftLeft(e - 1), r, this),
                    this.isEven() && this.dAddOffset(1, 0);
                    var s = this
                        , a = function () {
                        s.dAddOffset(2, 0),
                        s.bitLength() > e && s.subTo(t.ONE.shiftLeft(e - 1), s),
                            s.isProbablePrime(i) ? setTimeout((function () {
                                    o()
                                }
                            ), 0) : setTimeout(a, 0)
                    };
                    setTimeout(a, 0)
                }
            else {
                var h = []
                    , u = 7 & e;
                h.length = 1 + (e >> 3),
                    i.nextBytes(h),
                    u > 0 ? h[0] &= (1 << u) - 1 : h[0] = 0,
                    this.fromString(h, 256)
            }
        }
        ,
        t
}()

function I(t, e) {
    return new k(t, e)
}

var Q = function () {
    function t() {
        this.n = null,
            this.e = 0,
            this.d = null,
            this.p = null,
            this.q = null,
            this.dmp1 = null,
            this.dmq1 = null,
            this.coeff = null
    }

    return t.prototype.doPublic = function (t) {
        return t.modPowInt(this.e, this.n)
    }
        ,
        t.prototype.doPrivate = function (t) {
            if (null == this.p || null == this.q)
                return t.modPow(this.d, this.n);
            for (var e = t.mod(this.p).modPow(this.dmp1, this.p), i = t.mod(this.q).modPow(this.dmq1, this.q); e.compareTo(i) < 0;)
                e = e.add(this.p);
            return e.subtract(i).multiply(this.coeff).mod(this.p).multiply(this.q).add(i)
        }
        ,
        t.prototype.setPublic = function (t, e) {
            null != t && null != e && t.length > 0 && e.length > 0 ? (this.n = I(t, 16),
                this.e = parseInt(e, 16)) : console.error("Invalid RSA public key")
        }
        ,
        t.prototype.encrypt = function (t) {
            var e = this.n.bitLength() + 7 >> 3
                , i = function (t, e) {
                if (e < t.length + 11)
                    return console.error("Message too long for RSA"),
                        null;
                for (var i = [], r = t.length - 1; r >= 0 && e > 0;) {
                    var n = t.charCodeAt(r--);
                    n < 128 ? i[--e] = n : n > 127 && n < 2048 ? (i[--e] = 63 & n | 128,
                        i[--e] = n >> 6 | 192) : (i[--e] = 63 & n | 128,
                        i[--e] = n >> 6 & 63 | 128,
                        i[--e] = n >> 12 | 224)
                }
                i[--e] = 0;
                for (var o = new Y, s = []; e > 2;) {
                    for (s[0] = 0; 0 == s[0];)
                        o.nextBytes(s);
                    i[--e] = s[0]
                }
                return i[--e] = 2,
                    i[--e] = 0,
                    new k(i)
            }(t, e);
            if (null == i)
                return null;
            var r = this.doPublic(i);
            if (null == r)
                return null;
            for (var n = r.toString(16), o = n.length, s = 0; s < 2 * e - o; s++)
                n = "0" + n;
            return n
        }
        ,
        t.prototype.setPrivate = function (t, e, i) {
            null != t && null != e && t.length > 0 && e.length > 0 ? (this.n = I(t, 16),
                this.e = parseInt(e, 16),
                this.d = I(i, 16)) : console.error("Invalid RSA private key")
        }
        ,
        t.prototype.setPrivateEx = function (t, e, i, r, n, o, s, a) {
            null != t && null != e && t.length > 0 && e.length > 0 ? (this.n = I(t, 16),
                this.e = parseInt(e, 16),
                this.d = I(i, 16),
                this.p = I(r, 16),
                this.q = I(n, 16),
                this.dmp1 = I(o, 16),
                this.dmq1 = I(s, 16),
                this.coeff = I(a, 16)) : console.error("Invalid RSA private key")
        }
        ,
        t.prototype.generate = function (t, e) {
            var i = new Y
                , r = t >> 1;
            this.e = parseInt(e, 16);
            for (var n = new k(e, 16); ;) {
                for (; this.p = new k(t - r, 1, i),
                       0 != this.p.subtract(k.ONE).gcd(n).compareTo(k.ONE) || !this.p.isProbablePrime(10);)
                    ;
                for (; this.q = new k(r, 1, i),
                       0 != this.q.subtract(k.ONE).gcd(n).compareTo(k.ONE) || !this.q.isProbablePrime(10);)
                    ;
                if (this.p.compareTo(this.q) <= 0) {
                    var o = this.p;
                    this.p = this.q,
                        this.q = o
                }
                var s = this.p.subtract(k.ONE)
                    , a = this.q.subtract(k.ONE)
                    , h = s.multiply(a);
                if (0 == h.gcd(n).compareTo(k.ONE)) {
                    this.n = this.p.multiply(this.q),
                        this.d = n.modInverse(h),
                        this.dmp1 = this.d.mod(s),
                        this.dmq1 = this.d.mod(a),
                        this.coeff = this.q.modInverse(this.p);
                    break
                }
            }
        }
        ,
        t.prototype.decrypt = function (t) {
            var e = I(t, 16)
                , i = this.doPrivate(e);
            return null == i ? null : function (t, e) {
                var i = t.toByteArray()
                    , r = 0;
                for (; r < i.length && 0 == i[r];)
                    ++r;
                if (i.length - r != e - 1 || 2 != i[r])
                    return null;
                ++r;
                for (; 0 != i[r];)
                    if (++r >= i.length)
                        return null;
                var n = "";
                for (; ++r < i.length;) {
                    var o = 255 & i[r];
                    o < 128 ? n += String.fromCharCode(o) : o > 191 && o < 224 ? (n += String.fromCharCode((31 & o) << 6 | 63 & i[r + 1]),
                        ++r) : (n += String.fromCharCode((15 & o) << 12 | (63 & i[r + 1]) << 6 | 63 & i[r + 2]),
                        r += 2)
                }
                return n
            }(i, this.n.bitLength() + 7 >> 3)
        }
        ,
        t.prototype.generateAsync = function (t, e, i) {
            var r = new Y
                , n = t >> 1;
            this.e = parseInt(e, 16);
            var o = new k(e, 16)
                , s = this
                , a = function () {
                var e = function () {
                    if (s.p.compareTo(s.q) <= 0) {
                        var t = s.p;
                        s.p = s.q,
                            s.q = t
                    }
                    var e = s.p.subtract(k.ONE)
                        , r = s.q.subtract(k.ONE)
                        , n = e.multiply(r);
                    0 == n.gcd(o).compareTo(k.ONE) ? (s.n = s.p.multiply(s.q),
                        s.d = o.modInverse(n),
                        s.dmp1 = s.d.mod(e),
                        s.dmq1 = s.d.mod(r),
                        s.coeff = s.q.modInverse(s.p),
                        setTimeout((function () {
                                i()
                            }
                        ), 0)) : setTimeout(a, 0)
                }
                    , h = function () {
                    s.q = _(),
                        s.q.fromNumberAsync(n, 1, r, (function () {
                                s.q.subtract(k.ONE).gcda(o, (function (t) {
                                        0 == t.compareTo(k.ONE) && s.q.isProbablePrime(10) ? setTimeout(e, 0) : setTimeout(h, 0)
                                    }
                                ))
                            }
                        ))
                }
                    , u = function () {
                    s.p = _(),
                        s.p.fromNumberAsync(t - n, 1, r, (function () {
                                s.p.subtract(k.ONE).gcda(o, (function (t) {
                                        0 == t.compareTo(k.ONE) && s.p.isProbablePrime(10) ? setTimeout(h, 0) : setTimeout(u, 0)
                                    }
                                ))
                            }
                        ))
                };
                setTimeout(u, 0)
            };
            setTimeout(a, 0)
        }
        ,
        t.prototype.sign = function (t, e, i) {
            var r = function (t, e) {
                if (e < t.length + 22)
                    return console.error("Message too long for RSA"),
                        null;
                for (var i = e - t.length - 6, r = "", n = 0; n < i; n += 2)
                    r += "ff";
                return I("0001" + r + "00" + t, 16)
            }((J[i] || "") + e(t).toString(), this.n.bitLength() / 4);
            if (null == r)
                return null;
            var n = this.doPrivate(r);
            if (null == n)
                return null;
            var o = n.toString(16);
            return 0 == (1 & o.length) ? o : "0" + o
        }
        ,
        t.prototype.verify = function (t, e, i) {
            var r = I(e, 16)
                , n = this.doPublic(r);
            return null == n ? null : function (t) {
                for (var e in J)
                    if (J.hasOwnProperty(e)) {
                        var i = J[e]
                            , r = i.length;
                        if (t.substr(0, r) == i)
                            return t.substr(r)
                    }
                return t
            }/*!
  Copyright (c) 2011, Yahoo! Inc. All rights reserved.
  Code licensed under the BSD License:
  http://developer.yahoo.com/yui/license.html
  version: 2.9.0
  */
                (n.toString(16).replace(/^1f+00/, "")) == i(t).toString()
        }
        ,
        t
}();

const rsa = new Q();
rsa.generate(1024, "010001");

// 获取公钥和私钥
const publicKey = rsa.n.toString(16); // 公钥模数
const privateKey = rsa.d.toString(16); // 私钥指数

console.log("公钥模数:", publicKey);
console.log("私钥指数:", privateKey);

// 使用公钥加密数据
const data = "Hello World";
const encryptedData = rsa.encrypt(data);
console.log("加密后的数据:", encryptedData);

// 使用私钥解密数据
const decryptedData = rsa.decrypt(encryptedData);
console.log("解密后的数据:", decryptedData);
/* 此内容为调用Q函数中的加密解密的结果 */