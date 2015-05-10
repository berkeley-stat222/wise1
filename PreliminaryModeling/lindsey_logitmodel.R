setwd("/Users/Lindsey/Documents/Spring_2015/stat222/project5/PreliminaryModeling")
library(aod)
library(ggplot2)
library(lattice)


#============================================================================
# Logit model 
#============================================================================

### 1. funded_by_30 ~ poverty_level, pop_y, total_price
logit1 <- glm(funded_by_30 ~ poverty_level + pop_y + total_price, data = dfnew, family = "binomial")
summary(logit1)
data1 <- with(dfnew, data.frame(pop_y=mean(pop_y), total_price=mean(total_price), 
                                poverty_level = factor(levels(poverty_level))))
# Make a new data to predict
data1.2 <- with(dfnew, data.frame(total_price=rep(seq(from=0, to=4000, length.out=100), 4),
                                  pop_y=mean(pop_y),
                                  poverty_level=factor(rep(levels(poverty_level), each=100))))
# Predict the probability      
data1.3 <- cbind(data1.2, predict(logit1, newdata=data1.2, type="link", se=TRUE))
# Add 95% confidence interval to the predicted probability
data1.3 <- within(data1.3, {PredictedProb <- plogis(fit)
                            LL <- plogis(fit - (1.96 * se.fit))
                            UL <- plogis(fit + (1.96 * se.fit))
})
# view first few rows of final dataset
head(data1.3)
# Make a plot         
logit1.plot <- ggplot(data1.3, aes(x = total_price, y = PredictedProb)) + 
  geom_ribbon(aes(ymin = LL, ymax = UL, fill = poverty_level), alpha = 0.2) + 
  geom_line(aes(colour = poverty_level),size = 1)
logit1.plot + labs(title="Predicted Probability for Different Poverty Levels", 
                   x="Total Price", y="Predicted Probability")


### 2. funded_by_30 ~ grade_level, pop_y, total_price
logit2 <- glm(funded_by_30 ~ grade_level + pop_y + total_price, data = dfnew, family = "binomial")
summary(logit2)
data2 <- with(dfnew, data.frame(pop_y=mean(pop_y), total_price=mean(total_price), 
                                grade_level = factor(levels(grade_level))))
# Make a new data to predict
data2.2 <- with(dfnew, data.frame(pop_y=rep(seq(from=0, to=130000, length.out=100), 4),
                                  total_price=mean(total_price),
                                  grade_level=factor(rep(levels(grade_level), each=100))))
# Predict the probability      
data2.3 <- cbind(data2.2, predict(logit2, newdata=data2.2, type="link", se=TRUE))
# Add 95% confidence interval to the predicted probability
data2.3 <- within(data2.3, {PredictedProb <- plogis(fit)
                            LL <- plogis(fit - (1.96 * se.fit))
                            UL <- plogis(fit + (1.96 * se.fit))
})
# view first few rows of final dataset
head(data2.3)
# Make a plot         
logit2.plot <- ggplot(data2.3, aes(x = pop_y, y = PredictedProb)) + 
  geom_ribbon(aes(ymin = LL, ymax = UL, fill = grade_level), alpha = 0.2) + 
  geom_line(aes(colour = grade_level),size = 1)
logit2.plot + labs(title="Predicted Probability for Different Grade Levels", 
                   x="Population", y="Predicted Probability")


### 3. funded_by_30 ~ resource_type, pop_y, total_price
logit3 <- glm(funded_by_30 ~ resource_type + pop_y + total_price, data = dfnew, family = "binomial")
summary(logit3)
data3 <- with(dfnew, data.frame(pop_y=mean(pop_y), total_price=mean(total_price), 
                                resource_type = factor(levels(resource_type))))
# Make a new data to predict
data3.2 <- with(dfnew, data.frame(total_price=rep(seq(from=0, to=4000, length.out=100), 6),
                                  pop_y=mean(pop_y),
                                  resource_type=factor(rep(levels(resource_type), 100))))
# Predict the probability      
data3.3 <- cbind(data3.2, predict(logit3, newdata=data3.2, type="link", se=TRUE))
# Add 95% confidence interval to the predicted probability
data3.3 <- within(data3.3, {PredictedProb <- plogis(fit)
                            LL <- plogis(fit - (1.96 * se.fit))
                            UL <- plogis(fit + (1.96 * se.fit))
})
# view first few rows of final dataset
head(data3.3)
# Make a plot         
logit3.plot <- ggplot(data3.3, aes(x = total_price, y = PredictedProb)) + 
  geom_ribbon(aes(ymin = LL, ymax = UL, fill = resource_type), alpha = 0.2) + 
  geom_line(aes(colour = resource_type),size = 1)
logit3.plot + labs(title="Predicted Probability for Different Resource Types", 
                   x="Total Price", y="Predicted Probability")

