@echo off

:: -----------------------------------------------------------------------------
::
:: File: hab4_pki_tree.bat
::
:: Description: This script generates a basic HAB4 PKI tree for the Freescale
::              HAB code signing feature.  What the PKI tree looks like depends
::              on whether the SRK is chosen to be a CA key or not.  If the
::              SRKs are chosen to be CA keys then this script will generate the
::              following PKI tree:
::
::                                      CA Key
::                                      | | |
::                             -------- + | +---------------
::                            /           |                 \
::                         SRK1          SRK2       ...      SRKN
::                         / \            / \                / \
::                        /   \          /   \              /   \
::                   CSF1_1  IMG1_1  CSF2_1  IMG2_1 ... CSFN_1  IMGN_1
::
::              where: N can be 1 to 4.
::
::              Additional keys can be added to the tree separately.  In this
::              configuration SRKs may only be used to sign/verify other
::              keys/certificates
::
::              If the SRKs are chosen to be non-CA keys then this script will
::              generate the following PKI tree:
::
::                                      CA Key
::                                      | | |
::                             -------- + | +---------------
::                            /           |                 \
::                         SRK1          SRK2       ...      SRKN
::
::              In this configuration SRKs may only be used to sign code/data
::              and not other keys.  Note that not all Freescale processors
::              including HAB support this option.
::
::            (c) Freescale Semiconductor, Inc. 2011. All rights reserved.
::            (c) NXP Semiconductor, 2018. All rights reserved.
::
:: ----------------------------------------------------------------------------

echo.
echo     +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo     This script is a part of the Code signing tools for Freescale's
echo     High Assurance Boot.  It generates a basic PKI tree.  The PKI
echo     tree consists of one or more Super Root Keys (SRK), with each
echo     SRK having two subordinate keys:
echo         + a Command Sequence File (CSF) key
echo         + Image key.
echo     Additional keys can be added to the PKI tree but a separate
echo     script is available for this.  This this script assumes openssl
echo     is installed on your system and is included in your search
echo     path.  Finally, the private keys generated are password
echo     protectedwith the password provided by the file key_pass.txt.
echo     The format of the file is the password repeated twice:
echo         my_password
echo         my_password
echo     All private keys in the PKI tree will be protected by the same
echo     password.
echo     +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo.

set /P existing_ca="Do you want to use an existing CA key (y/n)?: "

if %existing_ca%==n goto KEY_LENGTH
set /P ca_key="Enter CA key name: "
set /P ca_cert="Enter CA certificate name: "

:KEY_LENGTH
set /P kl="Enter key length in bits for PKI tree: "

:: Confirm that a valid key length has been entered
if %kl%==1024 goto VALID_KEY_LENGTH
if %kl%==2048 goto VALID_KEY_LENGTH
if %kl%==3072 goto VALID_KEY_LENGTH
if %kl%==4096 goto VALID_KEY_LENGTH
echo Invalid key length. Supported key lengths: 1024, 2048, 3072, 4096
exit /B
:VALID_KEY_LENGTH

set /P duration="Enter PKI tree duration (years): "

:: Compute validity period
set /A val_period=%duration%*365


set /P num_srk="How many Super Root Keys should be generated? "

:: Check that 0 < num_srk < 4 (Max. number of SRKs)
if %num_srk%==1 goto VALID_NUM_KEYS
if %num_srk%==2 goto VALID_NUM_KEYS
if %num_srk%==3 goto VALID_NUM_KEYS
if %num_srk%==4 goto VALID_NUM_KEYS
echo The number of SRKs generated must be between 1 and 4
exit /B
:VALID_NUM_KEYS

:: Check if SRKs should be generated as CA certs or user certs
set /P srk_ca="Do you want the SRK certificates to have the CA flag set? (y/n)?: "

:SERIAL
:: Check that the file "serial" is present, if not create it:
if exist "serial" goto KEY_PASS
echo 12345678 > serial
echo A default 'serial' file was created!

