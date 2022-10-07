"""CSC110 Fall 2020: Final Project

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of Lemeng Dai, Arthur Iliescu,
Jiaxin Li, Maisarah Zulkefli. Arthur All forms of distribution of this code,
whether as given or with any changes, are expressly prohibited.

This file is Copyright (c) 2021 Lemeng Dai, Arthur Iliescu, Jiaxin Li, Maisarah Zulkefli.
"""
import csv
from dataclasses import dataclass
import datetime


@dataclass
class EmploymentData:
    """A bundle of data on employment statistics for each province.

    Instance Attributes:
        - province: the name of the province
        - date: the year and month of the data.
        - labour_force_statistics: a string describing which kind of data is recorded.
        - data_type: a string describing whether the value is given in the numbner of people
            or the percentage.
        - value: the float that gives the value.


    Representation Invariants:
        - province_name in ['Alberta', 'Ontario', 'Quebec', 'British Columbia', 'Manitoba',
                            'New Bruswick', 'Saskatchewan', 'Prince Edward Island',
                            'Newfoundland and Labrador', 'Nova Scotia']
        - data.year in [2020, 2021]
        - date.month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    """
    province: str
    date: datetime.date
    labour_force_statistics: str
    data_type: str
    value: float


def return_data(filename: str) -> dict[str, dict[tuple[int, int], float]]:
    """A function to run and return the data for the filename.
    """
    lst_provinces = ['Ontario', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan',
                     'Prince Edward Island', 'New Brunswick', 'Nova Scotia', 'Quebec',
                     'Newfoundland and Labrador']

    lst_years = [2020, 2021]
    lst_months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    inputs = load_data_employment(filename)
    data = employment_rate_total(inputs, lst_months, lst_years, lst_provinces)
    return data


def load_data_employment(filename: str) -> list[EmploymentData]:
    """Return a list containing the data for each entry in the file"""

    # ACCUMULATOR inputs_so_far: The CasesData passed from the filename so far

    inputs_so_far = []

    with open(filename, 'r', encoding='UTF-8') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)  # skip the header
        for row in reader:
            assert len(row) == 19, 'Expected every row to contain 19 elements.'
            split_date = str.split(str(row[0]), '-')
            new_inputs = EmploymentData(str(row[1]), datetime.date(int(split_date[0]),
                                        int(split_date[1]), 1),
                                        str(row[3]), str(row[8]), float(row[14]))
            inputs_so_far.append(new_inputs)

    return inputs_so_far


def population_num(inputs: list[EmploymentData], month: int, year: int, province: str) -> float:
    """Return the population in thousands of the province during set month and year.

    Precondition:
        - month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        - year in [2020, 2021]
        - province in ['Ontario', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan',
                        'Prince Edward Island','New Brunswick', 'Nova Scotia', 'Quebec',
                        'Newfoundland and Labrador']

    >>> population_num(load_data_employment('employment_combined.csv'), 1, 2020, 'Alberta')
    3487.0
    """

    for row in inputs:
        if year == 2021 and month != 12:
            if row.province == province and row.date.month == month and row.date.year == year and \
                    row.labour_force_statistics == 'Population' and row.data_type == 'Persons':
                return row.value
        elif year == 2020:
            if row.province == province and row.date.month == month and row.date.year == year and \
                    row.labour_force_statistics == 'Population' and row.data_type == 'Persons':
                return row.value


def employment_num(inputs: list[EmploymentData], month: int, year: int, province: str) -> float:
    """Return the number of people employed in thousands of the province during set month and year.

    Precondition:
        - month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        - year in [2020, 2021]
        - province in ['Ontario', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan',
                        'Prince Edward Island','New Brunswick', 'Nova Scotia', 'Quebec',
                        'Newfoundland and Labrador']

    >>> employment_num(load_data_employment('employment_combined.csv'), 1, 2020, 'Alberta')
    2261.0
    """

    for row in inputs:
        if year == 2021 and month != 12:
            if row.province == province and row.date.month == month and row.date.year == year and \
                    row.labour_force_statistics == 'Employment' and row.data_type == 'Persons':
                return row.value
        elif year == 2020:
            if row.province == province and row.date.month == month and row.date.year == year and \
                    row.labour_force_statistics == 'Employment' and row.data_type == 'Persons':
                return row.value


def employment_rate_per_month(inputs: list[EmploymentData], month: int, year: int, province: str) \
        -> any:
    """Return the employment rate for set month and year of the province.

    Precondition:
        - month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        - year in [2020, 2021]
        - province in ['Ontario', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan',
                        'Prince Edward Island','New Brunswick', 'Nova Scotia', 'Quebec',
                        'Newfoundland and Labrador']

    >>> e = load_data_employment('employment_combined.csv')
    >>> employment_rate_per_month(e, 1, 2020, 'Alberta')
    64.8
    """

    if year == 2021 and month != 12:
        population = population_num(inputs, month, year, province)
        employment = employment_num(inputs, month, year, province)

        rate = (employment / population) * 100
        return round(rate, 1)

    elif year == 2020:
        population = population_num(inputs, month, year, province)
        employment = employment_num(inputs, month, year, province)

        rate = (employment / population) * 100
        return round(rate, 1)


