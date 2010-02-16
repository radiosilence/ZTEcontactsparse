#!python
import csv
import pprint
from lxml import etree

pp = pprint

template = """<?xml version="1.0"?><root><Info><Location>1</Location><Version>3</Version><PB>true</PB><SMS>false</SMS></Info></root>"""

root = etree.fromstring( template )

csvContacts = csv.DictReader(
	open( "contacts.csv" ),
	delimiter = ",",
	quotechar = '"'
)

necessary = {
	"eLocation" 		: "1", \
	"uGroupId" 		: "3", \
	"uSize"			: "0", \
	"szName"		: "", \
	"szCompany"		: "", \
	"szDuty"		: "", \
	"szEmail"		: "", \
	"szOtherEmail"		: "", \
	"szHomeEmail"		: "", \
	"szNotes"		: "", \
	"uAvailableNumber"	: "0", \
	"szPhoneName0"		: "", \
	"szPhoneNumber0"	: "", \
	"szPhoneName1"		: "", \
	"szPhoneNumber1"	: "", \
	"szPhoneName2"		: "", \
	"szPhoneNumber2"	: "", \
	"szPhoneName3"		: "", \
	"szPhoneNumber3"	: "", \
	"szPhoneName4"		: "", \
	"szPhoneNumber4"	: "", \
	"szUrl"			: "", \
}

map = {
	"szName" 		: [ 
		"First Name", \
		"Middle Name", \
		"Last Name" \
		], \
	"szEmail" 		: "E-mail Address", \
	"szPhoneNumber0" 	: "Mobile Phone", \
	"szPhoneNumber1" 	: "Home Phone", \
	"szPhoneNumber4" 	: "Business Phone", \
	"szCompany" 		: "Company", \
}

for csvContact in csvContacts:
	childInfo = etree.SubElement( root, "ChildInfo", DataType="PB" )
	xmlContact = necessary
	for k, v in map.items():
		if type( v ) == type( [] ):
			s = []
			for f in v:
				if( len( csvContact[ f ] ) > 0 ):
					s.append( csvContact[ f ] )
			xmlContact[ k ] = " ".join( s )
		else:
			xmlContact[ k ] = csvContact[ v ]
	
	for k, v in xmlContact.items():
		e = etree.SubElement( childInfo, k )
		if len( "%s" % v ) > 0:
			e.text = "%s" % ( v.decode( "windows-1252" ) )
					
print etree.tostring( root )
	