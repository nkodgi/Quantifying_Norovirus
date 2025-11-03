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
  mutate(Noro1 = ifelse(grepl("Norovirus", .$Etiology1), 1, 0),
         Noro2 = ifelse(grepl("Norovirus", .$Etiology2), 1, 0),
         Noro3 = ifelse(grepl("Norovirus", .$Etiology3), 1, 0),
         Noro4 = ifelse(grepl("Norovirus", .$Etiology4), 1, 0),
         Noro5 = ifelse(grepl("Norovirus", .$Etiology5), 1, 0),
         Noro6 = ifelse(grepl("Norovirus", .$Etiology6), 1, 0),
         Confirmed1 = ifelse(grepl("Confirmed", .$Status1), 1, 0),
         Confirmed2 = ifelse(grepl("Confirmed", .$Status2), 1, 0),
         Confirmed3 = ifelse(grepl("Confirmed", .$Status3), 1, 0),
         Confirmed4 = ifelse(grepl("Confirmed", .$Status4), 1, 0),
         Confirmed5 = ifelse(grepl("Confirmed", .$Status5), 1, 0),
         Confirmed6 = ifelse(grepl("Confirmed", .$Status6), 1, 0)) %>%
  filter(Noro1*Confirmed1==1 | Noro2*Confirmed2==1 | Noro3*Confirmed3==1 |
           Noro4*Confirmed4==1 | Noro5*Confirmed5==1 | Noro6*Confirmed6==1) %>%
  select(-tail(names(.), 12))

write.csv(nors, "NORS_cleaned.csv", row.names=FALSE)