:KEY_PASS
:: Check that the file "key_pass.txt" is present, if not create it with default user/pwd:
if exist "key_pass.txt" goto OPENSSL_INIT
echo test > key_pass.txt
echo test >> key_pass.txt
echo A default file 'key_pass.txt' was created with password = test!

:OPENSSL_INIT
:: The following is required otherwise OpenSSL complains
if exist index.txt      del /F index.txt
if exist index.txt.attr del /F index.txt.attr
type nul > index.txt
echo unique_subject = no > index.txt.attr
set OPENSSL_CONF=..\ca\openssl.cnf

if %existing_ca%==y goto GEN_SRK
:: Generate CA key and certificate
:: -------------------------------
set ca_key=.\CA1_sha256_%kl%_65537_v3_ca_key
set ca_cert=..\crts\CA1_sha256_%kl%_65537_v3_ca_crt

echo.
echo +++++++++++++++++++++++++++++++++++++
echo + Generating CA key and certificate +
echo +++++++++++++++++++++++++++++++++++++
echo.
:: Note: '^' is to continue the command on the next line
openssl req -newkey rsa:%kl% -passout file:.\key_pass.txt ^
    -subj /CN=CA1_sha256_%kl%_65537_v3_ca/ ^
    -x509 -extensions v3_ca ^
    -keyout temp_ca.pem ^
    -out .\%ca_cert%.pem ^
    -days %val_period%

:: Generate CA key in PKCS #8 format - both PEM and DER
openssl pkcs8 -passin file:.\key_pass.txt -passout file:.\key_pass.txt ^
    -topk8 -inform PEM -outform DER -v2 des3 ^
    -in temp_ca.pem ^
    -out .\%ca_key%.der

openssl pkcs8 -passin file:.\key_pass.txt -passout file:.\key_pass.txt ^
    -topk8 -inform PEM -outform PEM -v2 des3 ^
    -in .\temp_ca.pem ^
    -out .\%ca_key%.pem

:: Convert CA Certificate to DER format
openssl x509 -inform PEM -outform DER -in .\%ca_cert%.pem -out .\%ca_cert%.der

:: Cleanup
del /F .\temp_ca.pem

:GEN_SRK
if %srk_ca%==y goto GEN_SRK_CSF_IMG
:: Generate SRK keys and certificates (non-CA)
:: SRKs suitable for signing code/data
:: -------------------------------------------
set /a i=1
set /a max=num_srk+1

:GEN_SRK_LOOP
echo.
echo ++++++++++++++++++++++++++++++++++++++++
echo + Generating SRK key and certificate %i% +
echo ++++++++++++++++++++++++++++++++++++++++
echo.
:: Generate SRK key
openssl genrsa -des3 -passout file:.\key_pass.txt -f4 ^
    -out .\temp_srk.pem %kl%

:: Generate SRK certificate signing request
openssl req -new -batch -passin file:.\key_pass.txt ^
    -subj /CN=SRK%i%_sha256_%kl%_65537_v3_usr/ ^
    -key .\temp_srk.pem ^
    -out .\temp_srk_req.pem

:: Generate SRK certificate (this is a CA cert)
openssl ca -batch -passin file:.\key_pass.txt ^
    -md sha256 -outdir . ^
    -in .\temp_srk_req.pem ^
    -cert %ca_cert%.pem ^
    -keyfile %ca_key%.pem ^
    -extfile ..\ca\v3_usr.cnf ^
    -out ..\crts\SRK%i%_sha256_%kl%_65537_v3_usr_crt.pem ^
    -days %val_period%

::Convert SRK Certificate to DER format
openssl x509 -inform PEM -outform DER ^
    -in ..\crts\SRK%i%_sha256_%kl%_65537_v3_usr_crt.pem ^
    -out ..\crts\SRK%i%_sha256_%kl%_65537_v3_usr_crt.der

