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
# default_exp __main__
# -

# ```
# # example: usage from code
#
# from lib_name.__main__ import run, ETL_SCRIPTS
#
# for etl in ETL_SCRIPTS:
#     run(etl)
# ```

# ```
# # example: usage as script
#
# DATA_PATH="..." python -m lib_name --name "*"
# ```

# +
# exporti

import datetime
import fnmatch
import argparse

from {lib_name} import paths
from {lib_name} import utils

# +
# export

# NOTE: the order of the list determines the execution order when using patterns for name argument
ETL_SCRIPTS = ['etl_sample']


# +
# export

def run(name):
    # get function by name
    fn = globals()[name]
    # and execute it
    fn()


# +
# exporti

def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Execute ETLs")
    parser.add_argument("--name", required=False, default="*", type=str, help="The name of the ETL to execute. Globs are allowed.")

    
    return parser.parse_args(args)


# +
# exporti

def etl_sample():

    name = "etl_sample"
    
    utils.log(f"Start etl {name}")

    # For example load and using the path of a dataset such as:
    #   > pd.read_csv(paths.DATASET_EXAMPLE)


    utils.log(f"End etl {name}")


# +
# export

# NOTE: Must be in the last cell of the jupyter notebook
if __name__ == "__main__":

    args = parse_args()
    names = fnmatch.filter(ETL_SCRIPTS, args.name)

    # clean logfile before start any process
    utils.clear_logfile()
    
    for name in names:
        run(name)
    
    # send the logfile
    utils.send_logfile(paths.DATA_PATH, f"logs/{datetime.datetime.utcnow().strftime('%Y-%m-%d')}-etl.json")
