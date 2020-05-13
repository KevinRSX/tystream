#!/bin/bash
# modified from Frank's script

website=${1:-https://www.quictest.com}
webhost=${2:-127.0.0.1} # apache server

function get_with_headers()
{
        wget -p --save-headers http://$1/$3;
        sed -i "1i\X-Original-Url: $2/$3" $1/$3;
}

cd /tmp/quic-data/
# wget -p --save-headers http://${webhost}/myindex_BB.html/;
# sed -i "1i\X-Original-Url: ${website}/myindex_BB.html/" ${webhost}/myindex_BB.html;

for file in myindex_BB.html myindex_BOLA.html myindex_fastMPC.html myindex_FESTIVE.html myindex_FIXED.html myindex.html myindex_newdash.html myindex_RB.html myindex_RL.html myindex_robustMPC.html
do
    get_with_headers $webhost $website $file
done

for file in Manifest.mpd dash.all.min.js
do
	get_with_headers $webhost $website $file
done

for i in {1..6}
do
    echo "getting video${i}"
	for j in {1..49}
	do
		get_with_headers $webhost $website video${i}/${j}.m4s 
	done
	get_with_headers $webhost $website video${i}/Header.m4s 
done