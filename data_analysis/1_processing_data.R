library(tidyverse)
library(here)

#### read in data ####
data_v3 <- read.csv(here("data","version3","Birdsong_v3_allData_040417.txt"),sep="\t")
data_v4 <- read.csv(here("data","version4","Birdsong_v4_allData_09192017.txt"),sep="\t")

#subject logs
subj_v3 <- read.csv(here("data","version3","Birdsong_v3_subject_landscape_deID.csv"))
subj_v4 <- read.csv(here("data","version4","Birdsong_v4_subject_landscape_deID.csv"))

#### unify participant naming ####
setdiff(unique(subj_v3$subjCode),unique(data_v3$subjCode))
setdiff(unique(data_v3$subjCode),unique(subj_v3$subjCode))

data_v3 <- data_v3 %>%
  mutate(subjCode=case_when(
    subjCode == "Bird_113" ~ "Bird_113_Prac_818",
    subjCode== "BIRD_118" ~"Bird_118",
    subjCode== "Bird_124a" ~ "Bird_124",
    TRUE ~ as.character(subjCode)))

setdiff(unique(subj_v4$subjCode),unique(data_v4$subjCode))
setdiff(unique(data_v4$subjCode),unique(subj_v4$subjCode))

data_v4 <- data_v4 %>%
  mutate(subjCode=case_when(
    subjCode == "201" ~ "Bird_201",
    subjCode=="202" ~ "Bird_202",
    subjCode=="203_Prac"~ "Bird_203Prac",
    subjCode == "204" ~ "Bird_204",
    subjCode=="205a" ~ "Bird_205a",
    subjCode=="206"~ "Bird_206",
    subjCode == "207" ~ "Bird_207",
    subjCode=="BIRD-221" ~ "Bird_221",
    subjCode=="Bird_211"~ "BirdPrac_211",
    TRUE ~ as.character(subjCode)))

#### merge participant and trial data ####
data_v3 <- data_v3 %>%
  left_join(subj_v3,by="subjCode")
data_v4 <- data_v4 %>%
  left_join(subj_v4,by="subjCode")

data_v3$version="version3"
data_v4$version="version4"
data <- bind_rows(data_v3,data_v4)

#### miscellaneous other fixes ####
data <- data %>%
  mutate(gender=tolower(Gender))


#### exclusions ####

#participants to exclude
pilot <- c("Bird_101", "Bird_102","Bird_103")
practice <- c("Bird_113","Bird_132Prac","Bird_203Prac","BirdPrac_211","Bird_226Prac")
fussiness <- c("Bird_109", "Bird_129","Bird_119", "Bird_135") 

data <- data %>%
  mutate(
    subj_exclusion = case_when(
      subjCode %in% c(pilot,practice,fussiness) ~ "yes",
      TRUE ~  "no"
    ),
    subj_exclusion_reason = case_when(
      subjCode %in% pilot ~ "pilot",
      subjCode %in% practice ~ "practice",
      subjCode %in% fussiness ~ "fussiness",
      TRUE ~ ""
    )
  )

#exclude trials if looking time shorter than 1000ms
data <- data %>%
  mutate(trial_exclusion = case_when(
    totalLookingTimeNS<1000 ~ "yes",
    TRUE ~ "no"
  ))

##subject level looking ##
subj_summarize <- data %>%
  group_by(version,subjCode,subj_exclusion,gender, Days,audioType) %>%
  summarize(
    N=n(),
    trial_exclusion_n=sum(trial_exclusion=="yes"),
    num_useable_trials=sum(trial_exclusion=="no")
  ) %>%
  ungroup()

#update subject exclusions based on number of useable trials
subj_summarize <- subj_summarize %>%
  mutate(subj_exclusion_trial =
           case_when(
             version=="version3"&num_useable_trials<2 ~ 1,
             version=="version4"&num_useable_trials<3 ~ 1,
             TRUE ~ 0
           )
  )

subj_exclude_for_trialNum <- subj_summarize %>%
  group_by(subjCode) %>% 
  summarize(subj_exclusion_trial=sum(subj_exclusion_trial)) %>%
  filter(subj_exclusion_trial>0) %>%
  select(subjCode)
subj_exclude_for_trialNum <- unique(subj_exclude_for_trialNum$subjCode)

data <- data %>%
  mutate(
    subj_exclusion = case_when(
      subjCode %in% subj_exclude_for_trialNum ~ "yes",
      TRUE ~  as.character(subj_exclusion)
    ),
    subj_exclusion_reason = case_when(
      subjCode %in% subj_exclude_for_trialNum  ~ "number of useable trials",
      TRUE ~ as.character(subj_exclusion_reason)
    )
  )

#### select columns ####
cols_to_keep <- c(
  version,
  subjCode,
  gender,
  Days,
  curTrialIndex,
  audio,
  audioType,
  expTimer,
  trialStart,
  trialTime,
  totalTime,
  lookAways,
  totalLookingTimeNS,
  ausioStartTime,
  audioEndTime,
  subj_exclusion,
  subj_exclusion_reason,
  trial_exclusion
)

data_to_write <- data %>%
  select(
    version,
    subjCode,
    gender,
    Days,
    curTrialIndex,
    audio,
    audioType,
    expTimer,
    trialStart,
    trialTime,
    totalTime,
    lookAways,
    totalLookingTimeNS,
    audioStartTime,
    audioEndTime,
    subj_exclusion,
    subj_exclusion_reason,
    trial_exclusion
  ) %>%
  rename(looking_time=totalLookingTimeNS)

#### write data ####
write.csv(data_to_write,here("processed_data","Birdsong_data.csv"),row.names=FALSE)
