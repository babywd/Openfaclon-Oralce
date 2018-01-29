#!/usr/bin/env python
# coding: utf-8

import urllib2
import argparse
import cx_Oracle
import inspect
import json
import re
import time
import socket
import re
import commands
import os
import sys

class Checks:

	def check_active(self):
		'''Check Intance is active and open'''
		sql = "select to_char(case when inst_cnt > 0 then 1 else 0 end,'FM99999999999999990') retvalue from (select count(*) inst_cnt from v$instance where status = 'OPEN' and logins = 'ALLOWED' and database_status = 'ACTIVE')"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def rcachehit(self):
		'''Read Cache hit ratio'''
		sql = "SELECT to_char((1 - (phy.value - lob.value - dir.value) / ses.value) * 100, 'FM99999990.9999') retvalue \
				FROM   v$sysstat ses, v$sysstat lob, \
					   v$sysstat dir, v$sysstat phy \
				WHERE  ses.name = 'session logical reads' \
				AND	dir.name = 'physical reads direct' \
				AND	lob.name = 'physical reads direct (lob)' \
				AND	phy.name = 'physical reads'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def dsksortratio(self):
		'''Disk sorts ratio'''
		sql = "SELECT to_char(d.value/(d.value + m.value)*100, 'FM99999990.9999') retvalue \
				 FROM  v$sysstat m, v$sysstat d \
				 WHERE m.name = 'sorts (memory)' \
				 AND d.name = 'sorts (disk)'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def activeusercount(self):
		'''Count of active users'''
		sql = "select to_char(count(*)-1, 'FM99999999999999990') retvalue from v$session where username is not null \
				 and status='ACTIVE'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def dbsize(self):
		'''Size of user data (without temp)'''
		sql = "SELECT to_char(sum(  NVL(a.bytes - NVL(f.bytes, 0), 0)), 'FM99999999999999990') retvalue \
				 FROM sys.dba_tablespaces d, \
				 (select tablespace_name, sum(bytes) bytes from dba_data_files group by tablespace_name) a, \
				 (select tablespace_name, sum(bytes) bytes from dba_free_space group by tablespace_name) f \
				 WHERE d.tablespace_name = a.tablespace_name(+) AND d.tablespace_name = f.tablespace_name(+) \
				 AND NOT (d.extent_management like 'LOCAL' AND d.contents like 'TEMPORARY')"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def dbfilesize(self):
		'''Size of all datafiles'''
		sql = "select to_char(sum(bytes), 'FM99999999999999990') retvalue from dba_data_files"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def commits(self):
		'''User Commits'''
		sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'user commits'"
		self.cur.execute(sql)
		res = self.cur.fetchmany(numRows=3)
		for i in res:
			return i[0]

	def rollbacks(self):
		'''User Rollbacks'''
		sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'user rollbacks'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def deadlocks(self):
		'''Deadlocks'''
		sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'enqueue deadlocks'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def redowrites(self):
		'''Redo Writes'''
		sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'redo writes'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def tblscans(self):
		'''Table scans (long tables)'''
		sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'table scans (long tables)'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def tblrowsscans(self):
		'''Table scan rows gotten'''
		sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'table scan rows gotten'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def indexffs(self):
		'''Index fast full scans (full)'''
		sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'index fast full scans (full)'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def hparsratio(self):
		'''Hard parse ratio'''
		sql = "SELECT to_char(h.value/t.value*100,'FM99999990.9999') retvalue \
				 FROM  v$sysstat h, v$sysstat t \
				 WHERE h.name = 'parse count (hard)' \
				 AND t.name = 'parse count (total)'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def netsent(self):
		'''Bytes sent via SQL*Net to client'''
		sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'bytes sent via SQL*Net to client'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def netresv(self):
		'''Bytes received via SQL*Net from client'''
		sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'bytes received via SQL*Net from client'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def netroundtrips(self):
		'''SQL*Net roundtrips to/from client'''
		sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'SQL*Net roundtrips to/from client'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def logonscurrent(self):
		'''Logons current'''
		sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'logons current'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]
	  
	def lastarclog(self):
		'''Last archived log sequence'''
		sql = "select to_char(max(SEQUENCE#), 'FM99999999999999990') retvalue from v$log where archived = 'YES'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def lastapplarclog(self):
		'''Last applied archive log (at standby).Next items requires [timed_statistics = true]'''
		sql = "select to_char(max(lh.SEQUENCE#), 'FM99999999999999990') retvalue \
				 from v$loghist lh, v$archived_log al \
				 where lh.SEQUENCE# = al.SEQUENCE# and applied='YES'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def freebufwaits(self):
		'''Free buffer waits'''
		sql = "select to_char(time_waited, 'FM99999999999999990') retvalue \
				 from v$system_event se, v$event_name en \
				 where se.event(+) = en.name and en.name = 'free buffer waits'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def bufbusywaits(self):
		'''Buffer busy waits'''
		sql = "select to_char(time_waited, 'FM99999999999999990') retvalue \
				 from v$system_event se, v$event_name en \
				 where se.event(+) = en.name and en.name = 'buffer busy waits'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def logswcompletion(self):
		'''log file switch completion'''
		sql = "select to_char(time_waited, 'FM99999999999999990') retvalue \
				 from v$system_event se, v$event_name en \
				 where se.event(+) = en.name and en.name = 'log file switch completion'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def logfilesync(self):
		'''Log file sync'''
		sql = "select to_char(time_waited, 'FM99999999999999990') retvalue \
				 from v$system_event se, v$event_name en \
				 where se.event(+) = en.name and en.name = 'log file sync'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def logprllwrite(self):
		'''Log file parallel write'''
		sql = "select to_char(time_waited, 'FM99999999999999990') retvalue \
				 from v$system_event se, v$event_name en \
				 where se.event(+) = en.name and en.name = 'log file parallel write'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def enqueue(self):
		'''Enqueue waits'''
		sql = "select to_char(time_waited, 'FM99999999999999990') retvalue \
				 from v$system_event se, v$event_name en \
				 where se.event(+) = en.name and en.name = 'enqueue'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def dbseqread(self):
		'''DB file sequential read waits'''
		sql = "select to_char(time_waited, 'FM99999999999999990') retvalue \
				 from v$system_event se, v$event_name en \
				 where se.event(+) = en.name and en.name = 'db file sequential read'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def dbscattread(self):
		'''DB file scattered read'''
		sql="select to_char(time_waited, 'FM99999999999999990') retvalue \
				 from v$system_event se, v$event_name en \
				 where se.event(+) = en.name and en.name = 'db file scattered read'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def dbsnglwrite(self):
		'''DB file single write'''
		sql="select to_char(time_waited, 'FM99999999999999990') retvalue \
				 from v$system_event se, v$event_name en \
				 where se.event(+) = en.name and en.name = 'db file single write'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def dbprllwrite(self):
		'''DB file parallel write'''
		sql="select to_char(time_waited, 'FM99999999999999990') retvalue \
				 from v$system_event se, v$event_name en \
				 where se.event(+) = en.name and en.name = 'db file parallel write'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def directread(self):
		'''Direct path read'''
		sql="select to_char(time_waited, 'FM99999999999999990') retvalue \
				 from v$system_event se, v$event_name en \
				 where se.event(+) = en.name and en.name = 'direct path read'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def directwrite(self):
		'''Direct path write'''
		sql="select to_char(time_waited, 'FM99999999999999990') retvalue \
				 from v$system_event se, v$event_name en \
				 where se.event(+) = en.name and en.name = 'direct path write'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def latchfree(self):
		'''latch free.'''
		sql="select to_char(time_waited, 'FM99999999999999990') retvalue \
				 from v$system_event se, v$event_name en \
				 where se.event(+) = en.name and en.name = 'latch free'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]
	

	def get_tablespaces_add_monitlist(self):
		sql = "SELECT tablespace_name FROM dba_tablespaces ORDER BY 1";
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			self.monit_keys.append(('TABLESPACE_%s'%i[0] , 'GAUGE'))

	def get_tablespaces_temp_add_monitlist(self):
		sql = "SELECT tablespace FROM V$TEMPSEG_USAGE group by tablespace ORDER BY 1";
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			self.monit_keys.append(('TABLESPACE_TEMP_%s'%i[0] , 'GAUGE'))

	def get_asm_add_monitlist(self):
		'''List als ASM volumes in a JSON like format for Zabbix use'''
		sql = "select NAME from v$asm_diskgroup_stat ORDER BY 1";
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			self.monit_keys.append(('ASMVOLUME_%s'%i[0] , 'GAUGE'))


	def tablespace(self,name):
		sql = '''SELECT df.tablespace_name "TABLESPACE",  ROUND ( (df.bytes - SUM (fs.bytes)) * 100 / df.bytes, 2) "USED" FROM  (SELECT TABLESPACE_NAME,BYTES FROM  sys.sm$ts_free fs UNION ALL SELECT TABLESPACE_NAME,FREE_SPACE FROM DBA_TEMP_FREE_SPACE ) FS, (SELECT tablespace_name, SUM (bytes) bytes FROM sys.sm$ts_avail GROUP BY tablespace_name UNION ALL SELECT TABLESPACE_NAME, SUM(bytes) FROM SYS.DBA_TEMP_FILES GROUP BY tablespace_name ) df WHERE fs.tablespace_name(+) = df.tablespace_name AND df.tablespace_name = '{0}' GROUP BY df.tablespace_name,df.bytes ORDER BY 1'''.format(name)
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[1]

	def tablespace_temp(self,name):
		'''Query temporary tablespaces'''
		sql = '''SELECT round(sum(a.blocks*8192)*100/bytes,2) percentual FROM V$TEMPSEG_USAGE a, dba_temp_files b where tablespace_name='{0}' and a.tablespace=b.tablespace_name group by a.tablespace,b.bytes'''.format(name)
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def asm_volume_use(self,name):
		sql = "select round(((TOTAL_MB-FREE_MB)/TOTAL_MB*100),2) from v$asm_diskgroup_stat where name = '{0}'".format(name)
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
				return i[0]
			
	def check_archive(self,archive):
		'''List archive used'''
		sql = "select trunc((total_mb-free_mb)*100/(total_mb)) PCT from v$asm_diskgroup_stat where name='{0}' ORDER BY 1".format(archive)
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def query_lock(self):
		'''Query lock'''
		sql = "SELECT count(*) FROM gv$lock l WHERE  block=1"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def query_redologs(self):
		'''Redo logs'''
		sql = "select COUNT(*) from v$LOG WHERE STATUS='ACTIVE'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def query_rollbacks(self):
		'''Query Rollback'''
		sql = "select nvl(trunc(sum(used_ublk*4096)/1024/1024),0) from gv$transaction t,gv$session s where ses_addr = saddr"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def query_sessions(self):
		'''Query Sessions'''
		sql = "select count(*) from gv$session where username is not null and status='ACTIVE'"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]

	def fra_use(self):
		'''Query the Fast Recovery Area usage'''
		sql = "select round((SPACE_LIMIT-(SPACE_LIMIT-SPACE_USED))/SPACE_LIMIT*100,2) FROM V$RECOVERY_FILE_DEST"
		self.cur.execute(sql)
		res = self.cur.fetchall()
		for i in res:
			return i[0]


