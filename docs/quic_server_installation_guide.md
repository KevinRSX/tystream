# QUIC Server Installation Guide for TyStream

## Preparation

TyStream uses Google's open source QUIC server, which is a part of Chromium project.

First, check out and build chromium on Linux, following: https://chromium.googlesource.com/chromium/src/+/master/docs/linux/build_instructions.md

Then, build a the QUIC server and client in `chromium/src/`:

```
ninja -C out/Debug quic_server quic_client
```

Copy `www.quictest.com/` to `/tmp/quic-data/`

```
cp -r www.quictest.com/ /tmp/quic-data/
```



## Certificate

In `chromium/src/`:

Generate a new certificate:

```
cd net/tools/quic/certs
./generate-certs.sh
```

Note that the certificate you generate lasts for three days. Then add it to Linux root certificate store:

```
certutil -d sql:$HOME/.pki/nssdb -A -t "C,," -n  <certificate_nickname> \
-i net/tools/quic/certs/out/2048-sha256-root.pem
```

Refer to this page: https://chromium.googlesource.com/chromium/src/+/master/docs/linux/cert_management.md for Linux certificate management information.



## Start the Server

When starting the server, you need to specify the directory of files you are serving the location of certificates:

```
./out/Debug/quic_server \
  --quic_response_cache_dir=/tmp/quic-data/www.quictest.com \
  --certificate_file=net/tools/quic/certs/out/leaf_cert.pem \
  --key_file=net/tools/quic/certs/out/leaf_cert.pkcs8
```



If you would like to test if the server is correctly serving videos, turn verbose on by adding `--v=1` to the above command. You may also want to play with the corresponding simple Quic client that requests HTML contents:

```
./out/Debug/quic_client --host=127.0.0.1 --port=6121 --disable_certificate_verification https://www.quictest.com/myindex_fastMPC.html
```



## Use BBR

The default CC used by QUIC is Cubic. You have to modify the source code of QUIC and recompile it to use BBR. Refer to this: https://groups.google.com/a/chromium.org/g/proto-quic/c/g27OSwdBeqM?pli=1

Notice that you can compile your BBR implementation to another directory. When generating the build directory using `gn`, specify your desired one. But it is recommended that you put it in `out/` for consistency.

```
gn gen out/[desired_bbr_dir]
```

