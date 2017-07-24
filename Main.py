#使用3个list
#[Wechat id]
#[Room id]
#{'Room id':[Wechatid1,Wechatid2]}
#Free_People=[]
##People[[WechatID,Gender,RoomID or Status,[...]]
#PeopleAll{'UserName':{'Gender':'Male/Female','Status':'RoomID'/False,'ToUser':''}}
import itchat
import _thread
import time
import random
from itchat.content import *
Room_Profile={}
Room_id=[]
People=[]
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
            if PeopleAll[msg['FromUserName']] in GamePeople:
                print('In Game')
                itchat.send_msg('#[系统提示]您还在聊天中,请先结束聊天.本消息仅您可见.已发送\"开始\"至对方。',toUserName=msg['FromUserName'])
                itchat.send_msg(msg['content'],toUserName=PeopleAll[msg['FromUserName']]['ToUser'])
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
            PeopleAll[msg['Content']]['Status']=False
            if msg['FromUserName'] in GamePeople:
                GamePeople.remove(msg['FromUserName'])
                itchat.send_msg('#[系统通知]对方已下线.',toUserName=PeopleAll[msg['FromUserName']]['ToUser'])
                GamePeople.remove(PeopleAll[msg['FromUserName']]['ToUser'])
                itchat.send_msg('#[系统通知]成功下线.',toUserName=msg['FromUserName'])
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
            People.pop(R)
            People.pop(0)
    print(PeopleAll)
    print(People)
    pair()
_thread.start_new_thread(pair,())
itchat.run()
'''
随机分配有可能会重复，存在问题。
先忽略它吧...
到这里已经把所有要随机分配的加入到People中了
之后计划：
使用多线程+for 第一个随机挑选剩下 然后确认<Status>值是否还是True(有中途离开) 然后更新状态 从people中删除 当len为0或者1的时候不工作，进入while延迟
[线程开始]
子程序开头
while(len(People)<=1):
    延迟指令(5s)
while(len(People)>=2):
    R=Random数
    People[0] --> People[R]
    if P[R]['Status']!=True:
        people.pop(R)
到子程序开头
[线程结束]

多线程参考 http://www.runoob.com/python3/python3-multithreading.html
'''
