# MaxQuant scripts

# Installation

```bash
cp -r /home/nprian/software/MaxQuant.16013.wiff_fix.cmd <software directory>

git clone http://git.ripcm.com/Prianichnikov/max_quant_py.git
cd max_quant_py
pip3 install --user .

cd ..
git clone https://github.com/lpenguin/simple_drmaa_scheduler
cd simple_drmaa_scheduler
pip3 install --user .

# Add $HOME/.local/bin to $PATH
```

# Usage

## Directory structure
```bash
$ ls -1
data/  # directory with .wiff and .wiff.scan files 
database.fasta@  # link to database 
MaxQuant@  # link to MaxQuant distribution
mqpar.base.xml@  # Link to mqpar base template
```

## Getting help
```bash
$ maxquant -h
usage: maxquant [-h] [-c MQPAR_GENERATED] [-T MQPAR_TEMPLATE] [-d DATABASE]
                [-t THREADS] [-C MAX_QUANT_CMD] [-p CUSTOM_PARAMS]
                files [files ...]

positional arguments:
  files                 *.wiff files

optional arguments:
  -h, --help            show this help message and exit
  -c MQPAR_GENERATED, --mqpar-generated MQPAR_GENERATED
                        Generated mqpar path (default: mqpar.gen.xml)
  -T MQPAR_TEMPLATE, --mqpar-template MQPAR_TEMPLATE
                        Template mqpar (default: mqpar.base.xml)
  -d DATABASE, --database DATABASE
                        Database (default: database.fasta)
  -t THREADS, --threads THREADS
                        Num of threads, do not use on cluster (default: 1)
  -C MAX_QUANT_CMD, --max-quant-cmd MAX_QUANT_CMD
                        MaxQuant Commandline.exe binary (default:
                        MaxQuant/bin/CommandLine.exe)
  -p CUSTOM_PARAMS, --custom-params CUSTOM_PARAMS

```

## Generating batch
```bash
$ maxquant ./data/*.wiff > batch.json
```

## Sending jobs to cluster
```bash
# Print batches
$ scheduler -d batch.json

# Send to cluster
$ scheduler -S -j <num of cores> -d batch.json
```

