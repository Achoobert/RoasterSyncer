RoasterSyncer

If you are interested in using this, please contact me! I'd be happy to take a look as long as there are real people who want to use it!

I made this project several years ago as a custom design for a roasting setup that uses 
"PLC controller for Red Lion.
This unit logs all data and current settings of the roaster every 5 seconds and puts out 1 file for each day we operate the machine.
So it spits out a lot of data off which we only need a few things."

The output is designed to be used in Artisan Roaster Scope. It's free and pretty popular with coffee roasters.

**Python script**
The purpouse of this scripts is to import a "daily" CSV and then output "Roasts CSV files"
The original daily files looked like this when imported to Artisan
![image](https://user-images.githubusercontent.com/8057443/118935366-abd35c80-b975-11eb-9306-28425fa5d2e5.png)

![image](https://user-images.githubusercontent.com/8057443/118935434-bee62c80-b975-11eb-970f-6813df3aa585.png)

![image](https://user-images.githubusercontent.com/8057443/118935457-c574a400-b975-11eb-92c4-1d0f99244196.png)

![image](https://user-images.githubusercontent.com/8057443/118935475-c9a0c180-b975-11eb-9e39-eb4a41e0d149.png)

The final result should be a bunch of these... actual individual roasts

![image](https://user-images.githubusercontent.com/8057443/118936258-9874c100-b976-11eb-98d9-740a976354bf.png)


**Google drive api**
Since the roaster is out-of-town, and operated by local workers. the client wanted the ability to access the files remotly
So I hooked up the google drive API to directly upload files as soon as they were processed

**TKlinter**
After getting the script to work, we put together a TKlinter UI so the warehouse workers could run the script, and get a picture with feedback on wither it worked... and if it didn't, where the problem was.

![image](https://user-images.githubusercontent.com/8057443/118936158-7c711f80-b976-11eb-90a7-54b76852543d.png)



I belive the best example of the splitter is
./roaster-syncer/roast_file_processor.py
