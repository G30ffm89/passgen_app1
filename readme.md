change the server ip in nginx conf 

#passgen PEM PASSPHRASE: n13e563"!:14$kdsa31;SAD


https://gist.github.com/dahlsailrunner/679e6dec5fd769f30bce90447ae80081 

sudo openssl req -x509 -nodes -days 365 -newkey rsa:3072 -keyout passgen.key -out passgn.crt -config passgen.conf

sudo openssl req -x509 -nodes -days 365 -newkey rsa:3072 -keyout passgen.key -out passgen.crt -config passgen.conf -passin pass:n13e563!

sudo openssl pkcs12 -export -out passgen.pfx -inkey passgen.key -in passgen.crt

sudo openssl pkcs12 -in passgen.pfx -clcerts -out passgen.pem

firefox - your certificates then import 

sudo cp passgen.pem  /usr/local/share/ca-certificates/

sudo update-ca-certificates
trust list | grep -i "localhost"