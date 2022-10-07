"""CSC110 Fall 2020: Final Project
Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of Lemeng Dai, Arthur Iliescu,
Jiaxin Li, Maisarah Zulkefli. All forms of distribution of this code,
whether as given or with any changes, are expressly prohibited.
This file is Copyright (c) 2021 Lemeng Dai, Arthur Iliescu, Jiaxin Li, Maisarah Zulkefli.
"""
import datetime
from dataclasses import dataclass
import csv


@dataclass
class CasesData:
    """A bundle of data on covid-19 for each province.
    Instance Attributes:
        - province_name: the name of the province
        - date: the time of the data entry
        - number_confirmed: the number of confirmed covid-19 cases
        - number_total: the number of total covid-19 cases
        - number_today: the number of covid-19 cases for the date
        - rate_total: case rate per one hundred thousand population,"Calculated by the
            total number of cases for a province divided by the population of that
            province [(number_total/population) x100,000].

    Representation Invariants:
        - province_id in [35, 59, 24, 48, 43, 17, 61, 62, 12, 60, 99, 46, 47, 11]
        - province_name in ['Alberta', 'Ontario', 'Quebec', 'British Columbia', 'Manitoba', \
                            'New Brunswick', 'Saskatchewan', 'Prince Edward Island', \
                            'Newfoundland and Labrador', 'Nova Scotia']
        - data.year in [2020, 2021]
        - date.month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    """
    province_name: str
    date: datetime.date
    number_confirmed: int
    number_total: int
    number_today: int
    number_tests: int
    rate_total: float


def return_data_cases(filename: str) -> dict[str, dict[tuple[int, int], int]]:
    """A function to run and return the data for the filename.
    """
    lst_provinces = ['Ontario', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan',
                     'Prince Edward Island', 'New Brunswick', 'Nova Scotia', 'Quebec',
                     'Newfoundland and Labrador']

    lst_years = [2020, 2021]
    lst_months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    inputs = load_data(filename)
    data = total_cases_per_years(inputs, lst_months, lst_years, lst_provinces)
    return data


def return_data_tests(filename: str) -> dict[str, dict[tuple[int, int], int]]:
    """A function to run and return the data for the filename.
    """
    lst_provinces = ['Ontario', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan',
                     'Prince Edward Island', 'New Brunswick', 'Nova Scotia', 'Quebec',
                     'Newfoundland and Labrador']

    lst_years = [2020, 2021]
    lst_months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    inputs = load_data(filename)
    data = total_tests_per_years(inputs, lst_months, lst_years, lst_provinces)
    return data


def return_data_rate(filename: str) -> dict[str, dict[tuple[int, int], float]]:
    """A function to run and return the data for the filename.
    """
    lst_provinces = ['Ontario', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan',
                     'Prince Edward Island', 'New Brunswick', 'Nova Scotia', 'Quebec',
                     'Newfoundland and Labrador']

    lst_years = [2020, 2021]
    lst_months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    inputs = load_data(filename)
    data = rate_per_years(inputs, lst_months, lst_years, lst_provinces)
    return data


def load_data(filename: str) -> list[CasesData]:
    """Return a list containing the data for each entry in the file
    """
    # ACCUMULATOR inputs_so_far: The CasesData passed from the filename so far
    inputs_so_far = []

    with open(filename) as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)  # skip the header

        for row in reader:
            if row[17] != '':
                assert len(row) == 40, 'Expected every row to contain 40 elements.'
                split_date = str.split(str(row[3]), '-')
                new_inputs = CasesData(str(row[1]), datetime.date(int(split_date[0]),
                                                                  int(split_date[1]),
                                                                  int(split_date[2])),
                                       int(row[5]), int(row[8]), int(row[15]), int(row[10]),
                                       float(row[17]))

                inputs_so_far.append(new_inputs)

    return inputs_so_far


def cases_per_month(inputs: list[CasesData], month: int, year: int, province: str) -> int:
    """Return the monthly cases for the given province.
    Preconditions:
        - month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        - year in [2020, 2021]
        - province in ['Alberta', 'Ontario', 'Quebec', 'British Columbia', 'Manitoba', \
                            'New Brunswick', 'Saskatchewan', 'Prince Edward Island', \
                            'Newfoundland and Labrador', 'Nova Scotia']
    >>> method = [CasesData(province_name='Ontario', \
    date=datetime.date(2020, 1, 31), number_confirmed=3, number_total=3, number_today=3, \
    number_tests=0, rate_total=0.0)]
    >>> cases_per_month(method, 1, 2020, 'Ontario')
    3
    """
    cases_so_far = 0
    for row in inputs:
        if row.province_name == province and row.date.month == month and row.date.year == year:
            cases_so_far = cases_so_far + row.number_today

    return cases_so_far


