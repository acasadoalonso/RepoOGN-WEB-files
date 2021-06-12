<?php
include 'config.php';
$dd = $_POST['dd'];
$mm = $_POST['mm'];
$yy = $_POST['yy'];
if ($secretKey != '') {

	if(isset($_POST['g-recaptcha-response'])){
          $captcha=$_POST['g-recaptcha-response'];
        }
	if(!$captcha){
          echo '<h2>Please check the the captcha form.</h2>';
          exit;
        }
	$ip = $_SERVER['REMOTE_ADDR'];
        // post request to server
	$url = 'https://www.google.com/recaptcha/api/siteverify?secret=' . urlencode($secretKey) .  '&response=' . urlencode($captcha);
	$response = file_get_contents($url);
	$responseKeys = json_decode($response,true);
        // should return JSON with success as true
	if(!$responseKeys["success"]) {
                echo '<h2>You are spammer ! Get the @$%K out</h2>';
                die;
       }
}
$cwd =getcwd();
$rc=0;
echo 'Date='.$dd.$mm.$yy.'<br>';
//echo getcwd();
ob_start();

passthru('/usr/bin/python3  ./gbydate.py '.$dd.$mm.$yy, $rc);

$output = ob_get_clean();
echo nl2br($output);
?>
