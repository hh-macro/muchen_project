Java.perform(function () {
    let NativeHelper = Java.use("com.zuoyebang.baseutil.NativeHelper");
    NativeHelper["nativeGetKey"].implementation = function (str) {
        // console.log(`NativeHelper.nativeGetKey is called: str=${str}`);
        let result = this["nativeGetKey"](str);
        console.log(`NativeHelper.nativeGetKey 此次获取的rc4秘钥为: ${result}`);
        // send(result);
        return result;
    };
});