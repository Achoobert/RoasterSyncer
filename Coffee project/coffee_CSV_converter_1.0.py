import csv
import re

outputfile_1 = open('16042900.csv', 'wb')
wr = csv.writer(outputfile_1, quoting=csv.QUOTE_ALL)

with open('16042900.csv', 'r') as f:
    text = f.read()
    comma_indices = [m.start() for m in re.finditer(',', text)] #Find all the commas - the fields are between them

    cursor = 0
    field_counter = 1
    row_count = 0
    csv_row = []

    for index in comma_indices:
        newrowflag = False

        if "\r" in text[cursor:index]:
            #This chunk has two fields, the last of one row and first of the next
            next_field=text[cursor:index].split('\r')
            next_field_trimmed = next_field[0].replace('\n',' ').rstrip().lstrip()
            csv_row.extend([next_field_trimmed]) #Add the last field of this row

            #Reset the cursor to be in the middle of the chuck (after the last field and before the next)
            #And set a flag that we need to start the next csvrow before we move on to the next comma index
            cursor = cursor+text[cursor:index].index('\r')+1
            newrowflag = True
        else:
            next_field_trimmed = text[cursor:index].replace('\n',' ').rstrip().lstrip()
            csv_row.extend([next_field_trimmed])

            #Advance the cursor to the character after the comma to start the next field
            cursor = index + 1

        #If we've done 7 fields then we've finished the row
        if field_counter%7==0:
            row_count = row_count + 1
            wr.writerow(csv_row)

            #Reset
            csv_row = []

            #If the last chunk had 2 fields in it...
            if newrowflag:
                next_field_trimmed = next_field[1].replace('\n',' ').rstrip().lstrip()
                csv_row.extend([next_field_trimmed])
                field_counter = field_counter + 1

        field_counter = field_counter + 1
    #Write the last row
    wr.writerow(csv_row)

outputfile_1.close()

# Process output.csv as normal CSV file...    
