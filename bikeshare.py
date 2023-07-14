# import the needed packages
import pandas as pd
import numpy as np
import datetime as dt

# define constants and global variables
CITY_DATA = {'chicago': './chicago.csv',
             'new york city': './new_york_city.csv',
             'washington': './washington.csv'}
weekdays = ['monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday', 'sunday']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'july']


# statistics functions
def time_charts(df):
    """
    Display the hourly distribution of trips.

    Args:
        df : The bikeshare data.

    """
    df['Hour'] = pd.to_datetime(df['Start Time']).dt.hour

    # Count the occurrences of each hour
    hour_counts = df['Hour'].value_counts().sort_index()

    print('Hourly Distribution of Trips:')
    print(hour_counts)
    print()


def user_information(df):
    """
    Display the user types and, if available, gender distribution.

    Args:
        df : The bikeshare data.

    """
    user_types = df['User Type'].value_counts()
    print('User Types:')
    print(user_types)
    print()

    # Check if 'Gender' column exists in the DataFrame
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('Gender Distribution:')
        print(gender_counts)
        print()


def trip_length_information(df):
    """
    Display the total and maximum travel time for the selected filters.

    Args:
        df : The bikeshare data.

    """
    print("the total travel time for the selected filters is {} hours".format(
        df['Trip Duration'].sum()/3600))
    print("the maximum travel time for the selected filters is {} hours!".format(
        df['Trip Duration'].max()/3600))


def gender_distribution(df):
    """
    Display the gender distribution if available, otherwise display a message.

    Args:
        df : The bikeshare data.

    """
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('Gender Distribution:')
        print(gender_counts)
        print()
    else:
        print('Gender information not available for this dataset.')


def station_information(df):
    """
    Display the most popular starting and ending stations.

    Args:
        df : The bikeshare data.

    """
    print('the most popular starting station is {}'.format(
        df['Start Station'].mode()[0]))
    print('the most popular ending station is {}'.format(
        df['End Station'].mode()[0]))


# UTILITY FUNCTIONS

def get_closest_match(city):
    """
    function used to get the closest match to the city the user entered ignores misspellings and spacings, uses a simple matching algorithm

    param: city - the city the user entered
    return: the closest match to the city the user entered"""
    city_match = {'new york city': 0, 'washington': 0, 'chicago': 0}
    ny = 'new york city'
    wa = 'washington'
    chi = 'chicago'
    for i in city:
        if i in ny:
            ny = ny[ny.index(i):]
            city_match['new york city'] += 1
        if i in wa:
            wa = wa[wa.index(i):]
            city_match['washington'] += 1
        if i in chi:
            chi = chi[chi.index(i):]
            city_match['chicago'] += 1
    return max(city_match, key=city_match.get)


def prompt_user(prompt, choices, aliases=[]):
    """
    function used to ask the user a question, and provide a list of choices to pick from and a list of aliases that the user can also answer from
    param: prompt - the question to ask the user
    param: choices - a list of choices to pick from
    param: aliases - a list of aliases that the user can also answer from
    return: the user's answer

    """
    while True:
        print(prompt, "answer with", choices)
        ans = input().lower().strip()
        if ans in choices:
            return ans
        elif ans == 'exit':
            raise SystemExit
        else:
            print('please provide an answer from the given list')


def format_time(col_name, new_col_name, df, pattern):
    """function to format the time in the dataframe to the specified pattern
    param: col_name - the name of the column to format
    param: new_col_name - the name of the new column to create
    param: df - the dataframe to format
    param: pattern - the pattern to format the time to"""
    df[new_col_name] = pd.to_datetime(
        df[col_name]).dt.time.map(lambda t: t.strftime(pattern))
    return df[new_col_name]


