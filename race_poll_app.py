import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.title('Analysis of Jeff Gluck\'s "Was it a good race?" Poll')
st.write('''Jeff Gluck (@jeff_gluck) has asked all of Twitter for
 their honest opinions on the day after every NASCAR Cup Series
 race since 2016. It's a very simple question really. "Was it a
 good race?" There are only 2 answers (Yes/No), but people have
 different criteria for what they consider to be a "good" race.
 Was the decision based solely on the quality of the racing?
 Did their favorite driver win? Did NASCAR make a questionable
 officiating decision? Did the race go green until one late
 caution that made for an exciting final restart(s)? Did an
 unpopular driver win? As we can see, there are many factors that
 can go into this 'Yes' or 'No' decision. Thankfully,
 Jeff has saved all of the results in a table on his website
 (https://jeffgluck.com) along with some additional information,
 including: number of votes, winner, track type, day/night, and
 time of race. So, I'm going analyze this data and try to make
 some interesting visualizations. Let's get started!''')

df = pd.read_csv('Good Race Poll - Races.csv',
                 header=0,
                 usecols=['Year',
                          'Race',
                          'Yes %',
                          'Votes',
                          'Winner',
                          'Type',
                          'Day/Night',
                          'Time of race'],
                 dtype={'Year': str,
                        'Yes %': np.float64,
                        'Votes': np.int32},
                 thousands=','
                 )

# Rename columns
df = df.rename(columns={'Year': 'year',
                        'Race': 'race',
                        'Yes %': 'like',
                        'Votes': 'votes',
                        'Winner': 'winner',
                        'Type': 'type',
                        'Day/Night': 'day_night',
                        'Time of race': 'time_of_race'
                        })

# A. Dillon and Dillon should be combined into 1 winner
# because they are the same driver.
df = df.replace('Dillon', 'A. Dillon')

poll_fig = px.scatter(df,
                      x='year',
                      y='like',
                      color='year',
                      size='votes',
                      hover_name='race',
                      hover_data={'year': False,
                                  'like': True,
                                  'votes': True,
                                  'winner': True},
                      labels={'like': 'Good Race %',
                              'year': 'Year'},
                      color_discrete_map={'2016': 'grey',
                                          '2017': 'red',
                                          '2018': 'dodgerblue',
                                          '2019': 'gold',
                                          '2020': 'limegreen'},
                      range_y=[0, 105],
                      title=('Jeff Gluck\'s "Was it a good race?" '
                             'Poll - NASCAR Cup Series 2016-2020'),
                      )
poll_fig.update_layout(title_x=0.5)
poll_fig.update_traces(showlegend=False)
st.plotly_chart(poll_fig, use_container_width=True)

st.header('Poll Growth')
poll_growth = df.groupby('year')['votes'].agg(['mean', 'max'])
poll_growth['mean'] = poll_growth['mean'].astype(int)
growth_fig = px.bar(poll_growth, x=poll_growth.index, y='mean',
                    color=poll_growth.index,
                    labels={'mean': 'Number of Votes',
                            'year': 'Year'},
                    color_discrete_map={'2016': 'grey',
                                        '2017': 'red',
                                        '2018': 'dodgerblue',
                                        '2019': 'gold',
                                        '2020': 'limegreen'},
                    title='Average Votes per Race by Year')
growth_fig.update_layout(title_x=0.5)
growth_fig.update_traces(showlegend=False)
st.plotly_chart(growth_fig, use_container_width=True)
percent_growth = round((15979 - 2387) / 2387 * 100)
st.write((f'Poll response has grown {percent_growth}% since its '
          'inception in 2016! But, has the racing gotten any better?'))

st.header('The Racing')

dist_fig = px.histogram(df.sort_values(by='year'),
                        x='like',
                        color='year',
                        facet_col='year',
                        facet_col_wrap=3,
                        facet_col_spacing=0.03,
                        hover_data={'year': False},
                        labels={'count': 'Races',
                                'like': 'Good Race %'},
                        color_discrete_map={'2016': 'grey',
                                            '2017': 'red',
                                            '2018': 'dodgerblue',
                                            '2019': 'gold',
                                            '2020': 'limegreen'},
                        nbins=10,
                        title='Distribution of Good Race % by Year')
