#!/bin/bash
dir="/data2/py/py27/pyspider/tmallPage"
cd $dir
. ../../bin/activate

while :
do
	scrapy crawl Aas
done
