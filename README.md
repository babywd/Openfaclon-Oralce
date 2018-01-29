# Openfaclon-Oralce

监控项：
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
		
使用方法：
username、password、address、databases换成自己线上的即可。