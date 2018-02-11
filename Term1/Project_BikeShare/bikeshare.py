import sys
import os
import glob
import time
import pandas as pd
import numpy as np



def get_city():
    '''
    Asks the user for a city name and returns the filename for that city's bike share data

    :param:
        none.
    :return:
        (str) Filename for a city's bike share data, e.g. "chicago.csv"
    '''

    city = input('\nHello! Let\'s explore some US bikeshare data!\n'
                 'Would you like to see data for Chicago, New York City, or Washington?   :   ')

    city = city.strip().lower()
    file_name = "_".join(city.split()) + ".csv"

    pwd = os.getcwd()
    city_data_available  = [os.path.basename(p) for p in glob.glob(pwd + "/*.csv")]

    if file_name not in city_data_available:
        print(f"Data file '{file_name}' for the city '{city}' is not available")
        print("Available dataset are: {}".format(city_data_available))
        print("Please Restart !!")
        sys.exit(0)
    else:
        return file_name, city


def get_time_period():
    '''
    Ask the user for time filer, like by month or day or nothing

    :param:
        none.
    :return:
        (str) month, day or none
    '''

    time_period = input('\nWould you like to filter the data by month, day ? [Type "month", "day" or "none" for no time'
                        ' filter]  :  ')

    time_period = time_period.strip().lower()
    if time_period not in ["month", "day", "none"]:
        print("Enter a valid filer, [month, day, none]")
        sys.exit(0)

    else:
        return time_period


def get_month():
    '''
    Ask the user for a specific month and returns month in integer

    :param:
        none.
    :return:
        (int) Returns the month entered by user in number, like 1-> Jan, 12-> Dec
    '''

    month_to_num = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7,
                    'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

    month = input('\nWhich month? Type [Jan, Feb, .., Dec]   : ')
    month = month.strip()[:3].capitalize()

    if month not in month_to_num.keys():
        print("Enter a valid month, [Jan, Feb, .. Dec]")
        print("Please Restart !!")
        sys.exit(0)
    else:
        return month_to_num[month]


def get_day():
    '''
    Ask the user for a specific day and returns day in integer

    :param:
        none.
    :return:
        (int) Returns the day entered by user in number, like 0-> Monday, 6-> Sunday
    '''

    day = input('\nWhich day? Please type your response as an integer [0 -> Monday, 1-> Tuesday, .. 6 -> Sunday]   : ')

    if int(day) not in range(7):
        print("Enter a valid day in integer, [0 -> Monday, 1-> Tuesday, .. 6 -> Sunday]")
        print("Please Restart !!")
        sys.exit(0)
    else:
        return int(day)


def get_data(city_file_name):
    '''
    This function returns a pandas data frame object and also it converts the "Start Time" and "End Time"
    to a datetime object from the CSV file for easy data analysis later on

    :param:
     (str) city_file_name: name of the CSV file, e.g. "chicago.csv"
    :return:
     (pd.DataFrame) pandas data frame object with the date loaded with datetime object
    '''

    df = pd.read_csv(city_file_name, parse_dates=[0, 1])

    return df


def popular_day(df):
    '''
    This function calculates the most popular day of the week

    :param:
     (pd.DataFrame) df: Takes the data frame
    :return:
     (tuple) Returns a tuple with the most popular day of the week and no_of_rides for that particular day
    '''

    num_to_day = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}

    df["Day_of_Start"] = df["Start Time"].dt.dayofweek
    day_stats = df.groupby(["Day_of_Start"]).size().to_dict()

    day_stats = list(day_stats.items())

    sorted_by_days = sorted(day_stats, key=lambda x: x[1], reverse=True)

    popular_day = num_to_day[sorted_by_days[0][0]]
    no_of_ride = sorted_by_days[0][1]

    return popular_day, no_of_ride


def popular_month(df):
    '''
    This function calculates the most popular month for start

    :param:
     (pd.DataFrame) df: Takes the data frame
    :return:
     (tuple) Returns a tuple with the most popular month of the year, like Jan, Feb, etc. and
             no_of_rides for that particular month
    '''

    num_to_month = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul",
                    8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}

    df["Month_of_Start"] = df["Start Time"].dt.month
    month_stats = df.groupby(["Month_of_Start"]).size().to_dict()

    month_stats = list(month_stats.items())

    sorted_by_months = sorted(month_stats, key=lambda x: x[1], reverse=True)

    popular_month = num_to_month[sorted_by_months[0][0]]
    no_of_ride = sorted_by_months[0][1]

    return popular_month, no_of_ride


