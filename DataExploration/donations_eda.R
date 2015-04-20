##### Subset in bash for quick look #####
#shuf -n 300000 opendata_donations.csv > dsample.csv
#head -1 opendata_donations.csv > dheader.csv
#cat dheader.csv dsample.csv > dsamplehead.csv
#########################################

library(dplyr)
library(ggplot2)
#setwd("C:/Users/rrruss/Desktop/stat222/wise")


donations <- read.csv("opendata_donations.csv", stringsAsFactors=FALSE)
# The fields donation_to_project, donation_optional_support and
# donation_total are not in the documentation. I will ignore them.

# Reminder to self: when dealing with the ID fields, escape the " with \ or use '

# Proportion of donations from teachers
table(donations$is_teacher_acct)
# small dataset: 16%
###
sum(donations$is_teacher_acct=="t")
sum(donations$is_teacher_acct=="f")
###

# Proportion of donations made via a giving page
table(donations$via_giving_page)
# small dataset: 62%
###
sum(donations$via_giving_page=="t")
sum(donations$via_giving_page=="f")
# the last 2 lines match the result in table() but still don't sum
# to the total number of lines
###

# Proportion of donations including an honoree
table(donations$for_honoree)
# small dataset: 2.2%



donate.dat <- donations %>%
  mutate(projectid=factor(X_projectid),
         donorid=factor(X_donor_acctid),
         cartid=factor(X_cartid),
         isteacher=ifelse(is_teacher_acct=="t", "Yes", "No"),
         dollar=factor(dollar_amount),
         method=factor(payment_method),
         givingpage=ifelse(via_giving_page=="t", "Yes", "No"),
         honoree=ifelse(for_honoree=="t", "Yes", "No")) %>%
  select(projectid, donorid, cartid, isteacher, dollar, method, givingpage,
         honoree, donor_city, donor_state)


donate.dat %>% select(projectid) %>% distinct() %>% nrow()
donate.dat %>% select(donorid) %>% distinct() %>% nrow()
donate.dat %>% select(cartid) %>% distinct() %>% nrow()
donate.dat %>%
  group_by(cartid) %>%
  summarise(count=n()) %>%
  arrange(desc(count))
donate.dat %>%
  group_by(cartid) %>%
  summarise(count=n()) %>%
  group_by(count) %>%
  summarise(num=n()) %>%
  arrange(desc(num))

donate.dat %>%
  group_by(donorid) %>%
  summarise(num=n()) %>%
  group_by(num) %>%
  summarise(count=n()) %>%
  arrange(desc(count))
# most people only donate once or twice

donate.dat %>%
  group_by(donorid) %>%
  summarise(num=n()) %>%
  arrange(desc(num)) %>%
  slice(1:20)
# some donors donate thousands of times
# highest is 59576 times (for whole dataset) or 7179 times for the small dataset 
# donorid for that guy is "e0dd67c660dc50ec1b2dadf37f3c65d4"
# investigate:
donations %>%
  filter(X_donor_acctid == "\"e0dd67c660dc50ec1b2dadf37f3c65d4\"") %>%
  group_by(payment_method) %>%
  summarise(n())
# promo_code_match is not documented
# Yellow Chair Foundation appears in some of the donation messages
# so it looks like some kind of matching donation from them
donate.often <- donate.dat %>%
  group_by(donorid) %>%
  summarise(num=n()) %>%
  arrange(desc(num)) %>%
  slice(1:20)

donate.dat %>%
  filter(donorid %in% donate.often$donorid) %>%
  group_by(dollar) %>%
  summarise(n())


donate.dat %>%
  group_by(donor_state) %>%
  summarise(count=n()) %>%
  arrange(desc(count))
# not surprisingly, states with the largest populations,
# CA, NY, IL have the most donors

jpeg("isteacher.jpg")
donate.dat %>% 
  group_by(isteacher, dollar) %>%
  summarise(count=n()) %>%
  ggplot(aes(x=dollar, y=count, fill=isteacher)) +
  geom_bar(stat="identity", position="dodge") +
  labs(title="Distribution of donation amounts according to whether
       the donation was made by a teacher",
       x="Donation amount", y="Count")
dev.off()

jpeg("giving.jpg")
donate.dat %>%
  group_by(givingpage, dollar) %>%
  summarise(count=n()) %>%
  ggplot(aes(x=dollar, y=count, fill=givingpage)) +
  geom_bar(stat="identity", position="dodge") +
  labs(title="Distribution of donation amounts according to whether
       the donation was made from a giving page",
       x="Donation amount", y="Count")
dev.off()

jpeg("dollaramounts.jpg")
donate.dat %>%
  group_by(dollar) %>%
  summarise(count=n()) %>%
  ggplot(aes(x=dollar, y=count)) +
  geom_bar(stat="identity") +
  labs(title="Distribution of donation amounts", x="Donation amount",
       y="Count")
dev.off()


jpeg("honoree.jpg")
donate.dat %>% 
  group_by(honoree, dollar) %>%
  summarise(count=n()) %>%
  ggplot(aes(x=dollar, y=count, fill=honoree)) +
  geom_bar(stat="identity", position="dodge")
dev.off()
# can't see distribution of for_honoree=="f" properly
# just look at the numbers without the plot