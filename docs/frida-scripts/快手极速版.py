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
    function showVarString(varAddr) {
        Java.perform(function () {
            send(Java.use('com.alibaba.fastjson.JSONObject').toJSONString(varAddr));
        })
    }
    
    /*
    Java.perform(function () {
        Java.use('com.yxcorp.gifshow.HomeActivity').onBackPressed.implementation = function () {
            send('onBackPress')
        }
    })
    Java.perform(function () {
        Java.use('retrofit2.l').a.overload('java.lang.Class').implementation = function (a1) {
            send('retrofit create')
            return this.a(a1)
        }
    })
    */
    // http://api.mock-host.com/rest/n/feed/profile2
    Java.perform(function () {
        Java.use('okhttp3.Request$a').b.overload().implementation = function () {
            send('okhttp3.Request$a build')
            var request = this.b()
            send(request.url().toString())
            return request
        }
    })
    """

    process = frida.get_usb_device().attach('com.kuaishou.nebula')
    script = process.create_script(js_code)
    script.on('message', on_message)
    print('[*] Running CTF')
    script.load()
    sys.stdin.read()


if __name__ == '__main__':
    main()
