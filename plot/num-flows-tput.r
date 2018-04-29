#!/usr/bin/env Rscript

library(plyr)
library(ggplot2)

args <- commandArgs(trailingOnly=TRUE)
tputs <- read.csv(args[1], sep=" ")
tputs$Throughput <- tputs$Throughput / 1e9
summarized <- ddply(tputs, c("NumFlows", "Scenario"), summarise, m=mean(Throughput), sd=sd(Throughput))

# line with std-dev ribbon
#ggplot(summarized, aes(x=NumFlows)) + 
#    geom_line(aes(y=m, color=Scenario)) + 
#    geom_point(aes(y=m)) +
#    geom_ribbon(aes(ymin=m-sd,ymax=m+sd,fill=Scenario), alpha=0.5) + 
#    scale_x_log10() +
#    labs(x="Flows", y="Throughput (Gbps)")
#ggsave("throughput_ribbon.pdf", width=6, height=4)
#
## box-plot
#ggplot(tputs, aes(x=factor(NumFlows), y=Throughput, fill=Scenario)) + 
#    geom_boxplot(outlier.alpha=0) +
#    labs(x="Flows", y="Throughput (Gbps)")
#ggsave("throughput_box.pdf", width=6, height=4)

# columns with error-bars    
dodge <- position_dodge(width=0.9)
ggplot(summarized, aes(x=factor(NumFlows), y=m, fill=Scenario)) + 
    geom_col(aes(x=factor(NumFlows), y=m, fill=Scenario), position=dodge) +
    geom_errorbar(aes(ymin=m-sd,ymax=m+sd), position=dodge) +
    scale_fill_brewer(
        type="qual",
        labels=c(
            "ccp_per_ack" = "CCP (Ack)", 
            "ccp_per_10ms" = "CCP (10ms)", 
            "kernel" = "Kernel"
        ),
        guide=guide_legend(title=NULL)
    ) +
    labs(x="Flows", y="Throughput (Gbps)") +
    theme_minimal()

ggsave(args[2], width=12, height=6)
