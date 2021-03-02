#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask
app = Flask(__name__)
from pathlib import Path
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import json
import random
import time
import sys
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC
import requests
line_bot_api = LineBotApi('EdemTiRiAfAgwlytogxKuq63Tqif+RHb3QlhT3fVo3h4hkEmvO3LskalLVHpZlLlYMTdlnZ5a1sbKi9yyBnxFDIilRkSayLRiSXaZPshWwNmD2xBELzA4895WxNJlt2wnRija1C7J24WmwFw4ho5uQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ca74c9052a5adb2ad0b148adfd2ee4d5')
getdiary= []
joke = ['醫生問小明：如果把你一邊耳朵割掉你會怎麼樣？\n小明：我會聽不見\n醫生又問：那再割掉另一個耳朵呢？\n小明：我會看不見\n醫生問他為什麼...\n小明：因為我有戴眼鏡',
       '有一天小美對小明說：「你能為我而死嗎？」\n結果小明很驚訝的慢慢把手伸進耳朵...\n(餵我耳屎)',
       '有個人對著山洞大喊 : 嗚郎滴欸某??\n山洞裡有聲音回答: 嗚 ～\n然後他就被火車撞死了',
       '有一天 有一隻深海魚\n在海裡自由自在得游啊游 但他一點也不開心\n為什麼?\n因為他壓力好大',
       '有一天郝棒棒 郝美麗 郝帥氣三個人去游泳\n結果三個人都溺水了，郝帥氣因為會游泳 所以先把郝美麗救上岸，\n郝美麗就問郝帥氣說\n.\n.\n.\n啊不救郝棒棒?']

good = ['真正成功的人生，不在於成就的大小，而在於你是否努力地去實現自我，喊出自己的聲音，走出屬於自己的道路。',
       '人的一生中不可能會一帆風順，總會遇到一些挫折，當你對生活失去了信心的時候，仔細的看一看、好好回想一下你所遇到的最美好的事情吧，那會讓你感覺到生活的美好。',
       '別自己製造壓力，我們沒有必要跟著時間走，只需跟著心態和能力走，凡事隨緣、盡力達命、問心無愧，其他的交給天。',
       '人生多一份挫折，就多一份人生的感悟；人生多一次跌打，就多一條抗爭的經驗。',
       '一個人最大的敵人是自己，沒有完不成的任務，只有失去信心的自己。']

@app.route("/callback", methods=['POST'])
def callback():
    global getdiary
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

