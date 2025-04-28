Java.perform(function () {
    // 替换为目标 App 中实际使用的 RC4 工具类名
    var targetClass = "com.example.app.RC4Utils";

    // Hook 加密方法（假设方法名为 encrypt，参数为密钥和数据）
    var RC4Utils = Java.use(targetClass);

    RC4Utils.encrypt.overload('[B', '[B').implementation = function (keyBytes, dataBytes) {
        // 打印 RC4 密钥（字节数组转十六进制字符串）
        var keyHex = Array.from(keyBytes).map(b => ('0' + (b & 0xFF).toString(16)).slice(-2)).join('');
        console.log("\n[+] RC4 Key Found:");
        console.log("   Hex: " + keyHex);
        console.log("   Raw: " + JSON.stringify(keyBytes));

        // 继续执行原方法
        return this.encrypt(keyBytes, dataBytes);
    };
});