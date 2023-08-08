# COnsider a dataframe with columns request_path, search_term, user_id, ip_address.
# date.

# It represents user interactions with movie search pages. Each interaction is represented
# by user_id of the user who made it, the movie search term that they looked for,
# and the date of the interaction, amongst other things

# Use this interaction dataframe, accessible as search_interactions_df in the code,
# to create a features dataframe of the following form:
# user_id, month_interaction_count, week_interaction_count, day_interaction_count

# Each user_id in the returned dataframe should have entries in the month_interaction_count,
# week_interaction_count, and day_interaction_count columns representing the number
# of search page interactions that the user had over the past month, week, and day,
# respectively.

# The past month, week, and day should be based off of the latest date present in 
# search_interactions_df; specifically they should be the last 30, 7 and 1 days
# before the last date, respectively.

# Solution:

# 1) Find the latest date in the dataframe
#   - Aggregation to find the max of a column
#   - Extract the value from the dataframe with collect() method

# 2) Select rows only in the last month and group the rows by user ID to get the month counts
# - where() to filter dates
# - groupby() to group the user_ids
# - count() to get counts

# 3) Repeat for week and day counts
# 4) Join the month, week, day counts into a single dataframe - join() on user_id

def get_user_interaction_counts(search_interactions_df):
  
  latest_date_string = search_interactions_df.agg({"date": "max"}).collect()[0][0]
  # agg function will take in a map of the column that we want to specify
  # the aggregation over as well as the operation that we want to perform on it
  # to extract the value that is produced by max, use collect (returns a matrix where we can xtract the element that we want)
  latest_date = datetime.strptime(latest_date_string, '%Y-%m-%d')
  
  user_month_counts = get_df_counts_from_date_by_user_id(search_interactions_df, latest_date, 30)
  user_week_counts = get_df_counts_from_date_by_user_id(search_interactions_df, latest_date, 7)
  user_day_counts = get_df_counts_from_date_by_user_id(search_interactions_df, latest_date, 1)
  
  user_month_counts = user_month_counts.withColumnRenamed("count", "month_interaction_count")
  user_week_counts = user_week_counts.withColumnRenamed("count", "week_interaction_count")
  user_day_counts = user_day_counts.withColumnRenamed("count", "day_interaction_count")
  
  user_interaction_counts = user_month_counts.join(user_week_counts, ['user_id'], "left")
  user_interaction_counts = user_interaction_counts.join(user_day_counts, ['user_id'], "left")
  user_interaction_counts = user_interaction_counts.na.fill(0)
  
  return user_interaction_counts

def get_df_counts_from_date_by_user_id(df, end_date, days_delta):
  start_date = end_date - timedelta(days = days_delta)
  
  return df.where(df['date'].between(start_date, end_date)).groupBy("user_id").count()
