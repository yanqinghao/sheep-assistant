# coding=utf-8

import random
import time
import requests
import suanpan
from suanpan.app import app
from suanpan.log import logger
from suanpan.app.arguments import String, Int
from suanpan import g

# 完成话题接口
g.finishTopicApi = "https://cat-match.easygame2021.com/sheep/v1/game/topic_game_over?rank_score=1&rank_state=1&rank_time=%s&rank_role=2&skin=%s&t=%s"

g.requestHeader = {
    "Host": "cat-match.easygame2021.com",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.27(0x18001b36) NetType/WIFI Language/zh_CN",
    "Referer": "https://servicewechat.com/wx141bfb9b73c970a9/17/page-frame.html",
    "Accept-Encoding": "gzip,compress,br,deflate",
    "Connection": "close"
}

g.successNum = 0

def waitForRandomInterval(is_show):
    interval_time = random.randint(2, 6)
    if is_show:
        logger.info(f"等待随机时间间隔，防止游戏服务器接口限流导致失败 : {interval_time} s")
    time.sleep(interval_time)


@app.input(String(key="inputData1"))
@app.param(Int(key="costTime"))
@app.param(Int(key="skin"))
@app.output(String(key="outputData1"))
def finishGameTopic(context):
    args = context.args
    s = requests.session()
    s.keep_alive = False
    if args.costTime == -1:
        costTime = random.randint(1, 3600)
    else:
        costTime = args.costTime
    res = requests.get(g.finishTopicApi % (costTime, args.skin, args.inputData1), headers=g.requestHeader, timeout=10, verify=False)
    if res.json()["err_code"] == 0:
        g.successNum += 1
        logger.info(f"恭喜你! 第{g.successNum}次闯关话题状态成功!")
        return f"恭喜你! 第{g.successNum}次闯关话题状态成功!"
    else:
        logger.info(res.json())
        logger.info("请检查t的值是否获取正确!")


if __name__ == "__main__":
    suanpan.run(app)