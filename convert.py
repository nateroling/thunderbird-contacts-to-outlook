import sys
import csv

if len(sys.argv) != 3:
    print "USAGE: convert.py INPUT_FILENAME OUTPUT_FILENAME"
else:
    infile = sys.argv[1]
    outfile = sys.argv[2]

FIELDS = """
First Name : @
Last Name : @
Display Name : Name
Nickname
Primary Email : E-mail Address
Secondary Email : E-mail 2 Address
Screen Name
Work Phone : Business Phone
Home Phone : Home Phone
Fax Number : Business Fax
Pager Number : Pager
Mobile Number : Mobile Phone
Home Address : Home Street 1
Home Address 2 : Home Street 2
Home City : @
Home State : @
Home ZipCode : Home Postal Code
Home Country : Home Country/Region
Work Address : Business Street
Work Address 2 : Business Street 2
Work City : Business City
Work State : Business State
Work ZipCode : Business Postal Code
Work Country : Business Country/Region
Job Title : @
Department : @
Organization : Company
Web Page 1 : Web Page
Web Page 2
Birth Year
Birth Month
Birth Day
Custom 1 : User 1
Custom 2 : User 2
Custom 3 : User 3
Custom 4 : User 4
Notes : Notes
"""

def get_replacements():
    replacements = {}
    for field in FIELDS.split("\n"):
        pair = [x.strip() for x in field.split(":")]
        if len(pair) == 2:
            original, replacement = pair
            if replacement == "@":
                replacement = original
            replacements[original] = replacement
    return replacements


headers = []

def process(column_map, row):
    output = []
    for idx, value in enumerate(row):
        if value:
            if idx in column_map:
                output.append(value.strip())
            else:
                print "Ignored: %s = %s" % (headers[idx], value)
    return output

with open(infile, 'r') as f, open(outfile, 'w') as o:

    reader = csv.reader(f)
    writer = csv.writer(o)

    replacements = get_replacements()
    column_map = []

    indexes = []
    header_output = []

    headers = reader.next()
    for hidx, header in enumerate(headers):
        if header in replacements:
            header_output.append(replacements[header])
            column_map.append(hidx)

    writer.writerow(header_output)

    for rowidx, row in enumerate(reader):
        if rowidx == 0:
            pass
        else:
            writer.writerow(process(column_map, row))