def popular_hour(df):
    '''
    This function calculates the most popular hour for the start

    :param:
     (pd.DataFrame) df: Takes the data frame
    :return:
     (tuple) Returns a tuple with the most popular hour of the day like, 00, 01, 13, 24 and
             no_of_rides for tha particular hour
    '''

    df["Hour_of_Day"] = df["Start Time"].dt.hour
    hour_stats = df.groupby(["Hour_of_Day"]).size().to_dict()

    hour_stats = list(hour_stats.items())

    sorted_by_hour = sorted(hour_stats, key=lambda x: x[1], reverse=True)

    popular_hour = sorted_by_hour[0][0]
    no_of_ride = sorted_by_hour[0][1]

    return popular_hour, no_of_ride


def trip_duration(df):
    '''
    This function calculates the total trip duration Returns and avg trip duration

    :param:
     (pd.DataFrame) df: Takes the data frame
    :return:
     (tuple) Tuple consists of Total_trip_duration(in hours) and Avg_trip_duration(in Mins)
    '''

    duration_hours = round(df["Trip Duration"].sum()/60/60, 2)
    avg_hours = round(df["Trip Duration"].mean()/60, 2)

    return duration_hours, avg_hours


def popular_stations(df):
    '''
    This function calculates the most popular start and end station

    :param:
     (pd.DataFrame) df: Takes a city data frame
    :return:
     (tuple) Tuple consists of the most popular start station and the most popular end station with ride counts
    '''

    start_station = df.groupby(df["Start Station"]).size().to_dict()
    end_station = df.groupby(df["End Station"]).size().to_dict()

    start_station = list(start_station.items())
    end_station = list(end_station.items())

    start_station_sorted = sorted(start_station, key=lambda x: x[1], reverse=True)
    end_station_sorted = sorted(end_station, key=lambda x: x[1], reverse=True)

    popular_start_station = start_station_sorted[0]
    popular_end_station = end_station_sorted[0]

    return popular_start_station, popular_end_station


def users(df):
    '''
    This function calculates the counts for different user type

    :param:
     (pd.DataFrame) df: Takes a city data frame
    :return:
     (list) List consists of tuples with (user type, user count) as each element of the list
    '''

    user_count = df.groupby(df["User Type"]).size().to_dict()
    user_count = list(user_count.items())

    return user_count


def gender(df):
    '''
    This function calculates the gender

    :param:
     (pd.DataFrame) df: Takes a city data frame
    :return:
     (list) List consists of tuples with (gender and count) as each element of the list
    '''

    gender_count = df.groupby("Gender").size().to_dict()
    gender_count = list(gender_count.items())

    return gender_count


def popular_trip(df):
    '''
    This function returns the most popular trip, eg. from 'X' starting point to 'Y' ending point

    :param:
     (pd.DataFrame) df: Takes a city data frame
    :return:
     (tuple)  A tuple with consists of (the most popular trip and count of such trip)
    '''

    df["Trip"] = df["Start Station"] + "__" + df["End Station"]
    trips = df.groupby("Trip").size().to_dict()
    trips = list(trips.items())

    popular_trips_sorted = sorted(trips, key=lambda x: x[1], reverse=True)

    most_popular_trip = popular_trips_sorted[0]

    return most_popular_trip


def birth(df):
    '''
    This function calculates the earliest, most recent, and most popular birth years

    :param:
     (pd.DataFrame) df: Takes a city data frame
    :return:
     (tuple) The tuple consists of the most popular, earliest, recent year of birth with their respective counts
    '''
    birth_years = df.groupby(df["Birth Year"]).size().to_dict()
    birth_years = list(birth_years.items())

    sorted_birth_count = sorted(birth_years, key=lambda x: x[1], reverse=True)
    sorted_birth_year = sorted(birth_years, key=lambda x: x[0])

    most_popular_year = sorted_birth_count[0]
    earliest_year, recent_year = sorted_birth_year[0], sorted_birth_year[-1]

    return most_popular_year, earliest_year, recent_year


def display_data(df1):
    '''
    Displays five lines of data if the user specifies that they would like to.
    After displaying five lines, ask the user if they would like to see five more,
    continuing asking until they say stop.

    :param:
     (pd.DataFrame) df: Takes a city data frame
    :return:
     Prints 5 lines of the data from the respective city data frame, and it continues until user says to continue("Yes")
    '''

    display = input('Would you like to view individual trip data? [Yes or No] : ')
    end = 5
    start = 0
    while display.lower() == "yes":
        dfRange = df1.iloc[start:end]
        print(dfRange)
        start = end
        end += 5
        display = input('Would you like to view more trip data(next 5 lines) ? [Yes or No]  :  ')



