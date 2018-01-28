#coding = utf-8

import re
import tkinter
import requests
import xlwt
import time
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
from tkinter import filedialog


class CardInfo(object):

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("泸州社保卡制卡查询（测试版1.0）  作者：yangyi")
        self.root.resizable(0,0)
        self.root.minsize(1200,600)

        self.frame1 = tkinter.LabelFrame(self.root,
                                         padx=10, pady=10,
                                         text='输入身份证号码',
                                         font=("Arial, 15"),
                                         width=250,
                                         height=600)
        self.frame1.grid(row=0, column=0)
        self.frame2 = tkinter.LabelFrame(self.root,
                                         padx=10, pady=10,
                                         text='身份证号码',
                                         font=("Arial, 15"),
                                         width=250,
                                         height=600)
        self.frame2.grid(row=0, column=1)
        self.frame3 = tkinter.LabelFrame(self.root,
                                         padx=10, pady=10,
                                         text='社保卡信息',
                                         font=("Arial, 15"),
                                         width=700,
                                         height=600)
        self.frame3.grid(row=0, column=2)

        self.inputText1 = ScrolledText(self.frame1, width=30, height=42)
        self.inputText2 = ScrolledText(self.frame2, width=30, height=42, state='disabled')
        self.inputText3 = ScrolledText(self.frame3, width=95, height=42, state='disabled')
        self.inputText1.grid(row=0, column=0)
        self.inputText2.grid(row=0, column=0)
        self.inputText3.grid(row=0, column=0)

        self.inputButton1 = tkinter.Button(self.frame1, text="导入", font=("Arial, 15"), command=self.input)
        self.inputButton2 = tkinter.Button(self.frame2, text="查询", font=("Arial, 15"), state='disabled', command=self.search)
        self.inputButton3 = tkinter.Button(self.frame3, text="导出", font=("Arial, 15"), state='disabled', command=self.output)
        self.inputButton1.grid(row=1, column=0)
        self.inputButton2.grid(row=1, column=0)
        self.inputButton3.grid(row=1, column=0)

        self.url = 'http://10.162.0.174:7777/servlet/CardServlet'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }

    # 点击导入按钮函数
    def input(self):
        cards = self.inputText1.get('0.0', tkinter.END)
        self.cardsList = []
        #根据长度判断是否身份证号码
        for val in cards.split():
            if val.isalnum() and len(val) == 18:
                self.cardsList.append(val)

        #将识别的身份证号码填入第二个框中
        if (self.cardsList):
            self.inputButton2['state'] = tkinter.NORMAL
        else:
            self.inputButton2['state'] = tkinter.DISABLED
        self.inputText2['state'] = tkinter.NORMAL
        self.inputText2.delete('0.0', tkinter.END) #全清空
        for index, item in enumerate(self.cardsList):
            self.inputText2.insert(tkinter.END, item + '\n')

        self.inputText2['state'] = tkinter.DISABLED

    # 点击查询按钮函数
    def search(self):
        self.inputButton2['state'] = tkinter.DISABLED
        if not self.checkNet():
            messagebox.showerror('网络链接错误', '请检查网络链接，本程序需要连接内网或者外网')
            return

        t1 = time.clock()
        self.cardResult = []
        for cardNum in self.cardsList:
            cardInfo = self.getCardInfo(cardNum)
            self.cardResult.append(cardInfo)

        print(time.clock() - t1)

        #在第三个文本框中显示查询结果
        self.inputText3['state'] = tkinter.NORMAL
        self.inputText3.delete('0.0', tkinter.END)
        self.inputText3.insert('0.0', '身份证号码\t社保卡状态\t银行网点\t网点地址\t网点电话\n')
        for cardInfo in self.cardResult:
            if cardInfo.__contains__('bank'):
                self.inputText3.insert(tkinter.END, cardInfo['id'] + '\t' + cardInfo['status'] + '\t' + cardInfo['bank'] + '\t' + cardInfo['address'] + '\t' + cardInfo['tel'] + '\n')
            else:
                self.inputText3.insert(tkinter.END, cardInfo['id'] + '\t' + cardInfo['status'] + '\n')
        self.inputText3['state'] = tkinter.DISABLED
        if self.cardsList:
            self.inputButton2['state'] = tkinter.NORMAL
        if self.cardResult:
            self.inputButton3['state'] = tkinter.NORMAL
        else:
            self.inputButton3['state'] = tkinter.DISABLED

    # 点击导出按钮函数
    def output(self):
        self.inputButton3['state'] = tkinter.DISABLED
        workBook = xlwt.Workbook()
        sheet1 = workBook.add_sheet('社保卡查询结果')
        sheet1.write(0, 0, '身份证号码')
        sheet1.write(0, 1, '社保卡状态')
        sheet1.write(0, 2, '领卡网点')
        sheet1.write(0, 3, '网点地址')
        sheet1.write(0, 4, '网点电话')

        for index, cardInfo in enumerate(self.cardResult):
            sheet1.write(index + 1, 0, cardInfo['id'])
            sheet1.write(index + 1, 1, cardInfo['status'])
            if cardInfo.__contains__('bank'):
                sheet1.write(index + 1, 2, cardInfo['bank'])
                sheet1.write(index + 1, 3, cardInfo['address'])
                sheet1.write(index + 1, 4, cardInfo['tel'])

        path = filedialog.asksaveasfilename()
        if path:
            workBook.save(path + '.xls')

        if self.cardResult:
            self.inputButton3['state'] = tkinter.NORMAL

    # 测试网络环境为内网还是外网
    def checkNet(self):
        try:
            requests.get('http://10.162.0.174:7777/search.jsp?method=000', headers=self.headers, timeout=2)
        except BaseException:
            self.url = 'http://182.130.246.34:8881/servlet/CardServlet'
            try:
                requests.get('http://182.130.246.34:8881/search.jsp?method=000', headers=self.headers, timeout=2)
            except BaseException:
                return False
        return True;

    def getCardInfo(self, cardNum):

        param = {
            'card': cardNum,
            'method': '000'
        }
        try:
            response = requests.post(self.url, headers=self.headers, data=param, timeout=2)
            result = {}
            result['id'] = cardNum
            if '提示' in response.text:
                result['status'] = '该人员还未办理社保卡,请尽快到社区或银行网点办理!'
            else:
                result['status'] = re.findall(r'社保卡状态</th><td>(.+?)</td>', response.text)[0]
                result['bank'] = re.findall(r'领卡网点</th><td>(.+?)</td>', response.text)[0]
                result['address'] = re.findall(r'网点地址</th><td>(.+?)</td>', response.text)[0]
                result['tel'] = re.findall(r'网点电话</th><td>(.+?)</td>', response.text)[0]
            return result;
        except BaseException as e:
            print(e)
            result = {}
            result['id'] = cardNum
            result['status'] = '网络状态不好，请重新查询'
            return result

def main():
    CI = CardInfo()
    tkinter.mainloop()

if __name__ == "__main__":
    main()
