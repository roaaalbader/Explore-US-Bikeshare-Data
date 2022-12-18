import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for Chicago, New York, or Washington?\n').lower()
        if city in ['chicago', 'new york', 'washington']:
            break
        else:
            print('Sorry wrong entry please try again\n')    

    # get user input for month (all, january, february, ... , june)
    while True: 
        month = input('Which month - January, February, March, April, May, June, or all?\n').lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        else:
            print('Sorry wrong entry please try again\n') 

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all?\n').lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        else:
            print('Sorry wrong entry please try again\n')
    
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
     # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        
    # filter by month to create the new dataframe
        df = df[df['month'] == month]
        
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('The most common month is: ', common_month)
    
    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most common day is: ', common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_st_hour = df['hour'].mode()[0]
    print('The most common start hour is: ', common_st_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('The most common used start station is: ', start_station)

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('The most common used end station is: ', end_station)

    # display most frequent combination of start station and end station trip
    df["station_combination"] = df['Start Station'] +"_"+ df['End Station']
    frequent_station = df['station_combination'].mode()[0]
    print('The most frequent combination of start station and end station trip is: ', frequent_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is: ', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time is: ', mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The counts of user types is: ', user_types)

    # Display counts of gender
    if city != 'washington':
        gender_ct = df['Gender'].value_counts()
        print('The counts of gender is: ', gender_ct)


    # Display earliest, most recent, and most common year of birth
    try:
        earliest = df['Birth Year'].min()
        print('The earliest year of birth is: ', earliest)
    except KeyError:
        print('No data available')
    
    try:
        most_recent = df['Birth Year'].max()
        print('The most recent year of birthis: ', most_recent)
    except KeyError:
        print('No data available')
    try:
        common_year = int(df['Birth Year'].mode()[0])
        print('The most common year of birth is: ', common_year)
    except KeyError:
        print('No data available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while True:
        if view_data == 'yes':
            print(df.iloc[start_loc:start_loc+5])
            start_loc += 5
        elif view_data == 'no':
            break
        else:
            print('Sorry wrong entry please try again\n')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()