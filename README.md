# SCU Second Chances Hackathon - Project 6
> Problem Statement
+ Scrape the website of Montgomery County Criminal Records - [Link](https://montgomery.tncrtinfo.com/crcaseList.aspx), to get all the criminal information and make it available in JSON or CSV format. The main reason for the project is to filter out those criminal records whose data is now less important or either the case is disposed, and clear those records which are irrelavant inorder to improve the life of those criminals.

## For Linux Machine
### Tools
+ selenium chrome driver for linux
+ pandas

### Setup
+ Download Selenium Chrome Driver [Downloads](http://chromedriver.chromium.org/downloads)
+ Install Selenium ```sudo pip install selenium```
+ Install pandas ```sudo pip install pandas```

### Running the project
+ run ```python scrape.py```
+ Let the script control your browser and gather all the data in criminal.json
+ Once all the data is collected, run ```python json_to_csv.py``` to convert json data to csv.
