<?php
$dd = $_POST['dd'];
$mm = $_POST['mm'];
$yy = $_POST['yy'];
$Filename='DATA'.$yy.$mm.$dd.'.log';
$cwd =getcwd();
$rc=0;
echo 'Filename='.$Filename.'<br>';
// Change directory
chdir("/nfs/OGN/DIRdata/data/");

ob_start();
passthru('/usr/bin/python2.7 ../../src/analysisrelay.py -sa YES -n '.$Filename.' ', $rc);
$output = ob_get_clean(); 
echo nl2br($output);
?>

