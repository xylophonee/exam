import requests
import re
import json
import time

class Score():
    
    def __init__(self,zkzh,id_num,password):
        self.zkzh = zkzh
        self.id_num = id_num
        self.password = password
        self.server = 'SCU43267Tdfa013d220d7955c54df031021df05b05c4af8f4d81c5'
        self.headers ={
            'Connection': 'keep-Alive',
            'Host': 'xxcx.hebeea.edu.cn',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; MI 6 MIUI/9.6.20)',
        }
        self.query_url = "http://xxcx.hebeea.edu.cn/hebeeaQuery/uee/cjcx"
        
    def get_score(self):
        
        data = {
            "uee_ksh": self.zkzh,
            "uee_zjhm": self.id_num,
            "uee_dlh": self.password,
        }
        
        try:
            response = requests.post(self.query_url, data='data='+json.dumps(data), headers=self.headers)
            text = response.text
            if 'html' in text:
                print('未开通')
                return 0
            else: 
                json_result = json.loads(text)
                if json_result['errorCode'] == '1':
                    print(json_result['errorMsg'])
                    return 0
                else:
                    self.analysis(text)
                    return 1      
        except:
            return 0

    def analysis(self,text):
        #json_score = json.loads(text)
        try:
            zf= re.compile("\"zf\":\"(.*?)\"").findall(text)[0]
            yw= re.compile("\"km1\":\"(.*?)\"").findall(text)[0]
            sx= re.compile("\"km2\":\"(.*?)\"").findall(text)[0]
            yy= re.compile("\"km3\":\"(.*?)\"").findall(text)[0]
            zh= re.compile("\"km4\":\"(.*?)\"").findall(text)[0]
            final = "总分:"+str(zf)+" 语文:"+str(yw)+" 数学:"+str(sx)+" 英语:"+str(yy)+" 综合:"+str(zh)
            self.send(str(zf),final)
            print(final)
        except:
            self.send('解析错误',text)
            print(text)
        
            
    def send(self,all_,text_):
        data = {
            'text':all_,
            'desp':text_
        }
        requests.post('https://sc.ftqq.com/'+self.server+'.send',data=data)
         
if __name__ == '__main__':
    score = Score("20130434151513","130434200211280024","19690718")
    while True:
        if score.get_score() == 1:
            exit()
        time.sleep(10)
    
    #score = Score("19130434150704","130434200111066063","740307")
    