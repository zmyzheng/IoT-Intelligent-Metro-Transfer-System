
This is the code for temperature collection and display using google chart and Intel Edison.

To run it, do the following:

1. go into directory lab6part1
	$ cd lab6part1

2. collect real-time temperature data into database:
	$ python temperatureRefresh.py

3. open another terminal, and go to directory lab6part1
	$ cd lab6part1

4. in the second terminal, start the server:
	$ python manage.py rumserver 0.0.0.0:8000

5. open your browser, go to http://192.168.0.101:8000/polls/  , then you can see a web page showing the temperature for the last 5 minutes.