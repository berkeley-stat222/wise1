###### 50 level donations city_state

donations = pd.read_csv('/Users/stephaniekim/Desktop/wise/ipython/opendata_donations.csv')


# city_state column
donations['donor_city_state'] = donations['donor_city'] + ', ' + donations['donor_state']


# ordered number of donations for each city_state
counts_donations = donations['donor_city_state'].value_counts()
# just counts
counts_donations_2 = pd.DataFrame(counts_donations.values, columns=['counts'])
# just names
names_donations = pd.DataFrame(counts_donations.index, columns = ['city_state'])


# rank 1~length
ranks_donations = pd.DataFrame([x+1 for x in range(counts_donations.shape[0])], columns = ['city_state_rank'])

# concat
ranks_donations_2 = pd.concat([names_donations, ranks_donations, counts_donations_2], axis=2)

# names 1~50 then others
ranks_donations_2['city_state_2'] = ranks_donations_2['city_state']
ranks_donations_2['city_state_2'][ranks_donations_2.city_state_rank > 50] = 'Other'

# ranks 1~50 then 0
ranks_donations_2['city_state_rank_2'] = ranks_donations_2['city_state_rank']
ranks_donations_2['city_state_rank_2'][ranks_donations_2['city_state_rank_2'] > 50] = 0


###### compared the top 50 city_states from donations table to those from projects table
pd.concat([pd.DataFrame(sorted(ranks_donations['city_state_rank_2'])),pd.DataFrame(sorted(ranks['city_state_cat']))], axis=1)

###### count number of donations for 50 top city_state with most projects
num_donations = pd.DataFrame(range(50), columns=['number of donations'])

col = donations['donor_city_state']

for i in range(0,49):
    num_donations['number of donations'][i] = int(col[col == ranks['city_state_cat'][i]].value_counts().values)

pd.concat([ranks['city_state_cat'],num_donations], axis=1)

