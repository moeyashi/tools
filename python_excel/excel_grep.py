"""
D:\01_work\00_店舗情報系\SVN\32_DPD作成中成果物(FJ) から文字列をGREP
"""
import os
import datetime
import csv
import pandas as pd
import wx
import sys

__CURDIR = 'C:\\01_work\\01_ANLS\\SVN\\32_DPD作成中成果物(FJ)'
__SUFFIX = ('.xlsx', '.xls', '.xlsm')
__OUTPUTDIR = 'C:\\01_work\\98_python\\python_excel'

# ダイアログ用
app = wx.App()

#### 対象フォルダからExcelファイルを抽出
def excel_walk(folder, recursive=False):
    if recursive:
        for root, dirs, files in os.walk(folder):
            for file in files:
                if os.path.splitext(file)[1] in __SUFFIX:
                    yield (root, file)
    else:
        for file in os.listdir(folder):
            if os.path.splitext(file)[1] in __SUFFIX:
                yield (folder, file)

#### 対象ファイルのすべてのシートからGREP
def grep(root, file, grepword):
    try:
        book = pd.ExcelFile(os.path.join(root, file))
        for sheet in book.sheet_names:
            df = book.parse(
                sheet
                , header=None
                , index_col=None
                )
            for i, row in df.iterrows():
                for word in row:
                    if grepword in str(word):
                        yield (sheet, i + 1, word)
    except Exception as e:
        print(e)
        e = 'error'
        yield (e, e, e)

# フォルダ選択 キャンセルの場合終了
folder = wx.DirDialog(None, style=wx.DD_CHANGE_DIR, message='フォルダを選択')
if folder.ShowModal() == wx.ID_OK:
    folder = folder.GetPath()
else:
    wx.MessageDialog(None, 'end', '', style=wx.OK).ShowModal()
    sys.exit()
print('対象folder:' + folder)

# 文字列入力
print('GREP対象の文字列を入力')
input_word = input('>>> ')
print('サブフォルダからも検索する y:サブフォルダからも検索する')
input_recursive = input('>>> ')

# 開始時間出力
print(datetime.datetime.now())

# ファイル削除
output_path = os.path.join(__OUTPUTDIR, 'grep_' + input_word + '.csv')
if os.path.exists(output_path):
    os.remove(output_path)

# 主処理
with open(output_path, 'w', newline='') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow(['path', 'file name', 'sheet_name', 'row', 'word'])
    
    for root, file in excel_walk(folder, input_recursive):
        #print(root + '/' + file)
        #writer.writerow([root, file, '', '', '']) #対象ファイルを出力
        for sheet, row, word in grep(root, file, input_word):
            writer.writerow([root, file, sheet, row, word])

# Excelにして出力
output_excelpath = os.path.join(__OUTPUTDIR, 'grep_' + input_word + '.xlsx')
if os.path.exists(output_excelpath):
    os.remove(output_excelpath)
pd.read_table(
    output_path
    , engine='python'
    ).to_excel(
    output_excelpath
    , index=False
    )

# 終了時間を出力
print(datetime.datetime.now())

# 終了
wx.MessageDialog(None, 'end', '', style=wx.OK).ShowModal()
