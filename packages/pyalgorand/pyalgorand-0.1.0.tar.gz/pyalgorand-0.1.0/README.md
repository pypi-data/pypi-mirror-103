# Pyalgorand


```

  ____           _    _                                 _
 |  _ \ _   _   / \  | | __ _  ___  _ __ __ _ _ __   __| |
 | |_) | | | | / _ \ | |/ _` |/ _ \| '__/ _` | '_ \ / _` |
 |  __/| |_| |/ ___ \| | (_| | (_) | | | (_| | | | | (_| |
 |_|    \__, /_/   \_\_|\__, |\___/|_|  \__,_|_| |_|\__,_|
        |___/           |___/

```


## Overview

PyAlgorand aims at simplifying development on the Algorand blockchain.

## Installation

pip install pyalgorand

## Optional installation

If one wants to use an Algorand sandbox network, please go to https://github.com/algorand/sandbox for more details.

If one wants to use IPFS features in pyalgorand and test them locally, it is recommended to use the following procedure:

```bash

 wget https://dist.ipfs.io/go-ipfs/v0.7.0/go-ipfs_v0.7.0_linux-amd64.tar.gz
 tar -xvzf go-ipfs_v0.7.0_linux-amd64.tar.gz
 cd go-ipfs && sudo ./install.sh && ipfs init && ipfs daemon &

```

Note that `sudo` might not be necessary on your system.


## Getting started

Some examples are available in [here](https://bitbucket.org/kuiristo/pyalgorand/src/master/examples/):

- how to create accounts
- share files on IPFS and secure them

Start with the creation of accounts. Some of the examples require Purestake API, register [here](https://developer.purestake.io/login).
