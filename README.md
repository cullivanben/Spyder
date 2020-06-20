# Spyder
A python application for simple and efficient web crawling. Built using the 
[popular Scrapy web scraping framework](https://scrapy.org/). The GUI is built using 
[tkinter](https://docs.python.org/3/library/tkinter.html).

Enter target urls and the css selectors you want to scrape and then recieve the 
output in JSON (.json), comma-separated values (.csv), tab-separated values (.tsv), or pipe-separated values (.psv) files.

## Using Spyder

Spyder is designed specifically to enable data to be extracted from the page source of web pages on the internet.

In order to use Spyder you must have a basic understanding of 
[css selectors](https://www.w3schools.com/cssref/css_selectors.asp). Css selectors allow specific html elements 
to be selected. In order to find the css selector of a particular html element on a page that you are viewing, on Chrome: 
right-click and then click "inspect", on Firefox: right-click and then click "Inspect Element".

It is very important to note that the format that css selectors must be passed into Spyder is different from standard 
css selector format. To view the Spyder css selector format, see the [Input Format](#Input-Format) section below.

## Running Spyder

In order to run Spyder, download the source code and load it into an IDE (I recommend 
[PyCharm](https://www.jetbrains.com/pycharm/)). Then, run the file titled main_gui.py which will start the GUI.
From there you will be able to do your crawling by passing input into the GUI.

The source code contains a venv folder. This contains the virtual environment that Spyder runs in and has all of the modules
installed that are needed in order for Spyder to run correctly. If the python interpreter on your computer is not installed
in the location /usr/local/bin/python3.* then you will not be able to run Spyder using this virtual environment and you will
have to manually install the modules that Spyder uses (as specified in the imports of the .py files).

## Input Format

Only one url may be passed in per target. However, an arbitrary amount of targets may be added. In addition, 
the url must abide by the [Crawling Rules](#Crawling-Rules).

Example url: http://quotes.toscrape.com/

Each target can have an arbitrary number of css selector key-selector pairs. The css selectors must be passed 
key-selector pairs where the key is the name that you want the scraped data to have assigned to it in the output files
and the selector is the css selector that you want to scrape. Only one css selector can be provided for each key-selector pair.

The key and selector must be connected by an equals sign and surrounded by parentheses in the format (key=selector)

In addition, key selector pairs must be separated by one comma and one space in the format (key=selector), (key=selector)

You may use element names and class names as css selectors when using Spyder.

Here is an example input of several css selectors for a specific target:

(quote=.quote), (paragraph=p), (header=h1)

In this example, the text of all the items of the quote class, the text of all the p elements 
and the text of all h1 elements is scraped.

## Which Output File Format To Use

It is very important to choose the correct output format. Gernerally it is best to choose .csv .tsv or .psv when you are 
scraping specific elements from a page and you are certain that there is an equal number of each element type. This is super 
important because if there is not an equal number of each element type then some of the rows in the output file would be 
incomplete. For this reason, if you attempt to scrape data that cannot be represented as a table in which all of the rows are
complete you must store the output in a .json file.

JSON works in any case. If you are scraping data that cannot be represented as a table with complete rows then you must 
use the JSON format.

## Crawling Rules

The source code of Spyder is set to obey robots.txt. 

If you attempt to crawl a url that is disallowed by the site's robots.txt file, Spyder will alert you and no data will be 
scraped.

**I claim no responsibility for any crawling that is done by people that download the Spyder source code, including crawling 
that is not in compliance with robots.txt**

Furthermore, if you decide to download the source code and run Spyder I **highly recommend** that you comply with robots.txt.
It is possible to change the settings file so that Spyder does not comply with robots.txt, however, I do not recommend that you
do this because failing to comply with robots.txt is a violation of many sites' terms and conditions.
