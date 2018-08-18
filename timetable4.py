import RPi.GPIO as GPIO
import time
import random
import sys
import select
import multiprocessing
import os
#
def enter_a_number(stdin,q):
  #print("Please enter a number")
  number = stdin.readline()
  q.put(number)
#
def setup():
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BOARD) # Numbers GPIOs based on physical location
  GPIO.setup(ledPin, GPIO.OUT) # Set ledPin to output mode
  GPIO.output(ledPin, GPIO.LOW) # Set ledPin low to turn off led
#
def setup_countdown():
  GPIO.setmode(GPIO.BOARD) # Number GPIOs by its physical location
  GPIO.setup(dataPin, GPIO.OUT)
  GPIO.setup(latchPin, GPIO.OUT)
  GPIO.setup(clockPin, GPIO.OUT)
#
def shiftOut(dPin,cPin,order,val):
  for i in range(0,8):
    GPIO.output(cPin,GPIO.LOW);
    if(order == LSBFIRST):
      GPIO.output(dPin,(0x01&(val>>i)==0x01) and GPIO.HIGH or GPIO.LOW)
    elif(order == MSBFIRST):
      GPIO.output(dPin,(0x80&(val<<i)==0x80) and GPIO.HIGH or GPIO.LOW)
    GPIO.output(cPin,GPIO.HIGH);
#
def right(currentscore):
  setup()
  GPIO.output(ledPin, GPIO.HIGH) # led is turned on
  time.sleep(1)
  GPIO.output(ledPin, GPIO.LOW) # led is turned off
  print 'well done'
  newscore = currentscore + 1
  print 'your score is: ' + str(newscore)
  return newscore
#
def wrong(finalscore,timeout=0):
  setup()
  GPIO.output(ledPin, GPIO.HIGH) # led is turned on
  time.sleep(2)
  setup()
  GPIO.output(ledPin, GPIO.LOW) # led is turned off
  print 'Looser!!!!'
  print 'Anwser was: ' + str(a*b)
  if timeout == 1:
    print 'too slow!!'
#
def destroy(): # When 'Ctrl+C' is pressed, the function is executed.
  GPIO.cleanup()
#  
if __name__ == '__main__':
  try:
    score = 0
    coutdown = 5
    print 'you have ' + str(coutdown) + ' seconds to answer'
    while True:
      a = random.randint(0,12)
      b = random.randint(0,12)
      print str(a) + 'x' + str(b) + '='
      queue1 = multiprocessing.Queue()
      newstdin = os.fdopen(os.dup(sys.stdin.fileno()))
      p = multiprocessing.Process(target=enter_a_number, name="Foo", args=(newstdin,queue1))
      p.start()
      for second in range(0,coutdown):
        LSBFIRST = 1
        MSBFIRST = 2
        dataPin = 11 #DS Pin of 74HC595(Pin14)
        latchPin = 13 #ST_CP Pin of 74HC595(Pin12)
        clockPin = 15 #SH_CP Pin of 74HC595(Pin11)
        num = [0x92,0x99,0xb0,0xa4,0xf9]
        setup_countdown()
        GPIO.output(latchPin,GPIO.LOW)
        shiftOut(dataPin,clockPin,MSBFIRST,num[second])
        GPIO.output(latchPin,GPIO.HIGH)
        time.sleep(1)
        if p.is_alive():
          pass
        else:
          result = queue1.get()
          break
      else:
        ledPin = 33
        wrong(finalscore=score,timeout=1)
        destroy()
        break
      if int(result) == a*b:
        ledPin = 12
        score = right(currentscore=score)
      else:
        ledPin = 33
        wrong(finalscore=score,timeout=0)
        destroy()
        break
    print '-'*10
  except KeyboardInterrupt:
    destroy()
    dataPin = 11
    latchPin = 13
    clockPin = 15
    destroy()
