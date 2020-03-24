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
        Java.use('com.bytedance.frameworks.baselib.network.http.ok3.impl.OkHttp3Builder').build.implementation = function () {
            // showStacks()
            return this.build()            
        }
        /* Java.use('com.bytedance.frameworks.baselib.network.http.ok3.impl.SsOkHttp3Client').newSsCall.implementation = function (a1) {
            showStacks()
            send('newSsCall')
            showVarString(a1)
            
            var res = this.newSsCall(a1)
            return res            
        }
         */
        
        /* Java.use('com.bytedance.ttnet.retrofit.SsRetrofitClient').newSsCall.implementation = function (a1) {
            showStacks()
            send('newSsCall 2')
            showVarString(a1)
            var res = this.newSsCall(a1)
            return res            
        }*/
        
        /*
        Java.use('com.bytedance.frameworks.baselib.network.http.retrofit.SsHttpExecutor').execute.implementation = function (a1) {
            send('execute')
            showStacks()
            var res = this.execute(a1)
            return res            
        }
        */
        
        /*
        Java.use('com.bytedance.retrofit2.ServiceMethod').toRequest.implementation = function (a1,a2) {
            send('toRequest')
            showStacks()
            var res = this.toRequest(a1, a2)
            showVarString(res)
            return res            
        }
        */
        
        Java.use('com.ss.android.ugc.live.search.v2.repository.SearchResultRepository').getFeedDataKey.implementation = function () {
            send('SearchResultRepository.getFeedDataKey')
            showStacks()
            var res = this.getFeedDataKey()
            showVarString(res)
            return res            
        }
    })
    """
   # com.bytedance.retrofit2.client.Request
    process = frida.get_usb_device().attach('com.ss.android.ugc.live')
    script = process.create_script(js_code)
    script.on('message', on_message)
    print('[*] Running CTF')
    script.load()
    sys.stdin.read()


if __name__ == '__main__':
    main()
