# ZTE Contacts Parser

Because 3 have made some bizarre hacky software that in my case fails completely to read vCard files, and all my contacts are stored on Google Mail, it seemed logical to write something that could connect the two by taking an Outlook CSV file, and massaging it into the weird XML based format used by the 3 software. Initially written in PHP, but ported to python for stability and academic reasons, here it is. If you want to use it, do these things:

1. Get your contacts in an Outlook compatible .csv file named contacts.csv and put in the same directory as script.
1. Run `python import.py > contacts.xml` at a command line or something.
1. Load this XML with the 3 program.
