<?php

class Box_FakeItem {
	public $iVal;
	public $bVal;
	public $dVal;
	public $sVal;
}

$v = new Box_FakeItem();

$v->iVal = 123;
$v->bVal = false;
$v->dVal = 1.23;
$v->sVal = "abc";

$s = serialize($v);

print $s;


$a = [];


$b = explode(";", $a[1]);

if (!$b || count($b) != 2) {
    print "error";
} else {
    print $b;
}

print "DONE";