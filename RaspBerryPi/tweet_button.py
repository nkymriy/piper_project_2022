import RPi.GPIO as GPIO
import time
import sys
import twitter_client

# LED_GPIO 変数に 24をセット
SW_GPIO = 22

# GPIO.BCMを設定することで、GPIO番号で制御出来るようになります。
GPIO.setmode(GPIO.BCM)

# GPIO.INを設定することで、入力モードになります。
# pull_up_down=GPIO.PUD_DOWNにすることで、内部プルダウンになります。
GPIO.setup(SW_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

LastStatus = False
# ボタン押し / 離し 動作確認用コード
while True:
    try:
        # GPIO24の値を読み込み、その値を出力します。
        # ボタンを押すと"1"（High）、離すと"0"（Low）。
        SwitchStatus = GPIO.input(SW_GPIO)
        #print(SwitchStatus)
        if LastStatus != SwitchStatus:
            print(SwitchStatus)
            
            if SwitchStatus == 0:
                twitter_client.tweet_tempture()
                time.sleep(10)
                
            time.sleep(0.2)
        LastStatus = SwitchStatus
            
    # Ctrl+Cキーを押すと処理を停止
    except KeyboardInterrupt:
        # ピンの設定を初期化
        # この処理をしないと、次回 プログラムを実行した時に「ピンが使用中」のエラーになります。
        GPIO.cleanup()
        sys.exit()
