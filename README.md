# real-estate-price-prediction
This project predicts the prices of house or apartment in Belgium based on current prices on the market. To collect the current prices of properties I have used IMMOWEB, the Belgian bigest site to sell or buy houses. The project has three main parts that are pipelined to make the final project.
The first part is data acquisition part, second the data cleaning and preprocessing part, the third part is the machine learning
part and the last one is the test and deployment part.

* Data acquisition part

	The data acquisition part is the part which collects prices and all other information of properties by scraping the immoweb.
	To extract all the links of the properties to scraped, I have used sitemap file and beautifulsoup. And after getiing all the links, 
	I have collected all the necessary information of the property from all the links and then stored in a file(CSV).

* Data analysis part
    
	The data analysis part contains all the work of data cleaning and analysis. The data gathered in the first part of the project be first cleaned the unwanted columns and rows based on the information and they contain to further analyse the data. After removing all the unwanted columns and rows, missing values are then inserted based on the type of the data. Categorical data NAN values be inputed with either 'Unknown' or most frequent values. For numerical data types mean values first calculated and then inserted to missing values. After cleaning data and inserting to missing values analysis has been done through different plots.