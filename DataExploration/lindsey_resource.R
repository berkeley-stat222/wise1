setwd("/Users/Lindsey/Documents/Spring_2015/stat222/project5/data")
rm(list=ls())
gc()

resources <- read.csv("opendata_resources.csv", header=T, stringsAsFactors=F)
summary(resources)

###
item_name         item_number        item_unit_price     item_quantity     
Length:4365548     Length:4365548     Min.   :     -100   Min.   :     0.0  
Class :character   Class :character   1st Qu.:        6   1st Qu.:     1.0  
Mode  :character   Mode  :character   Median :       14   Median :     1.0  
Mean   :      160   Mean   :     3.2  
3rd Qu.:       36   3rd Qu.:     2.0  
Max.   :448421569   Max.   :993108.0  
NA's   :14911       NA's   :9326    


sum(!duplicated(resources$X_projectid))
# 771604
sum(!duplicated(resources$project_resource_type))
table(resources$project_resource_type)
# Books / Other / Supplies / Technology / Trips / Visitors

total_price <- with(resources, item_unit_price * item_quantity)



### item_unit_price
price <- resources$item_unit_price
price1 <- price[which(is.na(resources$item_unit_price) == F) ] 

### item_unit_price < 0
resources$item_unit_price[resources$item_unit_price < 0 & is.na(resources$item_unit_price) == F]
[1] -26.05 -99.60 -22.00 -55.90 -39.60 -83.00  -5.49 -22.00  -2.05 -15.00 -63.43

a1 <- resources[resources$item_unit_price < 0 & is.na(resources$item_unit_price) == F, ]


### box plot of prices for the different type of resources
re_type <- as.factor(resources$project_resource_type)
dat1 <- data.frame(re_type, price)

boxplot(price~re_type,data=dat1)
# have couple of huge outliers so that we can't compare other box plots with this.

# extract only numeric values (remove NA values)
price_noNA <- price[is.na(price)==F]

# remove the outlier from the original data
which(grepl(max(price_noNA), resources$item_unit_price))
3124715
re_noOutlier <- resources[-3124715, ]

sort_price <- sort(price_noNA, decreasing=T)


re_type <- as.factor(re_noOutlier$project_resource_type)
dat2 <- data.frame(re_type, price=re_noOutlier$item_unit_price)
# box plot without outlier
boxplot(price~re_type, data=dat2)


### Summary statistic of item quantity
quantity <- resources$item_quantity
summary(quantity)

### histogram of item quantity (quantity less than 20)
quantity <- quantity[is.na(quantity)==F]
q1_20 <- quantity[quantity<=20]
hist(q1_20, main="Histogram of Item Quantity (Quantity < 20)", xlab="Item Quantity",
     ylab="count", col="lavender")

### histogram of item quantity (quantity less than 500)
q21_500 <- quantity[20<quantity & quantity<=500]
hist(q21_500, main="Histogram of Item Quantity (20 < Quantity < 500)", xlab="Item Quantity",
     ylab="count", col="mistyrose")
