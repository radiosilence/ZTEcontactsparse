#!python
import csv
import pprint
from xml.dom.minidom import parse

pp = pprint

doc = parse( 'template.xml' ) # parse an XML file by name
root = doc.getElementsByTagName( "root" )
for node in root:
	root = node
#print doc.toprettyxml(indent="  ")
#root = doc.createElement( "root" )
#doc.appendChild( root )


#info = doc.createElement("Info")
#root.appendChild(info)
#info.appendChild(
#	doc.createElement( "Location" ) ).appendChild(
#		doc.createTextNode( "1" ) )
#info.appendChild(
#	doc.createElement( "Version" ) ).appendChild(
#		doc.createTextNode( "3" ) )
#info.appendChild(
#	doc.createElement( "PB" ) ).appendChild(
#		doc.createTextNode( "true" ) )
#info.appendChild(
#	doc.createElement( "SMS" ) ).appendChild(
#		doc.createTextNode( "false" ) )


csvContacts = csv.DictReader(
	open( "contacts.csv" ),
	delimiter = ",",
	quotechar = '"'
)

necessary = {
	"eLocation" 		: 1, \
	"uGroupId" 		: 3, \
	"uSize"			: 0, \
	"szName"		: "", \
	"szCompany"		: "", \
	"szDuty"		: "", \
	"szEmail"		: "", \
	"szOtherEmail"		: "", \
	"szHomeEmail"		: "", \
	"szNotes"		: "", \
	"uAvailableNumber"	: 0, \
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

xmlContacts	= []

for csvContact in csvContacts:
	childInfo = doc.createElement("ChildInfo")
	childInfo.setAttribute( "DataType", "PB" )
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
		if len( "%s" % v ) > 0:
			childInfo.appendChild(
				doc.createElement( k ) ).appendChild(
					doc.createTextNode( "%s" % v ) )
		else:
			childInfo.appendChild(
				doc.createElement( k ) )
			
	root.appendChild( childInfo )
	


print doc.toprettyxml(indent="  ")