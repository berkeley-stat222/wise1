###### 50 level donations city_state

donations = pd.read_csv('/Users/stephaniekim/Desktop/wise/ipython/opendata_donations.csv')


# city_state column
donations['donor_city_state'] = donations['donor_city'] + ', ' + donations['donor_state']


# ordered number of donations for each city_state
counts_donations = donations['donor_city_state'].value_counts()
# just counts
counts_donations_2 = pd.DataFrame(counts_donations.values, columns=['donor_counts'])
# just names
names_donations = pd.DataFrame(counts_donations.index, columns = ['city_state'])


# rank 1~length
# ranks_donations = pd.DataFrame([x+1 for x in range(counts_donations.shape[0])], columns = ['city_state_rank'])

# concat
# ranks_donations_2 = pd.concat([names_donations, ranks_donations, counts_donations_2], axis=2)

# names 1~50 then others
# ranks_donations_2['city_state_2'] = ranks_donations_2['city_state']
# ranks_donations_2['city_state_2'][ranks_donations_2.city_state_rank > 50] = 'Other'

# ranks 1~50 then 0
# ranks_donations_2['city_state_rank_2'] = ranks_donations_2['city_state_rank']
# ranks_donations_2['city_state_rank_2'][ranks_donations_2['city_state_rank_2'] > 50] = 0

ranks_donations_3 = pd.concat([names_donations, counts_donations_2], axis=1)

donor_counts.to_csv('/Users/stephaniekim/Desktop/Files/donation_counts.csv',index=False)