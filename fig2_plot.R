library(tidyverse)
library(ggplot2)

lvls = c("OO", "OE", "EE", "EO")

Fig2 = read_csv("fig2_summary.csv")%>%
  mutate(Comparison = factor(Comparison, levels = lvls))

ggplot(Fig2, aes(x = Comparison, y = Percent_Recovery)) + 
  geom_boxplot() + theme_bw() + xlab("Comparisons") + ylab("Percent Recovery")
