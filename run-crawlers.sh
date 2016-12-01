#!/bin/sh
rm data/*
scrapy crawl cnn -o "data/cnn.json" -t json