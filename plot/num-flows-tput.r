#!/usr/bin/env Rscript

library(plyr)
library(ggplot2)

args <- commandArgs(trailingOnly=TRUE)
tputs <- read.csv(args[1], sep=" ")
darkMode <- ('dark' == args[3])
tputs$Throughput <- tputs$Throughput / 1e9
summarized <- ddply(tputs, c("Algorithm", "Impl", "NumFlows", "Scenario"), summarise, m=mean(Throughput), sd=sd(Throughput))

if (darkMode) {
    mytheme <- theme(
        axis.title.x = element_text(colour="#93a1a1"),
        axis.title.y = element_text(colour="#93a1a1"),
        axis.text.x = element_text(colour="#93a1a1"),
        axis.text.y = element_text(colour="#93a1a1"),
        legend.text = element_text(colour="#93a1a1"),
        strip.text = element_text(colour="#93a1a1")
        #axis.line.y.left = element_line(color="#839496"), 
        #axis.ticks.y.left = element_line(color="#839496"),
        #axis.line.x.left = element_line(color="#839496"), 
        #axis.ticks.x.left = element_line(color="#839496"),
    )
} else {
    mytheme <- theme()
}

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
ggplot(summarized, aes(x=factor(NumFlows), y=m, fill=Impl)) + 
    geom_col(aes(x=factor(NumFlows), y=m, fill=Impl), position=dodge) +
    geom_errorbar(aes(ymin=m-sd,ymax=m+sd), position=dodge) +
    scale_fill_manual(
        labels=c(
            "ccp_netlink_per_10ms" = "CCP (10ms)", 
            "ccp_netlink_per_ack" = "CCP (Ack)", 
            "kernel" = "Kernel"
        ),
        values=c(
            "ccp_netlink_per_10ms" = "#88419d", 
            "ccp_netlink_per_ack" = "#8c96c6", 
            "kernel" = "#b3cde3"
        ),
        guide=guide_legend(title=NULL)
    ) +
    labs(x="Flows", y="Throughput (Gbps)") +
    facet_wrap(~Algorithm) +
    theme_minimal() +
    mytheme

ggsave(args[2], width=6, height=2)