def cases_per_month_province(inputs: list[CasesData], months: list[int], years: list[int],
                             province: str) -> dict[tuple[int, int], int]:
    """Return a dictionary matching the month in a calendar year to the number of cases in
    that month for province.
    Preconditions:
        - month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        - year in [2020, 2021]
        - province in ['Alberta', 'Ontario', 'Quebec', 'British Columbia', 'Manitoba', \
                            'New Brunswick', 'Saskatchewan', 'Prince Edward Island', \
                            'Newfoundland and Labrador', 'Nova Scotia']
    >>> method = [CasesData(province_name='Ontario', \
    date=datetime.date(2020, 1, 31), number_confirmed=40, number_total=40, number_today=40, \
    number_tests=0, rate_total=0.0)]
    >>> lst_months = [1]
    >>> lst_years = [2020]
    >>> cases_per_month_province(method, lst_months, lst_years, 'Ontario')
    {(2020, 1): 40}
    """
    dict_so_far = {}
    for year in years:
        for month in months:
            if year == 2021 and month != 12:
                number = cases_per_month(inputs, month, year, province)
                dict_so_far[(year, month)] = number
            elif year == 2020:
                number = cases_per_month(inputs, month, year, province)
                dict_so_far[(year, month)] = number
    return dict_so_far


def total_cases_per_years(inputs: list[CasesData], months: list[int], years: list[int],
                          provinces: list[str]) -> dict[str, dict[tuple[int, int], int]]:
    """Return the Provinces mapped to the years mapped to the total cases per month.
    Preconditions:
        - month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        - year in [2020, 2021]
        - province in ['Alberta', 'Ontario', 'Quebec', 'British Columbia', 'Manitoba', \
                            'New Brunswick', 'Saskatchewan', 'Prince Edward Island', \
                            'Newfoundland and Labrador', 'Nova Scotia']
    >>> method = [CasesData(province_name='Ontario', \
    date=datetime.date(2020, 1, 31), number_confirmed=40, number_total=40, number_today=40, \
    number_tests=0, rate_total=0.0), CasesData(province_name='Alberta', \
    date=datetime.date(2020, 2, 10), number_confirmed=20, number_total=20, number_today=20, \
    number_tests=0, rate_total=0.0)]
    >>> lst_months = [1,2]
    >>> lst_years = [2020]
    >>> lst_provinces = ['Ontario', 'Alberta']
    >>> total_cases_per_years(method, lst_months, lst_years, lst_provinces)
    {'Ontario': {(2020, 1): 40, (2020, 2): 0}, 'Alberta': {(2020, 1): 0, (2020, 2): 20}}
    """
    province_cases_so_far = {}
    for province in provinces:
        a = cases_per_month_province(inputs, months, years, province)
        province_cases_so_far[province] = a
    return province_cases_so_far


def total_tests_per_month(inputs: list[CasesData], month: int, year: int, province: str) -> int:
    """Return the total number of tests for the month of the province.
    Preconditions:
        - month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        - year in [2020, 2021]
        - province in ['Alberta', 'Ontario', 'Quebec', 'British Columbia', 'Manitoba', \
                            'New Brunswick', 'Saskatchewan', 'Prince Edward Island', \
                            'Newfoundland and Labrador', 'Nova Scotia']
    >>> method = [CasesData(province_name='Ontario', \
    date=datetime.date(2020, 1, 31), number_confirmed=5, number_total=5, number_today=5, \
    number_tests=2, rate_total=0.0)]
    >>> total_tests_per_month(method, 1, 2020, 'Ontario')
    2
    """
    tests_so_far = 0
    for row in inputs:
        if row.province_name == province and row.date.month == month and row.date.year == year and \
                tests_so_far < row.number_tests:
            tests_so_far = row.number_tests

    return tests_so_far


