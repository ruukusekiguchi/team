import RPi.GPIO as GPIO
import time

# 初期設定
GPIO.setmode(GPIO.BCM)

# GPIO 15 をデジタル入力に設定
GPIO.setup(15, GPIO.IN)

try:
    # Ctrl-C 待ち
    while True:
        print(GPIO.input(15))
        # print "%s GPIO 15 is %d" % (time.strftime("%Y/%m/%d %H:%M:%S"), GPIO.input(15))

        if GPIO.input(15) == 1:
            print ("晴れています")
        else:
            print ("雨だー")

        time.sleep(1.0)

except:
    print ("interrupted")

finally:
    GPIO.cleanup()
