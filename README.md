# DRPCIV monitor

### Yay, got my booking
You've just booked a day for your theoretical driving exam, but it's a month from now... wtf ?

No worries, usually there are a free slots which appear now and then, but it's a pain in the ass to keep 
an eye on them all the time...or is it? 

### How the f it works

Go get yourself some of that sweet Twilio trial sms https://www.twilio.com/sms. We're gonna need the twilio auth key.


docker image build --build-arg TWILIO_AUTH={your_twilio_auth_key} -t drpciv-monitor .
docker run -it -t drpciv-monitor --start-date={when_to_start_looking} --end-date={until_when} 
--phone-number={your_phone_number}

--start-date, --end-date - date of format yyyy-mm-dd
--phone-number - (+prefix){your_number} (e.g +40749123242)