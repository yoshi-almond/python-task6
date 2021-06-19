"""
任意のジャンルのランキング一覧を取得
"""
import requests
import pandas as pd
import datetime
import sys
from time import sleep

LOG_FILE_PATH = "log/log_{datetime}.log"
OUTPUT_CSV_PATH="./output/output_list_{keyword}_{datetime}.csv"
log_file_path=LOG_FILE_PATH.format(datetime=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))

#ログ出力
def log(txt):
    now=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    logStr = f'[log: {now}] {txt}'
    # ログ出力
    with open(log_file_path, 'a', encoding='utf-8_sig') as f:
        f.write(logStr + '\n')
    print(logStr)

#CSV書き出し
def output_csv_file(info_list,keyword):
    now=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    df = pd.DataFrame(info_list,columns=info_list[0])
    df=df.drop(0)
    df.to_csv(OUTPUT_CSV_PATH.format(keyword=keyword,datetime=now))

class RakutenAPI:
    def __init__(self,url,payload):
        self.url = url
        self.payload = payload
        self.count = 0
        self.success = 0
        self.fail = 0
        self.info_list = [["順位","商品名","商品コード","値段","URL"]]    
    def get_data(self):
        r = requests.get(self.url, params=self.payload)
        self.resp = r.json()
    def get_total(self):
        self.total = int(self.resp['count'])
        self.max = int(self.total/30 + 1)
    def check_over1000(self):
        if self.max > 100:
            self.max = 100
            print('-'*40)
            print("100ページ（3000アイテム）を超えています")
            ans = input("このまま続けますか?(y/n) >> ")
            print('-'*40)
            while True:
                if ans == "y":            
                    break
                elif ans == "n":
                    sys.exit()
                else:
                    print("y/nで入力してください")
                    ans = input("このまま続けますか?(y/n) >> ")
                    continue    
        else:
            pass
    def extract_info(self):
        for i in self.resp['Items']:
            self.count += 1
            try:
                self.info_list.append([])
                #順位取得
                self.info_list[self.count].append(i['Item']['rank'])
                #商品名取得
                self.info_list[self.count].append(i['Item']['itemName'])
                #商品コード取得
                self.info_list[self.count].append(i['Item']['itemCode'])
                #値段取得
                self.info_list[self.count].append(i['Item']['itemPrice'])
                #URL取得
                self.info_list[self.count].append(i['Item']['itemUrl'])
                self.success += 1
                log(f'{self.count}件目取得成功')
            except Exception as e:
                log(f'{self.count}件目取得失敗')
                log(e)
                self.fail += 1
    def show_result(self):
        log("終了")
        log("---------------------------------------------")
        log(f"件数 : {self.count}")
        log(f"成功 : {self.success}")
        log(f"失敗 : {self.fail}")    

def main():
    genreId = 200162
    url = 'https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628'
    payload = {
        'applicationId':'1035981462778848427',
        'genreId':genreId,
        }
    rakutenAPI = RakutenAPI(url,payload)
    rakutenAPI.get_data()
    rakutenAPI.extract_info()
    output_csv_file(rakutenAPI.info_list,genreId)
    rakutenAPI.show_result()

if __name__ == "__main__":
    main()