# encoding=utf-8
#@author dezan zhao
import pdb
import jieba #分词框架
print('hello')
#seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
#print("Full Mode: " + "/ ".join(seg_list))  # 全模式
#通过本地缓存，类似于人类的自己的短时记忆
#通过本地图谱，类似于人类的自己的长时记忆
#通过外界图谱，类似于人类的互联网搜索
#通过百度知道，类似于人类的引用互联网
#知识图谱的内容包括知识图谱的构建、检索和生成对话，我要做的是将检索的拼成对话，这是我的研究的一个点，其他的不研究


#功能框架
#讲笑话
#讲新闻
#小说
import requests         # 导入requests库
import re               # 导入正则表达式库

while True:
	ask_sentence_str = input('你：')
	ask_sentence = jieba.cut(ask_sentence_str, cut_all=False)
	ask_sentence = "/ ".join(ask_sentence)
	ask_sentence_list = ask_sentence.split('/ ')
	#pdb.set_trace()
	ans_sentence = '编号89767'
	if '笑话' in ask_sentence:
		import random
		jokePage = requests.get('http://www.jokeji.cn/list.htm')
		jokePage.encoding = 'gbk'
		jokeList = re.findall('/jokehtml/[\w]+/[0-9]+.htm',jokePage.text)   # 使用正则表达式找到所有笑话页面的链接
		rand = random.randint(0, 20) 
		jokeContent = requests.get('http://www.jokeji.cn/'+jokeList[rand])     # 访问第一个链接
		jokeContent.encoding = 'gbk'
		jokes = re.findall('<P>[0-9].*</P>', jokeContent.text)      # 利用正则找到页面中的所有笑话
		ans_sentence = jokes[0]
		dr = re.compile(r'<[^>]+>',re.S)
		dd = dr.sub('',ans_sentence)
		ans_sentence = dd.strip()
	elif '新闻' in ask_sentence:
		import random
		newsPage = requests.get('http://news.qq.com/')
		news = re.findall('<a target="_blank" class="linkto".*</a>', newsPage.text)      # 利用正则找到页面中的所有笑话
		ans_sentence = '\n\r'.join(news)
		dr = re.compile(r'<[^>]+>',re.S)
		dd = dr.sub('',ans_sentence)
		ans_sentence = dd.strip()
	else : #http://kw.fudan.edu.cn/apis/cndbpedia/ 复旦的知识图谱开源接口，属性查询
		import jieba.analyse
		key_list = jieba.analyse.extract_tags(ask_sentence_str)
		print(key_list)
		try:
			content = requests.get('http://shuyantech.com/api/cndbpedia/value?q='+key_list[0]+'&attr='+key_list[1])
		except:
			content = requests.get('http://shuyantech.com/api/cndbpedia/value?q='+key_list[1]+'&attr='+key_list[0])
		else:
			mul_mean_content = ''
			try:
				mul_mean_content = requests.get('http://shuyantech.com/api/cndbpedia/ment2ent?q='+key_list[0])
				mul_mean_content = eval(mul_mean_content.text).get('ret')[0]
				content = requests.get('http://shuyantech.com/api/cndbpedia/value?q='+mul_mean_content+'&attr='+key_list[1])
			except:
				mul_mean_content = requests.get('http://shuyantech.com/api/cndbpedia/ment2ent?q='+key_list[1])
				mul_mean_content = eval(mul_mean_content.text).get('ret')[0]
				content = requests.get('http://shuyantech.com/api/cndbpedia/value?q='+mul_mean_content+'&attr='+key_list[0])		
			print(content.text)
			#ans_sentence = eval(content.text).get('ret')[0]
	print('宝：'+ans_sentence)
#知识问答


#学习机制：爬虫爬百度百科