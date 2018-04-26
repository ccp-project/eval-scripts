#!/usr/bin/env Rscript

library(ggplot2)

args <- commandArgs(trailingOnly=TRUE)
data <- read.csv(args[1], sep=" ")
alg  <- subset(data, grepl(args[2], Algorithm))

ccp_iter <- args[3]
kernel_iter <- args[4]

ggplot(alg[alg$IterationX == ccp_iter & alg$IterationY == kernel_iter,], aes(x=Time, y=Cwnd, colour=Impl)) + 
    geom_line(size=1) + 
    labs(x="Time (s)", y="Congestion Window (Pkts)") +
    ylim(200,750) +
    scale_colour_brewer(type="qual",palette=2,labels=c("ccp" = "CCP", "kernel" = "Kernel"),guide=guide_legend(title=NULL)) +
    theme_minimal() + 
    theme(legend.position="top", legend.margin=margin(c(0,5,1,5)))
ggsave(args[5], width=6, height=2.5)
