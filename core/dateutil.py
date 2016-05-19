# -*- coding: utf-8 -*-

import time
from datetime import datetime, timedelta
import re

days_name2days_count = {
	'current_day': 0,
	'one_week': 6,
	'two_weeks': 14,
	'one_month': 31,
	'today': 0,
	'yesterday': -1,
}

#用于解析日期的格式
date_fmt = "%Y-%m-%d"

CURRENT_DAY = 0
ONE_WEEK_DAYS = 6

ONEDAY_MODE = 'oneday'
WEEK_MODE = 'week'
MONTH_MODE = 'month'
RANGE_MODE = 'range'


def get_date_range(date_str, past_days, future_days=0):
	"""
	获取一段时间的第一天和最后一天
	参数:
		date_str: 基准日期 格式 '%Y-%m-%d'
		past_days: 
		future_days:
	"""
	#获取基准日期
	cur_date = datetime.strptime(date_str, date_fmt).date()
	
	#如果是日期段，特殊处理
	if '~' in past_days:
		low_date, high_date = past_days.split('~')
		low_date = datetime.strptime(low_date, date_fmt).date()
		high_date = datetime.strptime(high_date, date_fmt).date()
		
		total_days = (high_date - low_date).days + future_days + 1
		if total_days == 1:
			total_days = 2
		
		return total_days, low_date, cur_date, high_date
	
	#获取时间范围的左边界
	try:
		past_days = int(past_days) #天数
	except:
		past_days = days_name2days_count[past_days] #特定字符
		
	if past_days == 0:
		#只取一天的数据
		low_date = cur_date
		high_date = cur_date
	elif past_days == -1:
		#只取前一天的数据
		past_days = 0
		low_date = cur_date - timedelta(1)
		high_date = cur_date - timedelta(1)
	elif past_days == 'month':
		#获取一个月的第一天和最后一天
		low_date = cur_date.replace(day = 1)
		high_date = cur_date
		past_days = int(str(high_date - low_date)[:2])
	else:
		low_date = cur_date - timedelta(past_days)
		high_date = cur_date
		if future_days != 0:
			high_date = cur_date + timedelta(future_days)

	#确定总的天数
	total_days = past_days + future_days + 1
	if total_days == 1:
		total_days = 2

	return total_days, low_date, cur_date, high_date


def create_date_range(user, mode, date_str):
	range_str = None
	if date_str == 'today':
		date_str = time.strftime('%Y-%m-%d')
	if mode in days_name2days_count:
		range_str = mode
		mode = RANGE_MODE

	if mode == ONEDAY_MODE:
		return OneDay(date_str)
	elif mode == WEEK_MODE:
		return Week(date_str, user.get_profile().week_start)
	elif mode == MONTH_MODE:
		return Month(date_str, user.get_profile().month_start)
	else:
		if range_str:
			total_days, low_date, cur_date, high_date = get_date_range(date_str, range_str)
			range_str = '%s~%s' % (low_date.strftime('%Y-%m-%d'), high_date.strftime('%Y-%m-%d'))
			return DateRange(date_str, range_str)
		else:
			return DateRange(date_str)

		
class DateRange(object):
	def __init__(self, cur_date, range_str=''):
		self.first_day = None
		self.last_day = None
		self.range = None
		if '~' in cur_date:
			self.cur_day = cur_date
		else:
			self.cur_day = datetime.strptime(cur_date, date_fmt).date()
		self.cn_str = None
		if range_str:
			self._parse(range_str)
		else:
			self._parse(cur_date)

		self.days = (self.last_day - self.first_day).days + 1

	def _parse(self, date_str):
		first, last = date_str.split('~')
		self.first_day = datetime.strptime(first, date_fmt).date()
		self.last_day = datetime.strptime(last, date_fmt).date()

		self.range = u'%s~%s' % (self.first_day.strftime(date_fmt), self.last_day.strftime(date_fmt))
		self.format_cn()

	def format_cn(self):
		first_day = self.first_day
		last_day = self.last_day
		if last_day == first_day:
			self.cn_str = u'%s年%s月%s日' % (first_day.year, first_day.month, first_day.day)
		else:
			self.cn_str = u'%s年%s月%s日~%s月%s日' % (first_day.year, first_day.month, first_day.day, last_day.month, last_day.day)

	def plus(self, days):
		self.last_day = self.last_day + timedelta(days)
		self.range = u'%s~%s' % (self.first_day.strftime(date_fmt), self.last_day.strftime(date_fmt))
		self.format_cn()

	def days(self):
		return self.days

	def __str__(self):
		return self.range

	def cn_str(self):
		return self.cn_str

	def is_week(self):
		return False

	def is_month(self):
		return False

	def is_one_day(self):
		return False

	def is_range(self):
		return True

