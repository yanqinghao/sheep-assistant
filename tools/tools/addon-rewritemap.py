import mitmproxy.http
from mitmproxy import ctx
import os
import json

class Counter:
    def __init__(self):
        self.num = 0
        self.maps = None

    def request(self, flow: mitmproxy.http.HTTPFlow):
        self.num = self.num + 1
        ctx.log.info("We've seen %d flows" % self.num)

    def response(self, flow):
        # 匹配指定的url
        if flow.request.url.startswith ( 'https://cat-match-static.easygame2021.com/maps' ):
            # 设置响应据
            rawData = json.loads(flow.response.content)
            rawData["blockTypeData"] = {}
            flow.response.set_text(json.dumps(rawData))


addons = [
    Counter()
]


