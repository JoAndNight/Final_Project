# Final_Project
CSC110 Final Project: Pandemic impact on employment rates of Canadian Provinces and Territories

**Instructions**
1. Download the requirements.txt download all the modules that have been used in the project.
2. Save all files in the same folder, marking the folder as route directory. 
3. Run the main.py file.
4. After runing the main.py file, for the line visualization.main(), you are expected to see 8 pages open in your browser. Each two of them is a pair of choropleth maps. One of them shows the number of new COVID-19 cases of a given month in a given year for provinces in Canada. The other one shows that employment rate of a given month in a given year for provinces in Canada. On the left top of each page, there is a title that tells what is showing in the choropleth map. You can try other combination of month and year by calling visualization.choropleth_map_cases(month, year) or visualization.choropleth_map_emp(month, year) in the Python Console. Note that month is limited to one of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] and year is limited to one of [2020, 2021]. Note that these functions does not work when month is 12 and year is 2021 because there is no data for December 2021 yet.
5. After running the main.py file, for the line prediction.main() you will see three graphs in the browser, each shows the relationship between the number of covid 19 cases and the difference of employment rate in Canadian provinces, the relationship between the number of covid 19 tests issued and the difference of employment rate in Canadian provinces, and the relationship between the rate of total COVID-19 cases to the total population and the difference of employment rate in Canadian provinces. It also returns a dictionary that contains three dictionaries mapping the province name to a tuple that contains the score and and the mean squared error of the model for each of the three relationships.

Copyright and Usage Information
===============================
All files are provided solely for the personal and private use of Lemeng Dai, Arthur Iliescu, Jiaxin Li, Maisarah Zulkefli. Arthur All forms of distribution of this code,
whether as given or with any changes, are expressly prohibited.
All files are Copyright (c) 2021 Lemeng Dai, Arthur Iliescu, Jiaxin Li, Maisarah Zulkefli.
