# coding=utf-8

import subprocess
import os
import suanpan
from suanpan.app import app
from suanpan.log import logger
from suanpan.app.arguments import String
from suanpan import g
import shutil
import getpass



@app.afterInit
def init(context):
    args = context.args
    if args.param1 == "true":
        logger.info("-----------开始低版本微信-----------")
        cmd = "Start-Process ./WeChatSetup3.6.0.exe -Wait"
        subprocess.run(["powershell", "-Command", cmd])
        logger.info("-----------低版本微信安装完毕-----------")
    logger.info("-----------删除微信APP缓存文件-----------")
    shutil.rmtree(f"C:\\Users\\{getpass.getuser()}\\AppData\\Roaming\\Tencent\\WeChat\\XPlugin\\Plugins\\WMPFRuntime", ignore_errors=True)
    shutil.rmtree(f"C:\\Users\\{getpass.getuser()}\\AppData\\Roaming\\Tencent\\WeChat\\XPlugin\\Plugins\\XWeb", ignore_errors=True)
    shutil.rmtree(f"C:\\Users\\{getpass.getuser()}\\AppData\\Roaming\\Tencent\\WeChat\\wmpf_app", ignore_errors=True)
    if args.param2 == "true":
        logger.info("-----------开始安装证书-----------")
        cmd = "Start-Process ./mitmproxy-ca-cert.p12 -Wait"
        subprocess.run(["powershell", "-Command", cmd])
        logger.info("-----------证书安装完毕-----------")
        cmd = f"certutil.exe -addstore root C:\\Users\\{getpass.getuser()}\\.mitmproxy\\mitmproxy-ca-cert.cer"
        subprocess.run(["powershell", "-Command", cmd])
    logger.info("-----------运行mitmproxy进行抓包-----------")
    cmd = "./mitmweb.exe --ssl-insecure -s ./addon.py"
    subprocess.Popen(["powershell", "-Command", cmd])
    logger.info("-----------请手动开启系统代理，127.0.0.1：8080-----------")
    logger.info("-----------请手动开启微信，并在未登录时右上角设置中设置代理为127.0.0.1：8080-----------")

@app.input(String(key="inputData1"))
@app.param(String(key="param1"))
@app.param(String(key="param2"))
@app.output(String(key="outputData1"))
def grabToken(context):
    args = context.args
    if g.token is None:
        if os.path.exists("token.txt"):
            logger.info("-----------token获取成功-----------")
            with open("token.txt", "r") as f:
                g.token = f.readlines()[0]
    if g.token:
        return g.token


if __name__ == "__main__":
    suanpan.run(app)