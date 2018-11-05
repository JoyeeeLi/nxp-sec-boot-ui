@echo off

::-----------------------------------------------------------------------------
::
:: File: add_key.bat
::
:: Description: This script adds a key to an existing HAB PKI tree to be used
::              with the HAB code signing feature.  Both the private key and
::              corresponding certificate are generated.  This script can
::              generate new SRKs, CSF keys and Images keys for HAB3 or HAB4.
::              This script is not intended for generating CA root keys.
::
::            (c) Freescale Semiconductor, Inc. 2011. All rights reserved.
::
::-----------------------------------------------------------------------------

set /P key_name=Enter new key name (e.g. SRK5):
set /P kl=Enter new key length in bits:

:: Confirm that a valid key length has been entered
:: Confirm that a valid key length has been entered
if %kl%==1024 goto VALID_KEY_LENGTH
if %kl%==2048 goto VALID_KEY_LENGTH
if %kl%==3072 goto VALID_KEY_LENGTH
if %kl%==4096 goto VALID_KEY_LENGTH
echo Invalid key length. Supported key lengths: 1024, 2048, 3072, 4096
exit /B
:VALID_KEY_LENGTH

set /P duration=Enter certificate duration (years):

:: Compute validity period
set /A val_period=%duration%*365

set /P hab_ver=Which version of HAB do you want to generate the key for (3/4)?:
if %hab_ver%==3 goto VALID_HAB_VER
if %hab_ver%==4 goto VALID_HAB_VER
echo Error - HAB version selected must be either 3 or 4
exit /B
:VALID_HAB_VER

:: ---------------- Add SRK Key and Certificate -------------------
set /P srk=Is this an SRK key?
if %srk%==n goto GEN_CSF

set /P ca_key=Enter CA signing key name:
set /P ca_cert=Enter CA signing certificate name:

:: Generate key
:: Note: '^' is to continue the command on the next line
openssl genrsa -des3 -passout file:.\key_pass.txt -f4 ^
-out .\%key_name%_sha256_%kl%_65537_v3_ca_key.pem %kl%

:: Generate SRK certificate signing request
openssl req -new -batch -passin file:.\key_pass.txt ^
-subj /CN=%key_name%_sha256_%kl%_65537_v3_ca/ ^
-key .\%key_name%_sha256_%kl%_65537_v3_ca_key.pem ^
-out .\%key_name%_sha256_%kl%_65537_v3_ca_req.pem

:: Generate SRK certificate (this is a CA cert)
openssl ca -batch -passin file:.\key_pass.txt ^
-md sha256 -outdir . ^
-in .\%key_name%_sha256_%kl%_65537_v3_ca_req.pem ^
-cert %ca_cert% ^
-keyfile %ca_key% ^
-extfile ..\ca\v3_ca.cnf ^
-out ..\crts\%key_name%_sha256_%kl%_65537_v3_ca_crt.pem ^
-days %val_period% ^
-config ..\ca\openssl.cnf

if %hab_ver%==4 goto SRK_CLEANUP

:: Generate WTLS certificate, ...
..\windows\x5092wtls.exe ^
--cert=..\crts\%key_name%_sha256_%kl%_65537_v3_ca_crt.pem ^
--key=.\%ca_key% ^
--out=..\crts\%key_name%_sha256_%kl%_65537_wtls.crt ^
--passin=.\key_pass.txt

:: C file and add corresponding fuse information to srktool_wtls.txt
..\windows\srktool.exe ^
--hab_ver=3 ^
--certs=..\crts\%key_name%_sha256_%kl%_65537_wtls.crt ^
--o >> ..\crts\srktool_wtls.txt

:: Clean up
:SRK_CLEANUP
del *_req.pem
exit /B


:: ---------------- Add CSF Key and Certificate -------------------
:GEN_CSF
set /P csf=Is this a CSF key?:
if %csf%==n goto GEN_IMG

set /P srk_key=Enter SRK signing key name:
set /P srk_cert=Enter SRK signing certificate name:


if %hab_ver%==3 goto HAB3_CSF
:: Generate key
openssl genrsa -des3 -passout file:.\key_pass.txt ^
-f4 -out .\%key_name%_sha256_%kl%_65537_v3_usr_key.pem %kl%

:: Generate CSF certificate signing request
openssl req -new -batch -passin file:.\key_pass.txt ^
-subj /CN=%key_name%_sha256_%kl%_65537_v3_usr/ ^
-key .\%key_name%_sha256_%kl%_65537_v3_usr_key.pem ^
-out .\%key_name%_sha256_%kl%_65537_v3_usr_req.pem

