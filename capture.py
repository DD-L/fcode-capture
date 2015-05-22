#! /cygdrive/d/cocos2dx32/Python2732/python
# encoding=utf-8

## /usr/bin/python
## python v2.7

#
# capture.py 
# Usage: capture.py instance_id
#	instance_id, see the xml file  
#
# exit code: 
#	0	正常退出
#	1	因instance获取出错而致程序退出
#	2	因不支持的系统平台而致程序退出
#	3	当curl命令执行出错时, 重试的次数达到上限而致程序退出
#

import sys
import re
import os
import logging
import gzip
import commands
import time
import string

import curl_xml

reload(sys)
sys.setdefaultencoding('utf8')

instance_id = sys.argv[1]
data_dir = ''
instance = {'regex': '', 'curl': '', 'interval': 30, 'id': '', 'name': '', 'callback': ''}
instance_base_info = ''
wav_file = os.path.join(os.path.dirname(__file__), './music/pm_2.wav')
wav_alarm = os.path.join(os.path.dirname(__file__), './music/pm_1.wav')
AlarmSwitch = 'ON' # or 'OFF', 异常报警器开关

logfile = 'record.log'
logging.basicConfig(level=logging.DEBUG,
                format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                #format = '%(asctime)s %(levelname)s %(message)s',
                datefmt = '%a, %d %b %Y %H:%M:%S',
                filename = logfile,
                filemode = 'a')

def get_instance(ins_id):
	global instance
	ci = curl_xml.CaptureInstance()
	instance = ci.get_instance_data(ins_id)
	if instance:
		return instance
	else:
		msg = 'get instance failed. '
		print 'Error: ' + msg
		logging.error(msg)
		if AlarmSwitch == 'ON':
			play_wav(wav_alarm)
		sys.exit(1)

def mk_data_dir():
	global data_dir
	data_dir = os.path.join(os.path.dirname(__file__), 'data')
	if not os.path.isdir(data_dir):
		os.makedirs(data_dir)

def init():	
	global instance_id
	global instance_base_info
	global instance
	#global gzipfilePath 
	#global data_file 
	get_instance(instance_id)
	instance_base_info = ('instance info: id "'	+ instance['id'] + '", name "' + instance['name'] + '\"')
	mk_data_dir()
	#gzipfilePath = os.path.join(data_dir, instance['id'] + '.gz')
	#if os.path.isfile(gzipfilePath):
	#	os.remove(gzipfilePath)
	#data_file = os.path.join(data_dir, instance['id'] + '.data')
	if sys.platform[:5] == 'win32':
		# win32平台需要转义 & 符号
		instance['curl'] = instance['curl'].replace('&', r'^&')
	elif sys.platform[:5] != 'linux':
		logging.error('Initialization: Unsupported platform. ' + instance_base_info)
		print 'Error: Unsupported platform, Initialization. ' + instance_base_info
		if AlarmSwitch == 'ON':
			play_wav(wav_alarm)
		sys.exit(2)

'''执行curl命令'''
def gz_cmd(curl_cmd, gzipfilePath):
	os.system(curl_cmd + ' > ' + gzipfilePath)
	return True
#	hp = commands.getstatusoutput(curl_cmd)
#	if hp[1] == '':
#		logging.error("curl error, '%s' is empty", gzipfilePath);
#		print 'Error: write gzip file failed. "%s" is empty'  %gzipfilePath
#		return False
#	try:
#		file_object = open(gzipfilePath, 'wb')
#		file_object.write(hp[1])
#		file_object.close()
#		return True
#	except  IOError  as e: 
#		logging.error("open file: %s failed, except: %s", data_file, e);
#		print 'Error: write gzip file failed.'
#		return False

'''记录比较数据'''
def write_data(data_file, data):
	try:
		file_object = open(data_file, 'a')
		file_object.write(data + '\n')
		file_object.close()
	except  IOError  as e: 
		logging.error("open file: %s failed, except: %s. %s", data_file, e, instance_base_info);
		print 'Error: write data failed. ' + instance_base_info
'''读取比较数据'''
def read_data(data_file):
	content = ''
	try:
		file_object = open(data_file, 'r')
		content = file_object.read()
		file_object.close()
	except  IOError  as e: 
		logging.warning("open file: %s failed, except: %s. %s", data_file, e, instance_base_info);
		print 'Warning: read data failed. ' + instance_base_info 
	return content

'''匹配字串'''
def re_match(str_child, str_content):
	if (string.find(str_content, str_child) != -1):
		return True
	else:
		return False
	#pattern = re.compile(regex, re.I | re.M)
	#match = pattern.search(str_content)
	#if match:
	#	return match.group()
	#else:
	#	return ''


