<?php
//QC Get CDR From OVP And ICC

//获取前端提交的参数
$pbx = $_POST["pbx"];
$cdrdate = $_POST["cdrdate"]; //格式 yyyy-mm-dd
$cdrhour = $_POST["cdrhour"]; //格式 hh

//设置CDR数据库连接
$ovp_DB = 'host=10.71.55.42 port=5432 dbname=OVP_CDR user=postgres password=postgres#2017 connect_timeout=3';
//$icc_DB = "mysql:host=10.71.54.100;dbname=pbxdb3, hkdlcti, hkdl@plctidb!@#";
//echo "$icc_DB\n";
//输出参数
/*
echo            "pbx=" . $pbx           . "\n";
echo    "cdrdate=" . $cdrdate   . "\n";
echo    "cdrhour=" . $cdrhour   . "\n";
*/

//date_default_timezone_set("Asia/Manila");

//$cdrdatetime = new DateTime($cdrdate . " " . $cdrhour . ":00:00");
//echo $cdrdatetime -> format("Y-m-d H:i:s");
//echo "\nNew\n";
$cdrstarttime = new DateTime($cdrdate . " " . $cdrhour . ":00:00");
$cdrendtime = new DateTime($cdrdate . " " . $cdrhour . ":00:00");

$cdrstarttime -> sub(new DateInterval('PT4H'));
$cdrstarttime = $cdrstarttime -> format("Y-m-d H:i:s");

$cdrendtime -> sub(new DateInterval('PT3H1S'));
$cdrendtime = $cdrendtime -> format("Y-m-d H:i:s");

/*
echo $cdrstarttime;
echo "\n";
echo $cdrendtime; 
echo "\n";

return;
*/

//OVP_CDR
if ($pbx == 'ovp')
{
        //echo "ovp\n";

        $count_sql = "select count(id) from cdr where call_status = 'yes' and record_file_path is not null and start_stamp between '$cdrstarttime' and '$cdrendtime'";
        //echo $count_sql . "\n";
        $cdr_sql = "select row_to_json(t) from (select concat( 'OVP', id ) AS id, call_type, start_stamp::TIMESTAMP(0) AS begintime, end_stamp::TIMESTAMP(0) AS endtime, b_billsec, caller_id_number AS agentID, " .
                                "caller_id_number AS agentname, product_code, crm_uuid, concat( 'http://10.71.55.56:8080/SpeechManager/resources/Audio', record_file_path ) AS record_file_path " .
                                "from cdr where call_type = 'outbound_agent' and " .
                                "start_stamp between '$cdrstarttime' and '$cdrendtime' order by id) AS t";
        //echo $cdr_sql . "\n";

        $DBConn = pg_connect($ovp_DB) or die("PGSQL Connection Failed\n");
        $result = pg_query($DBConn, $count_sql);
        $cdr_count = pg_fetch_result($result, 0, 0);


        //echo "cdr_count: " . $cdr_count;
        //return;

        if ($cdr_count > 0)
        {
                //echo ">0\n";

                $result = pg_query($DBConn, $cdr_sql);
                $row = 0;

                while ($cdr_result = pg_fetch_result($result, $row, 0))
                {
                        echo $cdr_result;
                        echo "\n";
                        $row ++;
                }


                //$cdr_result = pg_fetch_object($result, 0);
                //$cdr_result = pg_fetch_result($result, 0, 0);
                //echo "result_count: " . $result_count;
                //echo $result_cdr;

                //$cdr_result = array('cdr_count' => $cdr_count);
                //echo json_encode($cdr_result) . "\n";
                //echo $cdr_result;
                //var_dump($cdr_result);
                //echo ">0\n";

                pg_free_result ($result);
                pg_close ($DB_conn);
                return;
        }
        else
        {
                //echo "=0\n";
                $cdr_count = array('cdr_count' => "0");
                echo json_encode($cdr_count) . "\n";

                pg_free_result ($result);
                pg_close ($DB_conn);
                return;
        }

}

