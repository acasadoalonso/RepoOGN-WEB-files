<?php
include 'config.php';
$regis = $_POST['regis'];
$ip    = $_SERVER['REMOTE_ADDR'];
$cwd =getcwd();
$rc=0;
echo 'regis='.$regis.' '.$ip.'<br>';
//echo getcwd();
ob_start();

passthru('/usr/bin/python3  ./gbyreg.py '.$regis, $rc);

$output = ob_get_clean();
echo nl2br($output);
?>
