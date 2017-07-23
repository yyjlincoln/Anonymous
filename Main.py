#使用3个list
#[Wechat id]
#[Room id]
#{'Room id':[Wechatid1,Wechatid2]}
#Free_People=[]
##People[[WechatID,Gender,RoomID or Status,[...]]
#PeopleAll{'UserName':{'Gender':'Male/Female','Status':'RoomID'/False,'ToUser':''}}
import itchat
import random
from itchat.content import *
Room_Profile={}
Room_id=[]
People=[]
PeopleAll={}
print('Trying to log in Wechat Server Account.')
itchat.auto_login(hotReload=True)
print('Logged in.')
@itchat.msg_register(TEXT)
def message_recieved(msg):
    global Room_Profile
    global Room_id
    global People
    global PeopleAll
    #print(msg['User']['Sex'])
    print(msg['Content'])
    if msg['Content']=='开始':
        if msg['FromUserName'] in PeopleAll:
            if PeopleAll[msg['FromUserName']]['Status']!=False:
                print('In Game')
                itchat.send_msg('#[系统提示]您还在聊天中,请先结束聊天.本消息仅您可见.已发送\"开始\"至对方。',toUserName=msg['FromUserName'])
                itchat.send_msg(msg['content'],toUserName=PeopleAll[msg['FromUserName']]['ToUser'])
            else:
                itchat.send_msg('正在加入,请稍等.',toUserName=msg['FromUserName'])
                #更新数据
                PeopleAll[msg['FromUserName']]['Status']=True
                #随机匹配
                People.append(msg['FromUserName'])
                if len(People)==1:
                    print('人不够')
                itchat.send_msg('正在等待匹配.您也可以随时输入[离开]退出等待。',toUserName=msg['FromUserName'])
                pair(msg)
        else:
             print(msg['User']['Sex'])
             PeopleAll[msg['FromUserName']]={'Gender':msg['User']['Sex'],'Status':False,'ToUser':''}
             People.append(msg['FromUserName'])
             if len(People)==1:
                 print('人不够')
             itchat.send_msg('正在等待匹配.您也可以随时输入[离开]退出等待。',toUserName=msg['FromUserName'])
             pair(msg)
def pair(msg):
    global Room_Profile
    global Room_id
    global People
    global PeopleAll
        print(Room_Profile)
        print(Room_id)
        print(PeopleAll)
        print(People)
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
'''
