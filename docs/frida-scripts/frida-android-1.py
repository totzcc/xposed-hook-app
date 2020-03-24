import frida, sys


def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


def main():
    js_code = """
    var awemeListApi;
    Java.perform(function () {
      Java.use('com.ss.android.ugc.aweme.profile.jedi.aweme.AwemeListApi$a').a.implementation = function () {
        send('awemeListApi has been call')
        awemeListApi = this.a()
        setInterval(function() {
            Java.perform(function () {
                send('call getPublishAweme')
                res = awemeListApi.getPublishAweme(10, '', 'MS4wLjABAAAA0MQ8KsdiiSN8lF_QYFxxLKPOisXlotf33u-Hys1hI-k', 1570883755000);
                send(res)
            })
        }, 1000)
        return awemeListApi;
      };
    });
    """

    """
    js_code = 
    Java.perform(function () {
      Java.use('com.ss.android.ugc.aweme.main.MainActivity').performHomeTabClick.implementation = function (v1) {
        send('performHomeTabClick 2')
        // this.performHomeTabClick()
      };
      Java.use('com.ss.android.ugc.aweme.main.page.a').a.implementation = function(v1) {
        send('click')
        this.a(v1)
      }
    });
    """
    process = frida.get_usb_device().attach('com.ss.android.ugc.aweme')
    script = process.create_script(js_code)
    script.on('message', on_message)
    print('[*] Running CTF')
    script.load()
    sys.stdin.read()


if __name__ == '__main__':
    main()
