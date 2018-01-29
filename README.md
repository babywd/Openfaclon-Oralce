# Openfaclon-Oralce

1.监控项：
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
		
2.使用方法：
username、password、address、databases换成自己线上的即可。
3.环境准备
(1)需要安装cx_Oralce,地址https://qa.debian.org/watch/sf.php/cx-oracle,找到对应python版本下载安装
(2)需要安装 oracle-instantclient-basic-10.2.0.4-1.x86_64.rpm oracle-instantclient-devel-10.2.0.4-1.x86_64.rpm这个10.2对应你的oracle版本
