# quic_server and quic_client Setting up Procedure

This procedure works fine on Ubuntu 18.04 (virtual machine). May also works on Mac.

## 1. Build and Basic Setup

-   Follow all the instructions before “Build Chromium” in  [Checking out and building Chromium](https://www.chromium.org/developers/how-tos/get-the-code) to fetch the source code of chromium and prepare for building `quic_server` and `quic_client`
-   Follow all the instructions in [Play with QUIC](https://www.chromium.org/quic/playing-with-quic)
    -   Build the QUIC client and server
    -   Prepare test data from www.example.org, and modify the header with adding `X-Original-Url`
    -   Generate certificates and import it into Google Chrome.
    -   Run the `quic_server`and `quic_client `to see if they works.

## 2. Run QUIC in chrome

### 2.1 Test with www.example.org

Run the `quic_server`with the following command:

```bash
./out/Debug/quic_server \
  --quic_response_cache_dir=/tmp/quic-data/www.example.org \
  --certificate_file=net/tools/quic/certs/out/leaf_cert.pem \
  --key_file=net/tools/quic/certs/out/leaf_cert.pkcs8
```

Note that the above paths may need to be changed to the actual location of the files on the machine.



Run the release verison of chrome in terminal:

```bash
google-chrome-stable \
	--no-proxy-server \
    --enable-quic \
    --origin-to-force-quic-on=www.example.org:443 \
    --host-resolver-rules='MAP www.example.org:443 127.0.0.1:6121' \
    https://www.example.org
```

## 3. Run customized `index.html` and Dash.js on QUIC

### 3.1 Prepare website files with headers

-   Use Caddy Web Server to server the following directory on 127.0.0.1:2015 (Default port)

```
quic_experiment_files/
|----index.html (calls dash.js)
|----dash.all.min.js
|----video/
     |----Manifest.mpd
     |----video1/
     |----video2/
     |----video3/
     |----video4/
     |----video5/
     |----video6/
```

-   Go to `/tmp/quic_data/`
-   Edit the shell script `getFilesWithHeaders.sh` to add headers to the website files:

```shell
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
```

-   Run by `bash getFilesWithHeaders.sh`
-   Modify the name of the generated folder from `127.0.0.1:2015` to `www.example.org`.

### 3.1 Test

Follow **2.1**.

## 4. Customize the website name

### 4.1 Regenerate certificate

Under `net/tools/quic/certs` directory, modify `leaf.cnf`:

```
SUBJECT_NAME = req_dn
KEY_SIZE = 2048

[req]
default_bits       = ${ENV::KEY_SIZE}
default_md         = sha256
string_mask        = utf8only
prompt             = no
encrypt_key        = no
distinguished_name = ${ENV::SUBJECT_NAME}
req_extensions     = req_extensions

[req_dn]
C  = US
ST = California
L  = Mountain View
O  = QUIC Server
CN = 127.0.0.1

[req_extensions]
subjectAltName = @other_hosts

[other_hosts]
DNS.1 = www.example.org
DNS.2 = mail.example.org
DNS.3 = mail.example.com
DNS.4 = www.quictest.com /Please delete me     Add an entry here	Please delete me/
IP.1 = 127.0.0.1
```

Regenerate the ceritificate by running `generate-certs.sh` and import the new certificate to Google Chrome.

### 4.2 Modify headers

Follow **3.1** and modify the website domain in the `getFilesWithHeaders.sh` to www.quictest.com, and regenerate the website files.

### 4.3 Test

Run the `quic_server`with the following command:

```bash
./out/Debug/quic_server \
  --quic_response_cache_dir=/tmp/quic-data/www.quictest.com \
  --certificate_file=net/tools/quic/certs/out/leaf_cert.pem \
  --key_file=net/tools/quic/certs/out/leaf_cert.pkcs8
```

Note that the above paths may need to be changed to the actual location of the files on the machine.



Run the release verison of chrome in terminal:

```bash
google-chrome-stable \
	--no-proxy-server \
    --enable-quic \
    --origin-to-force-quic-on=www.quictest.com:443 \
    --host-resolver-rules='MAP www.quictest.com:443 127.0.0.1:6121' \
    https://www.quictest.com
```

## Reference

[QUIC Prototype Protocol Discussion Group](https://groups.google.com/a/chromium.org/forum/#!topic/proto-quic/2nyLYC6JTBo)

[experiment-tasks](https://github.com/NetX-lab/Video-Streaming-Protocol/blob/master/experiments/notes/experiment-tasks.md)

[Checking out and building Chromium on Linux](https://chromium.googlesource.com/chromium/src/+/master/docs/linux_build_instructions.md)

[Playing with QUIC](https://www.chromium.org/quic/playing-with-quic)

