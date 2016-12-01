#!/bin/sh
rm -rf data
mkdir data
scrapy crawl cnn -o "data/cnn.json" -t json