# Modules import --------
library(ggplot2)
library(tidyverse)
library(gridExtra)

# Setting working directory-----
setwd("~/UCL/Energy Data Analysis/VizChallenge/R_code")

# Data import-------
fr_elec_mix <- read.csv("France_electricity_historic.csv",stringsAsFactors = F)
de_elec_mix <- read.csv("Germany_electricity_historic.csv",stringsAsFactors = F)
fr_elec_cost <- read.csv("France_electricity_historic_cost.csv",stringsAsFactors = F)
de_elec_cost <- read.csv("Germany_electricity_historic_cost.csv",stringsAsFactors = F)

# Data manipulation---------
fr_elec_mix <- fr_elec_mix %>% rename(Electricity_production_GWh = Value)
fr_elec_mix <- inner_join(fr_elec_mix, fr_elec_cost, by=c("Year"="Year"))
fr_elec_mix <- group_by(fr_elec_mix, Year)
fr_elec_mix <- mutate(fr_elec_mix, mix_share=Electricity_production_GWh*100/sum(Electricity_production_GWh))
fr_elec_mix <- fr_elec_mix[!(fr_elec_mix$Year==1990),]

de_elec_mix <- de_elec_mix %>% rename(Electricity_production_GWh = Value)
de_elec_mix <- inner_join(de_elec_mix, de_elec_cost, by=c("Year"="Year"))
de_elec_mix <- group_by(de_elec_mix, Year)
de_elec_mix <- mutate(de_elec_mix, mix_share=Electricity_production_GWh*100/sum(Electricity_production_GWh))
de_elec_mix <- de_elec_mix[!(de_elec_mix$Year==1990),]
  
# Graph for France---------
plot_fr <- ggplot(data=fr_elec_mix) +
           geom_area(mapping=aes(x=Year, y=mix_share, fill=Elec_Source))+
           
           ggtitle("France")+
           scale_fill_manual(values=c("#99CC33", "black","red","blue",
                                      "green","orange","#996633", "magenta", "yellow", "purple", '#003366', '#999900' , "#CCCCFF"),
                             labels=c("Biofuels", "Coal","Geothermal","Hydro",
                                      "Natural gas","Nuclear","Oil", "Other sources", "Solar PV", "Solar thermal",
                                      "Tide", "Waste", "Wind")) +
           geom_line(mapping=aes(x=Year, y=Elec_cost*500), size = 2, color = "grey") + 
           geom_point(mapping=aes(x=Year, y=Elec_cost*500), size = 1, color = "black") + 
           scale_y_continuous(name="Electricity production shares (%)", 
                              sec.axis = sec_axis(~ ./500))+
           theme(axis.title.y.right = element_text(color = "black"))
       
# Graph for Germany--------
plot_de <- ggplot(data=de_elec_mix) +
  geom_area(mapping=aes(x=Year, y=mix_share, fill=Elec_Source))+
  ggtitle("Germany")+
  scale_fill_manual(values=c("#99CC33", "black","red","blue",
                             "green","orange","#996633", "magenta", "yellow", "purple", '#003366', '#999900' , "#CCCCFF"),
                    labels=c("Biofuels", "Coal","Geothermal","Hydro",
                             "Natural gas","Nuclear","Oil", "Other sources", "Solar PV", "Solar thermal",
                             "Tide", "Waste", "Wind")) +
  geom_line(mapping=aes(x=Year, y=Elec_cost*500), size = 2, color = "grey") + 
  geom_point(mapping=aes(x=Year, y=Elec_cost*500), size = 1, color = "black") + 
  scale_y_continuous(sec.axis = sec_axis(~ ./500, name = "Electricity cost HT (€/kWh)"))+
  theme(axis.title.y.left = element_blank(), axis.title.y.right = element_text(color = "black"))

# Multi-plotting------
grid.arrange(plot_fr, plot_de, nrow = 1, ncol=2)
