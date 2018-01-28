#coding = utf-8

import re
import tkinter
import requests
from tkinter.scrolledtext import ScrolledText


class CardInfo(object):

    def __init__(self, master):
        self.root = master
        self.root.title("泸州社保卡制卡查询")
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

        self.inputText1 = ScrolledText(self.frame1, width=30, height=42).grid(row=0, column=0)
        self.inputText2 = ScrolledText(self.frame2, width=30, height=42, state='disabled').grid(row=0, column=0)
        self.inputText3 = ScrolledText(self.frame3, width=95, height=42, state='disabled').grid(row=0, column=0)

        self.inputButton1 = tkinter.Button(self.frame1, text="导入", font=("Arial, 15"), command=self.input).grid(row=1, column=0)
        self.inputButton2 = tkinter.Button(self.frame2, text="查询", font=("Arial, 15"), command=self.search).grid(row=1, column=0)
        self.inputButton3 = tkinter.Button(self.frame3, text="导出", font=("Arial, 15"), command=self.output).grid(row=1, column=0)

        self.url = 'http://10.162.0.174:7777/servlet/CardServlet'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }

    # 点击导入按钮函数
    def input(self):
        print(self.inputText1.gettext())

    # 点击查询按钮函数
    def search(self):
        print('查询')

    # 点击导出按钮函数
    def output(self):
        print('导出')

    # 测试网络环境为内网还是外网
    def checkNet(self):
        try:
            requests.get('http://10.162.0.174:7777/search.jsp?method=000', headers=self.headers, timeout=1)
        except BaseException:
            self.url = 'http://182.130.246.34:8881/servlet/CardServlet'
            try:
                requests.get('http://182.130.246.34:8881/search.jsp?method=000', headers=self.headers, timeout=1)
            except BaseException:
                return False
        return True;

    def getCardInfo(self, cardNum):

        param = {
            'card': cardNum,
            'method': '000'
        }
        response = requests.post(self.url, headers=self.headers, data=param, timeout=1)
        print(response.text)
        result = {}
        result['id'] = cardNum
        if '提示' in response.text:
            result['status'] = '未办卡'
        else:
            result['status'] = re.findall(r'社保卡状态</th><td>(.+?)</td>', response.text)
            result['bank'] = re.findall(r'领卡网点</th><td>(.+?)</td>', response.text)
            result['address'] = re.findall(r'网点地址</th><td>(.+?)</td>', response.text)
            result['tel'] = re.findall(r'网点电话</th><td>(.+?)</td>', response.text)
        return result;

def main():
    root = tkinter.Tk()
    CI = CardInfo(root)
    CI.checkNet()
    print(CI.getCardInfo('510524199108060558'))
    root.mainloop()

if __name__ == "__main__":
    main()
