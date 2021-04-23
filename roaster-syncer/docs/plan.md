read directory page from roaster
get list of csv filenames

read local google directory
get list of csv files


for each one on directory page that isn't in local dir list
download and put in directory

first pass will commit the csv to gitlab

after using chopper to chop each file into individual roasts

Isaac working on authentication with google drive
and upload and check for what is already there

Daniel is looking at gpiozero and how button and LED will
be used with the program

led off
push button
    turn on led, start timer
run get_roast_file
after 2s of timer, or end of get_roast_file, whichever is longer
    turn off led.

error codes

catch all exceptions
if there was an exception then identify it
optionally hold led on for 5s then flash an error code, repeat for 1 minute
what error codes and what can people do?

1) cannot connect to roaster
    is roaster on?
    is roaster connected to network?
    is pi connected to network?

2) cannot connect to external internet
    is there a problem with internet?

3) cannot authenticate with google drive
    um

x) Failed to parse CSV file
continue without flashing error code
but send original CSV renamed to PARSEFAIL-originalname.csv


script always running on pi?
how to start it?
is pi on all the time or started at same time as roaster?

