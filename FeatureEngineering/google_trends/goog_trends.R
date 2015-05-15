#goog = read.csv('~/Dropbox/Berkeley/Second_Sem/222_Capstone/goog_trends.csv', skip=4, col.names = c("Week", "Google_query"))
goog$year = substr(goog$Week,1,4)
goog$week_of_yr = c(rep(1:52, 2), 1:53, rep(1:52, 7), 1:53, rep(1:52, 100))[1:nrow(goog)]
goog$year_week = paste(goog$year, goog$week_of_yr)
#write.csv(goog[,c(2,5)], file='google_queries.csv', row.names=FALSE)
