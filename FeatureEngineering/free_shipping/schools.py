projects = pd.read_csv('/Users/stephaniekim/Desktop/wise/ipython/projects_modified.csv')


# city_state column
projects['school_city_state'] = projects['school_city'] + ', ' + projects['school_state']


# ordered number of projects for each city_state
counts_school = projects['school_city_state'].value_counts()
# just counts
counts_school_2 = pd.DataFrame(counts_school.values, columns=['counts'])
# just names
names_school = pd.DataFrame(counts_school.index, columns = ['city_state'])


# rank 1~length
ranks_school = pd.DataFrame([x+1 for x in range(counts_school.shape[0])], columns = ['city_state_rank'])


# concat
ranks_school_2 = pd.concat([names_school, ranks_school, counts_school_2], axis=2)


# names 1~50 then others
ranks_school_2['city_state_2'] = ranks_school_2['city_state']
ranks_school_2['city_state_2'][ranks_school_2.city_state_rank > 50] = 'Other'

# ranks 1~50 then 0
ranks_school_2['city_state_rank_2'] = ranks_school_2['city_state_rank']
ranks_school_2['city_state_rank_2'][ranks_school_2['city_state_rank_2'] > 50] = 0

