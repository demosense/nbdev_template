# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
# default_exp utils
# -

# exporti
import argparse
import gzip
from io import BytesIO, TextIOWrapper
import pandas as pd
import os
import sys
import s3fs
import logging
from logging.handlers import WatchedFileHandler
import psutil
import time
import json

# +
# exporti

# aws
s3 = s3fs.S3FileSystem()

def _get_filesystem(path):
    fs = "s3" if path.split(":")[0] == "s3" else "file"
    fs_open = s3.open if fs == "s3" else open

    if fs == "file":
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    return fs_open


# +
# export

def write_parquet(df, path):
    """
        Returns size in MBs
    """

    # path = os.path.normpath(f"{output_path}")

    _get_filesystem(path) 

    df.to_parquet(path, index=None)



# +
# export

LOG_FILEPATH = '/tmp/etl.log'

def log(message, **kwargs):
    logger.info(
        message,
        extra=dict(
            memory = process.memory_info().rss / (1024 * 1024),
            timestamp=int(time.time()),
            params=json.dumps(kwargs, default=str)  # params items must be json serializable
        )
    )
    
    
def clear_logfile():
    if os.path.isfile(LOG_FILEPATH):
        os.remove(LOG_FILEPATH)
        
def send_logfile(dirpath, filepath):
    try:
        with open(LOG_FILEPATH, 'rb') as f:
            bstr = f.read()
    except:
        bstr = None
    
    path = dirpath + '/' + filepath
    
    fs_open = _get_filesystem(path) 
    
    if bstr:
        with fs_open(path, "wb") as f:
            f.write(bstr)
        print(f"logfile has been written to {path}")
    else:
        print("No logfile to send")


# +
# exporti

# psutil
process = psutil.Process(os.getpid())

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# logging to stdout
syslog = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s %(asctime)s %(memory)dMB %(message)s')
syslog.setFormatter(formatter)
logger.addHandler(syslog)

# logging to file
fh = WatchedFileHandler(LOG_FILEPATH)
log_format = '{"timestamp": %(timestamp)s, "memory": %(memory)d, "message": %(message)s, "params": %(params)s}'
fh.setFormatter(logging.Formatter(log_format))
logger.setLevel(logging.INFO)
logger.addHandler(fh)