dist_fig.for_each_annotation(lambda x: x.update(text=x.text.split("=")[-1]))
dist_fig.update_xaxes(tickangle=90)
dist_fig.update_layout(showlegend=False,
                       title_x=0.5)
st.plotly_chart(dist_fig, use_container_width=True)

st.write('''2020 avoided any terrible races
and produced some of the best racing since the poll started.''')

st.subheader('Average Good Race % by Year')
year_like_avg = df.groupby('year', as_index=False).agg({'like': 'mean'})
year_like_avg = year_like_avg.sort_values(by='like', ascending=False)
year_like_avg['rank'] = [1, 2, 3, 4, 5]
year_like_avg = year_like_avg.set_index('rank')
year_like_avg = year_like_avg.rename(columns={'like': 'avg_like'})
st.table(year_like_avg[['year', 'avg_like']].style.set_precision(2))
st.write('''Actually, 2020 produced the best racing (by average) since
 the poll began!''')

st.header('Track Types')
track_type = df.groupby('type')['like'].mean().round(1)
tt_fig = px.bar(track_type,
                x=track_type.index,
                y='like',
                color='like',
                labels={'type': 'Track Type', 'like': 'Good Race %'},
                range_color=[55, 80],
                title='Good Race % by Track Type 2016-2020',
                range_y=[0, 100])
tt_fig.update_layout(title_x=0.5)
st.plotly_chart(tt_fig, use_container_width=True)
st.markdown(
    '##### *Other type includes: Darlington, Pocono, and Indianapolis.'
    )
st.write('''The top 3 track types that produce good races as voted by the
 fans are: Road, Short, and Super. It seems like NASCAR has finally been
 listening to the fans and have added more road courses to the schedule
 for 2021. Personally, I am very excited to see the Cup cars at COTA. Also,
 we now have a superspeedway at the end of the regular season as well as
 2 short tracks and a road course as the playoff cut races!''')

st.header('Top 5 Races by Good Race %')
top_5 = df.sort_values(by=['like', 'votes'], ascending=[False, False]).head(5)
top_5 = top_5.set_index('race')
st.table(top_5[['year', 'like', 'votes', 'winner']])
st.write('''What I find interesting here is that Bristol has 3 of the Top-5
 most liked races in the "Was it a good race?" poll era. In 2021, they will
 completely change the track and bring the Cup series back to dirt for the
 first time in 50 years. So, they're taking a big gamble when they already
 provide the best on-track product the series has to offer.''')

st.header('Not everyone loves a winner?')
mean_like_by_winner = df.groupby('winner').agg(
    {'race': 'count', 'like': 'mean'}
    ).reset_index()
mean_like_by_winner['like'] = mean_like_by_winner['like'].round(1)
mean_win_fig = px.scatter(mean_like_by_winner.sort_values(
                            by=['race', 'winner']),
                          x='winner',
                          y='like',
                          size='race',
                          color='race',
                          labels={'race': 'Wins',
                                  'like': 'Good Race %',
                                  'winner': 'Winner (by number of wins)'},
                          range_y=[40, 100],
                          title='Average Good Race % by Winner 2016-2020',
                          )
mean_win_fig.update_layout(title_x=0.5)
st.plotly_chart(mean_win_fig, use_container_width=True)

harv_wins = len(df.loc[(df['winner'] == 'Harvick')])
kb_wins = len(df.loc[(df['winner'] == 'KyBusch')])
truex_wins = len(df.loc[(df['winner'] == 'Truex')])
big_3_wins = harv_wins + kb_wins + truex_wins
total_races = len(df['race'])
big_3_win_pct = round(big_3_wins / total_races * 100, 2)

st.write((f'It seems like winning a lot of races leads to a lower average '
          f'Good Race %. The Big-3 (Harvick, KyBusch, and Truex) won '
          f'{big_3_wins} of the {total_races} races polled ({big_3_win_pct}'
          f'%). Of the drivers with 3+ wins, only Larson\'s Good Race % is '
          f'as low as any of the Big-3.'))

st.header('Day vs. Night')
dn_total = df.groupby('day_night').agg(
    {'like': ['count', 'mean']}
    ).reset_index()
# Flatten agg column names.
dn_total.columns = ['_'.join(col).strip()
                    if col[0].startswith('like')
                    else col[0]
                    for col in dn_total.columns.values]
