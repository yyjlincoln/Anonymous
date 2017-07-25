#People[] 空闲wxid
#GamePeople[] 游戏中wxid
#PeopleAll{'名称wxid':{'Gender':'微信提供 性别','Status':True/False(是否在等待中),'ToUser':'wxid 建立连接转发'}}
#其它全局变量为累赘。
import itchat
import _thread
import time
import random
from itchat.content import *
Room_Profile={}
Room_id=[]
People=[]
Video_Limit=False
Attachment_Limit=False
PeopleAll={}
GamePeople=[]
print('Trying to log in Wechat Server Account.')
itchat.auto_login(hotReload=True)
print('Logged in.')
@itchat.msg_register(TEXT)
def message_recieved(msg):
    global Room_Profile
    global Room_id
    global People
    global PeopleAll
    global GamePeople
    #print(msg['User']['Sex'])
    print(msg['Content'])
    if msg['Content']=='开始':
        if msg['FromUserName'] in PeopleAll:
            if msg['FromUserName'] in GamePeople:
                print('In Game')
                itchat.send_msg('#[系统提示]您还在聊天中,请先结束聊天.本消息仅您可见.已发送\"开始\"至对方。',toUserName=msg['FromUserName'])
            elif PeopleAll[msg['FromUserName']]['Status']==True:
                itchat.send_msg('#[系统提示]您已经在等待列表中了.本消息仅您可见.',toUserName=msg['FromUserName'])
            else:
                itchat.send_msg('正在加入,请稍等.',toUserName=msg['FromUserName'])
                #更新数据
                PeopleAll[msg['FromUserName']]['Status']=True
                #随机匹配
                People.append(msg['FromUserName'])
                if len(People)==1:
                    print('人不够')
                itchat.send_msg('正在等待匹配.您也可以随时输入[离开]退出等待。',toUserName=msg['FromUserName'])
                #pair(msg)
        else:
             print(msg['User']['Sex'])
             PeopleAll[msg['FromUserName']]={'Gender':msg['User']['Sex'],'Status':True,'ToUser':''}
             People.append(msg['FromUserName'])
             if len(People)==1:
                 print('人不够')
             itchat.send_msg('正在等待匹配.您也可以随时输入[离开]退出等待。',toUserName=msg['FromUserName'])
           #  pair()
    if msg['Content']=='离开':
        if msg['FromUserName'] in PeopleAll:
            PeopleAll[msg['FromUserName']]['Status']=False
            if msg['FromUserName'] in GamePeople:
                GamePeople.remove(msg['FromUserName'])
                itchat.send_msg('#[系统通知]对方已下线.',toUserName=PeopleAll[msg['FromUserName']]['ToUser'])
                GamePeople.remove(PeopleAll[msg['FromUserName']]['ToUser'])
                itchat.send_msg('#[系统通知]成功下线.',toUserName=msg['FromUserName'])
                PeopleAll[PeopleAll[msg['FromUserName']]['ToUser']]['ToUser']=''
                PeopleAll[PeopleAll[msg['FromUserName']]['ToUser']]['Status']=False
                PeopleAll[msg['FromUserName']]['ToUser']=''
                
    else:
        if msg['FromUserName'] not in GamePeople and msg['Content']!='开始':
            itchat.send_msg('您还没有开始聊天。请输入[开始]匹配对象。',toUserName=msg['FromUserName'])
            return
        itchat.send_msg(msg['Content'],toUserName=PeopleAll[msg['FromUserName']]['ToUser'])
@itchat.msg_register(PICTURE)
def picture_recieved(msg):
    if msg['FromUserName'] not in GamePeople:
        itchat.send_msg('您不在聊天中,图片/表情包将不会被接收.',toUserName=msg['FromUserName'])
    else:
        msg.download(msg.fileName)
        itchat.send_msg('#[系统提示]对方发送了一张图片,正在处理,请稍等...',toUserName=PeopleAll[msg['FromUserName']]['ToUser'])
        itchat.send_image(msg.fileName,toUserName=PeopleAll[msg['FromUserName']]['ToUser'])
