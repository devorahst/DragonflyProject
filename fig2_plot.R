library(tidyverse)
library(ggplot2)

lvls = c("OO", "OE", "EE", "EO")

Fig2 = read_csv("fig2_summary.csv")%>%
  mutate(Comparison = factor(Comparison, levels = lvls))

ggplot(Fig2, mapping = aes(x = Comparison, y = Percent_Recovery)) + 
  geom_boxplot() + theme_bw() + geom_jitter(color="black", size=0.5, alpha=0.9) +
  xlab("Comparisons") + ylab("Percent Recovery") + ggtitle("Figure 2 Example") +
  theme(plot.title = element_text(hjust = 0.5))

