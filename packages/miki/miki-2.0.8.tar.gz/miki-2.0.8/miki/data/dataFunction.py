import pandas as pd 
import numpy as np 
from datetime import datetime, timedelta
import bcolz, pickle, os
from miki.data import dataGlovar


class DataFunction(object):
	@staticmethod
	def get_path(security, unit='1m'):
		# 存储路径设置
		if [security[:3], security[-1]] in [['300','E']] or [security[0], security[-1]] in [['6','G'],['0','E']]:
			param1 = 'stock'
			param2 = security[4:6]		
		elif [security[:3], security[-1]] in [['399','E']] or [security[0], security[-1]] in [['0','G']]:
			param1 = 'index'
			param2 = security[4:6]
		elif security[0] in ['1','5']:
			param1 = 'fund'
			param2 = security[4:6]			
		else:
			raise Exception('{} unknown name type'.format(security))
		param1 += unit
		path = '{}/{}/{}/{}'.format(dataGlovar.DataPath, param1, param2, security)
		return path
	@staticmethod
	def get_today_date_list():
		# 获取当天交易时间列表
		prefix = datetime.now().strftime('%Y-%m-%d')
		t1 = pd.to_datetime(prefix+' 09:31:00')
		t2 = pd.to_datetime(prefix+' 11:30:00')
		t3 = pd.to_datetime(prefix+' 13:01:00')
		t4 = pd.to_datetime(prefix+' 15:00:00')
		t5 = pd.to_datetime(datetime.now().strftime('%Y-%m-%d %H:%M:00'))
		date_list = []
		c = t1
		for i in range(480):
			date_list.append(c)
			c += timedelta(seconds=60)
		date_list = [i for i in date_list if ((t1<=i<=t2 or t3<=i<=t4) and i<=t5)]
		return date_list
	@staticmethod
	def to_bcolz(security_list, data, unit):		
		# shape: (num, dims, length)
		for i,security in enumerate(security_list):
			if unit=='1d':
				names = ['date','factor','open','high','low','close','volume','high_limit','low_limit','paused']
			else:
				names = ['date','factor','open','high','low','close','volume']
			path = DataFunction.get_path(security, unit)
			array = data[i].astype('float')
			if not os.path.exists(path):
				os.makedirs(path, exist_ok=True)
				table = bcolz.ctable(rootdir=path, columns=list(array), names=names, mode='w')
				table.flush()
			else:
				# 进行数据检查
				table = bcolz.open(path, mode='a')					
				date_index = table.names.index('date')
				array = array[:,array[0,:]>table[-1][date_index]]
				array = list(map(lambda x:tuple(x), array))
				table.append(array)
				table.flush()
	@staticmethod
	def to_redis(redisCon, now_data, security_list, now_time):
		# 数据字段：'date','factor','open','high','low','close','volume','high_limit','low_limit','paused'		
		now_time = str(now_time)
		field_list = ['date','factor','open','high','low','close','volume','high_limit','low_limit','paused']
		redisCon.set(now_time, pickle.dumps([now_data, security_list, field_list]))
		redisCon.expire(now_time, 60*60*24)
	@staticmethod
	def reshape(df, unit):
		# dataframe格式数据周期重组
		how = {'date':'last','open':'first','high':'max','low':'min','close':'last','volume':'sum'}
		df['date'] = df.index.values
		if unit in ['5m','15m','30m','60m','120m']:
			df = df.groupby(np.array(range(len(df)))//int(unit[:-1]))
		elif unit=='1d':
			df = df.groupby(lambda x:x.year+x.month*0.01+x.day*0.0001)
		elif unit=='1W':
			df = df.groupby(lambda x:x.year+x.week*0.01)
		elif unit=='1M':
			df = df.groupby(lambda x:x.year+x.month*0.01)
		else:
			raise Exception('only 5m,15m,30m,60m,120m,1d,1W,1M unit is available')
		df = df.agg(how).set_index('date')
		return df
	@staticmethod
	def get_stock_data(stock, unit, init_factor=None, field=None, start=None, end=None, limit=None):
		'''
		1.获取本地数据库的股票数据, 返回array，不存在返回None
		2.init_factor为初始除权因子
		3.field为None时，array返回格式为date,factor,open,high,low,close,volume
		4.param1: stock, unit, init_factor, end, limit
		  param2: stock, unit, init_factor, limit
		  param3: stock, unit, init_factor, start, end
		  param4: stock, unit, field
		'''
		if end is not None and limit is not None and init_factor is not None and start is None and field is None:
			# param1: stock, unit, init_factor, end, limit
			# array: date,factor,open,high,low,close,volume
			path = DataFunction.get_path(stock, unit=unit)
			ctable = bcolz.open(path, mode='r')
			ctable = ctable.fetchwhere('date<={}'.format(end.timestamp()))[-limit:]
			if len(ctable)==0:
				return None
			array = np.array(list(map(lambda x:list(x), ctable)))
			if unit=='1d':
				array = array[:,:7]	
			array[:,2:6] = array[:,2:6] * (array[:,1:2] / init_factor[stock])
			array[:,6:7] = array[:,6:7] * array[:,1:2]
			array = np.delete(array, 1, axis=1).round(2)
		elif start is not None and end is not None and init_factor is not None and limit is None and field is None:
			# param2: stock, unit, init_factor, start, end
			# array: date,factor,open,high,low,close,volume
			path = DataFunction.get_path(stock, unit=unit)
			ctable = bcolz.open(path, mode='r')
			if len(ctable)==0:
				return None
			ctable = ctable.fetchwhere('(date<={})&(date>={})'.format(end.timestamp(), start.timestamp()))
			if len(ctable)==0:
				return None
			array = np.array(list(map(lambda x:list(x), ctable)))
			if unit=='1d':
				array = array[:,:7]
			array[:,2:6] = array[:,2:6] * (array[:,1:2] / init_factor[stock])
			array[:,6:7] = array[:,6:7] * array[:,1:2]
			array = np.delete(array, 1, axis=1).round(2)
		elif limit is not None and init_factor is not None and start is None and end is None and field is None:
			# param3: stock, unit, init_factor, limit
			# array: date,factor,open,high,low,close,volume
			path = DataFunction.get_path(stock, unit=unit)
			if not os.path.exists(path):
				return None
			ctable = bcolz.open(path, mode='r')[-limit:]
			if len(ctable)==0:
				return None
			array = np.array(list(map(lambda x:list(x), ctable)))
			if unit=='1d':
				array = array[:,:7]	
			array[:,2:6] = array[:,2:6] * (array[:,1:2] / init_factor[stock])
			array[:,6:7] = array[:,6:7] * array[:,1:2]
			array = np.delete(array, 1, axis=1).round(2)
		elif init_factor is not None and limit is None and start is None and end is None and field is None:
			# param4: stock, unit, init_factor
			# array: date,factor,open,high,low,close,volume
			path = DataFunction.get_path(stock, unit=unit)
			if not os.path.exists(path):
				return None
			ctable = bcolz.open(path, mode='r')
			if len(ctable)==0:
				return None
			array = np.array(list(map(lambda x:list(x), ctable)))
			if unit=='1d':
				array = array[:,:7]	
			array[:,2:6] = array[:,2:6] * (array[:,1:2] / init_factor[stock])
			array[:,6:7] = array[:,6:7] * array[:,1:2]
			array = np.delete(array, 1, axis=1).round(2)
		elif field is not None and end is not None and limit is not None and start is None and init_factor is None:
			# param6: stock, unit, field, end, limit			
			path = DataFunction.get_path(stock, unit=unit)
			ctable = bcolz.open(path, mode='r')
			if len(ctable)==0:
				return None
			ctable = ctable.fetchwhere('date<={}'.format(end.timestamp()), outcols=field)[-limit:]
			if len(ctable)==0:
				return None
			array = np.array(list(map(lambda x:list(x), ctable)))			
		elif field is not None and start is None and end is None and limit is None and init_factor is None:
			# param5: stock, unit, field
			# array: field
			path = DataFunction.get_path(stock, unit=unit)+'/'+field
			if not os.path.exists(path):
				return None
			ctable = bcolz.open(path, mode='r')
			array = np.array(ctable)
		else:
			raise Exception(
			'''
			param should be:
			param1: stock, unit, init_factor, end, limit
			param2: stock, unit, init_factor, limit
			param3: stock, unit, init_factor, start, end
			param4: stock, unit, init_factor
			param5: stock, unit, field
			param6: stock, unit, field, end, limit
			''')					
		return array
