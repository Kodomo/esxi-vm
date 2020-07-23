import os.path

import sys
import yaml
import datetime                   # For current Date/Time
import re                         # For regex
import paramiko                   # For remote ssh


def setup_config():

    #
    #   System wide defaults
    #
    config_data = dict(

        #   Your logfile
        LOG=os.path.expanduser("~") + "/esxi-vm.log",
        writeLog=False,  # By default, do NOT write logs

        #  Enable/Disable dryrun by default
        isDryRun=False,

        #  Enable/Disable Verbose output by default
        isVerbose=False,

        #  Enable/Disable exit summary by default
        isSummary=False,

        #  ESXi host/IP, port, root login & password
        HOST="esxi",
        PORT=22,
        USER="root",
        PASSWORD="",
        KEY="",

        #  Default number of vCPU's, MB Mem, & GB boot disk
        CPU=2,
        MEM=4096,
        HDISK=20,

        #  Default Disk format thin, zeroedthick, eagerzeroedthick
        DISKFORMAT="thin",

        #  Virtual Disk device type
        VIRTDEV="pvscsi",

        #  Specify default Disk store to "LeastUsed"
        STORE="LeastUsed",

        #  Default Network Interface (vswitch)
        NET="None",

        #  Default ISO
        ISO="None",

        #  Default GuestOS type.  (See VMware documentation for all available options)
        GUESTOS="debian8-64",

        # Extra VMX options
        VMXOPTS=""
    )

    config_data_file_location = os.path.expanduser("~") + "/.esxi-vm.yml"

    #
    # Get ConfigData from ConfigDataFile, then merge.
    #
    if os.path.exists(config_data_file_location):
        from_file_config_data = yaml.safe_load(open(config_data_file_location))
        config_data.update(from_file_config_data)

    try:
        with open(config_data_file_location, 'w') as FD:
            yaml.dump(config_data, FD, default_flow_style=False)
        FD.close()
    except Exception as e:
        print("Unable to create/update config file {}".format(config_data_file_location))
        print("The Error is {}".format(e))
        sys.exit(1)
    return config_data


def save_config(config_data):
    config_data_file_location = os.path.expanduser("~") + "/.esxi-vm.yml"
    try:
        with open(config_data_file_location, 'w') as FD:
            yaml.dump(config_data, FD, default_flow_style=False)
        FD.close()
    except Exception as e:
        print("Unable to create/update config file {}".format(config_data_file_location))
        print("The Error is {}".format(e))
        return 1
    return 0


def the_current_date_time():
    i = datetime.datetime.now()
    return str(i.isoformat())


def exec_ssh_command(message, command, ssh, verbose):
    if verbose:
        if message:
            print(message)
        print("SSH: " + command)
    return ssh.exec_command(command)


def get_esxi_version(ssh, verbose):
    try:
        (stdin, stdout, stderr) = exec_ssh_command("Get ESXi version", "esxcli system version get |grep Version",
                                                   ssh, verbose)
        if re.match("Version", str(stdout.readlines())) is not None:
            print("Unable to determine if this is a ESXi Host")
            sys.exit(1)

    except Exception as e:
        print("Unable to get ESXi version")
        print("The Error is {}".format(e))
        sys.exit(1)


def connect_to_esxi(host, port, user, password, key, verbose):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if key:
            ssh.connect(host, port=port, username=user, key_filename=key)
        else:
            ssh.connect(host, port=port, username=user, password=password)
        get_esxi_version(ssh, verbose)
        return ssh
    except Exception as e:
        print("Unable to access ESXi Host: {}, port: {}, username: {}, key: {}".format(host, port, user, key))
        print("The Error is {}".format(e))
        sys.exit(1)
