<?php

// do one set operation for key den_a_key1 and store current time
// and does maxIterations gets with 1 second sleep in between
// prints final result

$mc = new Memcached();

$mcaddress = 'localhost';
$mcport = 11211;
$mc->addServer($mcaddress, $mcport);

$value = date("H:i:s");
$key = "den_a_key1";

$result = $mc->set($key, $value);

$result = $mc->get($key);
print($result);
print("<br/>");

$maxIterations = 60;

$results = [];

while ($maxIterations > 0) {
	$maxIterations--;

	if (!$mc->get($key)) {
		 $results[$maxIterations] = "error" . $mc->getResultCode();
	} else {
		$results[$maxIterations] = "success";
	}

	sleep(1);
}

print("<br/>");
var_dump($results);
print ("<br/> done");

?>