:: Generate CSF certificate (this is a user cert)
openssl ca -batch -md sha256 -outdir . ^
-passin file:.\key_pass.txt ^
-in .\%key_name%_sha256_%kl%_65537_v3_usr_req.pem ^
-cert %srk_cert% ^
-keyfile .\%srk_key% ^
-extfile ..\ca\v3_usr.cnf ^
-out ..\crts\%key_name%_sha256_%kl%_65537_v3_usr_crt.pem ^
-days %val_period% ^
-config ..\ca\openssl.cnf
goto CSF_CLEANUP

:HAB3_CSF
:: Generate key
openssl genrsa -des3 -passout file:.\key_pass.txt ^
-f4 -out .\%key_name%_sha256_%kl%_65537_v3_ca_key.pem %kl%

:: Generate CSF certificate signing request
openssl req -new -batch -passin file:.\key_pass.txt ^
-subj /CN=%key_name%_sha256_%kl%_65537_v3_ca/ ^
-key .\%key_name%_sha256_%kl%_65537_v3_ca_key.pem ^
-out .\%key_name%_sha256_%kl%_65537_v3_ca_req.pem

:: Generate CSF certificate (this is a user cert)
openssl ca -batch -md sha256 -outdir . ^
-passin file:.\key_pass.txt ^
-in .\%key_name%_sha256_%kl%_65537_v3_ca_req.pem ^
-cert %srk_cert% ^
-keyfile .\%srk_key% ^
-extfile ..\ca\v3_ca.cnf ^
-out ..\crts\%key_name%_sha256_%kl%_65537_v3_ca_crt.pem ^
-days %val_period% ^
-config ..\ca\openssl.cnf

:: Generate WTLS certificate, ...
..\windows\x5092wtls.exe ^
--cert=..\crts\%key_name%_sha256_%kl%_65537_v3_ca_crt.pem ^
--key=.\%srk_key% ^
--out=..\crts\%key_name%_sha256_%kl%_65537_wtls.crt ^
--passin=.\key_pass.txt

:: Clean up
:CSF_CLEANUP
del *_req.pem
exit /B


:: ---------------- Add IMG Key and Certificate -------------------
:GEN_IMG
:: Generate key
openssl genrsa -des3 -passout file:.\key_pass.txt ^
-f4 -out .\%key_name%_sha256_%kl%_65537_v3_usr_key.pem %kl%


:: Generate IMG certificate signing request
openssl req -new -batch -passin file:.\key_pass.txt ^
-subj /CN=%key_name%_sha256_%kl%_65537_v3_usr/ ^
-key .\%key_name%_sha256_%kl%_65537_v3_usr_key.pem ^
-out .\%key_name%_sha256_%kl%_65537_v3_usr_req.pem


if %hab_ver%==3 goto HAB3_IMG
set /P srk_key=Enter SRK signing key name:
set /P srk_cert=Enter SRK signing certificate name:

openssl ca -batch -md sha256 -outdir . ^
-passin file:.\key_pass.txt ^
-in .\%key_name%_sha256_%kl%_65537_v3_usr_req.pem ^
-cert %srk_cert% ^
-keyfile %srk_key% ^
-extfile ..\ca\v3_usr.cnf ^
-out ..\crts\%key_name%_sha256_%kl%_65537_v3_usr_crt.pem ^
-days %val_period% ^
-config ..\ca\openssl.cnf
goto IMG_CLEANUP

:HAB3_IMG
set /P csf_key=Enter CSF signing key name:
set /P csf_cert=Enter CSF signing certificate name:

openssl ca -batch -md sha256 -outdir . ^
-passin file:.\key_pass.txt ^
-in .\%key_name%_sha256_%kl%_65537_v3_usr_req.pem ^
-cert %csf_cert% ^
-keyfile %csf_key% ^
-extfile ..\ca\v3_usr.cnf ^
-out ..\crts\%key_name%_sha256_%kl%_65537_v3_usr_crt.pem ^
-days %val_period% ^
-config ..\ca\openssl.cnf

:: Generate WTLS certificate, ...
..\windows\x5092wtls.exe ^
--cert=..\crts\%key_name%_sha256_%kl%_65537_v3_usr_crt.pem ^
--key=.\%csf_key% ^
--out=..\crts\%key_name%_sha256_%kl%_65537_wtls.crt ^
--passin=.\key_pass.txt

:: Clean up
:IMG_CLEANUP
del *_req.pem
exit /B
