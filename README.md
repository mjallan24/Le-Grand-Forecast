# Le-Grand-Forecast
A sales predictor for Le Grand Bistro Americain using time-series analysis of the restaurants sales and incorporating local weather patterns. Useful for both front and back of house cost estimations as an aid for staffing and food preparation.

## Data Collection
Dinerware is housed in a Microsoft SQL Server Database. By querying this database for the ticket sales across a 4 year period I pulled results for every transaction. 
Using this to derive overall sales and lunch / dinner breakdowns showed quantitative trends over the course of individual days, weeks, and years.

Metar data was collected from Seattle's Boeing Airfield via Iowa State University's Mesonet <url>https://mesonet.agron.iastate.edu/request/download.phtml?network=WA_ASOS</url>.
1:    Seattle / Boeing Field
2:    All Available Data
3:    (Start)   01-02-2015 
      (Final)   03-29-2019
4:    America / Los Angeles Timezone
5:    Comma Delimited
      NaN for missing data
      
Much of this data was missing, however converting raw metar strings into categorical 

## Data Cleaning 
