library(tidyverse)
library(zoo)

nors = read.csv("NORS.csv", header=TRUE) %>%
  select(-tail(names(.), 5)) %>%
  mutate(Date = as.yearmon(paste(.$Year, .$Month), "%Y %m")) %>%
  na.omit() %>%
  separate_wider_delim(Etiology, delim=";", too_few="align_start", too_many="drop",
                       names=c("Etiology1", "Etiology2", "Etiology3", "Etiology4",
                               "Etiology5", "Etiology6")) %>%
  separate_wider_delim(Etiology.Status, delim=";", too_few="align_start", too_many="drop",
                       names=c("Status1", "Status2", "Status3", "Status4",
                               "Status5", "Status6")) %>%
  filter(if_any(c(Etiology1, Etiology2, Etiology3, Etiology4, Etiology5, Etiology6), 
                ~ grepl("Norovirus", ., fixed=TRUE))) %>%
  filter(if_any(c(Status1, Status2, Status3, Status4, Status5, Status5), 
                ~ .=="Confirmed"))

# nors$Date = as.Date(paste(nors$Year, nors$Month, "01", sep = "-"))

write.csv(nors, "NORS_cleaned.csv", row.names=FALSE)

