# real-estate-price-prediction
This project predicts the prices of house or apartment in Belgium based on current prices on the market. To collect the current prices of properties I have used IMMOWEB, the Belgian bigest site to sell or buy houses. The project has three main parts that are pipelined to make the final project.
The first part is data acquisition part, second the data cleaning and preprocessing part, the third part is the machine learning
part and the last one is the test and deployment part.

## Data acquisition part

The data acquisition part is the part which collects prices and all other information of properties by scraping the immoweb.
To extract all the links of the properties to scraped, I have used sitemap file and beautifulsoup. And after getiing all the links, 
I have collected all the necessary information of the property from all the links and then stored in a file(CSV).
