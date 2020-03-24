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
        
        // NetworkUtils
        /** Java.use('com.ss.android.common.util.NetworkUtils').executeGet.overload('int', 'int', 'java.lang.String', 'boolean', 'boolean', 'java.util.List', 'com.ss.android.http.legacy.message.HeaderGroup', 'boolean').implementation = function (a1,a2,a3,a4,a5,a6,a7,a8) {
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
            return this.executeGet(a1,a2,a3,a4,a5,a6,a7,a8)
        };*/
        /**
        Java.use('com.ss.android.socialbase.basenetwork.HttpService').with.implementation = function(a1) {
            send(a1)
            return this.with(a1)
        }
        */
        
        Java.use('com.ss.android.socialbase.basenetwork.HttpRequest').doGet.implementation = function() {
            var res = this.doGet()
            send('doGet ' + this.getUrl())
            return res
        }
    });
    """

    process = frida.get_usb_device().attach('com.sup.android.slite')
    script = process.create_script(js_code)
    script.on('message', on_message)
    print('[*] Running CTF')
    script.load()
    sys.stdin.read()


if __name__ == '__main__':
    main()
