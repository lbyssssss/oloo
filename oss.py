import re,requests,os

def downloadpng(pac):
    url1 = url + pac
    resp1 = requests.get(url=url1,headers=headers)
    page_content1 = resp1.content
    with open(it.group('content'),"wb") as fp:
        fp.write(page_content1)
    # print(resp1.text)
    print("下载完成了"+it.group("content"))

def downloadzip(pac):
    url1 = url + pac
    resp1 = requests.get(url=url1, headers=headers)
    page_content1 = resp1.content
    with open(it.group('content'), "wb") as fp:
        fp.write(page_content1)
    # print(resp1.text)
    print("下载完成了" + it.group("content"))

url = input("请输入你想下载的url:")
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
}
obj = re.compile("<Contents>.*?<Key>(?P<content>.*?)</Key>")
resp = requests.get(url=url,headers=headers)
page_content = resp.text
result = obj.finditer(page_content)
for it in result:
    suffix = it.group("content").split(".")
    if suffix[-1] == "png" or suffix[-1] == "jpeg" or suffix[-1] == "jpg":
        downloadzip(pac=it.group("content"))
    elif suffix[-1] == "zip":
        downloadpng(pac=it.group("content"))
    # url1 = url + it.group("content")
    # resp1 = requests.get(url=url1,headers=headers)
    # page_content1 = resp1.content
    # with open(it.group('content'),"wb") as fp:
    #     fp.write(page_content1)
    # # print(resp1.text)
    # print("下载完成了"+it.group("content"))




