## Organization of Folders

```
scripts/
|----log_reader/
     |----__init__.py
     |----mahimahi.py
     |----rl_server.py
|----README.md
|----plot_throughput_abr.py
|----plot_throughput_cc.py
```



## General Requirements

- Put the information that can be fetched, as well as functions to fetch those information in classes in `mahimahi.py` and `rl_server.py`
- Implementations of plotting should be written in separate files categorized by functionality (what information to include, what to compare)



## Mahimahi Reader

Implemented in `mahimahi.py`.

Class:

- MMReader

Methods:

- constructor: with `MS_PER_BIN` and expected time

Attrtibutes:

- duration
- initial timestamp
- dictionary {time: throughput}
- dictionary {time: capacity}
- mean throughput
- mean capacity
- utilization of capacity



## Reinforcement Learning Log Reader

Implemented in `rl_server.py`

Class:

- RLReader

Methods:

- constructor

Attributes:

- duration
- mean QoE
- dictionary {time: estimation}