:: Generate CA key in PKCS #8 format - both PEM and DER
openssl pkcs8 -passin file:.\key_pass.txt -passout file:.\key_pass.txt ^
    -topk8 -inform PEM -outform DER -v2 des3 ^
    -in .\temp_srk.pem ^
    -out .\SRK%i%_sha256_%kl%_65537_v3_usr_key.der

openssl pkcs8 -passin file:./key_pass.txt -passout file:./key_pass.txt ^
    -topk8 -inform PEM -outform PEM -v2 des3 ^
    -in .\temp_srk.pem ^
    -out .\SRK%i%_sha256_%kl%_65537_v3_usr_key.pem

:: Cleanup
del /F .\temp_srk.pem .\temp_srk_req.pem

set /a i += 1
if %i%==%max% goto DONE
goto GEN_SRK_LOOP

:: Generate HAB keys and certificate
:: ---------------------------------
:GEN_SRK_CSF_IMG
set /a i=1
set /a max=num_srk+1

:GEN_SRK_CSF_IMG_LOOP
echo.
echo ++++++++++++++++++++++++++++++++++++++++
echo + Generating SRK key and certificate %i% +
echo ++++++++++++++++++++++++++++++++++++++++
echo.
:: Generate SRK key
openssl genrsa -des3 -passout file:.\key_pass.txt -f4 ^
    -out .\temp_srk.pem %kl%

:: Generate SRK certificate signing request
openssl req -new -batch -passin file:.\key_pass.txt ^
    -subj /CN=SRK%i%_sha256_%kl%_65537_v3_ca/ ^
    -key .\temp_srk.pem ^
    -out .\temp_srk_req.pem

:: Generate SRK certificate (this is a CA cert)
openssl ca -batch -passin file:.\key_pass.txt ^
    -md sha256 -outdir . ^
    -in .\temp_srk_req.pem ^
    -cert %ca_cert%.pem ^
    -keyfile %ca_key%.pem ^
    -extfile ..\ca\v3_ca.cnf ^
    -out ..\crts\SRK%i%_sha256_%kl%_65537_v3_ca_crt.pem ^
    -days %val_period%

::Convert SRK Certificate to DER format
openssl x509 -inform PEM -outform DER ^
    -in ..\crts\SRK%i%_sha256_%kl%_65537_v3_ca_crt.pem ^
    -out ..\crts\SRK%i%_sha256_%kl%_65537_v3_ca_crt.der

:: Generate CA key in PKCS #8 format - both PEM and DER
openssl pkcs8 -passin file:.\key_pass.txt -passout file:.\key_pass.txt ^
    -topk8 -inform PEM -outform DER -v2 des3 ^
    -in .\temp_srk.pem ^
    -out .\SRK%i%_sha256_%kl%_65537_v3_ca_key.der

openssl pkcs8 -passin file:./key_pass.txt -passout file:./key_pass.txt ^
    -topk8 -inform PEM -outform PEM -v2 des3 ^
    -in .\temp_srk.pem ^
    -out .\SRK%i%_sha256_%kl%_65537_v3_ca_key.pem

:: Cleanup
del /F .\temp_srk.pem .\temp_srk_req.pem

echo.
echo ++++++++++++++++++++++++++++++++++++++++
echo + Generating CSF key and certificate %i% +
echo ++++++++++++++++++++++++++++++++++++++++
echo.

:: Generate key
openssl genrsa -des3 -passout file:.\key_pass.txt ^
    -f4 -out .\temp_csf.pem %kl%

:: Generate CSF certificate signing request
openssl req -new -batch -passin file:.\key_pass.txt ^
    -subj /CN=CSF%i%_1_sha256_%kl%_65537_v3_usr/ ^
    -key .\temp_csf.pem ^
    -out .\temp_csf_req.pem

