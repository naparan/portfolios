import random
import pandas as pd
import csv
import sys
import requests
import tkinter as tk
from tkinter import messagebox,simpledialog
import os
import base64
from io import StringIO

# 読み込み中通知
print("Now Loading...")

# githubAPI系
Github_Token = os.getenv('GITHUB_TOKEN')
print("Successfully acquired Github token")
Repo_Owner = 'naparan'
Repo_Name = 'kintoreCSV'
user_api_url = f'https://api.github.com/repos/naparan/kintoreCSV/contents/user.csv'
menu_api_url = f'https://api.github.com/repos/naparan/kintoreCSV/contents/menu.csv'
admin_api_url = f'https://api.github.com/repos/naparan/kintoreCSV/contents/admin.csv'

headers = {
    'Authorization': f'token {Github_Token}',
    'Accept': 'application/vnd.github.v3+json'
}

# ローカルで取得
def get_localPath(apiurl,LocalFile_Path):
    req = requests.get
    if os.path.exists(LocalFile_Path) :
        print(f"Using cashed file : {LocalFile_Path}")
        return pd.read_csv(LocalFile_Path)
    else:
        print("Downloading from github now...")
        
        response = req(apiurl,headers=headers)
        if response.status_code == 200:
            content = response.json().get("content","")
            decode_content = base64.b64decode(content).decode("utf-8")
                
            with open(LocalFile_Path,"w",encoding="utf-8") as f:
                f.write(decode_content)
                
            df = pd.read_csv(StringIO(decode_content))
            print(f"File successfully loaded.   Path:'{LocalFile_Path}'")
            return df
        else:
            print(f"Error:Failed to load file.   status code:{response.status_code}")

#終了時ファイル削除
def remove_file(path):
    os.remove(path)
    print(f"File successfully deleted   path: {path}")
    
# ローカルファイル 配列
user_LocalFile_Path = './user.csv'
menu_LocalFile_Path = './menu.csv'
admin_LocalFile_Path = './admin.csv'

userDF = get_localPath(user_api_url,user_LocalFile_Path)
menu = get_localPath(menu_api_url,menu_LocalFile_Path)
admin_data = get_localPath(admin_api_url,admin_LocalFile_Path)

userDict = {i+1:row[1:].tolist() for i, row in userDF.iterrows()}