def per_month_province_test(inputs: list[CasesData], months: list[int], years: list[int],
                            province: str) -> dict[tuple[int, int], int]:
    """Return the date of each month in months for each year in years mapped to the total number
    of tests for that month.
    Preconditions:
        - month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        - year in [2020, 2021]
        - province in ['Alberta', 'Ontario', 'Quebec', 'British Columbia', 'Manitoba', \
                            'New Brunswick', 'Saskatchewan', 'Prince Edward Island', \
                            'Newfoundland and Labrador', 'Nova Scotia']
    >>> method = [CasesData(province_name='Ontario', \
    date=datetime.date(2020, 1, 31), number_confirmed=40, number_total=40, number_today=40, \
    number_tests=20, rate_total=0.0)]
    >>> lst_months = [1]
    >>> lst_years = [2020]
    >>> per_month_province_test(method, lst_months, lst_years, 'Ontario')
    {(2020, 1): 20}
    """
    dict_so_far = {}
    for year in years:
        for month in months:
            if year == 2021 and month != 12:
                number = total_tests_per_month(inputs, month, year, province)
                dict_so_far[(year, month)] = number
            elif year == 2020:
                number = total_tests_per_month(inputs, month, year, province)
                dict_so_far[(year, month)] = number
    return dict_so_far


def total_tests_per_years(inputs: list[CasesData], months: list[int], years: list[int],
                          provinces: list[str]) -> dict[str, dict[tuple[int, int], int]]:
    """Return the Provinces mapped to the years mapped to the total cases per month.
    Preconditions:
        - month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        - year in [2020, 2021]
        - province in ['Alberta', 'Ontario', 'Quebec', 'British Columbia', 'Manitoba', \
                            'New Brunswick', 'Saskatchewan', 'Prince Edward Island', \
                            'Newfoundland and Labrador', 'Nova Scotia']
    >>> method = [CasesData(province_name='Ontario', \
    date=datetime.date(2020, 1, 31), number_confirmed=40, number_total=40, number_today=40, \
    number_tests=25, rate_total=0.0), CasesData(province_name='Alberta', \
    date=datetime.date(2020, 2, 10), number_confirmed=20, number_total=20, number_today=20,\
     number_tests=15, rate_total=0.0)]
    >>> lst_months = [1,2]
    >>> lst_years = [2020]
    >>> lst_provinces = ['Ontario', 'Alberta']
    >>> total_tests_per_years(method, lst_months, lst_years, lst_provinces)
    {'Ontario': {(2020, 1): 25, (2020, 2): 0}, 'Alberta': {(2020, 1): 0, (2020, 2): 15}}
    """
    province_cases_so_far = {}
    for province in provinces:
        a = per_month_province_test(inputs, months, years, province)
        province_cases_so_far[province] = a
    return province_cases_so_far


def average_rate_per_month(inputs: list[CasesData], month: int, year: int, province: str) -> float:
    """Return the average of sum of rate_total in a month of a certain year for the given province.
    Preconditions:
        - month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        - year in [2020, 2021]
        - province in ['Ontario', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan',
        'Prince Edward Island', 'New Brunswick', 'Nova Scotia', 'Quebec',
        'Newfoundland and Labrador']
    >>> method = [CasesData(province_name='Alberta', \
    date=datetime.date(2020, 1, 31), number_confirmed=40, number_total=40, number_today=40, \
    number_tests=25, rate_total=2.0), CasesData(province_name='Alberta', \
    date=datetime.date(2020, 1, 10), number_confirmed=20, number_total=20, number_today=20, \
    number_tests=15, rate_total=4.0)]
    >>> average_rate_per_month(method, 1, 2020, 'Alberta')
    3.0
    """
    rate_so_far = 0
    length = 0
    for row in inputs:
        if row.province_name == province and row.date.month == month and row.date.year == year:
            rate_so_far = rate_so_far + row.rate_total
            length = length + 1

    if length == 0:
        return 0
    else:
        return round(rate_so_far / length, 2)


