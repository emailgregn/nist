## NIST Randomness Beacon verification routine
## Only slightly adapted by Elliot Williams
## from code provided by Lawrence Bassham, NIST
 
## The UNIX time that you'd like to test:
##
whichRecord=1400878200
 
## --------------- Utility Functions ----------------
 
## Extracts specified record from xml file
getValue() {
 xmllint --xpath "/record/$1/text()" $2
}
 
## Converts little-endian to big-endian
byteReverse() {
 len=${#1}
 for((i=${len}-2; i>=0; i=i-2)) do
 rev="$rev${1:$i:2}"
 done
 echo ${rev}
}
 
## ---------------- Get an arbitrary record -----------------
echo "Downloading data for: ${whichRecord}"
curl -s https://beacon.nist.gov/rest/record/${whichRecord} -o rec.xml
 
## ------------- Pack data into correct format --------------
echo
echo "## Create a summary of all of the data, save as beacon.bin"
 
## Strangest choice of format ever!
## Version number (ascii text)
## Update frequency (4 bytes)
## Time Stamp (8 bytes)
## The HW RNG seedValue (64 bytes)
## The previous output value, does the chaining (64 bytes)
## Status code (4 bytes)
 
getValue version rec.xml > beacon.bin
printf "%.8x" `getValue frequency rec.xml` | xxd -r -p >> beacon.bin
printf "%.16x" `getValue timeStamp rec.xml` | xxd -r -p >> beacon.bin
getValue seedValue rec.xml | xxd -r -p >> beacon.bin
getValue previousOutputValue rec.xml | xxd -r -p >> beacon.bin
printf "%.8x" `getValue statusCode rec.xml` | xxd -r -p >> beacon.bin
 
## ------------------ Verify signature on data --------------------
 
echo "## Verify that the signature and NIST's public key correctly SHA512 sign the data"
 
## Download Beacon's public key
echo "Downloading Beacon's public key"
curl -s https://beacon.nist.gov/certificate/beacon.cer -o beacon.cer
 
## Create a bytewise reversed version of the listed signature
## This is necessary b/c Beacon signs with Microsoft CryptoAPI which outputs
## the signature as little-endian instead of big-endian like many other tools
## This may change (personal communication) in a future revision of the Beacon
signature=`getValue signatureValue rec.xml`
byteReverse ${signature} | xxd -r -p > beacon.sig
 
## Pull public key out of certificate
/usr/bin/openssl x509 -pubkey -noout -in beacon.cer > beaconpubkey.pem
## Test signature / key on packed data
/usr/bin/openssl dgst -sha512 -verify beaconpubkey.pem -signature beacon.sig beacon.bin
echo
echo
 
## ------------------ Verify Signature -> Output and Chaining ------------
echo "The following three values should match: "
echo " a direct SHA512 of the extracted signature"
echo " the reported output value"
echo " next record's previous output value"
echo
 
## Just print output value
echo "Reported output value"
getValue outputValue rec.xml
echo
 
## Now turn the signature into the output value: again SHA512
echo "SHA512 of the signature"
getValue signatureValue rec.xml | xxd -r -p | sha512sum
 
## Now test chaining
## Get next record
echo "Downloading the next record"
curl -s https://beacon.nist.gov/rest/record/next/${whichRecord} -o next.xml
## Make sure that this period's output shows up as next period's "previous output"
echo "Next value's reported previous output (test of forward chaining)"
getValue previousOutputValue next.xml
echo
echo
 
## --------------------- The End -----------------------------------------
 
## If this all worked, we've verified that the signature (plus NIST's key)
## sign the hash of the random number and its support info
## _and_ we've verified that the outputValue is derived from them,
## so we know that this output value is in the chain.
 
## If we run this on every entry in the chain, and all works out just fine,
## then we'd know all is well

