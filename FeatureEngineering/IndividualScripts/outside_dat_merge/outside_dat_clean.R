################
### MED INC  ###
################
# read in original data, found by Bri
# inc = read.csv('ACS_13_5YR_B19013_with_ann.csv', skip=2, header=FALSE, stringsAsFactors=FALSE)
library('stringr')
names(inc) = c("GEO.id", "GEO.id2", "zip_disp", "med_inc", "margin_err")
inc$med_inc[which(!str_detect(inc$med_inc, "^[0-9]"))] = NA
inc$margin_err[which(!str_detect(inc$margin_err, "^[0-9]"))] = NA
inc$med_inc = str_replace_all(inc$med_inc, "(\\+)|-|,", "")
inc$med_inc = as.numeric(inc$med_inc)
inc$margin_err = as.numeric(inc$margin_err)
inc$zip = unlist(strsplit(inc$zip_disp, " "))[seq(2,nrow(inc)*2,by=2)]
inc_fin = inc[,c(4,6)]

################
### POP SIZE ###
################

# pop = read.csv('2010_pop_by_zip.csv', colClasses=c('character', 'numeric'), stringsAsFactors=FALSE)
names(pop) = c("zip", "pop")
pop[,1][nchar(pop[,1])==4] <- paste('0', pop[,1][nchar(pop[,1])==4], sep="")
t = !duplicated(pop$zip)
pop = subset(pop, t)
#head(pop)

##########################
### POLIT. AFFILIATION ###
##########################

# codes = read.csv("national_cd113.csv", colClasses='character')
codes2 = subset(codes[,1:2],!duplicated(codes$STATE))
# dist = read.csv('natl_zccd_delim.csv', skip=1, header=TRUE, colClasses='character', stringsAsFactors=FALSE)
dist_zip = merge(codes2, dist, by.x='STATEFP', by.y = 'State', all.y=TRUE, all.x=FALSE)
loc = merge(dist_zip, cbind(state.name, state.abb), by.x="STATE", by.y="state.abb")
loc$District = paste(loc$state.name, as.numeric(loc$Congressional.District))

library(XML)
url <- "http://en.wikipedia.org/wiki/Current_members_of_the_United_States_House_of_Representatives"
tables <- readHTMLTable(url)
n.rows <- unlist(lapply(tables, function(t) dim(t)[1]))
wiki_tab = tables[[which.max(n.rows)]]
wiki_tab = wiki_tab[,c(2,5)]
wiki_tab[,1] = as.character(wiki_tab[,1])
wiki_tab$state.name = sapply(strsplit(x = wiki_tab[,1], split=" "), "[[",1)
wiki_tab$Party = as.character(wiki_tab$Party)
wiki_tab$Party[wiki_tab$Party == '-' | wiki_tab$Party == 'DFL'] <- 'z.other'
house_affil = merge(wiki_tab, cbind(state.name, state.abb), by="state.name", all.x=TRUE)

pol = merge(loc, house_affil[,2:3], by = 'District', all.x=TRUE)
names(pol)[4] = "zip"
pol_sub = pol[,c(4,7)]

# deal with duplicate zip codes
sub = pol_sub[duplicated(pol_sub$zip) | duplicated(pol_sub$zip, fromLast=TRUE),]
dups = aggregate(as.numeric(as.factor(Party)) ~ zip, data=sub[order(sub$zip),][sub$Party!="z.other",], FUN=mean)
dups$Party[dups[,2] == 1.5] = "Bipartisan"
dups$Party[dups[,2] < 1.5] = "Democratic"
dups$Party[dups[,2]  > 1.5] = "Republican"

pol_fin = merge(pol_sub, dups[,c(1,3)], by="zip", all.x=TRUE)
pol_fin$Party.x[!is.na(pol_fin$Party.y)] = pol_fin$Party.y[!is.na(pol_fin$Party.y)]
pol_fin = pol_fin[,1:2]
names(pol_fin)[2] = 'party'

pol_fin = subset(pol_fin, !duplicated(pol_fin$zip))

##############################
### MERGE ALL OUTSIDE DATA ###
##############################

merge1 = merge(inc_fin, pop, by='zip', all = TRUE)
all_dat = merge(merge1, pol_fin, by='zip', all=TRUE)
# write.csv(all_dat, file = "outside_dat.csv", row.names=FALSE)