#===============================================================================
# OneDay : 表示当天
#===============================================================================
class OneDay(DateRange):
	def __init__(self, cur_date, date_str=''):
		DateRange.__init__(self, cur_date, cur_date)
		self._yesterday = None

	def _parse(self, date_str):
		date = datetime.strptime(date_str, date_fmt).date()
		self.cur_day = date
		self.first_day = date
		self.last_day = date
		self.range = date.strftime(date_fmt)
		self.format_cn()

	@property
	def yesterday(self):
		if not self._yesterday:
			yesterday_date = self.cur_day - timedelta(1)
			self._yesterday = OneDay(yesterday_date.strftime(date_fmt))

		return self._yesterday

	def plus(self, days):
		pass

	def is_week(self):
		return False

	def is_month(self):
		return False

	def is_one_day(self):
		return True

	def is_range(self):
		return False


#===============================================================================
# Week : 表示一周
#===============================================================================
class Week(DateRange):
	def __init__(self, cur_date, week_start=1, range_str=''):
		self.week_start = week_start
		DateRange.__init__(self, cur_date, range_str)
		self._last_week = None

	def _parse(self, date_str):
		if '~' in date_str:
			DateRange._parse(self, date_str)
		else:
			date = datetime.strptime(date_str, date_fmt).date()
			self.cur_day = date
			delta = date.isoweekday() - self.week_start
			if delta < 0:
				date = date - timedelta(7)
			self.first_day = date - timedelta(delta)
			self.last_day = date + timedelta(6-delta)
			self.range = u'%s~%s' % (self.first_day.strftime(date_fmt), self.last_day.strftime(date_fmt))
			self.format_cn()

	def plus(self, days):
		pass

	@property
	def last_week(self):
		if not self._last_week:
			last_week_first_day = self.first_day - timedelta(7)
			self._last_week = Week(str(last_week_first_day), self.week_start)

		return self._last_week

	def is_week(self):
		return True

	def is_month(self):
		return False

	def is_one_day(self):
		return False

	def is_range(self):
		return False


#===============================================================================
# Month : 表示一月
#===============================================================================
class Month(DateRange):
	def __init__(self, cur_date, month_start=1, range_str=''):
		self._month_start = month_start
		DateRange.__init__(self, cur_date, range_str)
		self._last_month = None

	def _parse(self, date_str):
		if '~' in date_str:
			DateRange._parse(self, date_str)
		else:
			date = datetime.strptime(date_str, date_fmt).date()
			self.cur_day = date
			day_of_month = date.day
			#确定月的第一天
			if day_of_month >= self._month_start:
				self.first_day = date.replace(day = self._month_start)
			else:
				try:
					self.first_day = date.replace(month=date.month-1, day=self._month_start)
				except:
					self.first_day = date.replace(year=date.year-1, month=12, day=self._month_start)

			#确定月的最后一天
			try:
				self.last_day = self.first_day.replace(month = self.first_day.month + 1) - timedelta(1)
			except:
				self.last_day = self.first_day.replace(year = self.first_day.year + 1, month = 1) - timedelta(1)

			self.range = u'%s~%s' % (self.first_day.strftime(date_fmt), self.last_day.strftime(date_fmt))
			self.format_cn()

	def plus(self, days):
		pass

	@property
	def last_month(self):
		if not self._last_month:
			last_month_date = self.first_day - timedelta(days=1)
			self._last_month = Month(str(last_month_date), self._month_start)

		return self._last_month

	def is_week(self):
		return False

	def is_month(self):
		return True

	def is_one_day(self):
		return False

	def is_range(self):
		return False
	

