import csv

contacts = csv.DictReader(
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

mapped	= []

for contact in contacts:
	currMappedItem = necessary
	for k, v in map.items():
		if type( v ) == type( [] ):
			s = []
			for f in v:
				if( len( contact[ f ] ) > 0 ):
					s.append( contact[ f ] )
			currMappedItem[ k ] = " ".join( s )
		else:
			currMappedItem[ k ] = contact[ v ]
	print currMappedItem
	mapped.append( currMappedItem )

currMappedItem = []
mapped.append( currMappedItem )

print "\
\
"
print mapped