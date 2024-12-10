# SPEEDER
Perform an automatic speedtest using librespeed server (https://github.com/librespeed/speedtest) and librespeed-cli (https://github.com/librespeed/speedtest-cli), given a server list (server_list.json) and store the results in a MariaDB database (speedtest.sql).

## INSTALLATION
Just clone the repository:

    git clone https://github.com/M0sfet/speeder.git
  
Once done install the needed libraries with the command:

    pip install -r requirements.txt
## RUNNING SPEEDER
-h|--help shows the usage

    python3 speeder.py -h
    usage: speeder.py [-h] -t TARGETS -d DATABASE [-f FREQ]

    Speeder - Automatic Speedtest daemon

    options:
      -h, --help            show this help message and exit
      -t TARGETS, --targets TARGETS
                        Path to the custom speedtest server list
      -d DATABASE, --database DATABASE
                        Path to database config file
      -f FREQ, --freq FREQ  Speed test frequency, specified in seconds. Default run test every 300 seconds.