def rate_per_month_province(inputs: list[CasesData], months: list[int], years: list[int],
                            province: str) -> dict[tuple[int, int], float]:
    """Return a dictionary matching the month in a calendar year to the average rate in that
     month for province.
    Preconditions:
        - all(month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] for month in months)
        - all(year in [2020, 2021] for year in years)
        - province in ['Ontario', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan',
        'Prince Edward Island', 'New Brunswick', 'Nova Scotia', 'Quebec',
        'Newfoundland and Labrador']
    >>> method = [CasesData(province_name='Alberta', \
    date=datetime.date(2020, 1, 31), number_confirmed=40, number_total=40, number_today=40, \
    number_tests=25, rate_total=2.0), CasesData(province_name='Alberta', \
    date=datetime.date(2020, 2, 10), number_confirmed=20, number_total=20, number_today=20, \
    number_tests=15, rate_total=4.0)]
    >>> rate_per_month_province(method, [1, 2], [2020], 'Alberta')
    {(2020, 1): 2.0, (2020, 2): 4.0}
    """
    dict_so_far = {}
    for year in years:
        for month in months:
            if year == 2021 and month != 12:
                rate = average_rate_per_month(inputs, month, year, province)
                dict_so_far[(year, month)] = rate
            elif year == 2020:
                rate = average_rate_per_month(inputs, month, year, province)
                dict_so_far[(year, month)] = rate
    return dict_so_far


def rate_per_years(inputs: list[CasesData], months: list[int], years: list[int],
                   provinces: list[str]) -> dict[str, dict[tuple[int, int], float]]:
    """Return the Provinces mapped to the years mapped to the total new cases per month.
    Preconditions:
        - all(month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] for month in months)
        - all(year in [2020, 2021] for year in years)
        - all(province in ['Ontario', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan',
        'Prince Edward Island', 'New Brunswick', 'Nova Scotia', 'Quebec',
        'Newfoundland and Labrador'] for province in provinces)
    >>> method = [CasesData(province_name='Alberta', \
    date=datetime.date(2020, 1, 31), number_confirmed=40, number_total=40, number_today=40, \
    number_tests=25, rate_total=2.0), CasesData(province_name='Ontario', \
    date=datetime.date(2020, 1, 10), number_confirmed=20, number_total=20, number_today=20, \
    number_tests=15, rate_total=4.0)]
    >>> rate_per_years(method, [1], [2020], ['Alberta', 'Ontario'])
    {'Alberta': {(2020, 1): 2.0}, 'Ontario': {(2020, 1): 4.0}}
    """
    province_cases_so_far = {}
    for province in provinces:
        a = rate_per_month_province(inputs, months, years, province)
        province_cases_so_far[province] = a
    return province_cases_so_far


def cases_map_provinces(inputs: list[CasesData], month: int, year: int, provinces: list[str]) \
        -> dict[str, list]:
    """Return a dictionary where 'provinces' mapped to provinces and 'cases' mapped to the list of
    new cases for respective provinces in the given month of the given year.
    Preconditions:
        - month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        - year in [2020, 2021]
        - all(x in ['Ontario', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan',
                        'Prince Edward Island','New Brunswick', 'Nova Scotia', 'Quebec',
                        'Newfoundland and Labrador'] for x in provinces)
    >>> method = [CasesData(province_name='Alberta', \
    date=datetime.date(2020, 1, 31), number_confirmed=40, number_total=40, number_today=40, \
    number_tests=25, rate_total=2.0), CasesData(province_name='Ontario', \
    date=datetime.date(2020, 1, 10), number_confirmed=20, number_total=20, number_today=20, \
    number_tests=15, rate_total=4.0)]
    >>> cases_map_provinces(method, 1, 2020, ['Alberta', 'Ontario'])
    {'provinces': ['Alberta', 'Ontario'], 'cases': [40, 20]}
    """
    cases_each = []
    for province in provinces:
        case = cases_per_month(inputs, month, year, province)
        cases_each = cases_each + [case]

    return {'provinces': provinces, 'cases': cases_each}


def return_case_for_map(month: int, year: int) -> dict[str, list]:
    """Return a dictionary where 'provinces' mapped to provinces and 'cases' mapped to the list of
    new cases for respective provinces in the given month of the given year.
    Preconditions:
        - month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        - year in [2020, 2021]
    """
    e = load_data('covid_19_cases.csv')
    provinces = ['Ontario', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan',
                 'Prince Edward Island', 'New Brunswick', 'Nova Scotia', 'Quebec',
                 'Newfoundland and Labrador']
    return cases_map_provinces(e, month, year, provinces)


if __name__ == '__main__':
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # Leave this code uncommented when you submit your files.
    import python_ta
    import doctest

    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts', 'csv', 'datetime', 'dataclass'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200', 'R1710', 'E9998']
    })
    doctest.testmod()
