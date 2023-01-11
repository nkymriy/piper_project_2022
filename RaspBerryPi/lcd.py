# -*- coding: utf-8 -*-
import i2clcdb as lcd
import time
import RPi.GPIO as GPIO
import dht11
import json
import datetime

# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

# read data using pin 14
#instance = dht11.DHT11(pin=14)
instance = dht11.DHT11(pin=24)


def main():
	lcd.lcd_init()
	try:
		while True:
			result = instance.read()
			if result.is_valid():
				print("Last valid input: " + str(datetime.datetime.now()))

				print("Temperature: %-3.1f C" % result.temperature)
				print("Humidity: %-3.1f %%" % result.humidity)
				
				line1 = f"{datetime.datetime.now():%m/%d　%H:%M:%S}"
				line2 = f"{result.temperature}゜C　{result.humidity}%　デス。"

				lcd.lcd_string_kana(line1, lcd.LCD_LINE_1)
				lcd.lcd_string_kana(line2, lcd.LCD_LINE_2)
				temp_dic = {
					"temp":result.temperature,
					"huid":result.humidity
				}
				tempture_file = open("tempture.json", "w")
				tempture_file.write(json.dumps(temp_dic))
				tempture_file.close()

			time.sleep(0.5)

	except KeyboardInterrupt:
		print("Cleanup")
		GPIO.cleanup()
	
	time.sleep(1)

	lcd.lcd_init()
	lcd.lcd_toggle_enable(0x01)

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		#pass
		lcd.lcd_byte(0x01, lcd.LCD_CMD)
	finally:
		lcd.lcd_byte(0x01, lcd.LCD_CMD)