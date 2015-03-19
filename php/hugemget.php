<?php

// do one set operation for key den_a_key1 and store current time
// and does maxIterations gets with 1 second sleep in between
// prints final result

$mc = new Memcached();

$mcaddress = 'dsamoylov2';
$mcport = 11211;
$mc->addServer($mcaddress, $mcport);

// check memcached is here
/*
$value = date("H:i:s");
$key = "den_a_key1";
$result = $mc->set($key, $value);
$result = $mc->get($key);
print($result);
*/
print("<br/>");

$numOfObjects = 2046;

$keys = [];

while ($numOfObjects > 0) {
    array_push($keys, 'a' . $numOfObjects);
    $numOfObjects--;
}

$res = $mc->getMulti($keys);
if (!$res) {
    print("error:" . $mc->getResultCode());
} else {
    print("success:" . count($res));
}

print ("<br/> done");

?>
