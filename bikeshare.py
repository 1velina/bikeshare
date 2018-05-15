import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']

days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

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

    while True:
        try:
            city_position = int(input('Choose a city name:\n 1. New York City\n 2. Chicago\n 3. Washington\n'))
            cities = ['new york city', 'chicago', 'washington']
            city = cities[city_position-1]

            # get user input for month (all, january, february, ... , june)
            month = input('Please enter a month (all, january, february, ... , june)\n').lower()
            if month != 'all' and month not in months:
                raise ValueError('Invalid month entered "{}". Only enter months from January to June or all'.format(month))

            # get user input for day of week (all, monday, tuesday, ... sunday)
            day = input('Please enter a day of the week (all, monday, tuesday, ... sunday)\n').lower()
            if day != 'all' and day not in days_of_week:
                raise ValueError('Invalid day entered "{}". Only enter days from Monday to Sunday or all'.format(day))

            print('-'*40)
            return city, month, day
        except ValueError as error:
            print(error)
        except KeyboardInterrupt:
            break
        except:
            print('Invalid Input')

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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['weekday_name'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    df['Combined Station'] = df['Start Station'] + " - " + df['End Station']

    #filter by month
    if month != 'all':
        month = months.index(month) + 1
        df = df[df['month'] == month]

    #filter by day of week
    if day != 'all':
        df = df[df['weekday_name'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    popular_month_name = months[popular_month-1]
    print('The most popular month is {}'.format(popular_month_name.title()))


    # display the most common day of week
    popular_day = df['weekday_name'].mode()[0]
    print('The most popular day of the week is {}'.format(popular_day))

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular hour is {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most popular start station is "{}"'.format(popular_start_station))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most popular end station is "{}"'.format(popular_end_station))


    # display most frequent combination of start station and end station trip


    popular_trip = df['Combined Station'].mode()[0]

    print('The most popular trip is "{}"'.format(popular_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is {} seconds '.format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time is {} seconds'.format(round(mean_travel_time,2)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The user count is \n{}'.format(user_types))

    # Display counts of gender
    try:
        user_gender = df['Gender'].value_counts()

        print('The user gender count is \n{}'.format(user_gender))
    except:
        print('Gender data not available\n')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = int(df['Birth Year'].min())
        print('The earliest birth year is {}'.format(earliest_birth_year))

        most_recent_birth_year = int(df['Birth Year'].max())
        print('The most recent birth year is {}'.format(most_recent_birth_year))

        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print('The most common birth year is {}'.format(most_common_birth_year))
    except:
        print('Birth Year data not available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Display 5 lines of data if the user asks, display 5 more if the user asks for more, continue until the user stops asking"""

    start_time = time.time()
    raw_data = input('Would you like to review 5 rows of raw data? Please enter: Yes or No\n')
    start_row = 0
    while raw_data.lower() == 'yes':
        for i in range(start_row, start_row + 5):
            print(df.ix[i])

        start_row += 5
        raw_data = input('Would you like to review 5 more rows of raw data? Please enter: Yes or No\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
