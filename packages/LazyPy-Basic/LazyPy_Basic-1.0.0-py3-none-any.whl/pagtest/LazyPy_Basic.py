#LazyPy_Basic
#by Lingtu/Ouzijie
import time
import calendar

def p(i):
          print(i)

def ts(i):
          time.sleep(i)

def ip(i):
          return input(i)

def gd():
          return  time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())

def tt():
          return time.time()

def cm(y, m):
          return calendar.month(y, m)




