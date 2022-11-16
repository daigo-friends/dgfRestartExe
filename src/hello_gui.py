import os
import subprocess
import sys
import PySimpleGUI as sg

pid = os.getpid()
print('pid:%s' % os.getpid())

args_len = len(sys.argv)

# ウィンドウの内容を定義する
layout = [
    [sg.Text('Hello world. ')],
    [sg.Text('')],
    [sg.Text('pid: %s' % str(pid))],
    [sg.Text('args_len: %s' % str(args_len))],
    [sg.Text('')],
    [sg.Button('再起動'), sg.Button('再起動(タイムアウト)'), sg.Button('終了')],
]

for count, value in enumerate(sys.argv):
    layout.insert(4 + count, [sg.Text('    args[%s]:%s' % (count, value))])

# ウィンドウを作成する
window = sg.Window('自身を再起動するテスト', layout, size=(640,480))

# イベントループを使用してウィンドウを表示し、対話する
while True:
    event, values = window.read()
    # ユーザーが終了したいのか、ウィンドウが閉じられたかどうかを確認してください
    if event == sg.WINDOW_CLOSED or event == '終了':
        break
    elif event == '再起動':
        result = subprocess.Popen('dgfRestartExe.exe %s %s' % (str(pid), '"hello_gui a b c"'), shell=False)
        break
    elif event == '再起動(タイムアウト)':
        result = subprocess.Popen('dgfRestartExe.exe %s %s' % (str(pid), '"hello_gui a b c"'), shell=False)
        # 自分自身を終了しなければタイムアウトする⇒dgfRestartExe.logを確認する

# 画面から削除して終了
window.close()