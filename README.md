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
    $ ldapadd -H ldap://$HOSTNAME -x -D "cn=Directory Manager" -w Yashjain@123 << EOF
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
      $ dsctl hello status
      ````
      *console output-*
      ````bash
      Ds intance *hello* is running
      ````
      **Note- If after all setup the ds instance is not running just simply restart it**
            ````bash
            $ dsctl hello restart
            ````
      
  #### Process to deploy DS container for pki
  
  - First create a network for the container. Our network name example. we can write our person network name instead for 
   ````bash
   $ podman network create example
   ````
  - Create DS volume
  ````bash
  $ podman volume create ds-data
  ````
  - Deploy the container with following command
  ````bash
   $ podman run \
    --name=ds \
    --hostname=ds.example.com \
    --network=example \
    --network-alias=ds.example.com \
    -v ds-data:/data \
    -e DS_DM_PASSWORD=Yashjain@123 \
    -p 3389:3389 \
    -p 3636:3636 \
    -d \
    quay.io/389ds/dirsrv
   ````
   - After deploying the container files. check the container is deploying successfully by fetching logs by command
    ````bash
    $ podman logs -f ds
    ````
     If conatiner is not running. start conatiner. ````bash podman start container_name ````
   - Creating DS Backend:
      ````bash
   $ podman exec ds dsconf hello backend create \
    --suffix dc=example,dc=com \
    --be-name userRoot
      ````
   - Creating PKI Subtree:
      ````bash
       $ podman exec -i ds ldapadd \
       -H ldap://ds.example.com:3389 \
      -D "cn=Directory Manager" \
      -w Secret.123 \
      -x << EOF
      dn: dc=example,dc=com
      objectClass: domain
      dc: example

      dn: dc=pki,dc=example,dc=com
      objectClass: domain
      dc: pki
      EOF
      ````
     - Accessing PKI Subtree:
     ````bash
      $ podman exec ds ldapsearch \
      -H ldap://ds.example.com:3389 \
      -D "cn=Directory Manager" \
      -w Secret.123 \
      -x \
      -b "dc=example,dc=com"
     ````
    
### 4. Creating PKI Subsystems or CA server:
      - to creating PKI subsytems. Run the command and configure as per according and requirments.
      
      `````bash
      $ pkispawn
      ````
      *console output and configuration-*
   ````bash               
      IMPORTANT:

    Interactive installation currently only exists for very basic deployments!

    For example, deployments intent upon using advanced features such as:

        * Cloning,
        * Elliptic Curve Cryptography (ECC),
        * External CA,
        * Hardware Security Module (HSM),
        * Subordinate CA,
        * etc.,

    must provide the necessary override parameters in a separate
    configuration file.

    Run 'man pkispawn' for details.

Subsystem (CA/KRA/OCSP/TKS/TPS) [CA]:

Tomcat:
  Instance [pki-tomcat]:
  HTTP port [8080]:
  Secure HTTP port [8443]:
  AJP port [8009]:
  Management port [8005]:

Administrator:
  Username [yjain7573]:
  Password: Yashjain@123
  Verify password: Yash jain@123
  Import certificate (Yes/No) [N]?
  Export certificate to [/root/.dogtag/pki-tomcat/ca_admin.cert]:

Directory Server:
  Hostname [pki.example.com]:
  Use a secure LDAPS connection (Yes/No/Quit) [N]? Yes
  LDAP Port [389]:
  Bind DN [cn=Directory Manager]:
  Password: Yashjain@123
  Base DN [o=pki-tomcat-CA]:

Security Domain:
  Name [example.com Security Domain]:

Begin installation (Yes/No/Quit)? Yes

Installing CA into /var/lib/pki/pki-tomcat.

    ==========================================================================
                                INSTALLATION SUMMARY
    ==========================================================================

      Administrator's username:             hello
      Administrator's PKCS #12 file:
            /root/.dogtag/pki-tomcat/ca_admin_cert.p12

      To check the status of the subsystem:
            systemctl status pki-tomcatd@pki-tomcat.service

      To restart the subsystem:
            systemctl restart pki-tomcatd@pki-tomcat.service

      The URL for the subsystem is:
            https://pki.example.com:8443/ca

      PKI instances will be enabled upon system boot
   ````

### 4. Creating Certificate request and approval:

- For creating a certificate request for pki cli. A new client database can be initialized with the following command:
   ````bash
   $ pki -c Secret.123 client-init
   ````
- The certificates in the client security database can be listed using the following command:
  ````bash
  $ pki -c Secret.123 client-cert-find
  ````
  
 - Generate a PKCS #10 client certificate request first.
   ````bash
   $ PKCS10Client \
    -d ~/.dogtag/nssdb \
    -p Yashjain@123 \
    -a rsa \
    -l 1024 \
    -o testuser.csr \
    -n "uid=testuser,ou=people,dc=example,dc=com"
    ````
    *console output-*
    ````bash
    PKCS10Client: Debug: got token.
    PKCS10Client: Debug: thread token set.
    PKCS10Client: token Internal Key Storage Token logged in...
   PKCS10Client: key pair generated.
   PKCS10Client: pair.getPublic() called.
   PKCS10Client: CertificationRequestInfo() created.
   PKCS10Client: CertificationRequest created.
   PKCS10Client: calling Utils.b64encode.
   PKCS10Client: b64encode completes.
   -----BEGIN NEW CERTIFICATE REQUEST-----
   MIIBfTCB5wIBADAaMRgwFgYKCZImiZPyLGQBARMIdGVzdHVzZXIwgZ8wDQYJKoZI
   hvcNAQEBBQADgY0AMIGJAoGBAPEcxFJBu2lNmIS+MNaZKO43h0dIhKZWZ8wEomQc
   tc9guIUGM5eFU+psj6n0XQCPMIVRe7mrzYHF8mlwAp416P5/97g9U6JOKkTXc5ia
   HVE1JRhykHiQ17Lp7Y6xXxfe6xKAXDoLOPJ4fNdadtbVeIGjudWktjgwh5CQBXsA
   GFP5AgMBAAGgJDAiBggrBgEFBQcHFzEWBBTmaclfLv+kkK5z5kTMP54dlnecUDAN
   BgkqhkiG9w0BAQQFAAOBgQAXrm979HwcG63Z64u+aybYrfOgyWxQ4kTtCA+NKYge
   HC6Z/mlb10J/wggOzrHUbE4IFyjbBo2k1FKe8zYcXIB6Ok5Z0TXueR1zKcb8hE35
   o9dkH2sGJsSqMLN8NRyY5QeqOKmtaX8pm1aPhJ0wkvOYou52YqJdq6LF9KXmBGOH
   hA==
   -----END NEW CERTIFICATE REQUEST-----
      PKCS10Client: done. Request written to file: testuser.csr
   ````
    
- To generate and submit a PKCS #10 request:
   ````bash
   $ pki -c Secret.123 client-cert-request uid=testuser
   ````
- To review the certificate request:
   ````bash
   $ pki <agent authentication> ca-cert-request-review <request ID> --file <filename>
   or
   $ pki <agent authentication> ca-cert-request-review <request ID> --action <action>
   ````
-  To approve the certificate request
   ````bash
   $ pki -n caadmin ca-cert-request-approve 6
   ````
 
  


     
     
     
      

      

