#! /usr/bin/env python3
# _*_ coding:utf-8 _*_


import requests
import time
import demjson
from datetime import datetime
from datetime import timedelta

#--------------------修改相应数据--------------------------
# 修改相应用户名
_username = "xx"

cookies = {
	'auth':'xxxxxx',
	'uid':'xxxxxx',
	'web_language':'en-us',
	'api_access_token':'qu8aBYUKRZenKNKooMzHtkg8qrIhUzYrebsXyfwzoETp9VadbojRts8cEBBzeQo_5a5ffab68679f47d2955ae13',
 
}
#--------------------修改相应数据--------------------------


_error_repeat =  "" + _username + "已有的预约，与当前预约时间有重叠"

# 日志文件 crontab需要书写绝对路径
_log_file = open("/home/alipond/workspaces/pyPro/library/log.txt","w+")

# 开始时间,只能设置为整数
# 时:分:秒
_begin_time = "9:00:00"

# 预约时长，服务器接收数据以秒为单位
# 此处以小时为单位
# 若更改开始时间，并且还需要预约到晚上十点需要对应更改_duration 
_duration = 13



request_url = 'https://hdu.huitu.zhishulib.com/Seat/Index/bookSeats?LAB_JSON=1 '

header = {

    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Mobile/14D27 MicroMessenger/6.6.5 NetType/WIFI Language/en',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Referer': 'https://hdu.huitu.zhishulib.com/Content/Index/startUp',
    'Origin': 'https://hdu.huitu.zhishulib.com',
    'Accept-Encoding': 'gzip, deflate',
}

datas = {
	# 开始时间
    'beginTime': '1520982000',
	# 预定时长  46800-13个小时
    'duration' : '46800',
	# 位置号  1为固定数，座位号前补零到5位数   比如，4号作为则位 10004
    'seats[0]' : '10072',
	# 固定的数
    'seatBookers[0]': '40432',
}


def ReserveSeat():
	set_time = (int)(datas['beginTime'])
	now = time.time()
	
	
	if set_time <= now:
		_log_file.write("[-] {0}设定的开始时间在当前时间之前\n".format(time.strftime("%Y-%m-%d ", time.localtime())))
		# 设定时间小于当前时间，则跳过当天的预定
		return 
	
	r = requests.post(request_url, data=datas, headers=header, cookies = cookies,verify=False)
	# 暂存座位号
	seat = datas['seats[0]']
	
	while r.json()['DATA']['result'] != 'success':
		if r.json()['DATA']['msg'] == _error_repeat:
			_log_file.write("{0}已有的预约，与当前预约时间有重叠\n".format(time.strftime("%Y-%m-%d ", time.localtime())))
			break
			
		_log_file.write("{0} : 预约座位{1}失败哦，换一个座位再试试\n".format(time.strftime("%Y-%m-%d", time.localtime()), datas['seats[0]']))
		book_seat_num = (int)(datas['seats[0]']) - 1
		if book_seat_num <= 0:
			# 预约到1号座位还未预约成功则退出
			break
		
		datas['seats[0]'] = (str)(book_seat_num)
		r = requests.post(request_url, data=datas, headers=header, cookies = cookies,verify=False)	
	# print(r.json())	
	# 恢复之前的座位号
	datas['seats[0]'] = seat
	
def SetDuration():
	datas['duration'] = (str)(_duration * 3600)
	
	
def GetNextDay():
	'''
		返回值： 返回下一天的日期
	'''
	now = datetime.now()
	aDay = timedelta(days=1)
	now = now + aDay
	set_time = now.strftime('%Y-%m-%d '+ _begin_time)
	return set_time
	
def SetBeginTime(set_time):

	# 服务器需要整型数据
	
	begin_time = (str)((int)(time.mktime(time.strptime(set_time,"%Y-%m-%d %H:%M:%S"))))
	datas['beginTime'] = begin_time
	print(datas['beginTime'])
	
def main():
	
	SetDuration()
	# 预约第一天
	# 获取当前时间
	set_time = time.strftime("%Y-%m-%d " + _begin_time, time.localtime()) 
	SetBeginTime(set_time)
	ReserveSeat()
	
	# 预约第二天
	set_time = GetNextDay()
	SetBeginTime(set_time)
	ReserveSeat()

if __name__ == '__main__':
	main()