getwd()
setwd('/Users/stephaniekim/Desktop/wise')
opendata_projects = read.csv("~/Desktop/wise/opendata_projects.csv")
#library(ggplot2)

###############################################################################
# number/ number of completed/ rate of completed of each subject
prim_subj = opendata_projects[,22]
uniq_subj = unique(prim_subj)
names_subj = as.matrix(uniq_subj[1:27])
num_subj = length(names)

prim_area = opendata_projects[,23]
uniq_area = unique(prim_area)[-8]
num_area = length(uniq_area)

status = opendata_projects[,40]
uniq_status = unique(status)

#
m1 = matrix(0,num_subj,3)

fun1 = function(data){
  for(i in 1:num_subj){
    subj = length(which(data[,22] == uniq_subj[i]))
    subj_comp = length(which(data[,22] == uniq_subj[i] & data[,40] == uniq_status[1]))
    rate = subj_comp/subj
    m1[i,] = c(subj,subj_comp,rate)
  }
  return(m1)
}

m1 = fun1(data=opendata_projects)

rownames(m1) = names_subj
colnames(m1) = c('# of projects', '# of completed projects', 'rate of completeness')
View(m1)

# order by most famous subject
m1_subj = m1[,1]
m1_subj = m1_subj[order(m1_subj,decreasing=T)]
m1_subj_portion = m1_subj/sum(m1_subj)

m1_pie = as.matrix(c(m1_subj[1:7],sum(m1_subj[8:27])))
m1_subj_names = c(rownames(as.matrix(m1_subj_portion[1:7])),"etc.")

slices = as.data.frame(m1_pie)
lbls =  m1_subj_names
pie(slices, labels = lbls, main="Subjects that need funding", clockwise=T, col=rainbow(8))

subject = data.frame(Subject=c("Literacy","Mathematics","Literature & Writing","Special Needs","Applied Sciences","Visual Arts","Environmental Science","etc."),Counts=c(slices))
colnames(subject) = c("Subject", "Count")
subject

p <- ggplot(subject, aes(x=1, y=Count, fill=Subject)) +
  geom_bar(stat="identity") +
  ggtitle("Subjects that need funding")
p <- p + coord_polar(theta='y')
p <- p +
  theme(axis.ticks=element_blank(), 
        axis.title=element_blank(), 
        axis.text.y=element_blank())
y.breaks <- cumsum(subject$Count) - subject$Count/2
p <- p +
  # prettiness: make the labels black
  theme(axis.text.x=element_text(color='black')) +
  scale_y_continuous(
    breaks=y.breaks,   # where to place the labels
    labels=subject$Subject # the labels
  )


# order by highest completion rate
m1_compl = m1[,3]
m1_compl = m1_compl[order(m1_compl,decreasing=T)]
View(m1_compl)

###############################################################################
# resource type
resource = opendata_projects[,26]
uniq_resource = unique(resource)[-7]
num_resource = length(uniq_resource)
r1= length(which(opendata_projects[,26] == uniq_resource[1])) #Books
r2= length(which(opendata_projects[,26] == uniq_resource[2])) #Technology
r3= length(which(opendata_projects[,26] == uniq_resource[3])) #Trips
r4= length(which(opendata_projects[,26] == uniq_resource[4])) #Visitors
r5= length(which(opendata_projects[,26] == uniq_resource[5])) #Other
r6= length(which(opendata_projects[,26] == uniq_resource[6])) #Supplies
m2 = matrix(c(r1,r2,r3,r4,r5,r6))
m2 = m2[order(m2,decreasing=T)]

resource = data.frame(Resources=c("Supplies","Technology","Books","Other","Trips","Visitors"),Count=c(m2))

p <- ggplot(resource, aes(x=1, y=Count, fill=Resources)) +
  geom_bar(stat="identity") +
  ggtitle("Resources request rate")
p <- p + coord_polar(theta='y')
p <- p +
  theme(axis.ticks=element_blank(), 
        axis.title=element_blank(), 
        axis.text.y=element_blank())
y.breaks <- cumsum(resource$Count) - resource$Count/2
p <- p +
  # prettiness: make the labels black
  theme(axis.text.x=element_text(color='black')) +
  scale_y_continuous(
    breaks=y.breaks,   # where to place the labels
    labels= c("Supplies","Technology","Books","Other","Trips","")# the labels
  )
p
