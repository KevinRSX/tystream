#!/bin/bash

website=https://www.quictest.com

wget -p --save-headers http://127.0.0.1:2015/;
sed -i "1i\X-Original-Url: ${website}/" 127.0.0.1:2015/index.html;

for  file in  video/Manifest.mpd dash.all.min.js
do
	wget -p --save-headers http://127.0.0.1:2015/${file};
	sed -i "1i\X-Original-Url: ${website}/${file}" 127.0.0.1:2015/${file};
done

for i in {1..6}
do
	echo $i
	for j in {1..49}
	do
		echo $j
		wget -p --save-headers http://127.0.0.1:2015/video/video${i}/${j}.m4s;
		sed -i "1i\X-Original-Url: ${website}/video/video${i}/${j}.m4s" 127.0.0.1:2015/video/video${i}/${j}.m4s;
	done
	wget -p --save-headers http://127.0.0.1:2015/video/video${i}/Header.m4s;
	sed -i "1i\X-Original-Url: ${website}/video/video${i}/Header.m4s" 127.0.0.1:2015/video/video${i}/Header.m4s;
done
