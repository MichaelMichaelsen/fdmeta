# fdmeta
Extract information from Datafordeler File Download files

## Background
I have a need to quickly view the metadatafile in file downloads from Datafordeler.
This script will read in the compressed file and show the metadata.

## File structure
The file downloaded is a zip-compressed archive. In this archive there should be two files:
1. The data in one file (xml or json)
2. The metadata file (in the same format as the data (xml or json)

## References
https://confluence.datafordeler.dk/pages/viewpage.action?pageId=16056696#Filudtr%C3%A6kp%C3%A5Datafordeleren-MetadatafiliFTP/SFTP
