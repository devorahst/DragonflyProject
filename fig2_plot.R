library(tidyverse)
library(ggplot2)

c_lvls = c("O/O", "E/E", "O/E", "E/O")
ct_lvls = c("Matched", "Mismatched")
Fig2 = read_csv("fig2_summary.csv")%>%
  mutate(Comparison = factor(Comparison, levels = c_lvls))
  mutate(Comparison_Type = factor(Comparison_Type, levels = ct_lvls))

ggplot(Fig2, mapping = aes(x = Comparison, y = Recovered_loci, fill = Comparison_Type)) + 
  geom_boxplot() + theme_bw() + geom_jitter(color="black", size=0.5, alpha=0.9) +
  labs(title="Recovered Loci vs AHE Probeset Combinations",x="AHE data/Reference loci", 
       y="Recovered loci", fill="Comparison Type")
  theme(plot.title = element_text(hjust = 0.5))


