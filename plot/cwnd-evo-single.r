#!/usr/bin/env Rscript

library(ggplot2)

args <- commandArgs(trailingOnly=TRUE)
data <- read.csv(args[1], sep=" ")
alg  <- subset(data, grepl(args[2], Algorithm))
scenario <- subset(alg, Scenario == args[3])

ggplot(scenario[scenario$IterationX == args[4] & scenario$IterationY == args[5],], aes(x=Time, y=Cwnd, colour=Impl)) + 
    geom_line(size=1) + 
    labs(x="Time (s)", y="Congestion Window (Pkts)") +
    ylim(200,750) +
    scale_colour_brewer(type="qual",palette=2,labels=c("ccp" = "CCP", "kernel" = "Kernel"),guide=guide_legend(title=NULL)) +
    theme_minimal() + 
    theme(legend.position="top", legend.margin=margin(c(0,5,1,5)))
ggsave(args[6], width=6, height=2.5)