dn_total['like_mean'] = dn_total['like_mean'].round(2)
dn_total = dn_total.rename(columns={'like_count': 'race_count'})
dn_total = dn_total.set_index('day_night')
st.table(dn_total[['race_count', 'like_mean']].style.set_precision(2))
st.write('''I was quite surprised when I saw that the average Good Race %
 between day and night races was within 1% of each other. So, I decided
 to break it down by year.''')

day_night = df.groupby(['year', 'day_night'],
                       as_index=False).agg(
                           {'like': ['count', 'mean']}
                           )
# Flatten agg column names.
day_night.columns = ['_'.join(col).strip()
                     if col[0].startswith('like')
                     else col[0]
                     for col in day_night.columns.values]
day_night['like_mean'] = day_night['like_mean'].round(2)
dn_fig = px.bar(day_night,
                x='year',
                y='like_mean',
                color='day_night',
                hover_data={
                    'like_count': True,
                    'year': False,
                    'like_mean': True
                },
                labels={
                    'day_night': 'Time of Race',
                    'like_mean': 'Avg Good Race %',
                    'like_count': 'Races',
                    'year': 'Year'
                },
                color_discrete_map={
                    'Day': 'yellow',
                    'Night': 'dimgray'
                },
                barmode='group',
                range_y=[0, 100],
                title='Day vs. Night Good Race % by Year'
                )
dn_fig.update_layout(title_x=0.5)
st.plotly_chart(dn_fig, use_container_width=True)
st.write('''People really enjoyed the night races in 2019.''')

st.subheader('2019 Night Races')
# df for the 2019 Night races
s_19 = df.query('year == "2019"')
s_19_night = s_19.query('day_night == "Night"')
s_19_night = s_19_night.set_index('race')
st.table(
    s_19_night[['like', 'time_of_race']].style.set_precision(1)
    )
st.write('''Also found in the 2019 night races are the longest race ever
 polled (Coke 600) and one the shortest races ever polled (All-Star).
 Let's see if the length of the race has anything to do with
 Good Race %.''')

st.header('Time of Race')
df['race_length'] = pd.to_datetime(df['time_of_race'], format='%H:%M')
race_times = df.groupby(
    pd.Grouper(key='race_length', freq='30min')
    ).agg({'like': 'mean', 'votes': 'count'}).reset_index()
race_times['like'] = race_times['like'].round(2)
race_times = race_times.append(
    [{
        'race_length': pd.Timestamp('1900-01-01 00:00:00'),
        'like': 0,
        'votes': 0
    },
     {
        'race_length': pd.Timestamp('1900-01-01 00:30:00'),
        'like': 0,
        'votes': 0
     },
     {
        'race_length': pd.Timestamp('1900-01-01 05:00:00'),
        'like': 0,
        'votes': 0
     }],
    ignore_index=True
)
# Convert column to str and remove date and seconds.
race_times['race_length'] = [
    str(x).split()[1][:5] for x in race_times['race_length']
    ]
race_times = race_times.sort_values(by='race_length').reset_index()

rl_fig = px.bar(race_times,
                x='race_length',
                y='like',
                color='votes',
                hover_data={
                    'like': True,
                    'race_length': False,
                    'votes': True
                    },
                labels={'like': 'Good Race %',
                        'race_length': 'Time of Race (h:mm)',
                        'votes': 'Race Count'
                        },
                color_continuous_scale=px.colors.sequential.Tealgrn,
                range_y=[0, 100],
                title='Good Race % by Length of Race'
                )
rl_fig.update_layout(
    xaxis=dict(
        ticks='inside',
        tickvals=race_times['race_length'],
        ticktext=['0:00', '0:30', '1:00', '1:30', '2:00',
                  '2:30', '3:00', '3:30', '4:00', '4:30', '5:00'],
    ),
    showlegend=False
)
rl_fig.update_layout(title_x=0.5)
st.plotly_chart(rl_fig, use_container_width=True)
st.write('''We can see that most races last between 2.5-4 hours, and
 Good Race % is close between all race lengths, except for the shortest
 races that last only 1-1.5 hours.''')

st.write('''A big thanks to Jeff for being the keeper of the poll and
 for keeping the data public. I'm excited to see what's in store for
 2021.''')
