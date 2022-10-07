"""CSC110 Fall 2020: Final Project

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of Lemeng Dai, Arthur Iliescu,
Jiaxin Li, Maisarah Zulkefli. Arthur All forms of distribution of this code,
whether as given or with any changes, are expressly prohibited.

This file is Copyright (c) 2021 Lemeng Dai, Arthur Iliescu, Jiaxin Li, Maisarah Zulkefli.

Transform the dict of data into DataFrame type. Transform dataframes of monthly covid 19 cases and
differences in employment rate between consecutive months into a dictionary that maps province name
to a dataframe that contains this province's monthly covid 19 cases and the difference in employment
rate. Choose 80% the data of each province to train the model and 20% of the data to test the model
later on. Draw a scatter diagram with the number of covid 19 cases as independent variable and
employment rate as dependent variable. Find the model that fits the relationship between covid cases
and employment rate for each province. Perform the model on the 20% testing data and compare it with
the actual data to get the score of how well the model fits, as well as mean squared error.
"""
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
# from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import covid19_cases
import employment_rate


def predict(data: pd.DataFrame) -> (float, float):
    """split data into training and testing sets to train the nonlinear model, then test how the
    model works."""
    independent_var = data.iloc[:, 0].values.reshape(-1, 1)
    employment = data.iloc[:, 1].values.reshape(-1, 1)
    x_train, x_test, y_train, y_test = train_test_split(independent_var, employment, test_size=0.2)
    dic = {}
    for i in range(1, 10):
        model = DecisionTreeRegressor(max_depth=i)  # non-linear regression
        # model = LinearRegression()  # linear regression
        model.fit(x_train, y_train)
        y_pred = model.predict(x_test)
        mse = mean_squared_error(y_test, y_pred)
        dic[mse] = model, x_test, y_pred
    mse = min(dic.keys())
    model = dic[mse][0]
    score = model.score(x_test, y_test)
    return (mse, score)


def predict_lst(data: dict[str, pd.DataFrame]) -> dict[str, tuple[float, float]]:
    """build model and make predictions and test for each province. returns a dictionary that maps
    the province name to the mean squared error and the score of the model. """
    dic = {}
    for province in data:
        dic[province] = predict(data[province])
    return dic


def draw_diagram1(data: dict[str, pd.DataFrame]) -> None:
    """draw a scatter diagram to visualize the dataset with the number of covid 19 cases as
    independent variable and difference of employment rate as dependent variable for each province.
    """
    fig = make_subplots(
        rows=3, cols=4,
        subplot_titles=list(data),
        x_title='number of covid 19 cases', y_title='difference in employment rate (%)')
    for i, df in enumerate(data.values()):
        fig.add_trace(go.Scatter(x=df['cases'], y=df['employment rate'], mode='markers'),
                      row=(i // 4 + 1), col=(i % 4 + 1))

    fig.update_layout(title_text="Relationship between the number of covid 19 cases and "
                                 "the difference of employment rate in Canadian provinces")

    fig.show()


def draw_diagram2(data: dict[str, pd.DataFrame]) -> None:
    """draw a scatter diagram to visualize the dataset with the number of covid 19 cases as
    independent variable and difference of employment rate as dependent variable for each province.
    """
    fig = make_subplots(
        rows=3, cols=4,
        subplot_titles=list(data),
        x_title='number of covid 19 tests', y_title='difference in employment rate (%)')
    for i, df in enumerate(data.values()):
        fig.add_trace(go.Scatter(x=df['tests'], y=df['employment rate'], mode='markers'),
                      row=(i // 4 + 1), col=(i % 4 + 1))

    fig.update_layout(title_text="Relationship between the number of covid 19 tests issued and "
                                 "the difference of employment rate in Canadian provinces")

    fig.show()


def draw_diagram3(data: dict[str, pd.DataFrame]) -> None:
    """draw a scatter diagram to visualize the dataset with the number of covid 19 cases as
    independent variable and difference of employment rate as dependent variable for each province.
    """
    fig = make_subplots(
        rows=3, cols=4,
        subplot_titles=list(data),
        x_title='rate of total covid 19 cases to the total population',
        y_title='difference in employment rate (%)')
    for i, df in enumerate(data.values()):
        fig.add_trace(go.Scatter(x=df['rates'], y=df['employment rate'], mode='markers'),
                      row=(i // 4 + 1), col=(i % 4 + 1))

    fig.update_layout(title_text="Relationship between the rate of total covid 19 cases to the "
                                 "total population and the difference of employment rate in"
                                 "Canadian provinces")

    fig.show()


def transform_data(covid: pd.DataFrame, employment: pd.DataFrame, column1: str) -> \
        dict[str, pd.DataFrame]:
    """transform dataframes of monthly covid 19 cases and differences in employment rate between
    consecutive months into a dictionary that maps province name to a dataframe that contains this
    province's monthly covid 19 cases and the difference in employment rate."""
    lst_province = {}
    for province in covid:
        dic = {column1: covid[province], 'employment rate': employment[province]}
        lst_province[province] = pd.DataFrame(dic)
    return lst_province


def prediction_employment_rate(filename: str) -> dict[str, dict[tuple[int, int], float]]:
    """Return a dictionary of difference number of covid cases mapping to differences of employment
    rate"""
    x = employment_rate.return_data(filename)
    prediction = {}
    for provinces in x:
        date_to_employment = {}
        for date in x[provinces]:
            if date == (2020, 1):
                date_to_employment[date] = 0
            elif date == (2021, 1):
                old_date = (2020, 12)
                date_to_employment[date] = x[provinces][date] - x[provinces][old_date]
            else:
                old_date = (date[0], date[1] - 1)
                date_to_employment[date] = ((x[provinces][date]) - (x[provinces][old_date]))
        prediction[provinces] = date_to_employment

    return prediction


def main() -> dict[str, dict[str, tuple[float, float]]]:
    """the main function that performs all the actions and executes all the other functions"""
    covid_data = covid19_cases.return_data_cases('covid_19_cases.csv')
    new_covid_data = pd.DataFrame(covid_data)

    tests_data = covid19_cases.return_data_tests('covid_19_cases.csv')
    new_tests_data = pd.DataFrame(tests_data)

    rates_data = covid19_cases.return_data_rate('covid_19_cases.csv')
    new_rates_data = pd.DataFrame(rates_data)

    difference_employment_rate = prediction_employment_rate('employment_combined.csv')
    new_difference_employment_rate = pd.DataFrame(difference_employment_rate)

    comparison1 = transform_data(new_covid_data, new_difference_employment_rate, 'cases')
    comparison2 = transform_data(new_tests_data, new_difference_employment_rate, 'tests')
    comparison3 = transform_data(new_rates_data, new_difference_employment_rate, 'rates')
    draw_diagram1(comparison1)
    draw_diagram2(comparison2)
    draw_diagram3(comparison3)
    a = predict_lst(comparison1)
    b = predict_lst(comparison2)
    c = predict_lst(comparison3)
    return {'cases': a, 'tests': b, 'rates': c}


if __name__ == '__main__':
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # Leave this code uncommented when you submit your files.
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts', 'csv', 'datetime', 'dataclass', 'pandas',
                          'sklearn.tree', 'covid19_cases', 'employment_rate',
                          'sklearn.model_selection', 'sklearn.metrics', 'plotly.subplots',
                          'plotly.graph_objects', 'sklearn.linear_model'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200', 'R1710']
    })
