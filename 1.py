import os
import re
import requests
from tqdm import tqdm
import time


class SentinelDownload:
    def __init__(self, UserName, Password, SearchUrl, Proxies):
        self.userName = UserName
        self.password = Password
        self.SearchUrl = self.CreatURL(SearchUrl)
        self.proxies = Proxies
        self.tokenStr = self.GetAccessToken()
        self.SearchResList = self.Search()

    def CreatURL(self, urlStr: str) -> str:
        return urlStr.strip()

    def GetAccessToken(self) -> str:
        """获取token,用于下载数据"""
        data = {
            "client_id": "cdse-public",
            "username": self.userName,
            "password": self.password,
            "grant_type": "password",
        }
        try:
            r = requests.post(
                "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
                data=data, proxies=self.proxies
            )
            r.raise_for_status()
            print("token获取成功！")
            return r.json()["access_token"]
        except Exception as e:
            print(f"获取token时捕获到异常: {e}")
            print("等待15秒后重新获取token...")
            time.sleep(15)
            return self.GetAccessToken()

    def Search(self) -> list:
        """检索数据"""
        SearchResult = []
        res = requests.get(self.SearchUrl, proxies=self.proxies)
        jsonInfo = res.json()
        res.close()
        n = jsonInfo["@odata.count"]
        if n == 0:
            print("没有检索到数据")
        else:
            print(f"共检索到{n}条数据，开始进行数据信息的采集")
            r = 900
            for k in range(0, n, r):
                print(f"正在进行第{k}-{k + r}条数据信息的采集")
                top = re.findall(r"(top=\d+)", self.SearchUrl)[0]
                skip = re.findall(r"(skip=\d+)", self.SearchUrl)[0]
                url = self.SearchUrl.replace(top, f"top={900}").replace(skip, f"skip={k}")
                jsonInfo = requests.get(url, proxies=self.proxies).json()
                SearchResult += [{"Id": i["Id"], "Name": i["Name"]} for i in jsonInfo['value']]
        print(f"数据采集完成，共采集到{len(SearchResult)}条数据信息")
        return SearchResult

    def DownloadWithResume(self, productID, savePath):
        """支持断点续传的下载函数，带进度条显示"""
        url = f"http://zipper.dataspace.copernicus.eu/odata/v1/Products({productID})/$value"
        headers = {"Authorization": f"Bearer {self.tokenStr}"}
        tempPath = f"{savePath}.part"
        downloaded_size = 0
        if os.path.exists(tempPath):
            downloaded_size = os.path.getsize(tempPath)

        headers["Range"] = f"bytes={downloaded_size}-"
        try:
            response = requests.get(url, headers=headers, stream=True, proxies=self.proxies, timeout=30)
            response.raise_for_status()

            if response.status_code == 206:
                total_size = int(response.headers["Content-Range"].split("/")[-1])
            elif response.status_code == 200:
                total_size = int(response.headers.get("Content-Length", 0))
                downloaded_size = 0
            else:
                print(f"无法处理响应状态码 {response.status_code}，跳过下载")
                return

            print(f"开始下载 {savePath}, 文件大小: {total_size / 1024 / 1024:.2f} MB")

            with open(tempPath, "ab") as f:
                with tqdm(total=total_size, initial=downloaded_size, unit="B", unit_scale=True, desc=savePath) as pbar:
                    for chunk in response.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))

            os.rename(tempPath, savePath)
            print(f"{savePath} 下载完成！")

        except requests.exceptions.RequestException as e:
            print(f"下载失败，异常: {e}. 文件: {savePath}")
            if os.path.exists(tempPath):
                os.remove(tempPath)

    def SingleDownload(self, saveFolder):
        """单线程下载数据，带总任务进度条"""
        print(f"开始进行单线程数据的下载...")
        if not os.path.exists(f"{saveFolder}/Finish"):
            os.makedirs(f"{saveFolder}/Finish")

        total_files = len(self.SearchResList)
        with tqdm(total=total_files, unit="file", desc="总任务进度") as task_pbar:
            for item in self.SearchResList:
                ID = item['Id']
                Name = item['Name']
                savePath = f"{saveFolder}/Finish/{Name}.zip"
                self.DownloadWithResume(productID=ID, savePath=savePath)
                task_pbar.update(1)


if __name__ == '__main__':
    IPPort = "替换1:替换2"  # 设置代理
    Folder = r"C:/Users/zzw/Desktop/sentineldata"  # 保存路径
    userName = "！"  # todo 用户名
    password = "!"  # todo 密码

    proxies = {
        "http": IPPort,
        "https": IPPort
    }

    with open("SearchURL.txt", mode="r") as f:
        urlString = f.read()

    SL = SentinelDownload(UserName=userName, Password=password, Proxies=proxies, SearchUrl=urlString)
    SL.SingleDownload(saveFolder=Folder)
