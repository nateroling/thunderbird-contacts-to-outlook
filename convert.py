import sys
import csv

# Columns that will be written to the output csv.
OUTLOOK_COLUMNS = [ 'First Name', 'Last Name', 'Name',
        'E-mail Address', 'E-mail 2 Address',
        'Business Phone', 'Home Phone', 'Business Fax',
        'Pager', 'Mobile Phone',
        'Home Street 1', 'Home Street 2', 'Home City',
        'Home State', 'Home Postal Code', 'Home Country/Region',
        'Business Street', 'Business Street 2', 'Business City',
        'Business State', 'Business Postal Code', 'Business Country/Region',
        'Job Title', 'Department', 'Company', 'Web Page',
        'User 1', 'User 2', 'User 3', 'User 4', 'Notes']

def convert(infile, outfile):
    """
    Convert a Thunderbird contacts csv file to one that can be imported into
    Outlook.

    The Thunderbird file must have column headers.
    """
    with open(infile, 'r') as i, open(outfile, 'w') as o:
        reader = csv.reader(i)
        writer = csv.writer(o, quoting=csv.QUOTE_ALL)

        thunderbird_columns = reader.next()
        writer.writerow(OUTLOOK_COLUMNS)

        # Convert and write each row.
        for row in reader:
            input_entry = dict(zip(thunderbird_columns, row))
            output_entry = convert_entry(input_entry)
            output_values = [output_entry.get(k, "") for k in OUTLOOK_COLUMNS]
            writer.writerow(output_values)

def convert_entry(thunderbird):
    """
    Convert a single entry from a Thunderbird csv file.
    Entry must be a dict of "Column Name": "Value"
    Nickname and Screen Name are ignored unless no other name is found.
    Web Page 2 is ignored.
    """
    outlook = {}

    if thunderbird["Display Name"]:
        outlook["Name"] = thunderbird["Display Name"]
    elif thunderbird["First Name"] or thunderbird["Last Name"]:
        pass # Outlook will use First/Last Name
    elif thunderbird["Screen Name"]:
        outlook["Name"] = thunderbird["Screen Name"]
    elif thunderbird["Nickname"]:
        outlook["Name"] = thunderbird["Nickname"]
    elif thunderbird["Organization"]:
        outlook["Name"] = thunderbird["Organization"]
    elif thunderbird["Primary Email"]:
        outlook["Name"] = thunderbird["Primary Email"]

    outlook["Birthday"] = ("%s-%s-%s" % (
            thunderbird["Birth Year"],
            thunderbird["Birth Month"],
            thunderbird["Birth Day"])).lstrip("-")

    outlook["First Name"] = thunderbird["First Name"]
    outlook["Last Name"] = thunderbird["Last Name"]
    outlook["E-mail Address"] = thunderbird["Primary Email"]
    outlook["E-mail 2 Address"] = thunderbird["Secondary Email"]
    outlook["Business Phone"] = thunderbird["Work Phone"]
    outlook["Home Phone"] = thunderbird["Home Phone"]
    outlook["Business Fax"] = thunderbird["Fax Number"]
    outlook["Pager"] = thunderbird["Pager Number"]
    outlook["Mobile Phone"] = thunderbird["Mobile Number"]
    outlook["Home Street 1"] = thunderbird["Home Address"]
    outlook["Home Street 2"] = thunderbird["Home Address 2"]
    outlook["Home City"] = thunderbird["Home City"]
    outlook["Home State"] = thunderbird["Home State"]
    outlook["Home Postal Code"] = thunderbird["Home ZipCode"]
    outlook["Home Country/Region"] = thunderbird["Home Country"]
    outlook["Business Street"] = thunderbird["Work Address"]
    outlook["Business Street 2"] = thunderbird["Work Address 2"]
    outlook["Business City"] = thunderbird["Work City"]
    outlook["Business State"] = thunderbird["Work State"]
    outlook["Business Postal Code"] = thunderbird["Work ZipCode"]
    outlook["Business Country/Region"] = thunderbird["Work Country"]
    outlook["Job Title"] = thunderbird["Job Title"]
    outlook["Department"] = thunderbird["Department"]
    outlook["Company"] = thunderbird["Organization"]
    outlook["Web Page"] = thunderbird["Web Page 1"]
    outlook["User 1"] = thunderbird["Custom 1"]
    outlook["User 2"] = thunderbird["Custom 2"]
    outlook["User 3"] = thunderbird["Custom 3"]
    outlook["User 4"] = thunderbird["Custom 4"]
    outlook["Notes"] = thunderbird["Notes"]
    return outlook

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "USAGE: convert.py INPUT_FILENAME OUTPUT_FILENAME"
    else:
        infile = sys.argv[1]
        outfile = sys.argv[2]
    convert(infile, outfile)