def employment_rate_to_date(inputs: list[EmploymentData], months: list[int], years: list[int],
                            province: str) -> dict[tuple[int, int], float]:
    """Return a dictionary mapping each date in months and years to the employment rate of province.

    Precondition:
        - all(month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] for month in months)
        - all(year in [2020, 2021] for year in years)
        - province in ['Ontario', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan',
                        'Prince Edward Island','New Brunswick', 'Nova Scotia', 'Quebec',
                        'Newfoundland and Labrador']

    >>> e = load_data_employment('employment_combined.csv')
    >>> employment_rate_to_date(e, [1, 2], [2020, 2021], 'Alberta')
    {(2020, 1): 64.8, (2020, 2): 65.0, (2021, 1): 61.8, (2021, 2): 62.2}
    """
    dict_years_so_far = {}
    for year in years:
        for month in months:
            if year == 2021 and month != 12:
                rate = employment_rate_per_month(inputs, month, year, province)
                dict_years_so_far[(year, month)] = rate
            elif year == 2020:
                rate = employment_rate_per_month(inputs, month, year, province)
                dict_years_so_far[(year, month)] = rate
    return dict_years_so_far


def employment_rate_total(inputs: list[EmploymentData], months: list[int], years: list[int],
                          provinces: list[str]) -> dict[str, dict[tuple[int, int], float]]:
    """Return a dictionary mapping each province to another dictionary with date mapped to
    employment rate for that province.

    Precondition:
        - all(month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] for month in months)
        - all(year in [2020, 2021] for year in years)
        - all(x in ['Ontario', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan',
                        'Prince Edward Island','New Brunswick', 'Nova Scotia', 'Quebec',
                        'Newfoundland and Labrador'] for x in provinces)

    >>> e = load_data_employment('employment_combined.csv')
    >>> employment_rate_total(e, [1, 2], [2020, 2021], ['Alberta', 'Ontario'])
    {'Alberta': {(2020, 1): 64.8, (2020, 2): 65.0, (2021, 1): 61.8, (2021, 2): 62.2}, \
'Ontario': {(2020, 1): 61.6, (2020, 2): 61.6, (2021, 1): 57.7, (2021, 2): 58.5}}
    """
    dict_so_far = {}
    for province in provinces:
        rate = employment_rate_to_date(inputs, months, years, province)
        dict_so_far[province] = rate
    return dict_so_far


def employment_rate_month_province(inputs: list[EmploymentData], month: int, year: int,
                                   provinces: list[str]) -> dict[str, list]:
    """Return a dictionary mapping province to its employment rate in the given month of the given
    year.

    Precondition:
        - month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        - year in [2020, 2021]
        - all(x in ['Ontario', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan',
                        'Prince Edward Island','New Brunswick', 'Nova Scotia', 'Quebec',
                        'Newfoundland and Labrador'] for x in provinces)

    >>> e = load_data_employment('employment_combined.csv')
    >>> employment_rate_month_province(e, 1, 2020, ['Alberta', 'Ontario'])
    {'provinces': ['Alberta', 'Ontario'], 'employment_rate': [64.8, 61.6]}
    """
    rate_so_far = []
    for province in provinces:
        rate = employment_rate_per_month(inputs, month, year, province)
        rate_so_far = rate_so_far + [rate]
    return {'provinces': provinces, 'employment_rate': rate_so_far}


def return_emp_for_map(month: int, year: int) -> dict[str, list]:
    """Return a dictionary mapping province to its employment rate in the given month of the given
    year.

    Precondition:
        - month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        - year in [2020, 2021]

    >>> e = load_data_employment('employment_combined.csv')
    >>> return_emp_for_map(1, 2020)
    {'provinces': ['Ontario', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan', \
'Prince Edward Island', 'New Brunswick', 'Nova Scotia', 'Quebec', 'Newfoundland and Labrador'], \
'employment_rate': [61.6, 61.8, 64.8, 63.3, 64.5, 62.0, 56.5, 57.2, 61.7, 50.2]}
    """
    e = load_data_employment('employment_combined.csv')
    provinces = ['Ontario', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan',
                 'Prince Edward Island', 'New Brunswick', 'Nova Scotia', 'Quebec',
                 'Newfoundland and Labrador']
    return employment_rate_month_province(e, month, year, provinces)


if __name__ == '__main__':
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # Leave this code uncommented when you submit your files.
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts', 'csv', 'datetime', 'dataclass'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200', 'R1710', 'E9998']
    })

    import doctest

    doctest.testmod()
