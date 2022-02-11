# voice_api_fs
just-study<br>
### fs接口规划
	呼叫接口
		点击拨号
			crmuuid
			extensin_number
			customer_number
			product_code
			//call_type
			url：/web/click-on-call/
			请求方式：POST
			请求主体：json 
			{
				"token":string(32),
				"data":{
					"crm_uuid":string(32),
					"extensin_number":string(8),
					"customer_number":string(32),(aes128_cdc加密)
					“product_code”：string(5)
				}
			}
			响应主体：json
			{
    			"data": "+OK Job-UUID: 1f6528d8-2c9a-449e-868b-aa197107ceac",
    			"msg": "Call OK"
			}

		群呼拨号
			队列
				新增
				删除
				列表
			坐席状态
				签入
				签出
			群呼任务建立
				号码列表,队列名称
		客服接听
			复用队列
	动态管理用户
		创建用户
		删除用户
		列表展示
	通话记录
		cdr模块存数据库
	事件推送
        使用mq

## 1.安装mariadb
	安装odbc
		sudo apt-get install unixodbc
		安装mysql-connector-odbc.deb
		配置odbcinst.ini

		# Example driver definitions

		# Driver from the postgresql-odbc package

		# Setup from the unixODBC package

		[PostgreSQL]

		Description = ODBC for PostgreSQL

		Driver = /usr/lib/psqlodbc.so

		Setup = /usr/lib/libodbcpsqlS.so

		Driver64 = /usr/lib64/psqlodbc.so

		Setup64 = /usr/lib64/libodbcpsqlS.so

		FileUsage = 1



		# Driver from the mysql-connector-odbc package

		# Setup from the unixODBC package

		[MySQL]

		Description = ODBC for MySQL

		Driver = /usr/lib/libmyodbc5.so

		Setup = /usr/lib/libodbcmyS.so

		Driver64 = /usr/lib64/libmyodbc5.so

		Setup64 = /usr/lib64/libodbcmyS.so


		FileUsage = 1
		
		配置odbc.ini
		[ldap]

		 DSN = ldap 

		 Description = The Database for mysql Driver = MySQL 

		 Database = ldap

		 Server = 10.10.211.6

		 User = ldap

		 Password = ldap123

		 Port = 3306

		 Socket = /var/lib/mysql/mysql.sock 

		 ReadOnly = no 

		 charset = UTF8

## 2.安装pgsql
	apt install postgresql
	设置密码
	切换到postgres执行psql连接数据库
	ALTER USER postgres WITH PASSWORD 'abc123ABC456\!.';
	创建pgsql用户
	create user ody with password 'abc123ABC456!.';
	创建用户数据库
	create database xxx owner xxxuser;
	赋予所有权限
	grant all on database xxxx to xxxuser;
	\q退出
	
## 3.修改fs核心数据库到pg，switch.xml sofiax.xml
	修改dsn开启自动创建表
	
## 4.动态管理用户
	ext.xml{
	<document type="freeswitch/xml">
	  <section name="directory">
	  <!--domain name-->
		<domain name="{{ext.domain}}">
		  <params>
			<param name="dial-string" value="{^^:sip_invite_domain=${dialed_domain}:presence_id=${dialed_user}@${dialed_domain}}${sofia_contact(*/${dialed_user}@${dialed_domain})},${verto_contact(${dialed_user}@${dialed_domain})}"/>
		  </params>
		  <groups>
			<group name="{{ext.group}}">
			  <users>
			  <!-- user-id -->
				<user id="{{ext.extnumber}}">
				  <params>
				  <!-- password -->
					<param name="password" value="{{ext.password}}"/>
					<param name="vm-password" value="{{ext.password}}"/>
					</params>
				  <variables>
					<variable name="toll_allow" value="domestic,international,local"/>
					<!-- user -->
					<variable name="accountcode" value="{{ext.extnumber}}"/>
					<variable name="user_context" value="default"/>
					<!-- caller_id_name -->
					<variable name="effective_caller_id_name" value="{{ext.extnumber}}"/>
					<!-- user -->
					<variable name="effective_caller_id_number" value="{{ext.extnumber}}"/>
					<variable name="outbound_caller_id_name" value="$${outbound_caller_name}"/>
					<variable name="outbound_caller_id_number" value="$${outbound_caller_id}"/>
					<!-- 呼叫组 -->
					<variable name="callgroup" value="{{ext.callgroup}}"/>
					<!-- 重写contact ip和端口 -->
					<variable name="sip-force-contact" value="NDLB-connectile-dysfunction"/>
					<variable name="x-powered-by" value="http://www.freeswitch.org.cn"/>
				  </variables>
				</user>
			  </users>
			</group>
		  </groups>
		</domain>
	  </section>
	</document>
	}
	修改xml_curl模块配置文件
	新增字段
	<binding name="directory">
      <param name="gateway-url" value="http://localhost/~seven/freeswitch/directory.php" bindings="directory"/>
    </binding>
	代码主要字段
	ext={
        'domain':domain,
        'group':'default',
        'extnumber':sip_auth_username,
        'password':'123456',
        'callgroup':'default'
    }
	保活改用option，降低注册服务器压力
	修改internal option参数 修改udp-only	
