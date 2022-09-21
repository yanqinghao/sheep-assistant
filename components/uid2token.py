# coding=utf-8

import sys
import random
import time
import base64
import requests
import suanpan
from suanpan.app import app
from suanpan.log import logger
from suanpan.app.arguments import String
from suanpan import g


g.getUserInfoApi = "https://cat-match.easygame2021.com/sheep/v1/game/user_info?uid=%s&t=%s"

# 用于请求oppenid以及token的t，感谢@lyzcren 老哥 ，简单加密处理
g.sacrificeTEncryption = "ZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SmxlSEFpT2pFMk9UUTFNelF4TXpjc0ltNWlaaUk2TVRZMk16UXpNVGt6Tnl3aWFXRjBJam94TmpZek5ETXdNVE0zTENKcWRHa2lPaUpEVFRwallYUmZiV0YwWTJnNmJIUXhNak0wTlRZaUxDSnZjR1Z1WDJsa0lqb2lJaXdpZFdsa0lqb3hNelU1TmprMU1pd2laR1ZpZFdjaU9pSWlMQ0pzWVc1bklqb2lJbjAucnhOcDY5Q3lfVW1ZWnQxdXpzR2tJS0ZCT1plaFczdlh6bzNrbHRKdHliWQ=="
g.sacrificeT = base64.b64decode(g.sacrificeTEncryption.encode("utf-8")).decode("utf-8")

# 用户登录接口，POST请求 需要wx_open_id
g.userLoginApi = "https://cat-match.easygame2021.com/sheep/v1/user/login_oppo"

g.requestHeader = {
    "Host": "cat-match.easygame2021.com",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.27(0x18001b36) NetType/WIFI Language/zh_CN",
    "Referer": "https://servicewechat.com/wx141bfb9b73c970a9/17/page-frame.html",
    "Accept-Encoding": "gzip,compress,br,deflate",
    "Connection": "close"
}

g.userToken = None

def waitForRandomInterval(is_show):
    interval_time = random.randint(2, 6)
    if is_show:
        logger.info(f"等待随机时间间隔，防止游戏服务器接口限流导致失败 : {interval_time} s")
    time.sleep(interval_time)


@app.input(String(key="inputData1"))
@app.param(String(key="uid"))
@app.output(String(key="outputData1"))
def uid2token(context):
    args = context.args
    if g.userToken is None:
        uuid = None
        tryGetUserInfoApiCount = 1
        tryUserLoginApi = 1
        maxTryCount = 5
        while True:
            logger.info(f"开始尝试第{tryGetUserInfoApiCount}次换取用户uuid")
            waitForRandomInterval(False)
            try:
                getRes = requests.get(g.getUserInfoApi % (args.uid, g.sacrificeT), headers=g.requestHeader, timeout=15,
                                    verify=False)
                
                if getRes.status_code == 200:
                    resultJson = getRes.json()
                    uuid = resultJson["data"]["wx_open_id"]
                    avatar = resultJson["data"]["avatar"]
                else:
                    logger.info("请求失败")
                    logger.info("请求状态：{}".format(getRes.status_code))
                    sys.exit(-1)
                loginBody = {
                    "uid": str(uuid),
                    "avatar": "1",
                    "nick_name": "1",
                    "sex": 1
                    
                }
            except Exception:
                tryGetUserInfoApiCount += 1
            finally:
                # 最大尝试次数，可能是个瞎搞的uid不可能一直访问
                if tryGetUserInfoApiCount > maxTryCount:
                    logger.info(f"超过target_uid模式最大尝试次数，本次程序运行结束，请稍后重试或者检查uid是否正确！")
                    raise Exception("超过target_uid模式最大尝试次数")
            if uuid:
                logger.info(f"第{tryGetUserInfoApiCount}次尝试换取用户uuid成功")
                break

        while True:
            logger.info(f"开始尝试第{tryUserLoginApi}次换取用户header_t")
            waitForRandomInterval(False)
            try:
                loginRes = requests.post(g.userLoginApi, headers=g.requestHeader, json=loginBody, timeout=15, verify=False)
                g.userToken = loginRes.json()["data"]["token"]
                logger.info("获取token成功:", g.userToken)
            except Exception as e:
                tryUserLoginApi += 1
                logger.info(e)
            finally:
                if tryUserLoginApi > maxTryCount:
                    logger.info(f"超过target_uid模式最大尝试次数，本次程序运行结束，请稍后重试或者检查uid是否正确！")
                    raise Exception("超过target_uid模式最大尝试次数")
            if g.userToken:
                logger.info(f"第{tryUserLoginApi}次尝试换取用户header_t成功")
                break
    return g.userToken


if __name__ == "__main__":
    suanpan.run(app)
