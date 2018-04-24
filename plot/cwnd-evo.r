#!/usr/bin/env Rscript

library(ggplot2)

args <- commandArgs(trailingOnly=TRUE)
data <- read.csv(args[1], sep=" ")

#ggplot(data[data$IterationX == 3 & data$IterationY == 3,], aes(x=Time, y=Cwnd, colour=Impl)) + 
#    geom_line(size=1) + 
#    labs(x="Time (s)", y="Congestion Window (Pkts)") +
#    ylim(200,750) +
#    scale_colour_brewer(type="qual",palette=2,labels=c("ccp" = "CCP", "kernel" = "Kernel"),guide=guide_legend(title=NULL)) +
#    theme_minimal() + 
#    theme(legend.position="top", legend.margin=margin(c(0,5,1,5)))
#ggsave("cubic-3-cwnd-evo-new.pdf", width=6, height=2.5)

ggplot(data[data$IterationX < 5 & data$IterationY < 5,], aes(x=Time, y=Cwnd, colour=Impl)) + 
  geom_line() + 
  facet_grid(IterationX ~ IterationY, scale="free")
ggsave(args[2], width=12, height=6)
