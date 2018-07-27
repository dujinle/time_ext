#!/usr/bin/python
#-*- coding:utf-8 -*-
import re
from time_base import TimeBase
#标记对象以及链接的网络
class TimeLamda(TimeBase):

	def encode(self,struct,time_conf):
		try:
			struct['TimeLamda'] = list();
			self.prev_label(struct);
			self.find_lamda(struct);
			self.creat_lamda(struct);
			self.clear_time_label(struct);
			self.creat_timedd_lamda(struct);
		except Exception as e: raise e;

	def find_lamda(self,struct):
		try:
			for key in self.data.keys():
				item = self.data[key];
				for reg in item.keys():
					p = re.compile(reg);
					amatch = p.search(struct['lamda_text']);
					if amatch is None: continue;
					struct['TimeLamda'].append(amatch.group());
					#struct['lamda_text'] = struct['lamda_text'].replace(amatch.group(),'',1);
			#去除重复的结果
			lamda_max = None;
			prev_len = 0;
			for lamda in struct['TimeLamda']:
				if len(lamda) >= prev_len:
					prev_len = len(lamda);
					lamda_max = lamda;
			struct['TimeLamda'] = list();
			if not lamda_max is None:
				struct['TimeLamda'].append(lamda_max);
		except Exception as e: raise e;

	def creat_lamda(self,struct):
		try:
			timelamda = list();
			for lamda in struct['TimeLamda']:
				tmp_lamda = lamda;
				lamda_stc = list();
				index = 7;
				while True:
					if len(tmp_lamda) == 0:
						print 'finish ok';
						break;
					index = index - 1;
					if index <= 0:
						print 'finish error';
						break;
					for timelabel in struct['TimeLabel']:
						idx = tmp_lamda.find(timelabel['label']);
						if idx == 0:
							tmp_lamda = tmp_lamda.replace(timelabel['label'],'',1);
							lamda_stc.append(timelabel);
							if len(tmp_lamda) == 0:
								break;
						else:
							tmp_lamda = lamda;
							lamda_stc = list();
							timelabel = struct['TimeLabel'].pop(0);
							struct['TimeLabel'].append(timelabel);
							break;
				if len(lamda_stc) > 0:
					timelamda.append(lamda_stc);
			if len(timelamda) > 0:
				struct['TimeLamda'] = timelamda.pop();
			else:
				struct['TimeLamda'] = timelamda;
		except Exception as e: raise e;

	def creat_timedd_lamda(self,struct):
		timelamda = list();
		first_flag = False;
		while True:
			if len(struct['TimeLamda']) == 0: break;
			item = struct['TimeLamda'].pop(0);
			if item['label'] == 'TimeD':
				first_flag = True;
				timelamda.append(item);
			elif item['label'] == 'Direct' and first_flag == True:
				prev_item = timelamda.pop();
				prev_item['dir'] = item;
				prev_item['label'] = 'TimeDD';
				timelamda.append(prev_item);
				first_flag = False;
			else:
				timelamda.append(item);
				first_flag = False;
		struct['TimeLamda'] = timelamda;

	def prev_label(self,struct):
		struct['lamda_text'] = list();
		for istr in struct['seg_text'].split(' '):
			if len(istr) == 0: continue;
			flag = False;
			for item in struct['TimeLabel']:
				if istr == item['str']:
					struct['lamda_text'].append(item['label']);
					flag = True;
					break;
			if flag == False:
				struct['lamda_text'].append(istr);
		struct['lamda_text'] = ''.join(struct['lamda_text']);

	def clear_time_label(self,struct):
		timelabel = list();
		for item in struct['TimeLabel']:
			flag = False;
			for lamda in struct['TimeLamda']:
				if lamda['str'] == item['str']:
					flag = True;
					break;
			if flag == False:
				timelabel.append(item);
		if len(timelabel) == 0:
			del struct['TimeLabel'];
		else:
			struct['TimeLabel'] = timelabel;
