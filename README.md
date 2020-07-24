TL-DR
-----
On a clean VM as root

```
apt install python3-pip git
git clone https://github.com/Kodomo/esxi-vm
pip3 install paramiko pyyaml
cd esxi-vm
make install
```

then, as a normal user you setup your credentials and create a VM

```
esxi-vm-create -u -H esxi.host.local -U root -P My!Secure#Password
esxi-vm-create -n TestDebian8VM
```

the VM is fully compatible with VMWare ESXi 6.0

Introduction
------------

This utility is a simple to use command line tool to create or destroy VMs on an ESXi host from from a system running python and SSH. vCenter is **not required**. This tool is an easy way to automate building VM's from command line or from other testing or automation tools such as Bamboo, Puppet, Saltstack, or Chef.

Requirements
------------

* You must enable SSH access on your ESXi server. The VMware VIX API tools are **not required**.

* It's **highly recommenced** to use password-less authentication by copying your SSH public keys to the ESXi host, otherwise your ESXi root password could be stored in clear-text in your home directory.

* Python **3**, [paramiko](http://www.paramiko.org) and [PyYAML](https://github.com/yaml/pyyaml):

```
apt install python3-pip
pip3 install paramiko pyyaml
```

Usage
-----

* Get help using `--help` option.   The defaults will be displayed in the help output.

* The only command line required parameter is the VM name (`-n`), all other command line arguments are optional.

* Defaults are stored in your home directory in `~/.esxi-vm.yml`.   You can edit this file directly, or you can use the tool to update most the defaults by specifying `--updateDefaults`.

* One of the first settings to set and save as defaults is the `--Host` (`-H`), `--User` (`-U`) and `--Password` (`-P`).

* Some basic sanity checks are done on the ESXi host before creating the VM.  The `--verbose` (`-V`) option will give you a little more details in the creation process.  If an invalid *Disk Stores* or *Network Interface* is specified, the available devices will be shown in the error message. The tool will not show the list of available ISO images, and Guest OS types.  CPU, Memory, Virtual Disk sizes are based on ESXi 6.0 limitations.

* The `--dry` (`-d`) option will go through the sanity checks, but will not create the VM.

* By default the Disk Store is set to `LeastUsed`.  This will use the *Disk Store* with the most free space (in bytes).

* By default the ISO is set to `None`.  Specify the full path to the ISO image.   If you specify just the ISO image filename (no path), the system will attempt to find the ISO image on your DataStores.

* By default the Network set set to `None`. A full or partial MAC address can be specified. A partial MAC address argument would be 3 Hex pairs which would then be prepended by VMware's OEM `00:50:56`.

* By default the VM is powered on. If an ISO was specified, then it will boot the ISO image.  Otherwise, the VM will attempt a PXE boot if a Network Interface was specified.  You could customize the ISO image to specify the kickstart file, or PXE boot using COBBLER, Foreman, Razor, or your favorite provisioning tool.

* To help with automated provisioning, the script will output the full MAC address and exit code 0 on success.  You can specify `--summary` to get a more detailed summary of the VM that was created.

Command Line Args
-----------------

```bash
./esxi-vm-create --help

usage: esxi-vm-create [-h] [-d] [-H HOST] [-T PORT] [-U USER] [-P PASSWORD]
                      [-K KEY] [-n NAME] [-c CPU] [-m MEM] [-v HDISK] [-i ISO]
                      [-N NET] [-M MAC] [-S STORE] [-g GUESTOS] [-o VMXOPTS]
                      [-p POOL] [-V] [--summary] [-u]

ESXi Create VM utility.

optional arguments:
  -h, --help            show this help message and exit
  -d, --dry             Enable Dry Run mode (False)
  -H HOST, --Host HOST  ESXi Host/IP (esxi)
  -T PORT, --Port PORT  ESXi Port number (22)
  -U USER, --User USER  ESXi Host username (root)
  -P PASSWORD, --Password PASSWORD
                        ESXi Host password (*****)
  -K KEY, --Key KEY     ESXi Host path to private key ()
  -n NAME, --name NAME  VM name ()
  -p POOL, --pool NAME  Resource pool to attach the VM (ha-root-pool)
  -c CPU, --cpu CPU     Number of vCPUS (2)
  -m MEM, --mem MEM     Memory in MB (4096)
  -v HDISK, --vdisk HDISK
                        Size of virt hdisk (16)
  -i ISO, --iso ISO     CDROM ISO Path | None (None)
  -N NET, --net NET     Network Interface | None (None)
  -M MAC, --mac MAC     MAC address
  -S STORE, --store STORE
                        vmfs Store | LeastUsed (LeastUsed)
  -g GUESTOS, --guestos GUESTOS
                        Guest OS (centos-64)
  -o VMXOPTS, --options VMXOPTS
                        Comma list of VMX options
  -V, --verbose         Enable Verbose mode (False)
  -f LOG, --logfile LOG
                        Path to the log file (/Users/sebastien/esxi-vm.log)
  -l, --log             Write to log file (False)
  --summary             Display Summary (False)
  -u, --updateDefaults  Update Default VM settings stored in ~/.esxi-vm.yml
```

```nash
./esxi-vm-destroy --help

usage: esxi-vm-destroy [-h] [-H HOST] [-T PORT] [-U USER] [-P PASSWORD]
                       [-K KEY] [-n NAME] [-V] [--summary]

ESXi Destroy VM utility.

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --Host HOST  ESXi Host/IP (esxi)
  -T PORT, --Port PORT  ESXi Port number (22)
  -U USER, --User USER  ESXi Host username (root)
  -P PASSWORD, --Password PASSWORD
                        ESXi Host password (*****)
  -K KEY, --Key KEY     ESXi Host path to private key ()
  -n NAME, --name NAME  VM name ()
  -V, --verbose         Enable Verbose mode (False)
  -f LOG, --logfile LOG
                        Path to the log file (/Users/sebastien/esxi-vm.log)
  -l, --log             Write to log file (False)
  --summary             Display Summary (False)
```

Example Usage
-------------

* Running the script for the first time is recommended to specify your defaults (ESXi HOST, USER, PASSWORD):

```bash
./esxi-vm-create -H esxi -P MySecurePassword -u
Saving new Defaults to ~/.esxi-vm.yml
```

* Create a new VM named `testvm01` using all defaults from `~/.esxi-vm.yml`:

```bash
./esxi-vm-create -n testvm01 --summary

Create VM Success:
RESOURCE POOL: ha-root-pool
VM NAME: testvm01
vCPU: 2
Memory: 4GB
VM Disk: 20GB
DS Store: DS_4TB
Network: None
```

* Change default number of vCPUs to `4`, Memory to `8GB` and vDisk size to `40GB`:

```bash
./esxi-vm-create -c 4 -m 8096 -v 40 -u
Saving new Defaults to ~/.esxi-vm.yml
```

*  Create a new VM named `testvm02` using new defaults from `~/.esxi-vm.yml` and specifying a Network interface and partial MAC:

```bash
./esxi-vm-create -n testvm02 -N 192.168.1 -M 01:02:03
00:50:56:01:02:03
```

* Available *Network Interfaces* and *Available Disk Storage* volumes are listed if an invalid option is specified:

```bash
./esxi-vm-create -n testvm03 -N BadNet -S BadDS
ERROR: Disk Storage BadDS doesn't exist.
    Available Disk Stores: ['DS_SSD500s', 'DS_SSD500c', 'DS_SSD250', 'DS_4TB', 'DS_3TB_m']
    LeastUsed Disk Store : DS_4TB
ERROR: Virtual NIC BadNet doesn't exist.
    Available VM NICs: ['192.168.1', '192.168.0', 'VM Network test'] or 'None'
```

* Create a new VM named `testvm03` using a valid *Network Interface*, valid *Disk Storage* volume, summary and verbose enabled; save as default:

```bash
./esxi-vm-create -n testvm03 -N 192.168.1 -S DS_3TB_m --summary --verbose --updateDefaults
Saving new Defaults to ~/.esxi-vm.yml
Create testvm03.vmx file
Create testvm03.vmdk file
Register VM
Power ON VM

Create VM Success:
RESOURCE POOL: ha-root-pool
ESXi Host: esxi
VM NAME: testvm03
vCPU: 4
Memory: 8096MB
VM Disk: 40GB
Format: thin
DS Store: DS_3TB_m
Network: 192.168.1
Guest OS: centos-64
MAC: 00:0c:29:32:63:92
00:0c:29:32:63:92
```

* Create a new VM named `testvm04` specifying an ISO file to boot:

```bash
./esxi-vm-create -n testvm04 --summary --iso CentOS-7-x86_64-Minimal-1611.iso
FoundISOPath: /vmfs/volumes/5430094d-5a4fa180-4962-0017a45127e2/ISO/CentOS-7-x86_64-Minimal-1611.iso
Create testvm04.vmx file
Create testvm04.vmdk file
Register VM
Power ON VM

Create VM Success:
ESXi Host: esxi
VM NAME: testvm04
vCPU: 4
Memory: 8096MB
VM Disk: 40GB
Format: thin
DS Store: DS_3TB_m
Network: 192.168.1
ISO: /vmfs/volumes/5430094d-5a4fa180-4962-0017a45127e2/ISO/CentOS-7-x86_64-Minimal-1611.iso
Guest OS: centos-64
MAC: 00:0c:29:ea:a0:42
00:0c:29:ea:a0:42
```

* Merge or add extra VMX options, saved as default:

```bash
./esxi-vm-create -o 'floppy0.present  = TRUE,svga.autodetect = TRUE,svga.present = TRUE' -u
Saving new Defaults to ~/.esxi-vm.yml
```

**IMPORTANT**: *Do not set double quotes around values (such as `TRUE`), they will be automatically added by the tool.*

* Set the *Virtual machine hardware version* to `11` (ESXI 6), be default it is `8`:

```bash
./esxi-vm-create -o "virtualHW.version = 11" -u
Saving new Defaults to ~/.esxi-vm.yml
```

**IMPORTANT**: *Do not set double quotes around values (such as `11`), they will be automatically added by the tool.*

* Create a new VM named `testvm04` on the host `esxi2` accessible on port `2222` (instead of the usual `22`) and with an explicit private key `/home/user1/.ssh/id_rsa_esxi2`:

```bash
./esxi-vm-create -H esxi2 -T 2222 -K /home/user1/.ssh/id_rsa_esxi2 -n testvm04 --summary

Create VM Success:
VM NAME: testvm04
vCPU: 2
Memory: 4GB
VM Disk: 20GB
DS Store: DS_4TB
Network: None
```

* Destroy the VM named `testvm04`:

```bash
./esxi-vm-destroy -H esxi -P MySecurePassword -U root -n testvm04
```

This fork
--------

This is a fork. Summary of changes in this fork:

* Fix a bug in the `vmx` file generation (double quotes missing)
* Migrate to Python 3, as [Python 2 is soon dead](https://pythonclock.org)
* Add parameters `--port` and `--key` (SSH port number and private key)
* Verbose is now more verbose (it displays also SSH commands)
* By default, does **not** write to log file
* `esxi-vm-destroy` is documented
* Move some common code in `esxi-vm-create` and `esxi-vm-destroy` to `esxi_vm_functions.py`
* Code cleaning (work in progress)
* VM Memory in MB **not GB** to be able to create low memory VM
* Default VM is now Debian 8-64bits
* Fixed a bug that didn't obtain the list of VMNIC from the esxi instance properly
* Upgraded virtualHW.version 11 (native ESXI 6.0 format)
* Added parameters `--pool` to attach the VM to a resource pool

Copyrights
----------
* **This fork** Copyright &copy; 2020 Israel Figueroa
* **[fork](https://github.com/andrivet/esxi-vm)** Copyright &copy; 2018 Sebastien Andrivet
* **[Original code](https://github.com/josenk/esxi-vm-create)** Copyright &copy; 2017 Jonathan Senkerik

License
-------

![](https://www.gnu.org/graphics/gplv3-127x51.png)

> This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

> This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

> You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.


