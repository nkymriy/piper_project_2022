#coding:utf-8
import smbus
import time
import sys

# Define some device parameters
I2C_ADDR  = 0x27 # I2C device address, if any error, change this address to 0x3f
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

def lcd_init():
	# Initialise display
	lcd_byte(0x33,LCD_CMD) # 110011 Initialise
	lcd_byte(0x32,LCD_CMD) # 110010 Initialise
	lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
	lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
	lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
	lcd_byte(0x01,LCD_CMD) # 000001 Clear display
	time.sleep(E_DELAY)

def lcd_byte(bits, mode):
	# Send byte to data pins
	# bits = the data
	# mode = 1 for data
	#        0 for command

	bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
	bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT
	
	# High bits
	bus.write_byte(I2C_ADDR, bits_high)
	lcd_toggle_enable(bits_high)

	# Low bits
	bus.write_byte(I2C_ADDR, bits_low)
	lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
	# Toggle enable
	time.sleep(E_DELAY)
	bus.write_byte(I2C_ADDR, (bits | ENABLE))
	time.sleep(E_PULSE)
	bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
	time.sleep(E_DELAY)

def lcd_string(message,line):
	# Send string to display

	message = message.ljust(LCD_WIDTH," ")

	lcd_byte(line, LCD_CMD)

	for i in range(LCD_WIDTH):
		lcd_byte(ord(message[i]),LCD_CHR)

def lcd_string_kana(message,line):
	#文字コードnの文字 ＝ n番目の文字
	codes = u'線線線線線線線線線線線線線線線線　　　　　　　　　　　　　　　　!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}→←　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　。「」、・ヲァィゥェォャュョッーアイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワン゛゜αäβεμσρq√陰ι×￠￡nöpqθ∞ΩüΣπxν千万円÷　塗'
	#変換する文字の辞書(ex.「バ」＝「ハ」「゛」)
	dic ={u'ガ':u'カ゛',u'ギ':u'キ゛',u'グ':u'ク゛',u'ゲ':u'ケ゛',u'ゴ':u'コ゛',u'ザ':u'サ゛',u'ジ':u'シ゛',u'ズ':u'ス゛',u'ゼ':u'セ゛',u'ゾ':u'ソ゛',u'ダ':u'タ゛',u'ヂ':u'チ゛',u'ヅ':u'ツ゛',u'デ':u'テ゛',u'ド':u'ト゛',u'バ':u'ハ゛',u'ビ':u'ヒ゛',u'ブ':u'フ゛',u'ベ':u'ヘ゛',u'ボ':u'ホ゛',u'パ':u'ハ゜',u'ピ':u'ヒ゜',u'プ':u'フ゜',u'ペ':u'ヘ゜',u'ポ':u'ホ゜',u'℃':u'゜C'}
	message = message.ljust(LCD_WIDTH," ")
	lcd_byte(line, LCD_CMD)
	
	#濁音など、文字の変換
	message2 = ""
	for i in range(LCD_WIDTH):
		if ( message[i] in dic.keys() ):
			message2 += dic[message[i]]
		else:
			message2 += message[i]
	
	#文字コードのリストにある文字なら表示、それ以外は表示しない
	for i in range(LCD_WIDTH):
		if (codes.find(message2[i]) >= 0):
			lcd_byte(codes.find(message2[i])+1,LCD_CHR)
		elif (message2[i] != u' '):
			print("No such character!    :" + message2[i])

if __name__ == '__main__':

	try:
		main()
	except KeyboardInterrupt:
		pass
	#finally:
		#lcd_byte(0x01, LCD_CMD)