"""Project for Udacity's Course Programming for Data Science with Python"""

import time
import pandas as pd
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city=''
    cities=['chicago','new york city','washington']
    while not city in cities:
        city=input('Would you like to see data for Chicago, New York City or Washington? ').lower()  
    
    # get user input for month (all, january, february, ... , june)
    month=''
    months=['all','january','february','march','april','may','june']
    while not month in months:
        month=input('Do you wish to filter by month? If no, please enter "all". If yes, please enter the corresponding month (January till June): ').lower()
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day=''
    days=['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    while not day in days:
        day=input('Do you wish to filter by day? If no, please enter "all". If yes, please enter the corresponding day (Monday till Sunday): ').lower()

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
    df['day_of_week'] = df['Start Time'].dt.day_name()   

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

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # display the most common month
    df['month'] = df['Start Time'].dt.month_name()
    popular_month = df['month'].mode()[0]
    print('Most Common Month:', popular_month)
    
    # display the most common day of week
    df['day'] = df['Start Time'].dt.day_name()
    popular_weekday = df['day'].mode()[0]
    print('Most Common Day of Week:', popular_weekday)

    # display the most common start hour    
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station)
    
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)    

    # display most frequent combination of start station and end station trip
    df['Trip'] = 'From ' + df['Start Station'] +' to '+ df['End Station']
    popular_trip = df['Trip'].mode()[0]
    print('Most Popular Trip:', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time=df['Trip Duration'].sum()
    print('Total Travel Time:', total_time,'Minutes')

    # display mean travel time
    mean_time=df['Trip Duration'].mean()
    print('Mean Travel Time:', mean_time,'Minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender in case city is not Washington
    if city!='washington':
        gender_types = df['Gender'].value_counts()
        print(gender_types)

    # Display earliest, most recent, and most common year of birth in case city is not Washington
    if city!='washington':
        birth_year_max = df['Birth Year'].max()
        birth_year_min=df['Birth Year'].min()
        birth_year_mod=df['Birth Year'].mode()[0]

        print('Most Recent Year of Birth:', int(birth_year_max))
        print('Earliest Year of Birth:', int(birth_year_min))
        print('Most Common Year of Birth:', int(birth_year_mod))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    """Main part to analyze US Bike Share Data"""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        
        #Offer the user the possibility to see 5 lines of raw data
        entries = ['yes','no']
        user_input = input('Would you like to see more data? Please enter "Yes" or "No".\n')
        
        while user_input.lower() not in entries:
            user_input = input('Please enter either "Yes" or "No".\n')
            user_input = user_input.lower()
        n = 0        
        while True :
            if user_input.lower() == 'yes':
        
                print(df.iloc[n : n + 5])
                n += 5
                user_input = input('Would you like to see 5 additional rows of data? Please enter "Yes" or "No".\n')
                while user_input.lower() not in entries:
                    user_input = input('Please enter either "Yes" or "No".\n')
                    user_input = user_input.lower()
            else:
                break           
                       
        restart = input('\nWould you like to restart? (Enter:Yes/No).\n')
        #check wheather the user is entering the valid entry or not
        while restart.lower() not in entries:
            restart = input('Please enter either "Yes" or "No".\n')
            restart = restart.lower()
        if restart.lower() != 'yes':
            print('Okay, then I guess we are done.\n')
            break

if __name__ == "__main__":
	main()
