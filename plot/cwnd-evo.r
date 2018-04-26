#!/usr/bin/env Rscript

library(ggplot2)

plot <- function(data, out) {
    ggplot(data, aes(x=Time, y=Cwnd, colour=Impl)) + 
      geom_line() + 
      facet_grid(IterationX ~ IterationY, scale="free")
    ggsave(out, width=12, height=6)
}

args <- commandArgs(trailingOnly=TRUE)
data <- read.csv(args[1], sep=" ")
alg  <- subset(data, grepl(args[2], Algorithm))
scenario <- subset(alg, Scenario == args[3])
plot(scenario, args[4])
