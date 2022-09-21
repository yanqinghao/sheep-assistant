import mitmproxy.http
from mitmproxy import ctx
import os


class Counter:
    def __init__(self):
        self.num = 0

    def request(self, flow: mitmproxy.http.HTTPFlow):
        self.num = self.num + 1
        ctx.log.info("We've seen %d flows" % self.num)

    def response(self, flow):
        # 匹配指定的url
        if flow.request.url.startswith( 'https://cat-match.easygame2021.com' ):
            ctx.log.info(flow.request.headers)
            if os.path.exists("token.txt"):
                ctx.log.info("token已存在")
            else:
                if flow.request.headers["t"]:
                    with open("token.txt", "w") as f:
                        f.writelines(flow.request.headers["t"])


addons = [
    Counter()
]


