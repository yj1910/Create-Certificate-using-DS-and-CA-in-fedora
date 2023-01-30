# Assingment Readme

## Problem

1. Setup your VM with DS and Dogtag PKI packages.

2. Setup a LDAP server (Creating DS Instance)

3. Setup a CA server (Creating PKI Subsystems)

4. Create a certificate request using : client-cert-request  and sign the certificate using : ca-cert-request-review (Refer : Request: https://github.com/dogtagpki/pki/wiki/PKI-Client-CLI , Approve : https://github.com/dogtagpki/pki/wiki/Handling-Certificate-Request : Basic Request and Approving the Request) 

5. Try to write step 4 in a Python script.

## Overview in readme

In this repo, In this we create Directory Server (DS) and Certificate Authority (CA) server on a Fedora VM and setup a LDAP server and CA server subsystem. Create a certificate request and automate python script. For more about assignment check [here](https://github.com/yj1910/Create-a-DS-and-CA-servers-in-fedora-vm-and-certificate-request-and-approval-/blob/main/Assignment)

## Setup Fedora VM in your windows machine.

- Here we assuming, Your host machine has windows OS. First for VM. your need to download oracle Virtualbox VM. install it and configure to install another OS. Oracle Virtual box download- [virtualbox](https://www.virtualbox.org/wiki/Downloads) .
- Second we need to download ISO file of fedora for windows host and install it. Fedora Download-
[Fedora](https://getfedora.org/en/workstation/download/) 
- Configure the setting to install fedora ISO in virtual box and allocate the CPUs, Memories to Fedora vm. 
#### Note - To run Fedora minimum required 2gb RAM and 20gb Disk space.

## Installing PKI and DS(Directory server) packages.
   Refer from 



