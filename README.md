# NFL-Pickem

NFL pickem program that uses google forms and text files to track weekly picks

Features hash maps, string manipulation, 2d arrays, web scraping, web automation, file processing

Uses google API. If you want to make your own version where you can create the weekly forms in 2 clicks 
you're going to need to go through the process of creating your own API project in google cloud.

When making the picks text file (where you input your predictions/winners), the first line will be "Week X", 
the second line will be the persons name followed by all the teams they have winning for that given week. 
Team names must be spelled correctly and are not case sensitive.

example:

Week 1

John ravens steelers bengals browns ...

The sendDMs function will message accounts specified by the username array passed in. You will also need to 
provide the forms url which you can get by using "url = form()" as form returns the url to the form it creates.
You can then pass in the username array and the url which sends the url to all users in the array. You must also
have selenium working with python and chromedriver.

You can also chose to display spreads and favorites in the forms document. You will need to input these spreads yourself in the lines.txt file. simply input "week x" and then the favored team name followed by the amount of points they're favored by.

Example:

week 8

ravens 1

jaguars 2

patriots 1.5

eagles 10.5

dolphins 3.5

vikings 4

cowboys 9

falcons 4.5

raiders 1.5

titans 2

seahawks 3

colts 2.5

49ers 1.5

bills 11

bengals 3.5
