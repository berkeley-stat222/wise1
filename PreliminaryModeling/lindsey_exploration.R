setwd("/Users/Lindsey/Documents/Spring_2015/stat222/project5/PreliminaryModeling")
library(aod)
library(ggplot2)
library(lattice)

#============================================================================
# Read and clean data
#============================================================================

### Read the data
df <- read.table("projects_prelim_data.csv", header=T, sep=",", fill = TRUE)

### Remove rows that has empty value for grade level, resource type, and population
clean1 <- df[-which(df$resource_type==""), ]
clean1$resource_type <- factor(clean1$resource_type)
clean2 <- clean1[-which(clean1$grade_level==""), ]
clean2$grade_level <- factor(clean2$grade_level)
dfnew <- clean3 <- clean2[-which(is.na(clean2$pop_y)), ]

### Change column name for total_price_excluding_optional_support
colnames(dfnew) <- c(colnames(dfnew)[1:33], "total_price", colnames(dfnew)[35:61])


#============================================================================
# Plot for the number of Yes/No for fundedn_by_30 variable
#============================================================================

### For poverty level
poverty.table <- xtabs(~funded_by_30 + poverty_level, data = dfnew)
poverty.table1 <- as.matrix(data.frame(poverty.table[,3], poverty.table[,4], poverty.table[,1], poverty.table[,2]))
colnames(poverty.table1) <- c("low poverty", "moderate poverty", "high poverty", "highest poverty")
barplot(poverty.table1, main=("Number of Projects Funded within 30 days by Poverty Level"), 
        col = c("rosybrown1", "palegoldenrod"), width=2, beside = TRUE)
legend("topleft", fill = c("rosybrown1", "palegoldenrod"), legend = c("No", "Yes"))
#quartz()
#dev.off()

### For grade level
grade.table <- xtabs(~funded_by_30 + grade_level, data = dfnew)
grade.table1 <- as.matrix(data.frame(grade.table[,4], grade.table[,1], grade.table[,2], grade.table[,3]))
colnames(grade.table1) <- c("Grades PreK-2", "Grades 3-5", "Grades 6-8", "Grades 9-12")
barplot(grade.table1, main=("Number of Projects Funded within 30 days by Grade Level"), 
        col = c("thistle2", "powderblue"), width = 2, beside = TRUE)
legend("topright", fill = c("thistle2", "powderblue"), legend = c("No", "Yes"))

### For resource type
resource.table <- xtabs(~funded_by_30 + resource_type, data = dfnew)
resource.table1 <- as.matrix(data.frame(resource.table[,-2], resource.table[,2]))
colnames(resource.table1) <- c(colnames(resource.table1)[-6], "Others")
barplot(resource.table1, main=("Number of Projects Funded in 30 days by Resource Type"), 
        col = c("mistyrose2", "mistyrose4"), width = 2, beside = TRUE)
legend("topright", fill = c("mistyrose2", "mistyrose4"), legend = c("No", "Yes"))

### For population
pop.yes <- dfnew[which(dfnew$funded_by_30=="Yes"),]$pop_y
pop.no <- dfnew[which(dfnew$funded_by_30=="No"),]$pop_y
boxplot(pop.yes, pop.no, names=c("Yes", "No"), col=c(rgb(1,1,0,0.2), rgb(0,1,0,0.2)),
        ylab="Polulation", xlab="Funding Status", main="Distribution of Poplulation by Funding Status")

### For total price(excluding optional support)
# summary(dfnew$total_price)
# Min.  1st Qu.   Median     Mean  3rd Qu.     Max. 
# 0      255      400      592      582    10250000

# total price less than 2,000
dfnew.out <- dfnew[-which(dfnew$total_price>=2000), ]
total_price.yes <- dfnew.out[which(dfnew.out$funded_by_30=="Yes"),]$total_price
total_price.no <- dfnew.out[which(dfnew.out$funded_by_30=="No"),]$total_price
boxplot(total_price.yes, total_price.no, names=c("Yes", "No"), col=c(rgb(1,0,0,0.2), rgb(0,0,1,0.2)),
        ylab="Total Price", xlab="Funding Status", 
        main="Distribution of Total Price Requested (less than $2,000) \nby Funding Status")
# total price less than 20,000
dfnew.out <- dfnew[-which(dfnew$total_price>=20000), ]
total_price.yes <- dfnew.out[which(dfnew.out$funded_by_30=="Yes"),]$total_price
total_price.no <- dfnew.out[which(dfnew.out$funded_by_30=="No"),]$total_price
boxplot(total_price.yes, total_price.no, names=c("Yes", "No"), col=c(rgb(1,0,0,0.2), rgb(0,0,1,0.2)),
        ylab="Total Price", xlab="Funding Status", 
        main="Distribution of Total Price Requested (less than $20,000) \nby Funding Status")

