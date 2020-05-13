# Pensieve and Mahimahi in Experiment

## Mahimahi

Install [Mahimahi](http://mahimahi.mit.edu/)

Use `man mm-link` to see how to use mahimahi and the documentation of mahimahi's log. In our experiment, basically we use

```
mm-delay 40 mm-link --uplink-log=[intended log location] --downlink-log=[intended log location] [uplink trace] [downlink trace]
```

This can be integrated into a python script

## Pensieve

`run_exp/run_all_traces` or any other trace runner will set up mahimahi shell and call `run_exp/run_video.py`, which will start `localhost:8333` as rl_server, start a web server, and use chrome to request chunks from the web server.

Files in web server are contained in `video_server`, which includes a modified `dash.js` and several html files used for different ABR algorithms.



## Experiment (Own PC)

Download/clone/recompile the following either from emulab server or github:

```
www.quictest.com/
quic/
Video-Streaming-Protocol/
mahimahi/
```

### Setting Up Quic Server

Generate certificate for quic server

```shell
cd quic/certs/
./generate-certs.sh
```

Under the same folder, add the generated certificate to linux's root certificate store, refer to [this site](https://chromium.googlesource.com/chromium/src/+/master/docs/linux_cert_management.md)

```shell
certutil -d sql:$HOME/.pki/nssdb -A -t "C,," -n chromium \
-i ./out/2048-sha256-root.pem
```
If error "certutil: function failed: security library: bad database" occured, solve it using commands below,
```
mkdir -p $HOME/.pki/nssdb
certutil -d $HOME/.pki/nssdb -N
```

Install google-chrome-stable and dpkg
```
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt-get install dpkg -y
sudo dpkg -i google-chrome-stable_current_amd64.deb
```
Move `www.quictest.com/` to `/tmp/quic-data/www.quictest.com/`

Start quic server:

```shell
cd quic
./out/Debug/quic_server \
  --quic_response_cache_dir=/tmp/quic-data/www.quictest.com \
  --certificate_file=certs/out/leaf_cert.pem \
  --key_file=certs/out/leaf_cert.pkcs8 --v=1
```

Note that `--v=1` flag is to enable server's logging, output to stdout

Use google chrome to test the client-server connection:

```shell
google-chrome-stable \
  --no-proxy-server \
  --enable-quic \
  --origin-to-force-quic-on=www.quictest.com:443 \
  --host-resolver-rules='MAP www.quictest.com:443 127.0.0.1:6121' \
  https://www.quictest.com/myindex_fastMPC.html
```



### Automated Experiment

Use a random `mm-link` command, enter the link and see the `$MAHIMAHI_BASE`

```shell
cd Video-Streaming-Protocol/experiments/scripts/trace_runner/
mm-link ../cooked_traces/Verizon-LTE-short.up ../cooked_traces/Verizon-LTE-short.down
```

then, in the link,

```shell
echo $MAHIMAHI_BASE
```

Copy the IP of `$MAHIMAHI_BASE` and modify it in `run_quic_video.py`. In line 13, change the last server IP to whatever your `$MAHIMAHI_BASE`

```
--host-resolver-rules='MAP www.quictest.com:443 100.64.0.15:6121' \
```

Then run the test using

```shell
python run_quic_traces.py [trace_name] [log_name] [running_time]
```

For example,

```
python run_quic_traces.py Verizon-LTE-short mmtest 1
```

runs over Verizon short link for one time with the downlink log's name of `mmtest_down1`