@itchat.msg_register(VOICE)
def voice_recieved(msg):
    if msg['FromUserName'] not in GamePeople:
        itchat.send_msg('您不在聊天中,语音将不会被接收.',toUserName=msg['FromUserName'])
    else:
        msg.download(msg.fileName)
        itchat.send_msg('#[系统提示]对方发送了一条语音,正在处理,请稍等...',toUserName=PeopleAll[msg['FromUserName']]['ToUser'])
        itchat.send_file(msg.fileName,toUserName=PeopleAll[msg['FromUserName']]['ToUser'])
@itchat.msg_register(VIDEO)
def video_recieved(msg):
    global Video_Limit
    if msg['FromUserName'] not in GamePeople:
        itchat.send_msg('您不在聊天中,视频将不会被接收.',toUserName=msg['FromUserName'])
    else:
        if Video_Limit==True:
            itchat.send_msg('#[系统提示]当前服务器人数较多或在维护中,视频将不会被转发.',toUserName=msg['FromUserName'])
            return
        msg.download(msg.fileName)
        itchat.send_msg('对方发送了一条视频消息,正在处理,请稍等...',toUserName=PeopleAll[msg['FromUserName']]['ToUser'])
        itchat.send_video(msg.fileName,toUserName=PeopleAll[msg['FromUserName']]['ToUser'])
@itchat.msg_register(ATTACHMENT)
def attachment_recieved(msg):
    global Attachment_Limit
    if msg['FromUserName'] not in GamePeople:
        itchat.send_msg('您不在聊天中,附件将不会被接收.',toUserName=msg['FromUserName'])
    else:
        if Attachment_Limit==True:
            itchat.send_msg('#[系统提示]当前服务器人数较多或在维护中,附件将不会被转发.',toUserName=msg['FromUserName'])
            return
        msg.download(msg.fileName)
        itchat.send_msg('对方发送了一个附件,正在处理,请稍等...\n温馨提示:请小心病毒,切勿输入个人机密信息!',toUserName=PeopleAll[msg['FromUserName']]['ToUser'])
        itchat.send_file(msg.fileName,toUserName=PeopleAll[msg['FromUserName']]['ToUser'])
def pair():
    global Room_Profile
    global Room_id
    global People
    global PeopleAll
   # print(PeopleAll)
   # print(People)
  #  print(0)
    while(len(People)<=1):
        time.sleep(10)
     #   print(0.1)
    while(len(People)>=2):
        x=list(range(len(People)))
     #   print(1)
        x.pop(0)
        R=random.choice(x)
        #People[0]+People[R]
        if PeopleAll[People[0]]['Status']==True and PeopleAll[People[R]]['Status']==True:
            print('匹配成功')
            PeopleAll[People[0]]['Status']=False
            PeopleAll[People[R]]['Status']=False
            PeopleAll[People[0]]['ToUser']=People[R]
            PeopleAll[People[R]]['ToUser']=People[0]
            #进入游戏
            if PeopleAll[People[R]]['Gender']==1:
                Gender='男生'
            elif PeopleAll[People[R]]['Gender']==2:
                Gender='女生'
            else:
                Gender='性别未知'
            itchat.send_msg('匹配成功,对方信息:'+Gender,toUserName=People[0])
            if PeopleAll[People[0]]['Gender']==1:
                Gender='男生'
            elif PeopleAll[People[0]]['Gender']==2:
                Gender='女生'
            else:
                Gender='性别未知'
            itchat.send_msg('匹配成功,对方信息:'+Gender,toUserName=People[R])
            GamePeople.append(People[0])
            GamePeople.append(People[R])
            People.pop(R)
            People.pop(0)
    print(PeopleAll)
    print(People)
    pair()
_thread.start_new_thread(pair,())
itchat.run()
