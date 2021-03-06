#!/usr/bin/python3
#
# fdmeta
#
# 
from zipfile import ZipFile
import datetime
import re
import json
import xmltodict
import xml.etree.ElementTree as ET
import sys, getopt
import os.path

class metadata:
  def __init__(self):
    self.parameters = []

  def setparam(self,section, name, value):
    self.parameters[section][name] = value

def extension(filename):
  regexpxml  = r"\.xml$"
  regexpjson = r"\.json$"
  filenamelowercase = filename.lower()

  if (re.search(regexpxml,filenamelowercase)):
    return "xml"
  elif (re.search(regexpjson,filenamelowercase)):
    return "json"
  else:
    return "Unknown"

def main(argv):
  file_name = ""
  try:
      opts, args = getopt.getopt(argv,"hi:",["ifile="])
  except getopt.GetoptError:
      print ('fdmeta.py -i <inputfile> ')
      sys.exit(2)
  for opt, arg in opts:
      if opt == '-h':
        print ( 'fdmeta.py -i <inputfile>' ) 
        sys.exit()
      elif opt in ("-i", "--ifile"):
        file_name = arg
  if not os.path.isfile(file_name):
    print( 'Unable to read %s' % (file_name))
    sys.exit(2)
  #
  # Metadata file sections
  #
  sections = ['leveranceNavn', 'miljoe', 'fortroligData', 'dataOmfattetAfPersondataloven', 'MD5CheckSum', 'DatafordelerUdtraekstidspunkt', 'tilgaengelighedsperiode', 'AbonnementsOplysninger', 'BrugerUdfyldteParametre']
  # 

  metadata_file = ""
  metadata = ""
  regexp   = r'.*Metadata\.(json|xml)'
  #
  #
  # opening the zip file in READ and extract the metadata file
  #
  with ZipFile(file_name, 'r') as zip: 
    # printing all the contents of the zip file 
    zip.printdir()
    for file in zip.namelist():
      # print (file)
      if re.search(regexp,file):
        #
        # If this XML or JSON. The extension of the metadata file in the
        # zipped archive will tell.
        # 
        metadata_file = file
        #print( metadata_file, extension(metadata_file))
        try:
          metadata = zip.read(file )
        except KeyError:
          print ('Error in reading metadata file')
        else:
          if (extension(metadata_file) == 'json'):
            metadata_json = json.loads( metadata )
            print()
            print( 'Metadata' )
            for section in sections:
              #
              if (type(metadata_json[section]) is str):
                print ( "%-30s \t: %s" % (section, metadata_json[section]) )
              if (type(metadata_json[section]) is list):
                print ( "%-30s \t:" % (section) )
                #  
                if (section == 'BrugerUdfyldteParametre'):
                  for arg in metadata_json[section]:
                    for parameter in arg:
                      if (parameter == "parameternavn"):
                        print ( '\t%-20s\t: ' % (arg[parameter]), end="")
                      else:
                        print ( '%s' % (arg[parameter]))            
                elif (section == "DatafordelerUdtraekstidspunkt" or section == 'AbonnementsOplysninger'):
                  #
                  for arg in metadata_json[section]:
                    for parameter in arg:
                      print ( '\t%-20s\t: %s' % (parameter,arg[parameter]))
          elif (extension(metadata_file) == 'xml'):
            metadata_xml = xmltodict.parse(metadata)
            print('Metadata')
            for section in metadata_xml['FiludtraekMetadata'].keys():
              # print(type(metadata_xml['FiludtraekMetadata'][section]))
              if (type(metadata_xml['FiludtraekMetadata'][section]) is str):
                print("%-30s \t: %s" % (section, metadata_xml['FiludtraekMetadata'][section]))
              else:
                # print('Dict ', type(metadata_xml['FiludtraekMetadata'][section]))
                print(section)
                if (section == 'BrugerUdfyldteParametre' ):
                  for p in range(len(metadata_xml['FiludtraekMetadata'][section]['parameternavn'])):
                    print("\t%-30s\t: %s" % (metadata_xml['FiludtraekMetadata'][section]['parameternavn'][p], metadata_xml['FiludtraekMetadata'][section]['parametervaerdi'][p]))
                else:
                  for arg in metadata_xml['FiludtraekMetadata'][section]:
                    print("\t%-30s\t: %s" % (arg, metadata_xml['FiludtraekMetadata'][section][arg]))
          else:
            print ('Unknown file extension')
            exit(2)   

if __name__ == "__main__":
   main(sys.argv[1:])
