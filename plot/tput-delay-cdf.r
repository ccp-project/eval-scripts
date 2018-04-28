#!/usr/bin/env Rscript

library(ggplot2)

args <- commandArgs(trailingOnly=TRUE)
d <- read.csv(args[1], sep=" ")
d$Throughput = d$Throughput / 1e6

ggplot(d, aes(x=Throughput, colour=Impl)) + 
    stat_ecdf(geom="step", alpha=0.8, size=1) +
    facet_grid(Algorithm ~ Scenario, scales="free_x") +
    xlab("Throughput (Mbps)") + ylab("CDF") +
    scale_colour_brewer(type="qual", palette=2, labels=c("ccp" = "CCP", "kernel" = "Kernel"),guide=guide_legend(title=NULL)) +
    theme_minimal() +
    theme(legend.position="top", legend.margin=margin(c(0,5,1,5)))
ggsave(args[2], width=12, height=6)

ggplot(d, aes(x=Delay, colour=Impl)) + 
    stat_ecdf(geom="step", alpha=0.8, size=1) +
    facet_grid(Algorithm ~ Scenario, scales="free_x") +
    xlab("Delay (ms)") + ylab("CDF") +
    scale_colour_brewer(type="qual", palette=2, labels=c("ccp" = "CCP", "kernel" = "Kernel"), guide=FALSE) +
    theme_minimal()
ggsave(args[3], width=12, height=6)
