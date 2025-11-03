library(tidyverse)
library(zoo)

settings_to_omit = c("Unknown", "Private home/residence", NA)
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
  separate_wider_delim(Setting, delim=";", too_few="align_start", too_many="drop",
                       names=c("Setting1", "Setting2", "Setting3", "Setting4",
                               "Setting5", "Setting6")) %>%
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
         Confirmed6 = ifelse(grepl("Confirmed", .$Status6), 1, 0),
         Set1 = ifelse(.$Setting1 %in% settings_to_omit, 0, 1),
         Set2 = ifelse(.$Setting2 %in% settings_to_omit, 0, 1),
         Set3 = ifelse(.$Setting3 %in% settings_to_omit, 0, 1),
         Set4 = ifelse(.$Setting4 %in% settings_to_omit, 0, 1),
         Set5 = ifelse(.$Setting5 %in% settings_to_omit, 0, 1),
         Set6 = ifelse(.$Setting6 %in% settings_to_omit, 0, 1)) %>%
  filter(Noro1*Confirmed1*Set1==1 | Noro2*Confirmed2*Set2==1 |
           Noro3*Confirmed3*Set3==1 | Noro4*Confirmed4*Set4==1 |
           Noro5*Confirmed5*Set5==1 | Noro6*Confirmed6*Set6==1) %>%
  select(-tail(names(.), 18))

write.csv(nors, "NORS_cleaned.csv", row.names=FALSE)