'''取出匹配的字串'''
def re_match_cutting(regex, str_content): 
	pattern = re.compile(regex, re.I | re.M)
	ret = ''
	for m in pattern.finditer(str_content):
		if m == None:
			break
		ret += (m.group() + '\n')
	return ret.strip() 

#def re_match_cutting_1st():	

'''去html标签'''
def strip_tags(html):
	from HTMLParser import HTMLParser
	html = html.strip()
	html = html.strip("\n")
	result = []
	parser = HTMLParser()
	parser.handle_data = result.append
	parser.feed(html)
	parser.close()
	return ''.join(result)


'''返回解压后的gzip文件内容'''
def ugzip(gzipfilePath):
	try:
		f = gzip.open(gzipfilePath, 'rb')
		file_content = f.read()
		f.close()
		return file_content
	except:
		return ''

'''执行回调命令'''
def callback_cmd():
	global instance
	os.system(instance['callback'])
	logging.info('callback command: ' + instance['callback'] + '\t' + instance_base_info)
	return True

'''播放声音'''
def play_wav(wav_file):
	if sys.platform[:5] == 'linux': 
		os.popen2('aplay -q ' + wav_file + ' >/dev/null  2>&1')
		time.sleep(1)	
	else:
		import winsound
		winsound.PlaySound(wav_file, winsound.SND_FILENAME)

'''主函数'''
# main:
if __name__ == '__main__':

	init()	
	gzipfilePath = os.path.join(data_dir, instance['id'] + '.gz')
	if os.path.isfile(gzipfilePath):
		os.remove(gzipfilePath)
	data_file = os.path.join(data_dir, instance['id'] + '.data')

	regex = instance['regex']
	try_times = 10 # 如果gzip为空，重新尝试的次数
	while True:
		print '\n'
		sys.stdout.flush()
		time.sleep(int(instance['interval']))
		# 执行curl命令
		if not gz_cmd(instance['curl'], gzipfilePath):
			continue

		time.sleep(0.4)	
		# 读取获取的网页内容
		file_content = ugzip(gzipfilePath)
		if file_content == '':
			try_times -= 1
			msg = ('gzip file ' + gzipfilePath 
					+ ' is empty, maybe curl command is expired. then try ' 
					+ str(try_times) + ' times. ' + instance_base_info)
			print 'Error: ' + msg
			logging.error(msg)
			if (try_times <= 0):
				msg = ('gzip file ' + gzipfilePath 
						+ ' is empty, and it has reached the maximum number of attempts. '
						+ instance_base_info) 
				print 'Error: ' + msg
				logging.error(msg)
				sys.stdout.flush()
				if AlarmSwitch == 'ON':
					play_wav(wav_alarm)
				sys.exit(3)
			continue
		else:
			try_times = 10 # 将重新尝试的次数重置为10

		# 去html标签
		ret = strip_tags(file_content)
		# 剪出匹配文本
		ret = re_match_cutting(regex, ret)
		# 存放未经处理的文本
		original_text = ret
		original_text = re.compile(r'来自$', re.M).sub('', original_text)

		if ret == '': # 没有匹配到
			print 'Warning: ' + regex + ' was not found. ' + instance_base_info
			logging.warning(regex +' was not found. ' + instance_base_info)
		else:
			# 修改'[\d]' 赞[x]转发[x]评论[x], 并去除之后的字符
			ret = re_match_cutting(r'.+?赞\[\d+?\]转发\[\d+?\]评论\[\d+?\]', ret)
			ret = re.compile(r'赞\[\d+?\]转发\[\d+?\]评论\[\d+?\]', re.M).sub('赞[x]转发[x]评论[x]', ret)
			# 修改 赞[x]原文转发[x]原文评论[x]转发理由:
			ret = re.compile(r'赞\[\d+?\]原文转发\[\d+?\]原文评论\[\d+?\]转发理由:', re.M).sub('赞[x]原文转发[x]原文评论[x]转发理由:', ret)

			# 和之前的数据比对
			f2code_flag = False
			last_data = read_data(data_file)  # 读取上一次记录的数据
			for val in ret.split('\n'):
				if not (os.path.isfile(data_file) and re_match(val, last_data)): # 和之前data比对 
					f2code_flag = True
					print '\n找到新F码:'
					print val
					write_data(data_file, val)
					logging.info('找到新F码:\t' + val + ' .\t' + instance_base_info)
			logging.info('Recent weibo: [[ ' + original_text + ' ]]\t' + instance_base_info)
			if f2code_flag == True:
				print '\ntext:\n'
				print original_text
				callback_cmd()
				sys.stdout.flush()
				while True:
					play_wav(wav_file)
			else:
				print '\nRecent weibo: (' + instance_base_info + ')'
				print original_text # 这里打的是原始数据

	sys.exit(0)

