# TyStream

*This is a final year project in City University of Hong Kong. Project code: 19CS038.*

Contact: kaiwenxue3-c@my.cityu.edu.hk

## Abstract

Video streaming is one of the most popular services on the Internet. Researchers have endeavored to develop new algorithms and protocols across the application layer and transport layer to improve the performance of such service. We propose TyStream, a generic evaluation platform, to simplify the evaluation process of these algorithms and protocols at different computer network layers. We define four network parameters and decouple them in our design. Results show that our evaluation platform can test the supported algorithms correctly and the design logic of TyStream ensures that this system is convenient, efficient, and extensible.



## Installation

Tested on: Ubuntu 18.04

- [Mahimahi](http://mahimahi.mit.edu/): **Build from source** by referring to the official guide. Then replace `packet/packetshell.*` with our files in `mahimahi`

- Video servers:
  - Apache: Ubuntu built-in. Copy everything inside `www.quictest.com` to `/var/www/html`. Delete the HTML header in each file.
  - QUIC: Read [Quic Server Installation Guide](./docs/quic_server_installation_guide.md)
- **Both** Python2 and Python3. Recommend managing environments with conda. Packages:
  - numpy
  - matplotlib
  - pyautogui
- Google chrome browser



## Usage

### CONFIG

Four sets of configurations are supported: `trace`, `transport`, `cc`, `abr`. A list of supported parameters are in `config/supported.json`

Check current configuration:

```
config
```

Switch a configuration:

```
config config_key config value
```

For example:

```
config trace ATT-LTE-driving
```



### EXP

```
exp run_time
```

`run_time` is the number of times that you want to repeat your experiment. Must be a positive integer.

Results are stored in `exp/results/`



### PLOT

The visualization configuration consists of external and internal. The internal one will be set to the same as the experiment configuration of the last experiment. If you want to change the default, find it in `vis/generic_visualizer.py` and rewrite your desired one.

The external one consists of the same set of `config_key`. 3 of them are fixed and one should be a list. There's another field called `dir` for the external configuration, which decides the directories of the varied parameter. For example, if your varied parameter is `abr` with `['mpc', 'robustmpc']`, `dir1` and `dir2`, where `dir: [dir1, dir2]`, should contain the log files of `mpc` and `robustmpc` respectively.

To change the external configuration:

```
plot dir n dir1 dir2 ... dirn, or
plot var config_key n config_value1 ... config_valuen
```

For the above example, it should be

```
plot dir 2 dir1 dir2
plot var abr 2 mpc fastmpc
```



To visualizer the results, use the above setting and

```
plot
plot link_utilization
plot qoe
plot bitrate_selection
plot bandwidth_estimation
```

, where the default diagram of `plot` is link utilization. We currently support 4 types of visualization methods.



## Acknowledgement

`Dash.js` and video files in `www.quictest.com` , and decision servers in`abr_servers/`are provided by [Pensieve](https://github.com/hongzimao/pensieve) with a few modifications. We also learn from Pensieve's evaluation code when designing the work flow of this project.