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
    
    Java.perform(function () {
        Java.use('com.xingin.skynet.b.d').a.overload().implementation = function () {
            send('com.xingin.skynet.b.d#a')
            return this.a()
        }
    })
    """

    process = frida.get_usb_device().attach('com.xingin.xhs')
    script = process.create_script(js_code)
    script.on('message', on_message)
    print('[*] Running CTF')
    script.load()
    sys.stdin.read()


if __name__ == '__main__':
    main()
