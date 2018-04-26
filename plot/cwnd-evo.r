#!/usr/bin/env Rscript

library(ggplot2)

args <- commandArgs(trailingOnly=TRUE)
data <- read.csv(args[1], sep=" ")
alg  <- subset(data, grepl(args[2], Algorithm))

ggplot(alg, aes(x=Time, y=Cwnd, colour=Impl)) + 
  geom_line() + 
  facet_grid(IterationX ~ IterationY, scale="free")
ggsave(args[3], width=12, height=6)
