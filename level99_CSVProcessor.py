import sys       #for commandline arguments
import datetime  #for date/time comparisons
import csv       #for writing to a csv file

csvList = []        #holds the original CSV file data
processedList = []  #holds the processed CSV file's data (date, time, ticket count)

comparisonList = []     #temporarily holds a specified (first instance) date/time for ticket comparison
sortedList = [0,0,0]    #temporarily holds the finalized ticket count for a specific date/time
exportList = []         #holds a specific date/time/ticket list for csv export

location = 0        #tracks the current csv file row
locationList = []   #holds a list of csv rows for deletion

labelFlag = True    #flag allows the exported csv file's fields to be written once
loopCounter = 0     #counter for ensuring that the row's date/time/ticket fields are properly exported
processCounter = 0

#####################################################
# Function: ImportCSV()
#   -imports the CSV and transfers data to a list
#####################################################
def ImportCSV():
    csvFile = open(sys.argv[1], 'r')
    print("Opening CSV File")

    #store CSV data into list
    global csvList

    print("Reading CSV File")
    csvList = csvFile.readlines()
    print("CSV entries: " + str(len(csvList)))

    print("Closing CSV File")
    csvFile.close()

#####################################################
# Function: sortCSVByBookingDate()
#   -sort imported CSV by booking date
#####################################################
def sortCSVByBookingDate():
    firstPassFlag = True  #flags for the storing of the intial date/time for each distinct date/time
    ticketCount = 0       #holds the date/time instance's ticket count
    global location

    #loops through the original csv file's rows (via lists)
    for item in list(csvList):
        if (item != csvList[0]):
            #remove delimeters and store
            bookingDateRaw = item.split(",")
            bookingDateList = bookingDateRaw[3].split("-")
            bookingTimeList = bookingDateRaw[2].split(":")
            bookingTicketCount = bookingDateRaw[4]

            #format date and time elements
            bookingDate = datetime.date(int(bookingDateList[0]), int(bookingDateList[1]), int(bookingDateList[2]))
            bookingTime = datetime.time(int(bookingTimeList[0]), int(bookingTimeList[1]))

            #stores the info from the first instance/appearance of a date/time
            if (firstPassFlag):
                firstPassFlag = False
                comparisonList.append(str(bookingDate) + " " + str(bookingTime))
                ticketCount = bookingTicketCount

                sortedList[0] = bookingDate
                sortedList[1] = bookingTime
                sortedList[2] = bookingTicketCount

            #compares ticket count for a specified date/time and...
            #stores (over the current elements) if less tickets are available
            for booking in list(comparisonList):
                #print(str(bookingDate) + " " + str(bookingTime))
                if (booking == str(bookingDate) + " " + str(bookingTime)):
                    locationList.append(location)

                    if (bookingTicketCount <= ticketCount):
                        sortedList[0] = bookingDate
                        sortedList[1] = bookingTime
                        sortedList[2] = bookingTicketCount

        #set next element location
        location = location + 1

######################################################
# Function: FormatAndExport()
#   -handles list formatting and exports to text file
######################################################
def FormatAndExport():
    global labelFlag
    global loopCounter

    fields = ['Booking Date', 'Booking Time', 'Ticket Count']

    for item in list(processedList):
        if (labelFlag):
            #write the initial fields only once (via labelFlag)
            with open('level99Bookings.csv','w') as csvFile:
                csvWriter = csv.writer(csvFile)
                csvWriter.writerow(fields)

            labelFlag = False

        #grab processsed element and set within a list
        exportList.append(str(item))
        loopCounter = loopCounter + 1

        #write list to a csv row if all three elements (date, time, tickets) have been 'read'ied'
        if (loopCounter == 3):
            print(exportList)

            with open('level99Bookings.csv','a') as csvFile:
                csvWriter = csv.writer(csvFile)
                csvWriter.writerow(exportList)

            exportList.clear()
            loopCounter = 0

######################################################
# Main area
#   -handles script flow
######################################################

ImportCSV()

#loop and remove csv elements until the list only contains the label fields
while (len(csvList) > 1):
    sortCSVByBookingDate()
    processCounter = processCounter + 1
    print("Sort/Process CSV File:" + " " + str(processCounter) + " distict Date/Time slots")

    #store distinct date, time, and final ticket count for export
    for item in list(sortedList):
        processedList.append(item)

    #remove all (original) csv rows (lists) that contain the prior "for" loops distinct date/time
    for element in reversed(list(locationList)):
        #print(element)
        csvList.pop(element)

    comparisonList.clear()
    locationList.clear()
    location = 0

#re-format and export to csv
FormatAndExport()
