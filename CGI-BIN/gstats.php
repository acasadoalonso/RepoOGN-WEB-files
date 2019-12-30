<?php
$station = $_POST['regis'];
header('Contet-Type: text/thml; charset=utf-8');
$cwd =getcwd();
$rc=0;
//echo 'station='.$station.'<br>';
//echo getcwd();
ob_start();

passthru('/usr/bin/python3  ./gstats.py '.$station, $rc);

$output = ob_get_clean();
echo nl2br($output);
?>