def statistics(time_period, df, city_name):
    '''
    Calculates and prints out the descriptive statistics about a city and time period
    specified by the user via raw input.

    :param:
     time_period (str) : month or day or none
     df (pd.DataFrame) : data frame object for the respective city
     city_name (str) : name of the city
    :return:
     nothing
    '''
    i = 150

    print("-" * i)
    if time_period == "none":
        # What is the most popular month for start time?
        month, count = popular_month(df)
        print(f"The most popular month for bikesharing is '{month.upper()}' with '{count}' numbers of rides\n")
        print("-" * i)

    if time_period in ['none', 'month']:
        # What is the most popular day of week for start time?
        day, count = popular_day(df)
        print(f"The most popular day for bikesharing is '{day.upper()}' with '{count}' numbers of rides\n")
        print("-" * i)

    # What is the most popular hour of day for start time?
    hours, count = popular_hour(df)
    print(f"The most popular hour of day for start time is '{hours}:00' hours with {count} number of rides\n")
    print("-" * i)

    # What is the total trip duration and average trip duration?
    total_trip_duration, avg_trip_duration = trip_duration(df)
    print(f"The total trip duration is '{total_trip_duration} hours'")
    print(f"The average trip duration is '{avg_trip_duration} mins'\n")
    print("-" * i)

    # What is the most popular start station and most popular end station?
    popular_start_station, popular_end_station = popular_stations(df)
    print(
        f"The most popular Starting Station is '{popular_start_station[0]}' where there were '{popular_start_station[1]}' number of rides")
    print(
        f"The most popular Ending Station is '{popular_end_station[0]}' where there were '{popular_end_station[1]}' number of rides\n")

    print("-" * i)

    # What is the most popular trip?
    full_trip, count = popular_trip(df)
    start_dest, end_dest = full_trip.split("__")
    print(
        f"The most popular trip is from '{start_dest.strip().upper()}' to '{end_dest.strip().upper()}' with '{count}' number of rides\n")
    print("-" * i)


    # What are the counts of each user type?
    all_users = users(df)
    print("The count of rides based on different users are as follows:")
    for u in all_users:
        print(u[0], u[1])

    print("-" * i)

    if city_name != "washington":
        # What are the counts of gender?
        gender_data = gender(df)
        print("The count of rides based on gender are as follows:")
        for g in gender_data:
            print(g[0], g[1])

        print("-" * i)
        # What are the earliest, most recent, and most popular birth years?
        pop_year, earliest_year, recent_year, = birth(df)
        print(f"The earliest birth year : '{int(earliest_year[0])}' with '{earliest_year[1]}' number of rides")
        print(f"The recent birth year : '{int(recent_year[0])}' with '{recent_year[1]}' number of rides")
        print(f"The most popular birth '{int(pop_year[0])}' with '{pop_year[1]}' number of rides\n")
        print("-" * i)



def main():
    '''
    This is the main funciton which gets started and intracts with the user with the command line inputs
    and prepares and calculates all the statistics

    :param:
     nothing
    :return:
     nothing
    '''


    # Filter by city (Chicago, New York, Washington)
    city_file_name, city_name = get_city()
    time_period = get_time_period()


    if time_period == 'none':

        # Loading the data
        start_time = time.time()
        df = get_data(city_file_name)
        df_for_display = df.copy()
        diff = time.time() - start_time

        print("Time to load the data : {}".format(round(diff, 2)))

        statistics('none', df, city_name=city_name)
        display_data(df_for_display)


    elif time_period == 'month':

        m = get_month()

        # Loading the data
        start_time = time.time()
        df = get_data(city_file_name)
        df = df[df["Start Time"].dt.month == m]
        if not bool(len(df)):
            print("No Data available for the requested month, please restart with a different month filer")
            sys.exit(0)
        df.index = np.arange(0, len(df))

        df_for_display = df.copy()
        diff = time.time() - start_time

        print("Time to load the data : {}".format(round(diff, 2)))

        statistics('month', df, city_name=city_name)
        display_data(df_for_display)


    elif time_period == 'day':

        d = get_day()

        # Loading the data
        start_time = time.time()
        df = get_data(city_file_name)
        df = df[df["Start Time"].dt.day == d]
        df.index = np.arange(0, len(df))
        df_for_display = df.copy()
        diff = time.time() - start_time

        print("Time to load the data : {}".format(round(diff, 2)))

        statistics('day', df, city_name=city_name)
        display_data(df_for_display)

    # Restart?
    restart = input('Would you like to restart?  [Yes or No]  :   ')
    if restart.lower() == 'yes':
        main()


if __name__ == "__main__":
    main()

