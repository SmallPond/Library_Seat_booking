# 图书馆座位自动预约脚本

> author:db

> data  : 2018.3.14   3.31

> version: v0.1        v0.3

> v0.3 进一步完善了预约逻辑问题

## 一、依赖库
-	requests
-	demjson
>**均可通过pip 安装**

## 二、说明：
### 因无法直接绕过图书馆座位预约系统的登录过程，同时为简化脚本程序，此脚本通过cookie实现的身份认证，cookie需要通过Fiddler抓包获取。

### **故脚本中需要修改的数据**
-	_username
-	cookies
> 其中均以xx表示

## 三、在ubuntu中添加crontab定时运行
	crontab -e

	# For more information see the manual pages of crontab(5) and cron(8)
	#
	# m h  dom mon dow   command
	
	1 0 * * * python /home/alipond/workspaces/pyPro/library/library_seat_db.py

## 结果

><center><img src = "result.png" width='360' height='580'></center>