#===============================================================================
# get_today : 获得当天
#===============================================================================
def get_today():
	return time.strftime("%Y-%m-%d")
	
#===============================================================================
# normalize_date : 转换date成统一格式
#===============================================================================
def normalize_date(date):
	if 'today' == date:
		date = time.strftime("%Y-%m-%d")
	return date


#===============================================================================
# is_today : 判断是否是今天
#===============================================================================
def is_today(date):
	return date == 'today' or date == time.strftime("%Y-%m-%d")


#===============================================================================
# get_previous_date: 得到今天之前n天的时间
#===============================================================================
def get_previous_date(from_date, days):
	if from_date == 'today':
		#from_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		from_date = time.strftime(date_fmt)

	from_date = datetime.strptime(from_date, date_fmt).date()
	date = from_date - timedelta(int(days))

	return date.strftime(date_fmt)


#===============================================================================
# get_yesterday_date: 得到昨天的日期
#===============================================================================
def get_yesterday_date(today_date):
	return datetime.strptime(today_date, date_fmt).date() - timedelta(1)

def get_yesterday_str(date_str):
	if 'today' == date_str:
		date_str = time.strftime(date_fmt)
		
	yesterday_date = datetime.strptime(date_str, date_fmt).date() - timedelta(1)
	return yesterday_date.strftime(date_fmt)

#===============================================================================
# get_tomorrow_date: 得到昨天的日期
#===============================================================================
def get_tomorrow_date(today_date):
	return datetime.strptime(today_date, date_fmt).date() + timedelta(1)

def get_tomorrow_str(date_str):
	if 'today' == date_str:
		date_str = time.strftime(date_fmt)

	tomorrow_date = datetime.strptime(date_str, date_fmt).date() + timedelta(1)
	return tomorrow_date.strftime(date_fmt)


#===============================================================================
# get_date_range_list : 获取一段时间的日期列表
#===============================================================================
def get_date_range_list(low_date, high_date):
	date_list = []
	loop_date = low_date
	while loop_date <= high_date:
		date_list.append(loop_date)
		loop_date += timedelta(1)

	return date_list

#===============================================================================
# get_current_time_in_millis : 获取当前时间（long类型）
#===============================================================================
def get_current_time_in_millis():
	return int(round(time.time() * 1000))

def yearsafter(years, from_date=None):
    if from_date is None:
        from_date = datetime.now()

    try:
        return from_date.replace(year=from_date.year + years)
    except:
        # Must be 2/29!
        assert from_date.month == 2 and from_date.day == 29 # can be removed
        return from_date.replace(month=2, day=28, 
                                 year=from_date.year+years)

def is_timespan_beyond_the_interval_util(start_datetime, seconds):
	if (start_datetime is None):
		return False

	span = datetime.now() - start_datetime
	return span > timedelta(seconds=seconds)


#===============================================================================
# get_datetime_before_by_hour: 得到N小时之前的日期
#===============================================================================
def get_datetime_before_by_hour(hours):
	return datetime.now()-timedelta(hours=hours)


#===============================================================================
# get_datetime_from_timestamp: 根据时间戳解析datetime
#===============================================================================
def get_datetime_from_timestamp(parse_timestamp):
	return datetime.fromtimestamp(int(parse_timestamp))


#===============================================================================
# get_timestamp_from_datetime: 根据datetime获取时间戳
#===============================================================================
def get_timestamp_from_datetime(parse_datetime):
	return int(time.mktime(parse_datetime.timetuple()))


PATTERN_DATE = re.compile("(\d{4})-(\d{1,2})-(\d{1,2})")
def get_date_string(datetime_string):
	"""
	用正则表达式匹配date

	举例：输入可以为 
	 * 1981-05-08
	 * 1981-5-8
	 * 1981-5-08
	"""
	result = PATTERN_DATE.search(datetime_string)
	date_string = None
	if len(result.groups()) == 3:
		date_string = "%s-%02d-%02d" % (result.group(1), int(result.group(2)), int(result.group(3)))
	return date_string
