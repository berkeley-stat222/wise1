setwd("/Users/Lindsey/Documents/Spring_2015/stat222/project5/PreliminaryModeling")
library(aod)
library(ggplot2)
library(lattice)
library(maps)
library(mapdata)

#============================================================================
# Read and clean data
#============================================================================

### Read in the csv file
df <- read.csv("newestdata.csv")

### Remove rows that has empty value for grade level, resource type, and population
clean1 <- df[-which(df$resource_type==""), ]
clean1$resource_type <- factor(clean1$resource_type)
clean2 <- clean1[-which(clean1$grade_level==""), ]
clean2$grade_level <- factor(clean2$grade_level)
dfnew <- clean3 <- clean2[-which(is.na(clean2$pop)), ]

### Change column name for total_price_excluding_optional_support
colnames(dfnew) <- c(colnames(dfnew)[1:32], "total_price", colnames(dfnew)[34:62])


#============================================================================
# Plots and Tables
#============================================================================

### Figure 2: Distribution of days to project
hist(dfnew$days_to_completion, breaks = 100, xlim = range(1:250), 
     xlab='Days to Completion', main='Distribution of Days to Project Completion')

### Figure 3: Total number of projects and funding % by state 
dtstates <- xtabs(~school_state + funding_status, data=dfnew)
state.count <- apply(dtstates, 1, function(x) sum(x))
state.percent <- apply(dtstates, 1, function(x) x[1]/sum(x))
states <- data.frame(state=levels(dfnew$school_state), counts=state.count, 
                     funding_percent=state.percent)
plot(states$funding_percent, states$counts, col= "blue", pch = 19, cex = 1, 
     lty = "solid", lwd = 2,
     main= "Total Number of Projects and Funding % By State",
     xlab= "Funding %",
     ylab= "Total Number of Projects")
text(states$funding_percent, states$counts, labels=states$state, cex= 0.7, pos=3)


### Figure 4: Subjects request rate
subjects <- sort(table(dfnew$primary_focus_subject), decreasing=T)
dtsubjects <- data.frame(Subject=c(rownames(subjects)[1:7], "ect."), Counts=c(slices[1:7,1], ect))
rownames(dtsubjects) <- NULL

pie1 <- ggplot(dtsubjects, aes(x=1, y=Counts, fill=Subject)) +
  geom_bar(stat="identity") +
  ggtitle("Subjects Request Rate")
pie1 <- pie1 + coord_polar(theta='y') + theme(axis.ticks=element_blank(), 
                                              axis.title=element_blank(), 
                                              axis.text.y=element_blank())
y.breaks <- cumsum(dtsubjects$Count) - dtsubjects$Count/2
pie1 <- pie1 +
  # prettiness: make the labels black
  theme(axis.text.x=element_text(color='black')) +
  scale_y_continuous(
    breaks=y.breaks,   # where to place the labels
    labels=dtsubjects$Subject # the labels
  )


### Figure 5: Resource request rate
resources <- sort(table(dfnew$resource_type), decreasing=T)
dtresources <- data.frame(Resource_type=rownames(resources), Counts=resources)
rownames(dtresources) <- NULL

pie2 <- ggplot(dtresources, aes(x=1, y=Counts, fill=Resource_type)) +
  geom_bar(stat="identity") +
  ggtitle("Resources Request Rate")
pie2 <- pie2 + coord_polar(theta='y') + theme(axis.ticks=element_blank(), 
                                              axis.title=element_blank(), 
                                              axis.text.y=element_blank())
y.breaks <- cumsum(dtresources$Count) - dtresources$Count/2
pie2 <- pie2 +
  # prettiness: make the labels black
  theme(axis.text.x=element_text(color='black')) +
  scale_y_continuous(
    breaks=y.breaks,   # where to place the labels
    labels= c("Supplies","Technology","Books","Other","Trips","") # the labels
  )


### Table 2: Comparison of subjects requested and subjects funded
dtsubjects <- xtabs(~primary_focus_subject + funding_status, data=dfnew)
subjects.req <- subjects/sum(subjects)
subjects.comp <- sort(apply(dtsubjects, 1, function(x) x[1]/sum(x)), decreasing=T)


### Table 3: Comparison of resource type requested and % funded
resource.table <- xtabs(~funded_by_30 + resource_type, data = dfnew)
prop.table(resource.table, margin=2)


### Table 4: Funding % by poverty level and grade level
# For poverty level (indepentently)
poverty.table <- xtabs(~funded_by_30 + poverty_level, data = dfnew)
prop.table(poverty.table, margin=2)
# For grade level (indepentently)
grade.table <- xtabs(~funded_by_30 + grade_level, data = dfnew)
prop.table(grade.table, margin=2)

# Interactions between poverty level and grade level
pov_grade <- xtabs(~grade_level + poverty_level + funded_by_30, data=dfnew)
pov_grade_total <- c()
for (i in 1:16) {
  pov_grade_total[i] <- pov_grade[i] + pov_grade[i+16]
}
pov_grade_rate <- c()
for (i in 1:16) {
  pov_grade_rate[i] <- pov_grade[i+16]/pov_grade_total[i]
}
dt.pov_grade<-data.frame(poverty_level=c(rep(levels(dfnew$poverty_level)[1],4),
                                         rep(levels(dfnew$poverty_level)[2],4),
                                         rep(levels(dfnew$poverty_level)[3],4),
                                         rep(levels(dfnew$poverty_level)[4],4)),
                         grade_level=rep(levels(dfnew$grade_level), 4),
                         Num_of_projects=pov_grade_total,
                         funded_rate=pov_grade_rate)
View(dt.pov_grade)



### Figure 7: Days to completion by population
plot(dfnew$pop, dfnew$days_to_completion, cex=0.7, pch=19,
     lty="solid", lwd=2, col=rgb(1,0,0,0.1),
     main="Days to Completion by Population",
     ylab="Days", xlab="Population")


### Table 5: Summary statistic for total price
summary(dfnew$total_price)
# Min.  1st Qu.   Median     Mean  3rd Qu.     Max. 
#  0     272       418       570    617     10250000


### Figure 8: Days to completion by total price
# Total price less than 20,000
price20 <- dfnew[-which(dfnew$total_price>=20000), ]
plot(price20$total_price, price20$days_to_completion, cex=0.7, pch=19,
     lty="solid", lwd=2, col=rgb(0,0,1,0.1),
     main="Days to Completion by Total Price(less than 20,000)",
     ylab="Days", xlab="Total Price")

