==================
python-reddcoinrpc
==================

AuthServiceProxy is an improved version of python-jsonrpc.

It includes the following generic improvements:

* HTTP connections persist for the life of the AuthServiceProxy object
* sends protocol 'version', per JSON-RPC 1.1
* sends proper, incrementing 'id'
* uses standard Python json lib
* can optionally log all RPC calls and results
* JSON-2.0 batch support

It also includes the following reddcoin-specific details:

* sends Basic HTTP authentication headers
* parses all JSON numbers that look like floats as Decimal,
  and serializes Decimal values to JSON-RPC connections.
* read config from ~/.reddcoin/reddcoin.conf as default or specify a different path

Installation
============

1. change the first line of setup.py to point to the directory of your installation of python 2.*
2. run setup.py

Note: This will only install reddcoinrpc. If you also want to install jsonrpc to preserve
backwards compatibility, you have to replace 'reddcoinrpc' with 'jsonrpc' in setup.py and run it again.

Or simply install the library using pip::

    pip install python-reddcoinrpc

Example
=======
.. code:: python

    from reddcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

    # rpc_user and rpc_password are set in the bitcoin.conf file
    rpc_connection = AuthServiceProxy()
    best_block_hash = rpc_connection.getbestblockhash()
    print(rpc_connection.getblock(best_block_hash))

    # batch support : print timestamps of blocks 0 to 99 in 2 RPC round-trips:
    commands = [ [ "getblockhash", height] for height in range(100) ]
    block_hashes = rpc_connection.batch_(commands)
    blocks = rpc_connection.batch_([ [ "getblock", h ] for h in block_hashes ])
    block_times = [ block["time"] for block in blocks ]
    print(block_times)

Logging all RPC calls to stderr
===============================
.. code:: python

    from reddcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
    import logging

    logging.basicConfig()
    logging.getLogger("ReddcoinRPC").setLevel(logging.DEBUG)

    rpc_connection = AuthServiceProxy()
    print(rpc_connection.getinfo())

Produces output on stderr like

    DEBUG:ReddcoinRPC:-1-> getinfo []
    DEBUG:ReddcoinRPC:<-1- {"connections": 8, ...etc }

Socket timeouts under heavy load
================================
Pass the timeout argument to prevent "socket timed out" exceptions:

.. code:: python

    rpc_connection = AuthServiceProxy(
                rpctimeout=120)
