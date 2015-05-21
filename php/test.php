<?php

$methods_to_use_slave = 'yyy, xxxx';
$methods_to_use_slave_arr = explode(',', $methods_to_use_slave);
$method = "xxxx";

if (in_array($method, $methods_to_use_slave_arr)) {
    print "in array";
} else {
    print "NOT in array";
}

print "DONE";