requests.get("https://script.google.com/macros/s/AKfycbxdOpRhd4E-pEUF3DVolJx1XAW2I2SSfYSPML5S0xiGEmrlu1Q/exec")
datemessage = []

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global getdiary
    global datemessage
    mtext = event.message.text
    money=0
    global joke
    if '存入' in mtext:
        money = 0
        income=''.join([x for x in mtext if x.isdigit()])
        if income != "":
            money += int(income)
        print(money)
        try:
            message = [TextSendMessage(
                text = "存入金額為:"+str(money)+"\n繼續維持存錢的好習慣喲~:)"
            ),
            StickerSendMessage(
                package_id = '1',
                sticker_id = '5'
            )
            ]
            GDriveJSON = 'PythonUpload.json'
            GSpreadSheet = '1IFbWd7HmLTt6944OlfvxhoGRgEERizL5DJztPyeEeUQ'
            scope = ['https://spreadsheets.google.com/feeds']
            key = SAC.from_json_keyfile_name(GDriveJSON, scope)
            gc = gspread.authorize(key)
            worksheet = gc.open_by_key(GSpreadSheet).sheet1
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='存入發生錯誤'))
        new = datetime.datetime.now().strftime('%Y/%m/%d')
        worksheet.append_row((new,'存入',int(money)))
            
    elif mtext == '趣記帳':
        try:
            FLEXmessage = FlexSendMessage(alt_text="我想記帳", contents=json.load(open('money.json',"r",encoding="utf-8") ))
            line_bot_api.reply_message(event.reply_token, FLEXmessage)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='記帳功能發生錯誤'))   

    elif mtext == '推播':
        today=int(time.strftime("%w"))
        if today == 1:
            message = TextSendMessage(
                text = "新的一週有甚麼安排呢？\n給努力的你來點掌聲吧！\n加油加油"
                )
            line_bot_api.reply_message(event.reply_token,message)
        elif today == 2:
            message = TextSendMessage(
                text = "星期二，猴子肚子餓\n早餐吃了嗎？\n要吃飽才有精神繼續努力哦！"
                )
            line_bot_api.reply_message(event.reply_token,message)
        elif today == 3:
            message = TextSendMessage(
                text = "恭喜!!!這週上課日已經要過一半了\n有發生什麼好玩的事嗎？"
                )
            line_bot_api.reply_message(event.reply_token,message)
        elif today == 4:
            message = TextSendMessage(
                text = "星期四，猴子去考試\n你呢？也在為各科作業煩惱嗎？\n可以找我傾訴心情哦~"
                )
            line_bot_api.reply_message(event.reply_token,message)
        elif today == 5:
            message = TextSendMessage(
                text = "耶!!!星期五啦~\n今晚要去哪裡放鬆呀？\n給努力了一週的自己獎勵吧!"
                )
            line_bot_api.reply_message(event.reply_token,message)
        elif today == 6:
            message = TextSendMessage(
                text = "今天去哪裡充實自己了呢？\n其實癱軟在床上也是種幸福啦 ;)"
                )
            line_bot_api.reply_message(event.reply_token,message)
        elif today == 7:
            message = TextSendMessage(
                text = "週末到來~好好讓自己放個假吧!\n要不要紀錄一下生活趣事呢？"
                )
            line_bot_api.reply_message(event.reply_token,message)
            
            
    elif mtext == '顯示餘額':
        GDriveJSON = 'PythonUpload.json'
        GSpreadSheet = '1IFbWd7HmLTt6944OlfvxhoGRgEERizL5DJztPyeEeUQ'
        scope = ['https://spreadsheets.google.com/feeds']
        key = SAC.from_json_keyfile_name(GDriveJSON, scope)
        gc = gspread.authorize(key)
        worksheet = gc.open_by_key(GSpreadSheet).sheet1
        Balance=worksheet.get('D1')#取出google sheet 總和金額
        Balance = str(Balance).replace('[',"")
        Balance = str(Balance).replace(']',"")
        Balance = str(Balance).replace("'","")
        try:
            message = TextSendMessage(
                text = "餘額為:"+Balance
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='顯示帳戶發生錯誤'))
            
    elif '查詢' in mtext:
        findate = str(mtext[2:]).replace(" ","")
        math=''.join([x for x in mtext if x.isdigit()])
        GDriveJSON = 'PythonUpload.json'
        GSpreadSheet = '1IFbWd7HmLTt6944OlfvxhoGRgEERizL5DJztPyeEeUQ'
        scope = ['https://spreadsheets.google.com/feeds']
        key = SAC.from_json_keyfile_name(GDriveJSON, scope)
        gc = gspread.authorize(key)
        worksheet = gc.open_by_key(GSpreadSheet).sheet1 
        if (int(math)>999) and (int(math) <10000):
            new = datetime.datetime.now().strftime('%Y/')
            findate = findate.replace(".","/")
            findate = new + findate
            print(findate)
        #將關鍵字出現的cell位置存到temp
        temp = worksheet.findall(findate)
        print(temp)
        #define result
        result = []
        #根據每筆資料出現的行數去抓取整個row的資料
        for i in temp:
            result.append(worksheet.row_values(i.row))
        funds = []
        fund=[]
        #輸出整個row的資料 
        for i in result:
            fund=i[1]+i[2].rjust(25)+'\n'
            funds.append(fund)
        funds="".join(funds)
        print(funds)
        sum=0
        #輸出colomn_index=2的欄位資料
        for i in result:
            sum+=int(i[2])
        try:
            message = TextSendMessage(
                text = funds+findate+"當日結餘為:"+str(sum)
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='查詢格式輸入錯誤'))
    
    elif mtext == '清除記帳':
        GDriveJSON = 'PythonUpload.json'
        GSpreadSheet = '1IFbWd7HmLTt6944OlfvxhoGRgEERizL5DJztPyeEeUQ'
        scope = ['https://spreadsheets.google.com/feeds']
        key = SAC.from_json_keyfile_name(GDriveJSON, scope)
        gc = gspread.authorize(key)
        worksheet = gc.open_by_key(GSpreadSheet).sheet1
        worksheet.delete_rows(2,)
        Balance=worksheet.get('D1')#取出google sheet 總和金額
        Balance = str(Balance).replace('[',"")
        Balance = str(Balance).replace(']',"")
        Balance = str(Balance).replace("'","")
        try:
            message = TextSendMessage(
                text = "清空記帳後餘額為:"+Balance
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='清空帳戶發生錯誤'))
    
    elif mtext == 'clear':
        GDriveJSON = 'PythonUpload.json'
        GSpreadSheet = '1IFbWd7HmLTt6944OlfvxhoGRgEERizL5DJztPyeEeUQ'
        scope = ['https://spreadsheets.google.com/feeds']
        key = SAC.from_json_keyfile_name(GDriveJSON, scope)
        gc = gspread.authorize(key)
        worksheet = gc.open_by_key(GSpreadSheet).sheet1
        worksheet.delete_rows(2,100)
        Balance=worksheet.get('D1')#取出google sheet 總和金額
        Balance = str(Balance).replace('[',"")
        Balance = str(Balance).replace(']',"")
        Balance = str(Balance).replace("'","")
        try:
            message = TextSendMessage(
                text = "清空記帳後餘額為:"+Balance
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='clear清空帳戶發生錯誤'))
            
    elif mtext == 'Clear':
        GDriveJSON = 'PythonUpload.json'
        GSpreadSheet = '1IFbWd7HmLTt6944OlfvxhoGRgEERizL5DJztPyeEeUQ'
        scope = ['https://spreadsheets.google.com/feeds']
        key = SAC.from_json_keyfile_name(GDriveJSON, scope)
        gc = gspread.authorize(key)
        worksheet = gc.open_by_key(GSpreadSheet).sheet1
        worksheet.delete_rows(2,100)
        Balance=worksheet.get('D1')#取出google sheet 總和金額
        Balance = str(Balance).replace('[',"")
        Balance = str(Balance).replace(']',"")
        Balance = str(Balance).replace("'","")
        try:
            message = TextSendMessage(
                text = "清空記帳後餘額為:"+Balance
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Clear清空帳戶發生錯誤'))

    elif mtext == "指定日期":
        diaryDate(event)
        try:
            message = TextSendMessage(
                text ='幫你查看日記唷~ \n\n' + getdiary
                )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='指定日記功能發生錯誤'))

    elif mtext == "歷史日記":
        diaryDate(event)
        try:
            message = TextSendMessage(
                text ='幫你查看日記唷~ \n\n' + getdiary
                )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='歷史功能發生錯誤'))
    elif '日記' in mtext:
        diary=''.join([x for x in mtext])
        try:
            GDriveJSON = 'pythonschool.json'
            GSpreadSheet = '1ldVx9q8iy1geUXNBuS1jQFFYMt0SuPaiMp0j2CTa4oE'
            scope = ['https://spreadsheets.google.com/feeds']
            key = SAC.from_json_keyfile_name(GDriveJSON, scope)
            gc = gspread.authorize(key)
            worksheet = gc.open_by_key(GSpreadSheet).sheet1
        except Exception as ex:
            print('connect google fail ', ex)
        diary2=diary[3:] #擷取第三個字元
        new = datetime.datetime.now().strftime('%Y-%m-%d')
        #print('will write to ' ,GSpreadSheet,'write ',new,' & ',count)
        worksheet.append_row((new,'日記',diary2))
        print('write OK ' ,GSpreadSheet)
        message = TextSendMessage(
                text = new+" 日記上傳完成"
                )
        line_bot_api.reply_message(event.reply_token,message) 
    
    elif mtext == '新增我的日常':
        message = TextSendMessage(
                text = "輸入日記，接續進行日記分享哦。\nEX：日記\n         今天很開心..."
                )
        line_bot_api.reply_message(event.reply_token,message) 
    
    elif mtext == '心情小語':
        FLEXmessage = FlexSendMessage(alt_text="我的心情", contents=json.load(open('happy.json',"r",encoding="utf-8") ))
        line_bot_api.reply_message(event.reply_token, FLEXmessage)

    elif mtext == '難過':
        j=random.randint(0,5)
        try:
            message = TextSendMessage(
                text ='別難過，分享個笑話給認真的你:) \n\n' + joke[j]
                )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='難過功能發生錯誤'))

    elif mtext == '生氣':
        j=random.randint(0,5)
        try:
            message = TextSendMessage(
                text ='別生氣，分享個笑話讓你舒緩心情:) \n\n' + joke[j]
                )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='生氣功能發生錯誤'))

    elif mtext == '疲憊':
        j=random.randint(0,5)
        try:
            message = TextSendMessage(
                text ='提起精神，分享個正能量小語給你 \n\n' + good[j]
                )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='疲憊功能發生錯誤'))

    elif mtext == '行事曆':  
        try:
            message = TextSendMessage(
                text = '行事曆 / 校內活動 / 推播示例',
                quick_reply = QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="行程規劃",text = "我的行事曆")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="校內資訊",text = "最新消息")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="關心推播",text = "推播")
                    )
                ]
                )
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='功能發生錯誤'))

    elif mtext == '最新消息':
        FLEXmessage = FlexSendMessage(alt_text="元智大學最新消息", contents=json.load(open('promoted.json',"r",encoding="utf-8") ))
        line_bot_api.reply_message(event.reply_token, FLEXmessage)

    elif mtext == '查看我的日常':
        FLEXmessage = FlexSendMessage(alt_text="查看我的日常", contents=json.load(open('mood.json',"r",encoding="utf-8") ))
        line_bot_api.reply_message(event.reply_token, FLEXmessage)

    elif '坐車' in mtext:
        money = 0
        spend=''.join([x for x in mtext if x.isdigit()])
        if spend != "":
            money -= int(spend)
        print(money)
        try:
            message = TextSendMessage(
                text = "坐車扣款金額為:"+str(money)
            )
            GDriveJSON = 'PythonUpload.json'
            GSpreadSheet = '1IFbWd7HmLTt6944OlfvxhoGRgEERizL5DJztPyeEeUQ'
            scope = ['https://spreadsheets.google.com/feeds']
            key = SAC.from_json_keyfile_name(GDriveJSON, scope)
            gc = gspread.authorize(key)
            worksheet = gc.open_by_key(GSpreadSheet).sheet1
            
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='坐車發生錯誤'))
        new = datetime.datetime.now().strftime('%Y/%m/%d')
        worksheet.append_row((new,'坐車',int(money)))

    elif '看電影' in mtext:
        money = 0
        spend=''.join([x for x in mtext if x.isdigit()])
        if spend != "":
            money -= int(spend)
        print(money)
        try:
            message = TextSendMessage(
                text = "看電影扣款為:"+str(money)+'\n電影好看嗎?\n要分享一下嗎 :)?'
            )
            GDriveJSON = 'PythonUpload.json'
            GSpreadSheet = '1IFbWd7HmLTt6944OlfvxhoGRgEERizL5DJztPyeEeUQ'
            scope = ['https://spreadsheets.google.com/feeds']
            key = SAC.from_json_keyfile_name(GDriveJSON, scope)
            gc = gspread.authorize(key)
            worksheet = gc.open_by_key(GSpreadSheet).sheet1
            
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='看電影發生錯誤'))
        new = datetime.datetime.now().strftime('%Y/%m/%d')
        worksheet.append_row((new,'看電影',int(money)))
        
    elif '買東西' in mtext:
        money = 0
        spend=''.join([x for x in mtext if x.isdigit()])
        if spend != "":
            money -= int(spend)
        print(money)
        try:
            message = TextSendMessage(
                text = "買東西扣款為:"+str(money)+'\n心情好就是要買爆!!!'
            )
            GDriveJSON = 'PythonUpload.json'
            GSpreadSheet = '1IFbWd7HmLTt6944OlfvxhoGRgEERizL5DJztPyeEeUQ'
            scope = ['https://spreadsheets.google.com/feeds']
            key = SAC.from_json_keyfile_name(GDriveJSON, scope)
            gc = gspread.authorize(key)
            worksheet = gc.open_by_key(GSpreadSheet).sheet1
            
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='買東西發生錯誤'))
        new = datetime.datetime.now().strftime('%Y/%m/%d')
        worksheet.append_row((new,'買東西',int(money)))
        
    elif '還錢' in mtext:
        money = 0
        spend=''.join([x for x in mtext if x.isdigit()])
        if spend != "":
            money -= int(spend)
        print(money)
        try:
            message = TextSendMessage(
                text = "還錢扣款為:"+str(money)+'欠錢不是好習慣唷~'
            )
            GDriveJSON = 'PythonUpload.json'
            GSpreadSheet = '1IFbWd7HmLTt6944OlfvxhoGRgEERizL5DJztPyeEeUQ'
            scope = ['https://spreadsheets.google.com/feeds']
            key = SAC.from_json_keyfile_name(GDriveJSON, scope)
            gc = gspread.authorize(key)
            worksheet = gc.open_by_key(GSpreadSheet).sheet1
            
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='還錢發生錯誤'))
        new = datetime.datetime.now().strftime('%Y/%m/%d')
        worksheet.append_row((new,'還錢',int(money)))
        
    elif '繳費' in mtext:
        money = 0
        spend=''.join([x for x in mtext if x.isdigit()])
        if spend != "":
            money -= int(spend)
        print(money)
        try:
            message = TextSendMessage(
                text = "繳費金額扣款為:"+str(money)+'繼續加油哦!'
            )
            GDriveJSON = 'PythonUpload.json'
            GSpreadSheet = '1IFbWd7HmLTt6944OlfvxhoGRgEERizL5DJztPyeEeUQ'
            scope = ['https://spreadsheets.google.com/feeds']
            key = SAC.from_json_keyfile_name(GDriveJSON, scope)
            gc = gspread.authorize(key)
            worksheet = gc.open_by_key(GSpreadSheet).sheet1
            
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='繳費發生錯誤'))
        new = datetime.datetime.now().strftime('%Y/%m/%d')
        worksheet.append_row((new,'繳費',int(money)))
        
    elif '吃飯' in mtext:
        money = 0
        spend=''.join([x for x in mtext if x.isdigit()])
        if spend != "":
            money -= int(spend)
        print(money)
        try:
            message = TextSendMessage(
                text = "吃飯花費為:"+str(money)+'剛剛那個一定超好吃~~'
            )
            GDriveJSON = 'PythonUpload.json'
            GSpreadSheet = '1IFbWd7HmLTt6944OlfvxhoGRgEERizL5DJztPyeEeUQ'
            scope = ['https://spreadsheets.google.com/feeds']
            key = SAC.from_json_keyfile_name(GDriveJSON, scope)
            gc = gspread.authorize(key)
            worksheet = gc.open_by_key(GSpreadSheet).sheet1
            
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='吃飯發生錯誤'))
        new = datetime.datetime.now().strftime('%Y/%m/%d')
        worksheet.append_row((new,'吃飯',int(money)))
        
    elif '水費' in mtext:
        money = 0
        spend=''.join([x for x in mtext if x.isdigit()])
        if spend != "":
            money -= int(spend)
        print(money)
        try:
            message = TextSendMessage(
                text = "水費扣款為:"+str(money)
            )
            GDriveJSON = 'PythonUpload.json'
            GSpreadSheet = '1IFbWd7HmLTt6944OlfvxhoGRgEERizL5DJztPyeEeUQ'
            scope = ['https://spreadsheets.google.com/feeds']
            key = SAC.from_json_keyfile_name(GDriveJSON, scope)
            gc = gspread.authorize(key)
            worksheet = gc.open_by_key(GSpreadSheet).sheet1
            
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='水費發生錯誤'))
        new = datetime.datetime.now().strftime('%Y/%m/%d')
        worksheet.append_row((new,'水費',int(money)))
        
    elif '電費' in mtext:
        money = 0
        spend=''.join([x for x in mtext if x.isdigit()])
        if spend != "":
            money -= int(spend)
        print(money)
        try:
            message = TextSendMessage(
                text = "電費扣款為:"+str(money)
            )
            GDriveJSON = 'PythonUpload.json'
            GSpreadSheet = '1IFbWd7HmLTt6944OlfvxhoGRgEERizL5DJztPyeEeUQ'
            scope = ['https://spreadsheets.google.com/feeds']
            key = SAC.from_json_keyfile_name(GDriveJSON, scope)
            gc = gspread.authorize(key)
            worksheet = gc.open_by_key(GSpreadSheet).sheet1
            
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='電費發生錯誤'))
        new = datetime.datetime.now().strftime('%Y/%m/%d')
        worksheet.append_row((new,'電費',int(money)))
        
    elif '房租' in mtext:
        money = 0
        spend=''.join([x for x in mtext if x.isdigit()])
        if spend != "":
            money -= int(spend)
        print(money)
        try:
            message = TextSendMessage(
                text = "房租扣款為:"+str(money)
            )
            GDriveJSON = 'PythonUpload.json'
            GSpreadSheet = '1IFbWd7HmLTt6944OlfvxhoGRgEERizL5DJztPyeEeUQ'
            scope = ['https://spreadsheets.google.com/feeds']
            key = SAC.from_json_keyfile_name(GDriveJSON, scope)
            gc = gspread.authorize(key)
            worksheet = gc.open_by_key(GSpreadSheet).sheet1
            
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='房租發生錯誤'))
        new = datetime.datetime.now().strftime('%Y/%m/%d')
        worksheet.append_row((new,'房租',int(money)))
        
    elif '電話費' in mtext:
        money = 0
        spend=''.join([x for x in mtext if x.isdigit()])
        if spend != "":
            money -= int(spend)
        print(money)
        try:
            message = TextSendMessage(
                text = "電話費扣款為:"+str(money)
            )
            GDriveJSON = 'PythonUpload.json'
            GSpreadSheet = '1IFbWd7HmLTt6944OlfvxhoGRgEERizL5DJztPyeEeUQ'
            scope = ['https://spreadsheets.google.com/feeds']
            key = SAC.from_json_keyfile_name(GDriveJSON, scope)
            gc = gspread.authorize(key)
            worksheet = gc.open_by_key(GSpreadSheet).sheet1
            
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='電話發生錯誤'))
        new = datetime.datetime.now().strftime('%Y/%m/%d')
        worksheet.append_row((new,'電話',int(money)))
        
    elif mtext == '行程':
        message = TextSendMessage(text = "請輸入行程\n  ex: 加入行程\n "+"       "+"雲端作業")
        line_bot_api.reply_message(event.reply_token, message)
    elif mtext == '地點':
        message = TextSendMessage(text = "請輸入地點\n ex:加入地點\n "+"     "+"1201(or 無)")
        line_bot_api.reply_message(event.reply_token, message)
    elif '加入行程' in mtext:
        cal=mtext[5:]
        datemessage.append(cal)
        #print("行程\n "+datemessage)
        message = TextSendMessage(text = "行程加入完成\n接下來按上面的選取行程日期時間")
        line_bot_api.reply_message(event.reply_token, message)
    elif '加入地點' in mtext:
        cal=mtext[5:]
        datemessage.append(cal)
        #print("行程時間地點\n"+datemessage)
        addsheet(datemessage)
        message = TextSendMessage(text = "行程完成加入至google表單")
        line_bot_api.reply_message(event.reply_token, message)
    """elif mtext == '我的行事曆' :
            print('enter datetime')
            sendDatetime(event)"""
    if isinstance(event,PostbackEvent):
        print('isinstance')
        backdata = dict(parse_qsl(event.postback.data))
        if backdata.get('action') == 'sell':
            sendData_sell(event,backdata)
            
