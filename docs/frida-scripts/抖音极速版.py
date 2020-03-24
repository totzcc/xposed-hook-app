import frida, sys


def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


def main():
    js_code = """
    function showStacks() {
        Java.perform(function () {
            send(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
        });
    }

    Java.perform(function () {
        /*Java.use('com.ss.android.ugc.aweme.profile.e.b').a.overload('boolean', 'java.lang.String', 'int', 'long', 'int').implementation = function (a1, a2, a3, a4, a5) {
            send(a1)
            send(a2)
            send(a3)
            send(a4)
            send(a5)
            showStacks()
            return this.a(a1, a2, a3, a4, a5)
        };*/
        
        /* Java.use('com.ss.android.ugc.aweme.app.b.a').a.overload('int', 'java.lang.String', 'java.lang.Class', 'java.lang.String', 'com.ss.android.c.a.b.f').implementation = function (a1, a2, a3, a4, a5) {
            // a3 = null
            // a5 = null
            send(a1)
            send(a2)
            send(a3)
            send(a4)
            send(a5)
            showStacks()
            return this.a(a1, a2, a3, a4, a5)
        };*/
        
        // ProfileManager.getUser(userId)
        /* Java.use('com.ss.android.ugc.aweme.profile.b.e').a.implementation = function (a1) {
            send(a1)
            showStacks()
            return this.a(a1)
        };*/
        
        
       /* Java.use('com.ss.android.ugc.aweme.profile.b.e').a.overload('android.os.Handler', 'java.lang.String').implementation = function (a1, a2) {
            send(a1)
            send(a2)
            showStacks()
            return this.a(a1, a2)
        };*/
        
        /*
        Java.use('com.ss.android.ugc.aweme.profile.b.d').a.implementation = function (a1) {
            send(a1)
            showStacks()
            return this.a(a1)
        };
        */
        
        // NetworkUtils
        /* Java.use('com.ss.android.common.util.NetworkUtils').executeGetRetry.implementation = function (a1,a2,a3,a4,a5,a6,a7,a8,a9) {
            // showStacks()
            send('----1----')
            send(a1)
            send(a2)
            send(a3)
            send(a4)
            send(a5)
            send('----6----')
            send(a6)
            send(a7)
            send(a8)
            send(a9)
            return this.executeGetRetry(a1,a2,a3,a4,a5,a6,a7,a8,a9)
        }; */
        
        // NetworkParams
        Java.use('com.bytedance.frameworks.baselib.network.http.e').a.overload('java.lang.String', 'java.util.Map').implementation = function (a1,a2) {
            // showStacks()
            send(a1)
            send(JSON.stringify(a2))
            return this.a(a1,a2)
        };
    });
    """

    process = frida.get_usb_device().attach('com.ss.android.ugc.aweme.lite')
    script = process.create_script(js_code)
    script.on('message', on_message)
    print('[*] Running CTF')
    script.load()
    sys.stdin.read()


if __name__ == '__main__':
    main()