class Main(Checks):

	def __init__(self):
		self.username = 'xxx'
		self.password = 'xxx'
		self.address = '1.1.1.1'
		self.database = 'xxx'
		self.ip = socket.gethostname()
		self.step = 60
		self.timestamp = int(time.time())			
		self.monit_keys = [
				('check_active','GAUGE'),
				('rcachehit','GAUGE'),
				('dsksortratio','GAUGE'),
				('activeusercount','GAUGE'),
				('dbsize','GAUGE'),
				('dbfilesize','GAUGE'),
				('commits','GAUGE'),
				('rollbacks','GAUGE'),
				('deadlocks','GAUGE'),
				('redowrites','GAUGE'),
				('tblscans','GAUGE'),
				('tblrowsscans','GAUGE'),
				('indexffs','GAUGE'),
				('hparsratio','GAUGE'),
				('netroundtrips','GAUGE'),
				('logonscurrent','GAUGE'),
				('lastarclog','GAUGE'),
				('lastapplarclog','GAUGE'),
				('bufbusywaits','GAUGE'),
				('logswcompletion','GAUGE'),
				('logfilesync','GAUGE'),
				('logprllwrite','GAUGE'),
				('enqueue','GAUGE'),
				('dbseqread','GAUGE'),
				('dbscattread','GAUGE'),
				('dbsnglwrite','GAUGE'),
				('dbprllwrite','GAUGE'),
				('directread','GAUGE'),
				('directwrite','GAUGE'),
				('latchfree','GAUGE'),
				('query_lock','GAUGE'),
				('query_redologs','GAUGE'),
				('query_rollbacks','GAUGE'),
				('query_sessions','GAUGE'),
				('fra_use','GAUGE')
		]
		
	def db_connect(self):
		self.db = cx_Oracle.connect('''{0}/{1}@{2}/{3}'''.format(self.username,self.password,self.address,self.database))
		self.cur = self.db.cursor()
	
	def db_close(self):
		self.db.close()
	
	def main(self):
		p = []
		try:
			self.db_connect()
			self.get_tablespaces_add_monitlist()
			self.get_tablespaces_temp_add_monitlist()
			self.get_asm_add_monitlist()
		finally:
			self.db_close()
		
		for key,vtype in self.monit_keys:
			try:
				self.db_connect()
				if key == 'check_active':
					try:
						value = int(self.check_active())
					except:
						value = 999
				elif key == 'rcachehit':
					try:
						value = round(self.rcachehit(),2)
					except:
						value = 999
				elif key == 'dsksortratio':
					try:
						value = round(self.dsksortratio(),2)
					except:
						value = 999
				elif key == 'activeusercount':
					try:
						value = int(self.activeusercount())
					except:
						value = 999
				elif key == 'dbsize':
					try:
						value = int(self.dbsize())
					except:
						value = 999
				elif key == 'dbfilesize':
					try:
						value = int(self.dbfilesize())
					except:
						value = 999
				elif key == 'commits':
					try:
						value = int(self.commits())
					except:
						value = 999
				elif key == 'rollbacks':
					try:
						value = int(self.rollbacks())
					except:
						value = 999
				elif key == 'deadlocks':
					try:
						value = int(self.deadlocks())
					except:
						value = 999
				elif key == 'redowrites':
					try:
						value = int(self.redowrites())
					except:
						value = 999
				elif key == 'tblscans':
					try:
						value = int(self.tblscans())
					except:
						value = 999
				elif key == 'tblrowsscans':
					try:
						value = int(self.tblrowsscans())
					except:
						value = 999
				elif key == 'indexffs':
					try:
						value = int(self.indexffs())
					except:
						value = 999
				elif key == 'hparsratio':
					try:
						value = round(self.hparsratio(),2)
					except:
						value = 999
				elif key == 'netroundtrips':
					try:
						value = int(self.netroundtrips())
					except:
						value = 999
				elif key == 'logonscurrent':
					try:
						value = int(self.logonscurrent())
					except:
						value = 999
				elif key == 'lastarclog':
					try:
						value = int(self.lastarclog())
					except:
						value = 999
				elif key == 'lastapplarclog':
					try:
						value = int(self.lastapplarclog())
					except:
						value = 999
				elif key == 'bufbusywaits':
					try:
						value = int(self.bufbusywaits())
					except:
						value = 999
				elif key == 'logswcompletion':
					try:
						value = int(self.logswcompletion())
					except:
						value = 999
				elif key == 'logfilesync':
					try:
						value = int(self.logfilesync())
					except:
						value = 999
				elif key == 'logprllwrite':
					try:
						value = int(self.logprllwrite())
					except:
						value = 999
				elif key == 'enqueue':
					try:
						if self.enqueue() == null:
							value = 0
					except:
						value = 999
				elif key == 'dbseqread':
					try:
						value = int(self.dbseqread())
					except:
						value = 999
				elif key == 'dbscattread':
					try:
						value = int(self.dbscattread())
					except:
						value = 999
				elif key == 'dbsnglwrite':
					try:
						value = int(self.dbsnglwrite())
					except:
						value = 999
				elif key == 'dbprllwrite':
					try:
						value = int(self.dbprllwrite())
					except:
						value = 999
				elif key == 'directread':
					try:
						value = int(self.directread())
					except:
						value = 999
				elif key == 'directwrite':
					try:
						value = int(self.directwrite())
					except:
						value = 999
				elif key == 'latchfree':
					try:
						value = int(self.latchfree())
					except:
						value = 999
				elif key == 'query_lock':
					try:
						value = int(self.query_lock())
					except:
						value = 999
				elif key == 'query_redologs':
					try:
						value =  int(self.query_redologs())
					except:
						value = 999
				elif key == 'query_rollbacks':
					try:
						value =  int(self.query_rollbacks())
					except:
						value = 999
				elif key == 'query_sessions':
					try:
						value =  int(self.query_sessions())
					except:
						value = 999
				elif key == 'fra_use':
					try:
						value = round((self.fra_use()),2)
					except:
						value = 999
				elif re.compile(ur'TABLESPACE_(\w+)').findall(key) !=[]:
					try:
						value = round((self.tablespace(re.compile(ur'TABLESPACE_(\w+)').findall(key)[0])),2)
					except:
						vlaue = 999
				elif re.compile(ur'TABLESPACE_TEMP_(\w+)').findall(key) !=[]:
					try:
						value = round((self.tablespace_temp(re.compile(ur'TABLESPACE_TEMP_(\w+)').findall(key)[0])),2)
					except:
						vlaue = 999
				elif re.compile(ur'ASMVOLUME_(\w+)').findall(key) !=[]:
					try:
						value = round((self.asm_volume_use(re.compile(ur'ASMVOLUME_(\w+)').findall(key)[0])),2)
					except:
						vlaue = 999
			except Exception, err:
				return 'err:',err		
			i = {
					'Metric': 'oracle.%s' % key,
					'Endpoint': self.ip,
					'Timestamp': self.timestamp ,
					'Step': self.step,
					'Value': value,
					'CounterType': vtype,
					'TAGS': 'port=1521'
			}
			p.append(i)
			
		method = "POST"
		handler = urllib2.HTTPHandler()
		opener = urllib2.build_opener(handler)
		url = 'http://172.18.14.5:6060/api/push'
		request = urllib2.Request(url, data=json.dumps(p) )
		request.add_header("Content-Type",'application/json')
		request.get_method = lambda: method
		try:
				pass
				connection = opener.open(request)
		except urllib2.HTTPError,e:
				connection = e

		if connection.code == 200:
				print connection.read()
		else:
				print '{"err":1,"msg":"%s"}' % connection
				
#		print json.dumps(p, sort_keys=True,indent=4)

if __name__ == '__main__':
	proc = commands.getoutput(' ps -ef|grep %s|grep -v grep|wc -l ' % os.path.basename(sys.argv[0]))
	sys.stdout.flush()
	if int(proc) < 5:
		Main().main()
