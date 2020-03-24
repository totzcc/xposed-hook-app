import frida, sys


def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


def main():
    js_code = """
    Java.perform(function () {
      Java.use('cn.fxit.campus.box.android.cabinet.util.api.ApiUtil').getCampusApi.implementation = function (v1) {
        send('getCampusApi')
        var api = this.getCampusApi(v1)
        send(api.getClass().toString())
        return api
      };
    });
    """

    process = frida.get_usb_device().attach('cn.fxit.campus.box.android.cabinet')
    script = process.create_script(js_code)
    script.on('message', on_message)
    print('[*] Running CTF')
    script.load()
    sys.stdin.read()


if __name__ == '__main__':
    main()
