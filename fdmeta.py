# importing required modules 
from zipfile import ZipFile
import datetime
import re
import json
import xmltodict
import sys, getopt
import os.path

def extension(filename):
  regexpxml  = r"\.xml$"
  regexpjson = r"\.json$"
  filenamelowercase = filname.lower()

  if (r.search(regexpxml,filenamelowercase)):
    return "xml"
  else:
    return "json"

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
  # specifying the zip file name 

  metadata_file = ""
  metadata = ""
  #
  print( extension(metadata_file))

  # opening the zip file in READ and extract the metadata file
  with ZipFile(file_name, 'r') as zip: 
    # printing all the contents of the zip file 
    zip.printdir()
    for file in zip.namelist():
      # print (file)
      if re.search(regex,file):
        #
        # If this XML or JSON. The extension of the metadata file in the
        # zipped archive will tell.
        # 
        metadata_file = file
        try:
          metadata = zip.read(file )
        except KeyError:
          print ('Error in reading metadata file')
        else:
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

if __name__ == "__main__":
   main(sys.argv[1:])