## 5.话单
	mod_cdr_csv 转换为逗号分隔的形式
	mod_cdr_pg_csv 直接存入数据库 写入失败会存入文件
	mod_xml(json,format)_cdr 把话单以xml格式发往http服务器，如果服务器不响应就会保持channel不关闭，出现僵尸channel，返回非ok存本地文件
	create table cdr (
    id                        serial primary key,
    local_ip_v4               inet not null,
    caller_id_name            varchar,
    caller_id_number          varchar,
    destination_number        varchar not null,
    context                   varchar not null,
    start_stamp               timestamp with time zone not null,
    answer_stamp              timestamp with time zone,
    end_stamp                 timestamp with time zone not null,
    duration                  int not null,
    billsec                   int not null,
    hangup_cause              varchar not null,
    uuid                      uuid not null,
    bleg_uuid                 uuid,
    accountcode               varchar,
    read_codec                varchar,
    write_codec               varchar,
    sip_hangup_disposition    varchar,
    ani                       varchar
};
	
## 6.HA
	track_call intelnal

## 7.ESL
	新版本SWIG不支持编译python-esl
	要安装3.0的SWIG
	pip install python-esl

## 8.rabbitmq
	sales_sys ZAQ!@#edc
	1.a腿建立
	2.呼叫成功建立b腿
	  呼叫失败无b腿，且a腿销毁
	3.b腿拒接或失败，b腿销毁，a腿销毁
	  b腿接通，建立呼叫
	4.挂断，b腿销毁，a腿销毁
	{
		"Event-Name":"CHANNEL_CREATE",
		"Core-UUID":"ed5499ef-3380-4e0c-934d-5e215f7e94aa","FreeSWITCH-Hostname":"ip-172-31-24-240","FreeSWITCH-Switchname":"ip-172-31-24-240",
		"FreeSWITCH-IPv4":"172.31.24.240",
		"FreeSWITCH-IPv6":"::1",
		"Event-Date-Local":"2021-10-03 19:45:01",
		"Event-Date-GMT":"Sun, 03 Oct 2021 11:45:01 GMT","Event-Date-Timestamp":"1633261501757401","Event-Calling-File":"switch_core_state_machine.c","Event-Calling-Function":"switch_core_session_run","Event-Calling-Line-Number":"630",
		"Event-Sequence":"44497",
		"Channel-State":"CS_INIT",
		"Channel-Call-State":"DOWN",
		"Channel-State-Number":"2",
		"Channel-Name":"sofia/internal/1001@175.176.64.197:38002","Unique-ID":"b661ba23-75aa-439f-93a0-4da9342352ec",
		"Call-Direction":"outbound",
		"Presence-Call-Direction":"outbound",
		"Channel-HIT-Dialplan":"false",
		"Channel-Presence-ID":"1001@172.31.24.240","Channel-Call-UUID":"b661ba23-75aa-439f-93a0-4da9342352ec","Answer-State":"ringing",
		"Caller-Direction":"outbound",
		"Caller-Logical-Direction":"outbound",
		"Caller-Caller-ID-Number":"0000000000","Caller-Orig-Caller-ID-Number":"0000000000",
		"Caller-Callee-ID-Name":"Outbound Call",
		"Caller-Callee-ID-Number":"1001",
		"Caller-ANI":"0000000000",
		"Caller-Destination-Number":"1001","Caller-Unique-ID":"b661ba23-75aa-439f-93a0-4da9342352ec",
		"Caller-Source":"src/switch_ivr_originate.c",
		"Caller-Context":"default",
		"Caller-Channel-Name":"sofia/internal/1001@175.176.64.197:38002","Caller-Profile-Index":"1",
		"Caller-Profile-Created-Time":"1633261501757401","Caller-Channel-Created-Time":"1633261501757401","Caller-Channel-Answered-Time":"0",
		"Caller-Channel-Progress-Time":"0",
		"Caller-Channel-Progress-Media-Time":"0",
		"Caller-Channel-Hangup-Time":"0",
		"Caller-Channel-Transfer-Time":"0",
		"Caller-Channel-Resurrect-Time":"0",
		"Caller-Channel-Bridged-Time":"0",
		"Caller-Channel-Last-Hold":"0",
		"Caller-Channel-Hold-Accum":"0",
		"Caller-Screen-Bit":"true",
		"Caller-Privacy-Hide-Name":"false",
		"Caller-Privacy-Hide-Number":"false",
		"variable_direction":"outbound",
		"variable_is_outbound":"true","variable_uuid":"b661ba23-75aa-439f-93a0-4da9342352ec","variable_call_uuid":"b661ba23-75aa-439f-93a0-4da9342352ec","variable_session_id":"73",
		"variable_sip_local_network_addr":"54.179.228.29","variable_sip_profile_name":"internal",
		"variable_text_media_flow":"disabled",
		"variable_channel_name":"sofia/internal/1001@175.176.64.197:38002","variable_sip_destination_url":"sip:1001@175.176.64.197:38002","variable_crm_uuid":"123",
		"variable_product_code":"C68",
		"variable_dialed_user":"1001",
		"variable_dialed_domain":"172.31.24.240",
		"variable_sip_invite_domain":"172.31.24.240",
		"variable_presence_id":"1001@172.31.24.240","variable_originate_early_media":"true",
		"variable_rtp_use_codec_string":"OPUS,G722,PCMU,PCMA,H264,VP8","variable_local_media_ip":"172.31.24.240",
		"variable_local_media_port":"22694",
		"variable_advertised_media_ip":"54.179.228.29","variable_audio_media_flow":"sendrecv",
		"variable_local_video_ip":"54.179.228.29",
		"variable_local_video_port":"27626",
		"variable_video_media_flow":"sendrecv","variable_rtp_local_sdp_str":"v=0\r\no=FreeSWITCH 1633238807 1633238808 IN IP4 54.179.228.29\r\ns=FreeSWITCH\r\nc=IN IP4 54.179.228.29\r\nt=0 0\r\nm=audio 22694 RTP/AVP 102 0 8 105 101\r\na=rtpmap:102 opus/48000/2\r\na=fmtp:102 useinbandfec=1; maxaveragebitrate=30000; maxplaybackrate=48000; ptime=20; minptime=10; maxptime=40\r\na=rtpmap:0 PCMU/8000\r\na=rtpmap:8 PCMA/8000\r\na=rtpmap:105 telephone-event/48000\r\na=fmtp:105 0-16\r\na=rtpmap:101 telephone-event/8000\r\na=fmtp:101 0-16\r\na=ptime:20\r\na=sendrecv\r\nm=video 27626 RTP/AVP 103 104\r\nb=AS:3072\r\na=rtpmap:103 H264/90000\r\na=rtpmap:104 VP8/90000\r\na=sendrecv\r\na=rtcp-fb:103 ccm fir\r\na=rtcp-fb:103 ccm tmmbr\r\na=rtcp-fb:103 nack\r\na=rtcp-fb:103 nack pli\r\na=rtcp-fb:104 ccm fir\r\na=rtcp-fb:104 ccm tmmbr\r\na=rtcp-fb:104 nack\r\na=rtcp-fb:104 nack pli\r\n",
		"variable_sip_outgoing_contact_uri":"<sip:mod_sofia@54.179.228.29:5060>","variable_sip_req_uri":"1001@175.176.64.197:38002",
		"variable_sip_to_host":"175.176.64.197:38002",
		"variable_sip_from_host":"172.31.24.240","variable_sofia_profile_name":"internal","variable_recovery_profile_name":"internal","variable_sofia_profile_url":"sip:mod_sofia@54.179.228.29:5060"
		}

## 9.完善日志记录 