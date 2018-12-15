#!/usr/bin/Rscript

library(ggplot2)

args <- commandArgs(trailingOnly=TRUE)
d <- read.csv(args[1], sep=" ")
d$Rtt = d$Rtt / 1e3
q <- quantile(d$Rtt, 0.99)

ggplot(d, aes(x=Rtt, colour=Impl, linetype=Mode)) + 
    stat_ecdf(alpha=0.8, size=1) +
    xlab("RTT (us)") + ylab("CDF") +
    xlim(0, q) +
    scale_colour_brewer(
        type="qual", 
        palette=2, 
        guide=guide_legend(title=NULL)
    ) +
    theme_minimal() +
    theme(
        legend.position=c(0.85, 0.45),
        legend.spacing.y = unit(-0.5, "cm"),
        legend.title = element_blank(),
        legend.text = element_text(
            size=8
        )
    ) +
    guides(shape=guide_legend(
        override.aes = list(
            linetype=c("Blocking", "Nonblocking"),
            colour=c("Unix", "Netlink", "Chardev")
        )
    ))
ggsave(args[2], device="pdf", width=4, height=2)
