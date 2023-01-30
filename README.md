# Assingment Readme

## Problem

1. Setup your VM with DS and Dogtag PKI packages.

2. Setup a LDAP server (Creating DS Instance)

3. Setup a CA server (Creating PKI Subsystems)

4. Create a certificate request using : client-cert-request  and sign the certificate using : ca-cert-request-review (Refer : Request: https://github.com/dogtagpki/pki/wiki/PKI-Client-CLI , Approve : https://github.com/dogtagpki/pki/wiki/Handling-Certificate-Request : Basic Request and Approving the Request) 

5. Try to write step 4 in a Python script.

## Overview in readme

In this repo, In this we create Directory Server (DS) and Certificate Authority (CA) server on a Fedora VM and setup a LDAP server and CA server subsystem. Create a certificate request and automate python script. For more about assignment check [here](https://github.com/yj1910/Create-a-DS-and-CA-servers-in-fedora-vm-and-certificate-request-and-approval-/blob/main/Assignment)

### 1.Setup Fedora VM in your windows machine.

- Here we assuming, Your host machine has windows OS. First for VM. your need to download oracle Virtualbox VM. install it and configure to install another OS. Oracle Virtual box download- [virtualbox](https://www.virtualbox.org/wiki/Downloads) .
- Second we need to download ISO file of fedora for windows host and install it. Fedora Download-
[Fedora](https://getfedora.org/en/workstation/download/) 
- Configure the setting to install fedora ISO in virtual box and allocate the CPUs, Memories to Fedora vm. 
##### Note - To run Fedora minimum required 2gb RAM and 20gb Disk space.

### 2. Installing PKI and DS(Directory server) packages.
   Refer from [Dogtag pki](https://github.com/dogtagpki/pki/wiki/Quick-Start)
   
   - First you have to be root user. To root access for machine. Enter following command and after that you have to enter root password
      ````bash
      $ sudo -s
      [sudo] password for root:
      ````
   - To install Dogtag PKI package. use following command
      ````bash
      $ dnf install dogtag-pki
      ````
   - To install Directory server(DS) package:
      ````bash
      $ dnf install -y 389-ds-base
      ````
      
 ### 3. Creating DS intance or LDAP server:
         
 - Generate a DS configuration file-
     
       ````bash
      $ dscreate create-template ds.inf
       ````
  - Customize the DS configuration file-
     ````bash
     $ sed -i \
    -e "s/;instance_name = .*/instance_name = hello/g" \
    -e "s/;root_password = .*/root_password = Yashjain@123/g" \
    -e "s/;suffix = .*/suffix = dc=example,dc=com/g" \
    -e "s/;create_suffix_entry = .*/create_suffix_entry = True/g" \
    -e "s/;self_sign_cert = .*/self_sign_cert = True/g" \
    ds.inf
    ````
  where,
   - instance_name shows the name of the DS instance. For this our intance_name is "hello".
   - root_password specifies the password for DS admin (i.e. cn=Directory Manager). Here root_passowrd is "Yashjain@123".
   - suffix specifies the namespace for the DS instance. In this example it’s set to dc=example,dc=com.
   - self_sign_cert create self-signed certificates for SSL connection. I am enabling the ssl connection to to set to be "True".Precaution for in future during sending certificate request sslexception error is not coming.
   
 - At last, create file for ds intance
   ````bash
   $ dscreate from-file ds.inf
   ````
 - Creating pki subtree
   The DS instance is empty. So, Use an LDAP client to add a root entry and PKI base entry. By following command
      ````bash
    $ ldapadd -H ldap://$HOSTNAME -x -D "cn=Directory Manager" -w Secret.123 << EOF
      dn: dc=pki,dc=example,dc=com
      objectClass: domain
      dc: pki
      EOF
      ````
      *console output-*
      ````bash
      dc=example,dc=com
      ````
  - At last for check the status of ds intance that your ds intance running or not. You can check  by following command.
      ````bash
      $ dsctl localhost status
      ````
      *console output-*
      ````bash
      Ds intance *localhost* is running
      ````
      **Note- If after all setup the ds instance is not running just simply restart it**
            ````bash
            $ dsctl localhost status
            ````
      
  
  #### Process to deploy DS container for pki
  
  -First create a network for the container. Our network name example. we can write our person network name instead for 
  ````bash
  $ podman network create example
  ````
  


     
     
     
      

      

