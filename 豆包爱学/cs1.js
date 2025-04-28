function onLoad(name, callback) {
    const android_dlopen_ext = Module.findExportByName(null, "android_dlopen_ext");
    if (android_dlopen_ext != null) {
        Interceptor.attach(android_dlopen_ext, {
            onEnter: function (args) {
                console.log("dlopen called: " + args[0].readCString());
                if (args[0].readCString().indexOf(name) !== -1) {
                    this.hook = true;
                }
            },
            onLeave: function (retval) {
                if (this.hook) {
                    console.log("dlopen finished: " + retval);
                    callback();
                }
            }
        });
    }
}

function main() {
    Java.perform(function () {
        const soName = 'libsscronet.so';
        onLoad(soName, () => {
            console.log("libsscronet.so loaded, performing patch...");
            let libsscronet = Module.getBaseAddress(soName);
            if (!libsscronet) {
                console.error("libsscronet.so not loaded yet!");
                return;
            }
            let verifyCert = libsscronet.add(0x3700F0);
            patch(verifyCert);
            console.log("Patch applied at " + verifyCert);
        });

        // 绕过常见的反调试检测
        try {
            var ActivityThread = Java.use('android.app.ActivityThread');
            ActivityThread.isInTestMode.implementation = function () {
                return false;
            };
            ActivityThread.isDebuggerAttached.implementation = function () {
                return false;
            };

            var Debug = Java.use('android.os.Debug');
            Debug.isDebuggerConnected.implementation = function () {
                return false;
            };
        } catch (e) {
            console.error("Error: " + e.message);
        }

        // 绕过 TracerPid 检测
        try {
            var fopen = new NativeFunction(Module.findExportByName("libc.so", "fopen"), "pointer", ["pointer", "pointer"]);
            var fgets = new NativeFunction(Module.findExportByName("libc.so", "fgets"), "pointer", ["pointer", "int", "pointer"]);
            var fclose = new NativeFunction(Module.findExportByName("libc.so", "fclose"), "int", ["pointer"]);

            Interceptor.attach(Module.findExportByName("libc.so", "fgets"), {
                onEnter: function (args) {
                    var buffer = args[0];
                    var size = args[1];
                    var stream = args[2];
                    var result = fgets(buffer, size, stream);
                    var content = Memory.readUtf8String(buffer);
                    if (content.indexOf("TracerPid:") !== -1) {
                        Memory.writeUtf8String(buffer, "TracerPid:\t0\n");
                    }
                    return result;
                }
            });
        } catch (e) {
            console.error("Error: " + e.message);
        }
    });
}

setImmediate(main);