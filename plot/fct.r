#!/usr/bin/env Rscript

library(ggplot2)

args <- commandArgs(trailingOnly=TRUE)
fcts_raw <- read.csv(args[1], sep="")
#fcts <- fcts_raw[fcts_raw$FctUs < 500000,]
fcts <- fcts_raw
sml <- fcts[fcts$Size <= 10000,]
med <- fcts[fcts$Size > 10000 & fcts$Size <= 1000000,]
big <- fcts[fcts$Size > 1000000,]

ggplot(sml, aes(x=FctUs, colour=Impl)) + stat_ecdf(size=1) + xlim(0, 1e6) +
    scale_colour_brewer(type="qual", palette=2,limit=c("ccp_plain", "kernel_plain"), labels=c("ccp_plain" = "CCP", "kernel_plain" = "Kernel"),guide=guide_legend(title=NULL)) +
    ylab("CDF") + xlab("Flow Completion Time (us)") +
    theme_minimal() +
    theme(legend.position=c(0.8, 0.2), legend.margin=margin(c(0,5,1,5)))
ggsave("small_fcts.pdf", width=6, height=2)

ggplot(med, aes(x=FctUs, colour=Impl)) + stat_ecdf(size=1) + xlim(0, 5e5) +
    scale_colour_brewer(type="qual", palette=2, limit=c("ccp_plain", "kernel_plain"), labels=c("ccp_plain" = "CCP", "kernel_plain" = "Kernel"),guide=guide_legend(title=NULL)) +
    ylab("CDF") + xlab("Flow Completion Time (us)") +
    theme_minimal() + 
    theme(legend.position=c(0.8, 0.2), legend.margin=margin(c(0,5,1,5)))
ggsave("med_fcts.pdf", width=6, height=2)

ggplot(big, aes(x=FctUs, colour=Impl)) + stat_ecdf(size=1) +
    scale_colour_brewer(type="qual", palette=2,limit=c("ccp_plain", "kernel_plain"), labels=c("ccp_plain" = "CCP", "kernel_plain" = "Kernel"),guide=guide_legend(title=NULL)) +
    ylab("CDF") + xlab("Flow Completion Time (us)") +
    theme_minimal() +
    theme(legend.position=c(0.8, 0.2), legend.margin=margin(c(0,5,1,5)))
ggsave("big_fcts.pdf", width=6, height=2)

