#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gspread
import sys
import json
import pandas as pd
import shutil
import os
import re
from oauth2client.service_account import ServiceAccountCredentials
import ast

# modelファイル作成
def save_model(new_dir_path, new_filename, new_file_content, mode='w'):
    os.makedirs(new_dir_path, exist_ok=True)
    with open(os.path.join(new_dir_path, new_filename), mode,encoding='utf-8') as f:
        f.write(new_file_content)

def read_sheet(sheet_name, SECRET_JSON, SPREADSHEET_KEY):
    # 2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    # Googleの各サービスへアクセスできるservice変数を生成
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        SECRET_JSON, scope)

    # OAuth2の資格情報を使用してGoogle APIにログイン
    gc = gspread.authorize(credentials)

    # 共有設定したスプレッドシートを開く
    wb = gc.open_by_key(SPREADSHEET_KEY)
    ws = wb.worksheet(sheet_name)

    # DataFrameに保存 1行目columns 2行目まで削除
    df = pd.DataFrame(ws.get_all_values())
    df.columns = list(df.loc[0, :])
    df.drop([0,1], inplace=True)
    df.reset_index(inplace=True)
    df.drop('index', axis=1, inplace=True)
    for i in range(len(df.columns)):
        df.iloc[:, i] = pd.to_numeric(df.iloc[:, i], errors='ignore')
    return df

if __name__ == '__main__':
  args = sys.argv
  PROJECT_ID = args[1]
  PRIVATE_KEY_ID = args[2]
  PRIVATE_KEY = args[3]
  CLIENT_EMAIL = args[4]
  CLIENT_ID = args[5]
  CLIENT_X509_CERT_URL = args[6]
  SPREADSHEET_KEY = args[7]

  SECRET_JSON = {
    'type': 'service_account',
    'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
    'token_uri': 'https://oauth2.googleapis.com/token',
    'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs'
  }
  SECRET_JSON['project_id'] = PROJECT_ID
  SECRET_JSON['private_key_id'] = PRIVATE_KEY_ID
  SECRET_JSON['private_key'] = re.sub('@',' ',re.sub('\\\\n','\n',PRIVATE_KEY))
  SECRET_JSON['client_email'] = CLIENT_EMAIL
  SECRET_JSON['client_id'] = CLIENT_ID
  SECRET_JSON['client_x509_cert_url'] = CLIENT_X509_CERT_URL
  
  # modelフォルダを削除
  if os.path.exists('assets/minecraft/models/item'):
    shutil.rmtree('assets/minecraft/models/item')

  ### アイテム
  # シートを取得
  df = read_sheet('アイテム', SECRET_JSON, SPREADSHEET_KEY)
  df = df.drop(0)
  df = df[df['CMD']>=1]
  df = df.sort_values(['ID','CMD'])

  # CustomModel出力
  for i in df.index:
    if df.loc[i,'ID'] == 'bow':
      model_list = ['','_pulling_0','_pulling_1','_pulling_2']
    elif df.loc[i,'ID'] == 'crossbow':
      model_list = ['','_arrow','_firework','_pulling_0','_pulling_1','_pulling_2']
    elif df.loc[i,'ID'] == 'fishing_rod':
      model_list = ['','_cast']
    else:
      model_list = ['']

    for j in model_list:
      export_dir = 'assets/minecraft/models/item/' + df.loc[i,'ID']
      export_json = json.dumps(json.loads(df.loc[i,'model' + j]), indent=4)
      export_json = re.sub('"(rotation|translation|scale)": \[\n +(.*),\n +(.*),\n +(.*)\n +\]', '"\\1": [ \\2, \\3, \\4]', export_json)
      new_filename = df.loc[i,'US名 / ModelName'] + j + '.json'
      save_model(export_dir, new_filename, export_json)
  
  ### アイテム計算用
  # シートを取得
  df = read_sheet('アイテム計算用', SECRET_JSON, SPREADSHEET_KEY)
  df = df[df['model_item']!='']

  # CMD=1ならItemModel出力
  for i in df.index:
    export_dir = 'assets/minecraft/models/item'
    export_json = json.dumps(json.loads(df.loc[i,'model_item']), indent=4)
    if df.loc[i,'ID'] not in ['bow','crossbow','fishing_rod']:
      export_json = re.sub('\{\n +"predicate": \{\n +"custom_model_data": ([0-9]+)\n +\},\n +"model": "(.*)"\n +\}', '{ "predicate": {"custom_model_data": \\1}, "model": "\\2"}', export_json)
    export_json = re.sub('"(rotation|translation|scale)": \[\n +(.*),\n +(.*),\n +(.*)\n +\]', '"\\1": [ \\2, \\3, \\4]', export_json)
    new_filename = str(df.loc[i,'ID']) + '.json'
    save_model(export_dir, new_filename, export_json)

  ### エンチャント
  # シートを取得
  df = read_sheet('エンチャント', SECRET_JSON, SPREADSHEET_KEY)

  # CustomModel出力
  for i in df.index:
    for j in ['shards','gemstone','crystal','jewel']:
      if df.loc[i,'テクスチャ_' + j] == 'TRUE':
        export_dir = 'assets/minecraft/models/item/gold_nugget/' + df.loc[i,'石名US']
        export_json = json.dumps(json.loads(df.loc[i,'model_' + j]), indent=4)
        new_filename = j + '.json'
        save_model(export_dir, new_filename, export_json)
