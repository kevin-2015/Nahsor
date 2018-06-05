# -*- coding:utf-8 -*-
'''
作者：浪晋
时间：2018-6-2
说明：处理接受命令行的命令
'''
import argparse
# version = "test"
parser = argparse.ArgumentParser()
parser.add_argument(
    '-v', '--version',  action='store_true',
    help="show version")
args = parser.parse_args()
if args.version:
    print("version")
    exit(0)

