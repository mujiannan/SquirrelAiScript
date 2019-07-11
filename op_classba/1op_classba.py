import requests
import sys
class ClassbaOP:
    '乂学题库登录'
    Session=requests.Session()
    LoginSuccess=False
    Token=''

    #标记是否需要查视频
    NeedToCheckVideo=True

    ##声明异常记录
    __itemsNotExist=[]
    __itemsWithoutVideo=[]
    __otherExceptions=[]

    def Login(self):
        '登陆'
        ##输入用户名及密码
        import getpass
        print('用户名:')
        userName=input()
        password=getpass.getpass('密码')

        loginUrl="http://op.classba.cn/api/login"
        loginPayLoad={"user_name":userName,"password":password}
        response=self.Session.post(loginUrl,params=loginPayLoad)
        try:
            jsonResponse=response.json()
            message=jsonResponse["message"]
            print("登陆http://op.classba.cn/api/login，结果："+jsonResponse["message"])
            if message=="登陆成功":
                self.LoginSuccess=True
                self.Token=jsonResponse["token"]
                print("此次登陆Token:"+self.Token)
            else:
                self.LoginSuccess=False
        except:
            print("错误")
            print("登陆错误："+response.text)
    def CheckQuestion(self):
        '检查题目'
        print("请粘贴题目编号(运行完毕后直接回车可以查看问题汇总）:")
        ##公用URL
        searchQuestionUrl="http://op.classba.cn/api/v3/searchQuestion/2"
        previewUrl="http://op.classba.cn/api/v3/getQuestionByUuid/2"
        while 1==1:
            print('\n')
            questionNum=input()
            print('\n')
            try:
                if questionNum=="End" or questionNum=="":
                    break
                else:
                    print("【"+questionNum+"】")
                ##搜索题目
                payLoad={"subject_id":"2","question_uuid":"","knowledge_code": "", "serial_number": questionNum, "content": "","token":self.Token}
                jsonResponse=self.Session.post(searchQuestionUrl,params=payLoad).json()
                message=jsonResponse["message"]
                print("搜索："+message)
                if message!="成功":
                    self.__itemsNotExist.append(questionNum)
                    print("题目搜索失败，跳过")
                    continue

                ##解析uuid
                if jsonResponse["message"]=="成功":
                    question_uuid=jsonResponse["data"]["list"][0]["question_uuid"]
                    print("uuid:"+question_uuid)
                else:
                    print("解析uuid失败，跳过")
                    continue

                ##获取预览结果
                payLoad={"subject_id":"2","question_uuid":question_uuid,"token":self.Token}
                jsonResponse=self.Session.post(previewUrl,params=payLoad).json()
                print("预览:"+jsonResponse["message"])
                if jsonResponse["message"]!="成功":
                    print("预览失败，跳过")
                    continue

                #查看是否有视频
                videos=jsonResponse["data"]["question_source"]
                print("绑定视频个数："+str(len(videos)))
                if len(videos)==0:
                    print("没有找到视频，跳过")
                    ##这里记录了异常
                    self.__itemsWithoutVideo.append(questionNum)
                    continue
                for video in videos:
                    print(video["source"])
            except Exception as e:
                ##这里记录了异常
                self.__otherExceptions.append(questionNum)

    def PrintExceptions(self):
        '打印异常，调用后即刻清空'
        print("下面打印异常状况")
        print("1.没有找到的编号:")
        for ex in self.__itemsNotExist:
            print(ex)
        self.__itemsNotExist.clear()
        if self.NeedToCheckVideo:
            print("2.没有绑定视频的编号:")
            for ex in self.__itemsWithoutVideo:
                print(ex)
        self.__itemsWithoutVideo.clear()
        print("3.出现错误的编号（原因多样，请重试或人工复核）:")
        for ex in self.__otherExceptions:
            print(ex)
        self.__otherExceptions.clear()
    def CheckKp(self):
        '检查知识点'
        print('请粘贴知识点编号（运行完毕后直接回车可查看问题汇总）：')
        ##公用URL
        searchKpUrl='http://op.classba.cn/api/v3/searchKnowledge/2'

        while 1==1:
            print('\n')
            kpNum=input()
            print('\n')
            if kpNum=="End" or kpNum=="":
                break
            else:
                print("【"+kpNum+"】")
            try:

                ##搜索知识点编号
                payLoad={'subject_id':'2','page':'1','page_size':'60','tag_code':kpNum,'token':self.Token}
                response=self.Session.post(searchKpUrl,params=payLoad)
                jsonResponse=response.json()
                message=jsonResponse['message']
                print('搜索：'+message)
                if message!='成功':
                    print('搜索失败，跳过')
                    self.__itemsNotExist.append(kpNum)
                    continue
                ##查看视频
                if self.NeedToCheckVideo:
                    videos=jsonResponse['data']['list'][kpNum]['tag_source']
                    print('找到'+str(len(videos))+'个资源')
                    if len(videos)>0:
                        for video in videos:
                            print(video['source'])
                    else:
                       self.__itemsWithoutVideo.append(kpNum)
            except :
                self.__otherExceptions.append(kpNum)
                print('错误')
    def DownLoadQueLib(self):
        '爬题库'
        import time
        import json
        print('正在下载题库..')
        ##公用URL
        serchQueUrl='http://op.classba.cn/api/v3/searchQuestion/2'
        page=0
        pageCount=10
        myPagesCount=500
        main_path='C:\\SquirrelAiScript\\OutPut\\'
        print('将存储在目录'+mmain_path)
        while(page<pageCount):
            if page%myPagesCount==0:
                try:
                    SquirrelQueLib.write(']}')
                    SquirrelQueLib.close()
                except:
                    pass
                SquirrelQueLib=open(main_path+str(page/myPagesCount)+'.json','w',1)
                SquirrelQueLib.write('{"questionlist":[')
                isFirstQuestion=True
            payLoad={'subject_id':'2','page':page+1,'token':self.Token}
            response=self.Session.post(serchQueUrl,params=payLoad)
            jsonResponse=response.json()
            data=jsonResponse['data']
            page=data['page']
            pageCount=data['page_count']
            sys.stdout.write('\r'+str(page)+'/'+str(pageCount))
            sys.stdout.flush()
            questions=data['list']
            i=0
            count=len(questions)
            while i<count:
                if not isFirstQuestion:
                    SquirrelQueLib.write(',')
                question=questions[i]
                SquirrelQueLib.write(json.dumps(obj=question))
                i=i+1
                isFirstQuestion=False
        try:
            SquirrelQueLib.write(']}')
            SquirrelQueLib.close()
        except:
            pass

##尝试登陆
while(1==1):
    classbaOp=ClassbaOP()
    classbaOp.Login()
    if not classbaOp.LoginSuccess:
        print("登陆失败，请重试")
    else:
        break
##选择功能模块
while(1==1):
    print('')
    print("请选择功能模块(1、2、3、4）：")
    print("1.题目 2.知识点 3.爬题库 4.退出")
    Selection=input()
    if Selection=='1':
        classbaOp.CheckQuestion()
        classbaOp.PrintExceptions()
    elif Selection=='2':
        classbaOp.CheckKp()
        classbaOp.PrintExceptions()
    elif Selection=='3':
        classbaOp.DownLoadQueLib()
    elif Selection=='4':
        sys.exit(0)
    

