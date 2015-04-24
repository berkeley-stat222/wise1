dat = read.csv('ACS_13_5YR_B19013_with_ann.csv', skip=2, header=FALSE, stringsAsFactors=FALSE)
# BRI SENT THIS DATA

names(dat) = c("GEO.id", "GEO.id2", "zip_disp", "med_inc", "margin_err")
dat$med_inc[which(!str_detect(dat$med_inc, "^[0-9]"))] = NA
dat$margin_err[which(!str_detect(dat$margin_err, "^[0-9]"))] = NA
dat$med_inc = str_replace_all(dat$med_inc, "(\\+)|-|,", "")
dat$med_inc = as.numeric(dat$med_inc)
dat$margin_err = as.numeric(dat$margin_err)
dat$zip = unlist(strsplit(dat$zip_disp, " "))[seq(2,nrow(dat)*2,by=2)]
write.csv(dat[,c(4,6)], file = "medInc_byZip.csv", row.names=FALSE)