:: Generate CSF certificate (this is a user cert)
openssl ca -batch -md sha256 -outdir . ^
    -passin file:.\key_pass.txt ^
    -in .\temp_csf_req.pem ^
    -cert ..\crts\SRK%i%_sha256_%kl%_65537_v3_ca_crt.pem ^
    -keyfile .\SRK%i%_sha256_%kl%_65537_v3_ca_key.pem ^
    -extfile ..\ca\v3_usr.cnf ^
    -out ..\crts\CSF%i%_1_sha256_%kl%_65537_v3_usr_crt.pem ^
    -days %val_period%

::Convert CSF Certificate to DER format
openssl x509 -inform PEM -outform DER ^
    -in ..\crts\CSF%i%_1_sha256_%kl%_65537_v3_usr_crt.pem ^
    -out ..\crts\CSF%i%_1_sha256_%kl%_65537_v3_usr_crt.der

:: Generate CA key in PKCS #8 format - both PEM and DER
openssl pkcs8 -passin file:.\key_pass.txt -passout file:.\key_pass.txt ^
    -topk8 -inform PEM -outform PEM -v2 des3 ^
    -in .\temp_csf.pem ^
    -out .\CSF%i%_1_sha256_%kl%_65537_v3_usr_key.der

openssl pkcs8 -passin file:.\key_pass.txt -passout file:.\key_pass.txt ^
    -topk8 -inform PEM -outform PEM -v2 des3 ^
    -in .\temp_csf.pem ^
    -out .\CSF%i%_1_sha256_%kl%_65537_v3_usr_key.pem

:: Cleanup
del /F .\temp_csf.pem .\temp_csf_req.pem

echo.
echo ++++++++++++++++++++++++++++++++++++++++
echo + Generating IMG key and certificate %i% +
echo ++++++++++++++++++++++++++++++++++++++++
echo.

:: Generate key
openssl genrsa -des3 -passout file:.\key_pass.txt ^
    -f4 -out .\temp_img.pem %kl%

:: Generate IMG certificate signing request
openssl req -new -batch -passin file:.\key_pass.txt ^
    -subj /CN=IMG%i%_1_sha256_%kl%_65537_v3_usr/ ^
    -key .\temp_img.pem ^
    -out .\temp_img_req.pem

openssl ca -batch -md sha256 -outdir . ^
    -passin file:.\key_pass.txt ^
    -in .\temp_img_req.pem ^
    -cert ..\crts\SRK%i%_sha256_%kl%_65537_v3_ca_crt.pem ^
    -keyfile .\SRK%i%_sha256_%kl%_65537_v3_ca_key.pem ^
    -extfile ..\ca\v3_usr.cnf ^
    -out ..\crts\IMG%i%_1_sha256_%kl%_65537_v3_usr_crt.pem ^
    -days %val_period%

:: Convert SRK Certificate to DER format
openssl x509 -inform PEM -outform DER ^
    -in ..\crts\IMG%i%_1_sha256_%kl%_65537_v3_usr_crt.pem ^
    -out ..\crts\IMG%i%_1_sha256_%kl%_65537_v3_usr_crt.der

:: Generate CA key in PKCS #8 format - both PEM and DER
openssl pkcs8 -passin file:.\key_pass.txt -passout file:.\key_pass.txt ^
    -topk8 -inform PEM -outform DER -v2 des3 ^
    -in .\temp_img.pem ^
    -out ./IMG%i%_1_sha256_%kl%_65537_v3_usr_key.der

openssl pkcs8 -passin file:.\key_pass.txt -passout file:.\key_pass.txt ^
    -topk8 -inform PEM -outform PEM -v2 des3 ^
    -in .\temp_img.pem ^
    -out .\IMG%i%_1_sha256_%kl%_65537_v3_usr_key.pem

:: Cleanup
del /F .\temp_img.pem .\temp_img_req.pem

set /a i += 1
if %i%==%max% goto DONE
goto GEN_SRK_CSF_IMG_LOOP
:DONE
