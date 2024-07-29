<?php
include 'config.php';
$dd = $_POST['dd'];
$mm = $_POST['mm'];
$yy = $_POST['yy'];
$hostname = gethostname(); 

$ip = $_SERVER['REMOTE_ADDR'];
$cwd =getcwd();
$rc=0;
echo 'Date='.$dd.$mm.$yy.' '.$ip.'<br>';
//echo getcwd();
ob_start();

passthru('/usr/bin/python3  ./gbydate.py '.$dd.$mm.$yy, $rc);

$output = ob_get_clean();
echo nl2br($output);
?>
