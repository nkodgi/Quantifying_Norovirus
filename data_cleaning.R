library(tidyverse)

nors = read.csv("NORS.csv", header=TRUE) %>%
  select(-tail(names(.), 5)) %>%
  na.omit() %>%
  separate_wider_delim(Etiology, delim=";", too_few="align_start", too_many="drop",
                       names=c("Etiology1", "Etiology2", "Etiology3", "Etiology4",
                               "Etiology5", "Etiology6")) %>%
  separate_wider_delim(Etiology.Status, delim=";", too_few="align_start", too_many="drop",
                       names=c("Status1", "Status2", "Status3", "Status4",
                               "Status5", "Status6"))

tab = data.frame(table(nors$Serotype.or.Genotype))
counts = data.frame(str_count(nors$Serotype.or.Genotype, ";"))

write.csv(nors, "NORS_cleaned.csv")