class userData:

    def __init__(self):
        self.uid = 0
        self.uname = ""
        self.user_path = user_LocalFile_Path

    def upload(self):
        with open(self.user_path,'r',encoding="utf-8") as f:
            content = f.read()
            base64_content = base64.b64encode(content.encode("utf-8")).decode('utf-8')
        print(f"Content:{base64_content}")
        print("Now Loading...")
        
        data = {
            'message':'update user CSV file',
            'content':base64_content,
            'branch':'main'
        }
        
        user_res = requests.get(user_api_url, headers=headers)
        if user_res.status_code == 200 or user_res.status_code == 201:
            sha = user_res.json()['sha']
            data['sha'] = sha
        
        user_res = requests.put(user_api_url, headers=headers, json=data)

        if user_res.status_code == 201:
            print("File successfully created\nstatus:201")
        elif user_res.status_code == 200:
            print("File successfully updated\nstatus:200")
        else:
            print(f"Error{user_res.status_code}")
            print(user_res.json())
    
    # 新規会員の情報をCSVに追加
    def append_user(self,user_arr):
        with open(self.user_path,'a',newline="",encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(user_arr)

        self.upload()
        
    # 新規会員登録
    def newuser(self,num):
        def inner():
            while True:
                
                uname_new = simpledialog.askstring("登録","ユーザー名を入力してください")
                if uname_new:
                    uid_new = len(userDict)+1
                    user = [uid_new,uname_new]
                    for i in range(len(menu)):
                        user.append("no")
                    self.append_user(user)
                
                    messagebox.showinfo("登録完了","登録ありがとうございます！\nユーザーID："+str(len(userDict)+1)+"\nユーザー名："+uname_new+"ログインするには再起動してください")
                    sys.exit()
                else:
                    messagebox.showerror("Error","無効な入力です")
        return inner

    # ログイン
    def login(self):
        global userDict
        try:
            self.uid = int(simpledialog.askinteger("ログイン","ユーザーIDを入力："))
            
            self.uname = simpledialog.askstring("ログイン","ユーザー名を入力：")
            
            if self.uid in userDict and "".join(userDict[self.uid][0]) == self.uname:
                messagebox.showinfo("ログイン成功")
                self.userinfo()
                return True
            else:
                messagebox.showerror("Error","ID又はユーザー名が間違っています")
                return False
        except ValueError:
            messagebox.showerror("Error：無効な入力")
            return False
        
    # ユーザーのメニュー取り組み状況を表示
    def userinfo(self):
        info_text = f"ユーザーID:{self.uid}\nユーザー名:{self.uname}\n\n取り組み状況：\n{userDF.iloc[self.uid-1][2:]}"
        messagebox.showinfo("ユーザー情報",info_text)

    # ユーザーの取り組み状況をアップデート
    # menudict i番目 = userDict i+1番目
    def update_userCSV(self,menu_num):
        print("Now Loading...")
        update_userDF = pd.DataFrame(userDF)
        print(update_userDF)
        menu_name = (menu.iloc[menu_num-1][1])
        
        userDict[self.uid][menu_num] = "ok"
        update_userDF.loc[update_userDF["id"] == self.uid, menu_name] = userDict[self.uid][menu_num]
        update_userDF.to_csv(self.user_path,index=False,encoding='utf-8')
        
        self.upload()
        
        messagebox.showinfo("info","取り組み状況を更新しました")
        self.userinfo()

    # メニュー選択
    def kinds_in(self):

        # メニュー一覧を出力
        while True:
            temp = simpledialog.askinteger("メニュー選択","1,プランク\n2,ヒップリフト\n3,クランチ\n4,フロントランジ\n5,ランジ\n6,レッグレイズ\n")
            # messagebox.showinfo(userDict[self.uid][temp])

            if temp>=1 and temp<=len(menu):
                if userDict[self.uid][temp] == "ok":
                    
                    judge = messagebox.askyesno("注意！","このメニューは今週既に取り組んでいます！本当によろしいですか？：")
                    if not judge:
                        continue
                    else:
                        return temp
                return temp
            else:
                messagebox.showerror("Error","1~"+str(len(menu))+"までの数値を入力してください")
                continue

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.res = 0
        self.userData = userData()
        self.has_login  = False
        self.title("乱数筋トレアプリ")
        self.geometry("400x300")
        tk.Label(self,text="乱数筋トレプログラム",font=("Arial", 16)).pack(pady=10)
        
        self.login_button = tk.Button(self,text="ログイン",command=self.login)
        self.login_button.pack(pady=5)
        
        self.newuser_button = tk.Button(self,text="新規登録",command=self.userData.newuser(len(userDict)))
        self.newuser_button.pack(pady=5)
        
        self.selectMenu_button = tk.Button(self,text="メニューを選択",command=self.selectMenu)
        self.selectMenu_button.pack(pady=5)
        
    def login(self):
        self.has_login = self.userData.login()
        
    def selectMenu(self):
        if self.has_login:
            menu_num = self.userData.kinds_in()
            n = simpledialog.askinteger("乱数生成","好きな数字を入れてね")
            n = int(n)
            print("Now Loading...")
            random.seed(n)
            self.res = random.randint(0,20)
            
            if self.res != 0:
                messagebox.showinfo("結果", f"{self.res}回！\n{menu.iloc[menu_num-1,1]} 頑張ろう！")
            else:
                messagebox.showinfo("結果","今日はお休み！ラッキー！")

            self.userData.update_userCSV(menu_num)
        else:
            messagebox.showerror("Error","ログインしていません")

# 関数呼び出し
Application().mainloop()
