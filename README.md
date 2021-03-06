# Tax calculator - flask web app
 Final project for cs50

# Description
Russian citizens have to calculate and pay taxes on dividends received from investments made through US brokers and submit a tax declaration.

Threre are two main difficulties with that:

* Dividends received in US Dollars, but tax base should be converted to Russian roubles on date of transaction.
* Personal income tax rates in Russia is 13% which is different from US. If US withholds less than 13% in taxes, remaining difference should be paid to Russian Tax Service  

Two main sources of income are:
* capital gain tax on share price change
* dividends received

Current web application makes it easier to present and calculate how much taxes should be paid to Russian Tax Service on dividends received from investments in US assets through Interactive brokers LLC

## How it works
* user downloads Dividends report from Interactive brokers
* uploads csv to web app
* then for each transaction:
    * from csv python extracts information:
        * gross income received in US dollars
        * tax withheld in US in US dollars
        * date of transaction
    * app parses another csv file with USD/RUB exchange rates 
    * converts gross income to Russian roubles using exchange rate at date of transaction
    * converts tax withheld in US to Russian roubles using exchange rate at date of transaction
    * calculate personal income tax at rate of 13% as total tax to be paid
    * deducts tax withheld in US from total personal income tax
    * the result is tax to be paid to Russian Tax Service 
* then data is grouped by each year to better present results for each year

# Example

## Csv Dividends report

Report opened in Excel - contains excessive data.  

* First we extract it 

<img src="images/Dividends_report.png" width="1100">

## Calculations

* Then make calculations 

<img src="images/scheme.PNG" height="500">

* Then Save to Database

<img src="images/div_DB.png" width="1100">

## Detailed table

* Then query and show it to user each transaction

<img src="images/detailed.PNG" width="1100">

## Summary

* And grouped by each year

<img src="images/summary.PNG" width="1100">

# Technology

Application uses:
* Python Flask
* SQLite
* Flask_wtf, wtforms, flask_login, flask_sqlalchemy
* Bootstrap