//ICC_CDR
if ($pbx == 'icc')
{
        //echo "icc\n";

        $count_sql = "select count(id) from cti_record t1 WHERE t1.begintime BETWEEN '$cdrstarttime' and '$cdrendtime'";
        //echo $count_sql . "\n";

        //$cdr_sql = "select id, call_type, begintime, endtime from cti_record where id in (4378728,4378729)";

        $cdr_sql = "SELECT concat( 'ICC', t1.id ) AS id, t2.call_type, t1.begintime, t1.endtime, " .
                                "t2.billsec - t2.incall_ringsec AS b_billsec, t1.agent_num AS agentid, t1.agentname, t1.agent_group_name AS product_code, " .
                                "concat( 'http://10.71.55.100:8080/CTI/recoredings/', t1.record_file_name ) AS record_file_path, " .
                                "t3.grade FROM (cti_record t1 LEFT JOIN cti_cdr_call_leg t2 ON ( t1.record_uuid = t2.leg_uuid ) " .
                                "LEFT JOIN cti_agent_grade t3 ON ( t1.customer_uuid = t3.customer_uuid )) " .
                                "WHERE t1.begintime BETWEEN '$cdrstarttime' AND '$cdrendtime' " .
                                "AND t2.billsec - t2.incall_ringsec >= 0 ORDER BY t1.begintime DESC";
        //echo $cdr_sql . "\n";


        try
        {
                //$DBConn = new PDO($icc_DB);
                $DBConn = new PDO('mysql:host=10.71.55.100;dbname=ctiserver', 'hkdlcti', 'hkdl@plctidb!@#', array(PDO::ATTR_TIMEOUT => 2));
        }
    catch (PDOException $exception)
        {
                echo "MySQL Connection Failed: " . $exception->getMessage() . "\n";
        }

                $result = $DBConn -> query($count_sql);
                $sql_result = $result -> fetch(PDO::FETCH_NUM);
                $cdr_count = $sql_result[0];
                //echo "cdr_count: " . $cdr_count;
                $result -> closeCursor();

                //$result_ColumnCount = $result -> columnCount();
                //$cdr_result = $result -> fetch(PDO::FETCH_ASSOC, PDO::FETCH_ORI_NEXT); 
                //echo "result_ColumnCount:$result_ColumnCount\n";
                //$arrlen = count($cdr_result);
                //echo "$arrlen";

                /*
                for ($x=0;$x<$arrlen;$x++)
                {
                        echo $cdr_result[$x];
                        echo "\n";
                }
                */
                /*
                while ($cdr_result)
                {
                $cdr = $cdr_result;
                foreach ($cdr as $y=>$y_value)
                {
                        echo $y . ":" . $y_value;
                        echo "\n";
                }

                */

/*
                while ($cdr_result)
                {
                        echo json_encode($cdr_result) . "\n";
                }


*/

/* 

                print_r ($cdr_result);
                print ("\n");
        //$cdr_count = array('cdr_count' => $cdr_count);
                echo json_encode($cdr_result) . "\n";


 */



//return;




//
        //return;

        if ($cdr_count > 0)
        {
                //echo ">0\n";

                $result = $DBConn -> query($cdr_sql);
                while ($cdr_result = $result->fetch(PDO::FETCH_ASSOC, PDO::FETCH_ORI_NEXT)) 
                {
                        echo json_encode($cdr_result) . "\n";
                }

                $result -> closeCursor();
                $DBConn = null;
                return;

/*
                $result = $DBConn -> query($cdr_sql);
                $cdr_result = $result -> fetchAll(); 
                echo $cdr_result;
                foreach ($cdr_result as $y=>$y_value)
                        {
                        echo '"$y"' . ":" . $y_value;
                        echo "\n";
                        }
*/
                        //while ($cdr_result) {
      //$data = $cdr_result[id] . "\t" . $cdr_result[call_type] . "\t" . $cdr_result[begintime] . "\n";
      //print $data;


                //$cdr_result = pg_fetch_object($result, 0);
                //$cdr_result = pg_fetch_result($result, 0, 0);
                //echo "result_count: " . $result_count;
                //echo $result_cdr;

                //$cdr_result = array('cdr_count' => $cdr_count);
                //echo json_encode($cdr_result) . "\n";
                //echo $cdr_result;
                //var_dump($cdr_result);
                //echo ">0\n";


        }
        else
        {
                //echo "=0\n";
                $cdr_count = array('cdr_count' => $cdr_count);
                echo json_encode($cdr_count) . "\n";

                $DBConn = null;
                return;
        }

}


/*
//初始化
$curl = curl_init();

//设置抓取的url
if ($pbx == 'ovp') $cdrurl = $cdr_ovp;
if ($pbx == 'icc') $cdrurl = $cdr_icc;

curl_setopt($curl, CURLOPT_URL, $cdrurl);

//设置头文件的信息作为数据流输出
curl_setopt($curl, CURLOPT_HEADER, 1);

//设置获取的信息以文件流的形式返回，而不是直接输出。
curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);

//设置超时时间=1s。
curl_setopt($curl, CURLOPT_TIMEOUT, 1);

//设置post方式提交
curl_setopt($curl, CURLOPT_POST, 1);


//设置post数据
$post_data =              'cdrstarttime='       . $cdrstarttime;
$post_data = $post_data . '&cdrendtime='        . $cdrendtime;

//echo $post_data;

curl_setopt($curl, CURLOPT_POSTFIELDS, $post_data);

//执行命令
$data = curl_exec($curl);

//关闭URL请求
curl_close($curl);

//显示获得的数据
//echo $post_data;

//输出错误日志
//$file = fopen("/tmp/test.log", "a") or die("Unable to open file!");
//$txt1 = date(r) . " [ERROR] customerForeignId = " . $customerForeignId . ",customerNum = " . $customerNum . ",queueNum = " . $queueNum . "\n";
//$txt2 = date(r) . " [ERROR] post_data = " . $post_data . "\n";
//fwrite($file, $txt1);
//fwrite($file, $txt2);
//fclose($file);

echo $post_data;

//退出脚本
return;
*/
?>
