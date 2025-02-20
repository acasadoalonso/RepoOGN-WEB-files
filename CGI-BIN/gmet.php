<?php
$station = $_POST['station'];

$cwd =getcwd();
$rc=0;
echo 'Station='.$station.'<br>';
//echo getcwd();
ob_start();

passthru('/usr/bin/python3  ./gmet.py '.$station, $rc);

$output = ob_get_clean();
echo nl2br($output);
?>
