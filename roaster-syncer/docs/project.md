# Internet of Beans

## Introduction 

This project involves collecting data from a coffee roaster and
transferring it to Google Docs so that remote personnel can retrieve the data
and analyse it. The coffee roaster is connected to a local network and has a web
interface that allows the downloading of CSV files. The location of the coffee
roaster is in a relatively remote village, although there is wifi internet
access from the room as well as the LAN.

While the project customer has technical skills, it would be good if we can
produce a turnkey solution already configured and ready to simply plug in and
use.

### Project Team

. Daniel Glassey
. Isaac Schubert
. Martin Hosken
. Rien de Bel

## Project Design

Currently an expert visits the village every week or so and downloads the data
from the coffee roaster onto a laptop and then takes it away to analyse. They
would like to not have to visit so often and have a local be able to pull the
data from the roaster and put it online for the expert to analyse.

Rather than requiring a laptop and heavy manual processing, the approach taken
is to invest in a Raspberry Pi, and give it a button and LED. The roaster
presses the button just before they turn off the roaster. The LED lights up for
at least 2s, during which the data is pulled from the roaster and uploaded to
the internet. Once the data is safely transferred, the LED is extinguished and
the roaster can turn off the machine.

### Hardware

Since the RPi has to connect to two networks: the LAN via a wire; and the
internet via wifi, a model B RPi3 is chosen as the base harware. Adding an LED
and a button to two GPIO pins completes the hardware requirements.

### Errors

Being, in effect, embedded software, the program must not crash. If the program
crashes, then the operator will be aware of this since if they press the button
then then LED will not light. They can power cycle and hopefully everything will
restart correctly.

Other errors can arise from the inability to connect to the roaster or Google.
Errors are reported to the operator via a flash code on the LED. The flash code
is flashed for about a minute before giving up. In addition, if it is possible
to connect to Google, then an error report can be stored there.

The error codes are:

| Code | Description |
|------|-------------|
| 1    | Unable to download a file from the roaster - check the LAN or reset the roaster
| 2    | Unable to upload to Google - check internet connection

## Results

Due to outside time constraints, there was very little development time with the raspberry pi
and hardware. In addition, it was not possible, due to network constraints, to have the
pi talk to Google. So end to end testing, even with local mocking, was not possible.

## Further Work

There is a bug in this code in that if someone presses the button more than once per day
files that have already been uploaded to Google will be uploaded again. What needs to
happen is that the splitter returns a list of files and these are checksum checked, etc.

An alternative is to not have a button but to check the roaster every so often and see what
has changed and then do the upload after each completed roast. If this is the case, then
a watchdog timer would be needed. But there would be no need for a button and LED.

The Google upload structure is too flat. There should be some hierarchy to it.

