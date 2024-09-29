# this function takes input as string data and outputs a dataframe with the following columns
# for each message
    # message_date - contains the date and time
    # user - contains the sender
    # date, time, day, month, year 

import re 
import pandas as pd

def preprocess(data):
    # now, we have separate date , time, sender and message in two different columns
    # we have written a regular expression string which can be used to separate them
    # tool names regex 101 can be used to build a regular expression string like this

    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    #re.split(pattern,data) will split the data using the pattern
    
    dates = re.findall(pattern, data)
    #re.findall(pattern,data) will find all the pattern matches in the data
    #it will return a list of dates


    # Create a new DataFrame from the provided messages and dates lists
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Remove the trailing ' - ' from the message_date column to clean up the data
    df['message_date'] = df['message_date'].str.rstrip(' - ')

    # Convert the message_date column to a datetime object using the specified format
    # The format '%d/%m/%y, %H:%M' indicates day/month/year, hour:minute
    # The dayfirst=True parameter ensures that the day is parsed before the month
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M', dayfirst=True)

    # Rename the message_date column to a more concise and descriptive name
    df.rename(columns={'message_date': 'date'}, inplace=True)


    # Initialize empty lists to store user names and messages
    users = []
    messages = []

    # Iterate over each message in the 'user_message' column of the dataframe
    for message in df['user_message']:
        # Split the message into parts using a regular expression
        # The regex pattern matches one or more characters (including spaces and punctuation) 
        # followed by a colon and a space, capturing the part before the colon
        entry = re.split('([\w\W]+?):\s', message)

        # If the split resulted in more than one part (i.e., a user name was found)
        if entry[1:]:  
            # Extract the user name (the second part of the split)
            # first part will be empty string if no user name is found
            users.append(entry[1])
            # Extract the message (the remaining parts of the split, joined back together)
            messages.append(" ".join(entry[2:]))
        else:
            # If no user name was found, use a default value
            users.append('group_notification')
            # Use the original message as the message text
            messages.append(entry[0])

    # Create new columns in the dataframe for the user names and messages
    df['user'] = users
    df['message'] = messages

    # Drop the original 'user_message' column
    df.drop(columns=['user_message'], inplace=True)


    # the existing object is a date time object, we extract year, month .. easily
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df