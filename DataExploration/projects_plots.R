library(data.table)
library(ggplot2)

# Read in csv files created in Python
funded <- read.csv("~/Documents/School/Spring2015/STAT222/FinalProject/funded.csv")
states <- read.csv("~/Downloads/states (1).csv")
opendata_projects <- read.csv("~/Downloads/opendata_projects.csv")

# Convert dataframes to data tables
dtfunded <- data.table(funded)
dtstates <- data.table(states)
dtopen <- data.table(opendata_projects)


mean_days_comp <- dtfunded[,list(mean_days=mean(days_to_completion)),by=school_state]
sorted_days <- mean_days_comp[order(mean_days), , drop = FALSE]

one_day_or_less <- subset(dtfunded, days_to_completion %in% 0:1)
two_to_7days <- subset(dtfunded, days_to_completion %in% 2:7)
eight_to_14days <- subset(dtfunded, days_to_completion %in% 8:14)
fifteen_to_30days <- subset(dtfunded, days_to_completion %in% 15:30)

# plots
# State funding percentages
q <- ggplot(dtstates, aes(X, funding_percent)) + geom_point(aes(size = counts))
q <- q + labs(x = 'State', y = 'Funding %') + 
     theme(axis.ticks = element_blank(), axis.text.x = element_blank(), legend.position = 'none')
q

# Days to completion (includes only fully funded projects)
hist(dtfunded$days_to_completion, breaks = 100, xlim = range(1:250), xlab = 'Days to Completion', main = 'Distribution of Days to Project Completion')

# Poverty level and days to completion
p <- ggplot(dtfunded, aes(days_to_completion, poverty_level)) + geom_point((aes(size = total_price_excluding_optional_support, color = factor(poverty_level))))
p <- p + labs(title="Poverty Level and Days to Completion", x="Days", y="Poverty Level")
p <- p + theme(legend.position = 'none')
p