def format_date(col_name, new_col_name, df, pattern):
    """
    function to format the date in the dataframe to the specified pattern
    param: col_name - the name of the column to format
    param: new_col_name - the name of the new column to create
    param: df - the dataframe to format
    param: pattern - the pattern to format the date to
    """
    df[new_col_name] = pd.to_datetime(
        df[col_name]).dt.date.map(lambda t: t.strftime(pattern))
    return df[new_col_name]


def seconds_to_dhm(seconds):
    """
    function to convert seconds to hours and minutes
    param: seconds - the number of seconds to convert
    return: the number of hours and minutes"""
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 86400) // 60
    return "{} Hours and {} Minutes".format(hours, minutes)


def filter_data(df, month_list, day_list):
    """
    filterdata function to filter the data by month and day
    param: df - the dataframe to filter
    param: month_list - the list of months to filter by
    param: day_list - the list of days to filter by
    return: the filtered dataframe"""
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.day_name()
    df = pd.concat(
        map(lambda month: df[df['Month'] == (months.index(month)+1)], month_list))
    df = pd.concat(
        map(lambda day: df[df['Weekday'] == (day.title())], day_list))
    df = df.sample(frac=1)
    return df


def get_filters():
    """
    function to get the filters from the user by which the data will be restricted
    return: the filters the user entered"""
    month_filter = day_filter = 0
    input_error = False
    while 1:
        month_filter = input("enter a month or a list of months between January and July: ").lower(
        ).strip().replace(' ', '').split(',')
        for month in month_filter:
            if month not in months:
                print("please enter a month within the specified range.")
                input_error = True
        if input_error:
            input_error = False
            continue
        else:
            break
    while 1:
        day_filter = input("enter a day or a list of days of the week: ").lower(
        ).strip().replace(' ', '').split(',')
        for day in day_filter:
            if day not in weekdays:
                print("please check your spelling. could not understand {}".format(day))

        if input_error:
            input_error = False
            continue
        else:
            break

    return day_filter, month_filter


def load_city_data(city, month, day):
    """function to load the city data from the csv file and filter it according to the user's input
    param: city - the city the user entered
    param: month - the month the user entered
    param: day -the day the user entered"""
    # try:
    print("loading data for {} filtering by {}, {}".format(city, month, day))

    bikeshare_data = pd.DataFrame(
        pd.read_csv(CITY_DATA[city])).drop("Unnamed: 0", axis=1)

    # bikeshare_data = filter_data(bikeshare_data, month, day)
    # format_date(
    #     'Start Time', 'Date', bikeshare_data, '%d/%m/%Y')

    # format_time(
    #     'Start Time', 'Start Time', bikeshare_data, '%H:%M')
    # format_time(
    #     'End Time', 'End Time', bikeshare_data, '%H:%M')

    return bikeshare_data.fillna('other')
    # .head(row_count), hourly_chart_data, daily_chart_data


def get_city(city):
    """
    function to get the city from the user, and check if the city is valid and if not, provide a suggestion

    param: city - the city the user entered
    return: the city the user entered or the closest match to the city the user entered or None if the city does not match the user's input"""
    ny = 'new york city'
    wa = 'washington'
    chi = 'chicago'

    if city in [ny, wa, chi]:
        return city
    else:
        city = get_closest_match(city)
        prompt = "did you mean " + city + "?"
        ans = prompt_user(prompt, ['yes', 'no'])
        if ans == 'yes':
            return city
        else:
            return None


def main():
    while True:
        count = 5
        city = input("enter city: ")
        city = get_city(city)
        if city != None:
            days, months = get_filters()
            bikeshare_data = load_city_data(city, months, days)

            while True:
                time_charts(bikeshare_data)
                user_information(bikeshare_data)
                trip_length_information(bikeshare_data)
                gender_distribution(bikeshare_data)
                station_information(bikeshare_data)
                ans = prompt_user(
                    "would you like to view raw data?", choices=['yes', 'no'])
                if ans == 'yes':
                    print(bikeshare_data.head(count))
                    count += 5
                elif ans == 'no':
                    break


if __name__ == "__main__":
    main()
