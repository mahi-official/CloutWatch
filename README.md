Discontinued project!
# CloutWatch
Bot for scraping shoe information, price, size availability and images off of (for now) Nike.com using Python, Selenium (chromeDriver) and BeautifullSoup4.

## How it works
Here is a (really early) [video](https://www.youtube.com/watch?v=8goaSL_7WgQ) of how it worked (note that it doesn't include a lot of features described below!)

It first opens a thread that scrapes the main Nike.com sneaker page to index every shoe available for purchase. It holds those shoes in an array. Then it opens up 2 threads that scrape free US proxies off a website (because Nike's website tends to block connections quite quick if you make a lot of requests in succession). After that's done it checks every item in the scraped array for items already in the SQL database. It will place the items that are not yet in the database at the front of the queue (because some shoes sell out after a couple minutes of being released, so being able to scrape those first is paramount!), then it launches a specified amount of threads that are passed with their own sub queues. The thread opens each url and filters the content for a name, price, sizes and availability.
If it finds an item that doesn't match its database counterpart it checks for differences and pushes those to the "notification" database (for further use in a discord or cop bot, ect). Rinse and repeat!

## Why it's discontinued 
I was originally tasked to build this system for a freelance client, they were going to sell API access to the databases that this system generates. But due to the nature of this project  (having to scan each individual item) it requires a lot of processing power for it to be very functional or competitive (with 2 threads it would take an average of 7 minutes to finish scraping all 800 nike shoes. and that doesn't include the likelihood of your connection getting broken by nike). So in reality you would need a-lot of EC2 instances (or 1 big one) for it to be valuable in any way. After discovering this and reporting it to my client, the project was disbanded since there was no apparent way it would be profitable anytime soon.

## What would I do differently if I knew what I know now
Because I didn't have that much experience with web-scraping, queuing or SQL in Python when I first started this, I went into it quite naively and without much thought about system architecture. I felt the repercussions of that later on as I needed to optimize the flow of data to improve speed and readability.

I also wasn't that familiar with pythons' object oriented way of programming so basically all of the code is written functionally. I have since gotten myself more accustomed with classes and their pros and cons.

Another thing I regretted not doing is containerising it either using docker or venv (not really containerising but similar in many ways) because when I started deploying my application on Ubuntu EC2 instances I had a lot of trouble with getting it to work as there were tons of small issues I hadn't foreseen, such as having to write a script that selects the right chromedriver depending on the operating system.

Not wiriting documentation/comments was probably also one of my worst habbits. Because I didn't have much experience with big codebases at the time I wasn't very familiar with forgetting what a function does, what argument it takes and what it returns. Since I had spent countless hours trying to figure out what some piece of code I wrote at 3 am did, I have in fact started (or trying at least) writing insightfull documentation/comments.

And some other things such as error handling and logging and making test code.