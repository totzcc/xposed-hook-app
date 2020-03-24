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
    // SsOkHttp3Client
    Java.perform(function () {
      Java.use('com.bytedance.frameworks.baselib.network.http.ok3.impl.SsOkHttp3Client').createExtraInfo.implementation = function (a1) {
        send('SsOkHttp3Client')
        var res = this.createExtraInfo(a1)
        send(res.toString())
        return res
      };
    });
    

     // CookieManager
    Java.perform(function () {
      Java.use('android.webkit.CookieManager').getInstance.implementation = function () {
        send('CookieManager getInstance')
        var res = this.getInstance()
        send(res.getClass().toString())
        return res
      };
    });
    
    
    // CookieManagerAdapter
    Java.perform(function () {
      Java.use('android.webkit.CookieManager').getCookie.overload('java.lang.String').implementation = function (a1) {
        send('CookieManager getCookie ')
        var res = this.getCookie(a1)
        return res
      };
    });
    
    
    // 拦截Header
    Java.perform(function () {
      Java.use('com.bytedance.frameworks.baselib.network.http.NetworkParams').tryAddSecurityFactor.overload('java.lang.String', 'java.util.Map').implementation = function (a1,a2) {
        showStacks()
        send('tryAddSecurityFactor')
        var res = this.tryAddSecurityFactor(a1,a2)
        showVarString(res)
        return res
      };
    });
    
    Java.perform(function () {
      Java.use('com.bytedance.frameworks.baselib.network.http.ok3.impl.OkHttp3CookieInterceptor').intercept.implementation = function (a1) {
        send('intercept')
        showVarString(a1.request().headers())
        return this.intercept(a1)
      };
    });
    
    
    Java.perform(function () {
        Java.use('com.bytedance.frameworks.baselib.network.http.ok3.impl.OkHttp3CookieInterceptor').tryEncryptHeader.overload('java.net.URI', 'java.lang.String', 'java.lang.String', 'okhttp3.Request$Builder').implementation = function (a1,a2,a3,a4) {
            send('tryEncryptHeader')
            send(a2)
            send(a3)
            return this.tryEncryptHeader(a1,a2,a3,a4)
        }
    }
    */
    
    
    Java.perform(function () {
        Java.use('com.bytedance.frameworks.baselib.network.http.ok3.impl.OkHttp3CookieInterceptor').tryEncryptHeader.overload('java.net.URI', 'java.lang.String', 'java.lang.String', 'okhttp3.Request$Builder').implementation = function (a1,a2,a3,a4) {
            send('tryEncryptHeader')
            /* 
            if (a2 === 'Cookie' || a2 === 'x-tt-token') {
                a3 = ''
            }
            */
            send(a2)
            send(a3)
            return this.tryEncryptHeader(a1,a2,a3,a4)
        }
    })
    
    Java.perform(function () {
        Java.use('com.ss.android.ugc.core.network.g.e').ResponseInterceptor__intercept$___twin___.implementation = function (a1,a2) {
            send('block ResponseInterceptor__intercept$___twin___')
            send(a2.code())
            // return this.ResponseInterceptor__intercept$___twin___(a1,a2)
        }
    })
    """

    process = frida.get_usb_device().attach('com.ss.android.ugc.live')
    script = process.create_script(js_code)
    script.on('message', on_message)
    print('[*] Running CTF')
    script.load()
    sys.stdin.read()


if __name__ == '__main__':
    main()
