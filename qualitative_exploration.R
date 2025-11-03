library(tidyverse)

nors = read.csv("NORS_cleaned.csv", header=TRUE)
nors$Date = as.Date(paste(nors$Year, nors$Month, "01", sep = "-"))

# Count of Illnesses and Outbreaks plotted by month and year
ill_by_date = group_by(nors, Date) %>% summarise(Illnesses = sum(Illnesses),
                                                 Outbreaks = n())
ill_by_date$Outbreaks_rescaled = ill_by_date$Outbreaks * max(ill_by_date$Illnesses) / max(ill_by_date$Outbreaks)

ggplot(ill_by_date, aes(x = Date, color=color)) + 
  geom_line(aes(y = Illnesses, color = "Illnesses"), color="steelblue", linewidth = 1) +
  geom_point(aes(y = Illnesses, color = "Illnesses"), color="darkred", size = 1.5) +
  geom_line(aes(y=Outbreaks_rescaled, color = "Outbreaks"), color="black",
            linewidth = 0.5, linetype="dashed") +
  geom_point(aes(y = Outbreaks_rescaled, color = "Outbreaks"), color="grey", size = 1) +
  scale_x_date(date_labels = "%b %Y", date_breaks = "1 year") +
  scale_y_continuous(
    name="Illnesses",
    sec.axis = sec_axis(~.*max(ill_by_date$Outbreaks)/max(ill_by_date$Illnesses),
                        name="Outbreaks")
  ) +
  labs(title="Monthly Number of Illnesses and Outbreaks",
       x="Year", y="Count", color="Legend") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Limiting data to where only Status 1 is Confirmed. We are looking at the first
# Etiology of a row, and only if it was confirmed.
settings = data.frame(table(nors$Setting))