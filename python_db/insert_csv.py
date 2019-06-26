from mysqlEngine import get_engine
import pandas as pd
import wx
import traceback

# ダイアログ用
app = wx.App()

# SQL engine
engine = get_engine()

# ファイル選択 キャンセルの場合終了
selected_file = wx.FileDialog(None, style=wx.DD_CHANGE_DIR, message='ファイルを選択')
if selected_file.ShowModal() == wx.ID_OK:
    selected_file = selected_file.GetPath()
else:
    wx.MessageDialog(None, 'end', '', style=wx.OK).ShowModal()
    sys.exit()
print('対象ファイル:' + selected_file)

# テーブル名 小文字に変換する
print('テーブル物理名を入力 e.g:BSS_TJ049...')
table_name = input('>>> ').lower()

# sql
truncate = f'truncate table {table_name}'

csvReader = pd.read_csv(
    selected_file
    , dtype = 'object'
    , engine='python'
    , chunksize=50000
    )

for csv in csvReader:
    print(counter)
    try:
        csv.to_sql(
            table_name
            , engine
            , index=False
            , if_exists='append'
            )
    except:
        traceback.print_exc()
        wx.MessageDialog(None, 'Error!!', '', style=wx.OK).ShowModal()
