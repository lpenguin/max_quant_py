import argparse
import sys
from os.path import abspath, exists
from typing import Dict, Any

from maxquant.batch import parse_batches
from maxquant.cli.misc import print_and_exit
from maxquant.maxquant import run_maxquant
from maxquant.mqpar import read_mqpar_config
from maxquant import version

from scheduler.parser import json, sh

def validate_args(args):
    if not exists(args.mqpar):
        print_and_exit('mqpar file does not exist: {}'.format(args.mqpar))

    if not exists(args.max_quant_cmd):
        print_and_exit('MaxQuant command binary {} does not exist'.format(args.max_quant_cmd))


def validate_config(config: Dict[str, Any]):
    for file_path in config['filepaths']:
        if not exists(file_path):
            print_and_exit('Raw file does not exist: {}'.format(file_path))

    if not exists(config['database']):
        print_and_exit('FASTA database does not exist: {}'.format(config['database']))


def main():
    parser = argparse.ArgumentParser(
        prog='maxquant-batch',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('-c', '--mqpar', help='mqpar.xml path', default='mqpar.gen.xml')
    parser.add_argument('-C', '--max-quant-cmd', default='MaxQuant/bin/CommandLine.exe',
                        help='MaxQuant Commandline.exe binary')
    parser.add_argument('-p', '--custom-params')
    parser.add_argument('-o', '--output', help='Output file, default is stdout')
    parser.add_argument('-f', '--format', choices=['json', 'sh'], default='json')
    parser.add_argument('--version', '-V', action='version', version="%(prog)s " + version.get_version())

    args = parser.parse_args()
    validate_args(args)

    args.mqpar = abspath(args.mqpar)

    if args.custom_params:
        custom_params = args.custom_params.split(' ')
    else:
        custom_params = []

    mqpar_config = read_mqpar_config(args.mqpar)

    validate_config(mqpar_config)
    filepaths = mqpar_config['filepaths']

    res = run_maxquant(
        max_quant_cmd=args.max_quant_cmd,
        options=['-c', args.mqpar, '-D'] + custom_params
    )

    batches = parse_batches(res, filepaths, threads=mqpar_config['threads'])

    if args.output:
        f = open(args.output, 'w')
    else:
        f = sys.stdout

    if args.format == 'json':
        json.write_config(f, batches)
    elif args.format == 'sh':
        sh.write_config(f, batches)

    if f is not sys.stdout:
        f.close()


if __name__ == '__main__':
    main()


