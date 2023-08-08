# As a data analyst for a marketing agency, your services have been requested to
# advise on the best type of content to create that has the highest potential
# customer sentiment for prospective advertisers. 

# Using Youtube channel data, determine which content has the highest sentiment

# Consider the following dataframe with columns: video_id, title, category_id, likes, dislikes

# It represents information about each video_id

# Use this dataframe, accessible as video_stats_df in the code, to create and return
# a dataframe with columns category_id and mean_sentiment sorted by descending mean_sentiment

# Sentiment is defined as number of likes over the total number of likes and dislikes.
# We need to determine each category's average sentiment

# Solution:

# 1) Get the sentiment for each video_id and category_id
# 2) Average the sentiment across all data points and partition by category_id

import pandas as pd

def get_youtube_sentiment(video_stats_df):
  
  video_stats_df['sentiment'] = video_stats_df['likes'] / (video_stats_df['likes'] + video_stats_df['dislikes'])
  
  mean_sentiments = pd.DataFrame(video_stats_df.groupby('category_id')['sentiment'].mean())
  
  mean_sentiments.columns = ['mean_sentiment']
  
  mean_sentiments.sort_values(by = 'mean_sentiment', inplace = True, ascending = False)
  
  return mean_sentiments
  
