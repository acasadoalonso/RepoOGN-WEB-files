<?php
$station = $_POST['regis'];

$cwd =getcwd();
$rc=0;
echo 'station='.$station.'<br>';
//echo getcwd();
ob_start();

<<<<<<< HEAD
passthru('/usr/bin/python3  ./gstats.py '.$station, $rc);
=======
passthru('/usr/bin/python2.7  ./gstats.py '.$station, $rc);
>>>>>>> b327be6f7782a4e8677b2b133fbec3c25ad19743

$output = ob_get_clean();
echo nl2br($output);
?>
