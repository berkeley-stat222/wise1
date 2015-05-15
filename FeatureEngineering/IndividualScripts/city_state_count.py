max_count = max(counts)

counts_cut = counts

counts_cut[(counts_cut>=1) & (counts_cut<=10)] = 1

counts_cut[(counts_cut>10) & (counts_cut<=50)] = 2

counts_cut[(counts_cut>50) & (counts_cut<=100)] = 3

counts_cut[(counts_cut>100) & (counts_cut<=200)] = 4

counts_cut[(counts_cut>200) & (counts_cut<=500)] = 5

counts_cut[(counts_cut>500) & (counts_cut<=max_count)] = 6

cut = pd.DataFrame(counts_cut.values, columns = ['city_state_counts'])