def addsheet(datemessage):
    print("addsheet")
    cal=datemessage[:]
    GDriveJSON = 'calen.json'
    GSpreadSheet = '1aNUfm8eVBLrcsHEsmDJl9qKeYdiBfWzFP24h68NmYJw'
    try:
            
        scope = ['https://spreadsheets.google.com/feeds']
        key = SAC.from_json_keyfile_name(GDriveJSON, scope)
        gc = gspread.authorize(key)
        worksheet = gc.open_by_key(GSpreadSheet).sheet1
        print('worksheet complete')
    except Exception as ex:
        print('connect google fail ', ex)
    #new = datetime.datetime.now().strftime('%Y/%m/%d')
    #print('will write to ' ,GSpreadSheet,'write ',new,' & ',count)
    worksheet.append_row((datemessage))
    datemessage = 0
    datemessage = []
    print('write OK ' ,GSpreadSheet)

    
    
def sendDatetime(event):
    print('開始新增行程!')
    global getdiary 
    getdiary = []
    try:
        message = TemplateSendMessage(
            alt_text = '行程新增',
            template = ButtonsTemplate(
                thumbnail_image_url = 'https://i.imgur.com/wAU9Epy.png',
                title = '開始新增行程!',
                text = '請依序輸入',
                actions=[
                    MessageTemplateAction(
                       label = "行程名稱",
                       text = "行程"
                    ),
                    DatetimePickerTemplateAction(
                        label = "選取行程日期時間",
                        data = "action=sell&mode=datetime",
                            #觸發postback
                        mode = "datetime",
                        initial = "2020-12-11T10:00",
                        min = "2020-12-11T00:00",
                        max = "2080-12-31T23:59",
                    ),
                    MessageTemplateAction(
                       label = "地點",
                       text = "地點"
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='時間選擇沒問題嗎~?'))

def diaryDate(event):
    print('開始查詢日記!')
    global getdiary 
    getdiary = []
    try:
        message = TemplateSendMessage(
            alt_text = '行程新增',
            template = ButtonsTemplate(
                thumbnail_image_url = 'https://i.imgur.com/GpeEjEO.jpg',
                title = '是哪一天的日記呢~?',
                text = '點選下方按鈕選擇日期',
                actions=[
                    DatetimePickerTemplateAction(
                        label = "選擇要查詢的日記日期",
                        data = "action=sell&mode=date",
                            #觸發postback
                        mode = "date",
                        initial = "2020-12-09",
                        min = "2020-12-09",
                        max = "2080-12-31",
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='時間選擇沒問題嗎~?'))


@handler.add(PostbackEvent)
def sendData_sell(event):
    global getdiary
    global datemessage
    backdata = event.postback.data
    print(backdata)
    try:
        print(event.postback.params.get('datetime'))
        #print(event.postback.params.get('datetime'))
        if 'mode=datetime' in backdata:
            dt = datetime.datetime.strptime(event.postback.params.get('datetime'),'%Y-%m-%dT%H:%M')
            dt = dt.strftime('%Y-%m-%d %H:%M')
            #dt = dt.strftime('{d}%Y-%m-%d, {t}%H:%M').format(d='日期為:',t='時間為:')
            datemessage.append(dt)
            message = TextSendMessage(
                text ='加入的日期時間為:'+ dt+'剩下地點要輸入哦~ \nex:加入地點\n "+"     "+"1201(or 無)"'
            )
            line_bot_api.reply_message(event.reply_token,message)
        elif 'mode=date' in backdata:
            print('進入date模式以下為按鍵資料')
            print("findate1 = "+event.postback.params.get('date'))
            findate = event.postback.params.get('date')
            
            GDriveJSON = 'pythonschool.json'
            GSpreadSheet = '1ldVx9q8iy1geUXNBuS1jQFFYMt0SuPaiMp0j2CTa4oE'
            scope = ['https://spreadsheets.google.com/feeds']
            key = SAC.from_json_keyfile_name(GDriveJSON, scope)
            gc = gspread.authorize(key)
            worksheet = gc.open_by_key(GSpreadSheet).sheet1 
            print('findate= ' + findate )
            #將關鍵字出現的cell位置存到temp
            temp = worksheet.findall(findate)
            result = []
            #根據每筆資料出現的行數去抓取整個row的資料
            for i in temp:
                result.append(worksheet.row_values(i.row)) 
            funds = []
            fund=[]
            #輸出整個row的資料 
            for i in result:
                fund=i[0]+str(i[2])+'\n'
                getdiary.append(fund)
                print(getdiary)
            getdiary="".join(getdiary)
            getdiary='當天日記如下:\n'+getdiary
            
            message = TextSendMessage(
                text = getdiary
            )
            line_bot_api.reply_message(event.reply_token,message)
        elif '日期時間' in dt:
            cal=dt[5:]
            datemessage.append(cal)
            #print("行程日期\n"+datemessage)
        
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='點選時間時發生錯誤!'))


        
if __name__ == '__main__':
    app.run()
