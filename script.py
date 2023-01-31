import subprocess

#Before run the script make sure .csr .csr.key and .crt file will be in same path

# client-cert-request: create a certificate request
cert_request_cmd = "client-cert-request --csr-file=client.csr --key-file=client.key"
subprocess.run(cert_request_cmd, shell=True)

# ca-cert-request-review: sign the certificate request
sign_request_cmd = "ca-cert-request-review --approve --cert-file=client.crt client.csr"
subprocess.run(sign_request_cmd, shell=True)

print("Certificate request created and signed successfully")