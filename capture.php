<!-- ./xmsh.php?sec=20  sec的值默认为25秒 -->
<script type="text/javascript">
	step = 0;
	var ytitle = document.title;
	function titleWink(msg) {
		setInterval(function() {
			step++;
			if (step >= 3) { step = 1; }
			if (step == 1) { document.title = '【' + msg + '】' + ytitle; }
			if (step == 2) { document.title = '【                  】' + ytitle;}
		}, 200);
	}
	function open_new_window(url) {
		window.open(url, "newwindow", "height=600, width=900, toolbar=no, menubar=no, scrollbars=no, resizable=no, location=no, status=no");
	}
</script>

<?php
$time_interval = 25; // 默认25秒一次
if (!empty($_GET['sec'])) { // ?sec=20
	if (is_numeric($_GET['sec'])) {
		$time_interval = $_GET['sec'];
	}
}

define('PLAYMUSIC_FCode', '<audio src="./music/pm_2.mp3" autoplay="autoplay" loop="loop"></audio>');
define('PLAYMUSIC_VCode', '<audio src="./music/pm_3.mp3" autoplay="autoplay" loop="loop"></audio>');
define('META_REFRESH', '<meta http-equiv=refresh content="' . $time_interval . '">'); // 25秒一次
define('RECORD_FILE', './record.txt');
define('DATA_FILE', './data.txt');
date_default_timezone_set('PRC'); 

set_time_limit(0);
$url = 'http://s.weibo.com/wb/XMSH&scope=ori&xsort=time'; // XMSH <-- 替换此url
read_data($last_data);
ob_start();

$des_url = $url . '&v=' . time();
echo '<hr>';
$contents = @file_get_contents($des_url);
if (empty($contents)) {
	echo META_REFRESH;
}

$regex_exc = '/\\\\u4f60\\\\u7684\\\\u884c\\\\u4e3a\\\\u6709\\\\u4e9b\\\\u5f02\\\\u5e38\\\\uff0c\\\\u8bf7\\\\u8f93\\\\u5165\\\\u9a8c\\\\u8bc1\\\\u7801\\\\uff1a/ism';
$regex = '/<span\s+?style=\\\"color:red;\\\">XMSH<\\\\\/span>.{17}.*?<\\\\\/em>/ism';
if (preg_match($regex_exc, $contents)) { // 需处理验证码
	echo META_REFRESH;
	echo PLAYMUSIC_VCode;
	echo '<br/>"你的行为有些异常，请输入验证码" !<br/>';
	write_log('中断："你的行为有些异常，请输入验证码" !');
	echo '<script type="text/javascript">titleWink("验证码");' . " open_new_window(\"$url\");" . '</script>';
	echo '<br/><a href="javascript:location.reload(true);"><font style="size:5">Refresh</font></a><br/>';
	echo "<p>refresh interval: $time_interval s</p>";

	die();
}
else if (!(preg_match($regex, $contents, $matches))) {
	echo META_REFRESH;
	echo "<br/>没有匹配到!<br/>";
	write_log("没有匹配到!  regex = $regex ");
	//echo "<hr><script>location.reload(true);</script>";
	echo "<p>refresh interval: $time_interval s</p>";
	die();
}
$data = $matches[0];
$data = substr(preg_replace('/\\\\u([0-9a-fA-F]{4})/', "&#x\\1;", $data), 1); // UNICODE 转汉字
$data = stripslashes('<' . $data); // 去转义
$data = strip_tags($data); // 转纯文本

if (! @strstr($last_data, $data)) { 
	// 出现新码：
	echo PLAYMUSIC_FCode;
	//$last_data += ($data . chr(10));
	write_log("-----> 出现新F码 <-----");
	write_log($data);	
	write_data($data);
	echo '<h1><font style="color:red">出现新F码</font></h1>';
	echo $data;
	echo '<script type="text/javascript">titleWink("出现新码");</script>';
	die();
}
echo META_REFRESH;
echo "Recent weibo: <font style=\"color:green\">";
echo $data;
echo "</font>";
write_log($data);
echo '<hr>';
echo "<p>refresh interval: $time_interval s</p>";
unset($contents);

?>
<?php

function write_log($msg) {
	@$handle=fopen(RECORD_FILE, "abw");
	$msg = date("Y-m-d H:i:s  ", time()) . $msg . chr(10);
	@fputs($handle, $msg);
	@fclose($handle);
}

function write_data($data) {
	@$handle=fopen(DATA_FILE, "abw");
	@fputs($handle, $data);
	@fputs($handle, chr(10));
	@fclose($handle);
}
function read_data(&$data) {
	if (! file_exists(DATA_FILE)) {
		return $data = '';
	}
	$data = file_get_contents(DATA_FILE);
	return $data;
}
/*
function unicode_decode($name)
{
    // 转换编码，将Unicode编码转换成可以浏览的utf-8编码
    $pattern = '/([\w]+)|(\\\u([\w]{4}))/i';
    preg_match_all($pattern, $name, $matches);
    if (!empty($matches))
    {
        $name = '';
        for ($j = 0; $j < count($matches[0]); $j++)
        {
            $str = $matches[0][$j];
            if (strpos($str, '\\u') === 0)
            {
                $code = base_convert(substr($str, 2, 2), 16, 10);
                $code2 = base_convert(substr($str, 4), 16, 10);
                $c = chr($code).chr($code2);
                $c = iconv('UCS-2', 'UTF-8', $c);
                $name .= $c;
            }
            else
            {
                $name .= $str;
            }
        }
    }
    echo $name;
    return $name;
}
*/
?>
