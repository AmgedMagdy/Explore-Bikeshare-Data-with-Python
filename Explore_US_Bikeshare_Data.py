import time
import pandas as pd
import statistics as st


CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


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
        cities = ['chicago', 'new york city', 'washington']
        user_city = input('Select a city from (Chicago, New York City, Washington): ')
        city = user_city.lower()
        if city in cities:
            print('selected city is:', city.title())
            break
        if city not in cities:
            print('Invalid selection, please select a city from the given cities!')
            continue
    while True:
        user_ask = input('Do you want to filter by day, month or both? , for no time filter type \'none\': ')
        ask = user_ask.lower()
        # get user input for month (all, january, february, ... , june)
        if ask == 'month':
            day = None
            while True:
                months = ['january', 'february', 'march', 'april', 'may', 'june']
                user_month = input('Please select a month from January to June by typing'
                                   ' its full name (eg.: january): ')
                month = user_month.lower()
                if month in months:
                    print('You\'re currently filtering by month and the selected month is:', month.title())
                    break
                if month not in months:
                    print('Invalid selection, please try again.')
                    continue
            break
        elif ask == 'day':
            # get user input for day of week (all, monday, tuesday, ... sunday)
            month = None
            while True:
                days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
                user_day = input('Please select a day by typing its full name (eg.: Sunday): ')
                day = user_day.lower()
                if day in days:
                    if day != 'all':
                        print('You\'re currently filtering by day and the selected day is:', day.title())
                        break
                else:
                    print('Invalid selection, please try again.')
                    continue
            break
        elif ask == 'both':
            while True:
                months = ['january', 'february', 'march', 'april', 'may', 'june']
                user_month = input('Please select a month from January to June by typing'
                                   ' its full name (eg.: january): ')
                month = user_month.lower()
                if month in months:
                    print('The selected month is:', month.title())
                else:
                    print('Invalid selection, please try again.')
                    continue
                days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
                user_day = input('Please select a day by typing its full name (eg.: Sunday): ')
                day = user_day.lower()
                if day in days:
                    print('The selected day is:', day.title())
                    break
                else:
                    print('Invalid selection, please try again.')
                    continue
            break
        elif ask == 'none':
            print('You\'ve selcted not to apply any time filter..')
            month = 'all'
            day = 'all'
            break

        else:
            print('Invalid selection, please try again.')
            continue

    print('-'*40)
    return city, month, day, ask


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
    print('Loading data.. Please wait!')
    start_time = time.time()
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if (month != 'all') and (month is not None):
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if (day != 'all') and (day is not None):
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    # if user selected no filter
    #if (month == 'all') and (day == 'all'):
    #    return df

    print("\nData loaded successfully,This took %s seconds." % (time.time() - start_time))
    # Viewing row data
    n = 5
    while True:
        view_data = input('Do you want to view the first {} rows of the raw data? Enter yes or no: '.format(n))
        if view_data.lower() == 'yes':
            print(df.head(n))
            n += 5
        elif view_data.lower() == 'no':
            break
        else:
            print('Invalid selection, please try again!')
            continue
    return df


def time_stats(df, ask):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    if (ask == 'day') or (ask == 'none'):
        print('Most common month is {}'.format(st.mode(df['month'])))

    # display the most common day of week
    if (ask == 'month') or (ask == 'none'):
        print('Most common day of the week is {}'.format(st.mode(df['day_of_week'])))

    # display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    print('Most common start hour is {}'.format(st.mode(df['start_hour'])))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_stats = df['Start Station'].value_counts()
    most_start = start_stats.max()
    print('Most commonly used start station is {}'.format(start_stats[start_stats == most_start].index[0]))

    # display most commonly used end station
    end_stats = df['End Station'].value_counts()
    most_end = end_stats.max()
    print('Most commonly used end station is {}'.format(end_stats[end_stats == most_end].index[0]))

    # display most frequent combination of start station and end station trip
    df['Start_End_Combined'] = df['Start Station'] + ' to ' + df['End Station']
    start_end_stats = df['Start_End_Combined'].value_counts()
    most_start_end = start_end_stats.max()
    print('Most commonly used start end combination of stations is {}'
          .format(start_end_stats[start_end_stats == most_start_end].index[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    time_sum = round((df['Trip Duration'] / (60*60)).sum(), 2)
    print('Total travel time is {} hours'.format(time_sum))

    # display mean travel time
    trip_mean = round((df['Trip Duration']/60).mean(), 2)
    print('Mean travel time for a trip is {} minutes'.format(trip_mean))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print('Bikeshare user types and their count is:\n{}\n'.format(user_type))
    try:
        # Display counts of gender
        user_gender = df['Gender'].value_counts()
        print('Bikeshare users gender and their count is:\n{}]\n'.format(user_gender))
        # Display earliest, most recent, and most common year of birth
        print('Earliest year of birth: {}\nMost recent year of birth: {}\nMost common year of birth: {}'
              .format(int(min(df['Birth Year'])), int((df['Birth Year'].max())),
                      int(df['Birth Year'].mode())))
    except KeyError:
        print('No details about gender and birth dates available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day, ask = get_filters()
        df = load_data(city, month, day)
        time_stats(df, ask)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
