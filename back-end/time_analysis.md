# Time Analysis Report

Αυτό το report μεταφέρει το session-time / reading-speed κομμάτι έξω από το `quiz_analysis_report.md`. Χρησιμοποιεί μόνο rows που έχουν πραγματικό matched DB session (`matchType = db_session`) και corrected `startedAt` / `endedAt` από το current analysis database. Τα inferred condition-only quiz rows δεν μπαίνουν στα timing statistics, γιατί δεν έχουν αξιόπιστο session duration.

Συνολικά χρησιμοποιούνται **374** matched sessions από **51** users. Έχουν αφαιρεθεί **3** matched setup/error sessions κάτω από **1.00 λεπτό**, επειδή συνήθως αντιστοιχούν σε λάθος αρχική ρύθμιση που διορθώθηκε αμέσως, π.χ. popup `on` που άλλαξε σε `off`. Το reading speed υπολογίζεται ως `λέξεις κειμένου / λεπτά session`, άρα είναι εκτίμηση λέξεων ανά λεπτό ανάγνωσης και όχι αριθμός μεταφρασμένων λέξεων.

## Excluded Setup/Error Sessions Under 1 Minute
| user | PDF | duration min | startedAt | endedAt | popup | sessionID |
| --- | --- | --- | --- | --- | --- | --- |
| 1093413 | c1_native_american_conflicts_3.pdf | 0.45 | 2026-05-28T13:53:38 | 2026-05-28T13:54:05 | off | b5c0b348-3e95-4a09-b719-9a10bcae7dad |
| 1103080 | c2_rosa_parks_2.pdf | 0.92 | 2026-06-02T16:39:13 | 2026-06-02T16:40:08 | on | 64082b11-2ea5-43af-ad8e-52515f878a9e |
| 1112096 | c1_walt_disney_4.pdf | 0.58 | 2026-05-21T10:45:07 | 2026-05-21T10:45:42 | on | a7b34be5-4bcc-4dfd-8503-3ca4343a39be |

## Text Word Counts Used
| PDF | Title | Level | Grade | Words | Lexile |
| --- | --- | --- | --- | --- | --- |
| b2_animals_of_rainforests_1.pdf | Animals of the Tropical Rainforest | B2 | 4 | 714 | 1180L |
| b2_electromagnetic_radiation_2.pdf | Electromagnetic Radiation | B2 | 8 | 609 | 1180L |
| b2_first_american_3.pdf | The First American | B2 | 8 | 516 | 1180L |
| b2_sticky_fingers_4.pdf | Sticky Fingers, Helping Hands | B2 | 5 | 727 | 1180L |
| c1_age_of_exploration_1.pdf | The Age of Exploration | C1 | 8 | 677 | 1340L |
| c1_bee_reading_2.pdf | Worldwide Loss of Bees a Growing Concern | C1 | 7 | 688 | 1340L |
| c1_native_american_conflicts_3.pdf | Native American Conflicts | C1 | 9-10 | 554 | 1340L |
| c1_walt_disney_4.pdf | Walt Disney Goes to War | C1 | 9-10 | 633 | 1340L |
| c2_noisy_humans_1.pdf | Noisy Humans Drown Out Sounds of Nature in Protected Areas | C2 | 11-12 | 688 | 1500L |
| c2_rosa_parks_2.pdf | Rosa Parks: 100th Birthday | C2 | 8 | 419 | 1470L |

## Overall Session Time and Words Per Minute by Popup Mode
| Popup | sessions | users | total min | mean min | median min | sd min | range min | mean WPM | median WPM | sd WPM |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| on | 190 | 51 | 897.72 | 4.72 | 4.52 | 1.58 | 1.60-9.85 | 144.10 | 138.41 | 46.37 |
| off | 184 | 51 | 904.73 | 4.92 | 4.57 | 2.06 | 1.82-18.15 | 139.97 | 137.27 | 42.53 |

Overall, popup `on` sessions είχαν μέσο χρόνο **4.72 min**, ενώ popup `off` sessions είχαν μέσο χρόνο **4.92 min**. Η διαφορά `on-off` είναι **-0.19 min**. Σε reading speed, popup `on` είχε μέσο **144.10 WPM**, ενώ popup `off` είχε **139.97 WPM** (`on-off` = **4.14 WPM**).

Αυτό δείχνει μικρό descriptive advantage υπέρ του popup-on στο συνολικό dataset: λίγο μικρότερος χρόνος και λίγο μεγαλύτερο WPM. Δεν είναι από μόνο του causal proof, γιατί οι users/texts δεν είναι ανεξάρτητα μεταξύ τους και το κάθε κείμενο έχει διαφορετική δυσκολία.

## User-Level: Who Was Faster With Popup On vs Off
Η σύγκριση γίνεται ανά user, με βάση τον μέσο χρόνο και το μέσο WPM των δικών του popup-on και popup-off sessions. Συγκρίνονται μόνο users που έχουν τουλάχιστον ένα `on` και ένα `off` matched session: **51 users**.

| comparison | users | percent | mean advantage | median advantage |
| --- | --- | --- | --- | --- |
| Mean duration: popup on faster | 27 | 52.9% | 1.27 min saved | median 0.62 min |
| Mean duration: popup off faster | 24 | 47.1% | 0.79 min saved | median 0.49 min |
| Mean duration: tie | 0 | 0.0% | - | - |
| Mean WPM: popup on faster | 25 | 49.0% | +24.19 WPM | median +20.56 WPM |
| Mean WPM: popup off faster | 26 | 51.0% | +15.17 WPM | median +12.22 WPM |
| Mean WPM: tie | 0 | 0.0% | - | - |

Με βάση τον μέσο χρόνο, **27 users (52.9%)** ήταν πιο γρήγοροι με popup-on και **24 users (47.1%)** ήταν πιο γρήγοροι με popup-off. Με βάση το WPM, **25 users (49.0%)** είχαν μεγαλύτερη ταχύτητα με popup-on και **26 users (51.0%)** με popup-off.

Ο μέσος user-level χρόνος `on-off` είναι **-0.30 min** και ο διάμεσος **-0.07 min**. Το αρνητικό πρόσημο σημαίνει ότι το popup-on ήταν γρηγορότερο. Το μέσο user-level WPM `on-off` είναι **4.13 WPM** και ο διάμεσος **-1.21 WPM**. Το θετικό πρόσημο σημαίνει ότι το popup-on είχε μεγαλύτερη ταχύτητα ανάγνωσης.

## Per-User Mean On/Off Timing and Reading Speed
Στον πίνακα, `minutes on-off` < 0 σημαίνει ότι ο user ήταν γρηγορότερος με popup-on. `WPM on-off` > 0 σημαίνει ότι ο user είχε μεγαλύτερο WPM με popup-on.

| user | on n | off n | mean min on | mean min off | minutes on-off | faster time | mean WPM on | mean WPM off | WPM on-off | faster WPM |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1059657 | 4 | 4 | 5.67 | 4.51 | 1.16 | off | 121.15 | 129.66 | -8.51 | off |
| 1065023 | 4 | 4 | 4.05 | 5.62 | -1.57 | on | 144.77 | 122.33 | 22.45 | on |
| 1070729 | 4 | 4 | 4.61 | 4.44 | 0.17 | off | 135.41 | 138.54 | -3.13 | off |
| 1080401 | 4 | 4 | 7.52 | 11.69 | -4.17 | on | 86.53 | 50.50 | 36.03 | on |
| 1084609 | 4 | 4 | 4.07 | 6.43 | -2.36 | on | 151.07 | 121.12 | 29.94 | on |
| 1090053 | 4 | 4 | 4.17 | 4.67 | -0.50 | on | 131.36 | 150.03 | -18.67 | off |
| 1093313 | 3 | 3 | 5.42 | 3.44 | 1.98 | off | 115.91 | 195.68 | -79.76 | off |
| 1093322 | 2 | 3 | 6.01 | 5.51 | 0.50 | off | 105.43 | 128.99 | -23.56 | off |
| 1093332 | 4 | 4 | 6.75 | 4.36 | 2.40 | off | 106.36 | 121.23 | -14.87 | off |
| 1093348 | 4 | 4 | 5.13 | 5.29 | -0.16 | on | 114.83 | 116.87 | -2.04 | off |
| 1093379 | 4 | 4 | 7.25 | 5.39 | 1.86 | off | 88.91 | 109.95 | -21.05 | off |
| 1093390 | 4 | 4 | 5.53 | 5.23 | 0.29 | off | 114.17 | 119.41 | -5.25 | off |
| 1093403 | 4 | 4 | 4.19 | 4.27 | -0.08 | on | 173.44 | 135.77 | 37.67 | on |
| 1093413 | 4 | 3 | 4.64 | 4.75 | -0.11 | on | 149.50 | 128.94 | 20.56 | on |
| 1093505 | 4 | 4 | 3.75 | 5.06 | -1.30 | on | 155.13 | 137.94 | 17.18 | on |
| 1093515 | 3 | 3 | 4.87 | 4.62 | 0.25 | off | 117.85 | 139.45 | -21.60 | off |
| 1095564 | 4 | 2 | 2.92 | 3.17 | -0.25 | on | 217.27 | 223.19 | -5.92 | off |
| 1097463 | 4 | 4 | 3.58 | 4.82 | -1.24 | on | 161.44 | 141.47 | 19.97 | on |
| 1100496 | 4 | 4 | 4.50 | 4.91 | -0.41 | on | 138.18 | 133.71 | 4.47 | on |
| 1100497 | 4 | 4 | 4.35 | 4.42 | -0.07 | on | 130.84 | 154.49 | -23.65 | off |
| 1100613 | 4 | 4 | 4.75 | 4.69 | 0.06 | off | 124.93 | 141.29 | -16.36 | off |
| 1100663 | 4 | 4 | 4.49 | 5.99 | -1.50 | on | 134.26 | 111.12 | 23.15 | on |
| 1100758 | 4 | 4 | 4.71 | 6.75 | -2.03 | on | 121.66 | 123.36 | -1.70 | off |
| 1103080 | 3 | 3 | 3.17 | 2.92 | 0.25 | off | 231.14 | 204.48 | 26.67 | on |
| 1104782 | 4 | 4 | 6.85 | 4.64 | 2.21 | off | 99.58 | 118.42 | -18.84 | off |
| 1104806 | 4 | 4 | 5.90 | 4.71 | 1.19 | off | 115.01 | 124.74 | -9.73 | off |
| 1104816 | 4 | 4 | 4.83 | 3.79 | 1.04 | off | 131.60 | 161.15 | -29.55 | off |
| 1104818 | 4 | 4 | 3.92 | 3.85 | 0.06 | off | 179.65 | 150.03 | 29.62 | on |
| 1108323 | 4 | 4 | 4.20 | 3.71 | 0.49 | off | 162.28 | 164.64 | -2.36 | off |
| 1108328 | 3 | 2 | 4.06 | 3.79 | 0.27 | off | 167.78 | 148.16 | 19.61 | on |
| 1108330 | 3 | 4 | 5.18 | 5.43 | -0.24 | on | 126.73 | 108.68 | 18.05 | on |
| 1108335 | 4 | 4 | 5.63 | 4.71 | 0.92 | off | 122.99 | 125.77 | -2.78 | off |
| 1108339 | 3 | 5 | 4.00 | 4.11 | -0.12 | on | 156.09 | 160.03 | -3.94 | off |
| 1108344 | 4 | 4 | 4.09 | 3.81 | 0.28 | off | 159.74 | 160.96 | -1.21 | off |
| 1108346 | 4 | 4 | 3.56 | 4.10 | -0.54 | on | 167.78 | 166.27 | 1.51 | on |
| 1108348 | 4 | 4 | 5.13 | 7.26 | -2.13 | on | 110.01 | 96.44 | 13.57 | on |
| 1108349 | 4 | 4 | 2.76 | 2.81 | -0.05 | on | 235.15 | 222.63 | 12.52 | on |
| 1108353 | 1 | 1 | 8.73 | 18.15 | -9.42 | on | 77.55 | 30.52 | 47.03 | on |
| 1108357 | 4 | 4 | 4.85 | 5.63 | -0.79 | on | 117.93 | 113.02 | 4.91 | on |
| 1108360 | 5 | 3 | 3.27 | 3.08 | 0.19 | off | 200.75 | 213.55 | -12.80 | off |
| 1108364 | 4 | 4 | 5.93 | 4.52 | 1.41 | off | 110.39 | 130.28 | -19.89 | off |
| 1108365 | 4 | 4 | 3.35 | 3.47 | -0.12 | on | 209.61 | 162.73 | 46.88 | on |
| 1108367 | 4 | 4 | 3.45 | 2.83 | 0.62 | off | 196.11 | 205.61 | -9.50 | off |
| 1108382 | 4 | 3 | 5.57 | 6.16 | -0.59 | on | 122.62 | 100.87 | 21.75 | on |
| 1108387 | 3 | 3 | 6.89 | 5.91 | 0.98 | off | 90.12 | 116.12 | -25.99 | off |
| 1112096 | 3 | 1 | 6.62 | 7.52 | -0.90 | on | 102.48 | 55.72 | 46.76 | on |
| 1112106 | 3 | 4 | 3.06 | 4.25 | -1.19 | on | 179.73 | 170.63 | 9.10 | on |
| 1112115 | 4 | 4 | 3.62 | 4.25 | -0.62 | on | 165.96 | 152.88 | 13.09 | on |
| 1112119c | 3 | 2 | 5.27 | 5.17 | 0.10 | off | 134.93 | 114.38 | 20.55 | on |
| 1112121 | 4 | 3 | 2.70 | 4.49 | -1.80 | on | 212.86 | 151.13 | 61.72 | on |
| 1112139 | 4 | 4 | 5.75 | 5.59 | 0.16 | off | 134.31 | 145.95 | -11.64 | off |

## Session Time and WPM by Level
| Level | Popup | sessions | total min | mean min | median min | sd min | mean WPM | median WPM | sd WPM |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B2 | on | 75 | 329.04 | 4.39 | 4.28 | 1.32 | 155.95 | 150.37 | 41.74 |
| B2 | off | 72 | 333.80 | 4.64 | 4.33 | 1.19 | 147.31 | 141.77 | 36.42 |
| C1 | on | 70 | 355.40 | 5.08 | 4.67 | 1.69 | 140.41 | 134.91 | 46.94 |
| C1 | off | 68 | 365.23 | 5.37 | 4.66 | 2.84 | 138.46 | 137.26 | 47.75 |
| C2 | on | 45 | 213.28 | 4.74 | 4.85 | 1.72 | 130.10 | 111.51 | 48.87 |
| C2 | off | 44 | 205.70 | 4.67 | 4.58 | 1.64 | 130.28 | 125.43 | 42.03 |

## Session Time and WPM by Text and Popup Mode
| PDF | Title | Level | Words | Lexile | Popup | sessions | total min | mean min | median min | sd min | mean WPM | median WPM | sd WPM |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| b2_animals_of_rainforests_1.pdf | Animals of the Tropical Rainforest | B2 | 714 | 1180L | on | 17 | 82.48 | 4.85 | 4.93 | 1.30 | 157.48 | 144.83 | 43.83 |
| b2_animals_of_rainforests_1.pdf | Animals of the Tropical Rainforest | B2 | 714 | 1180L | off | 19 | 95.39 | 5.02 | 4.87 | 0.92 | 146.57 | 146.61 | 25.38 |
| b2_electromagnetic_radiation_2.pdf | Electromagnetic Radiation | B2 | 609 | 1180L | on | 18 | 80.03 | 4.45 | 4.39 | 1.33 | 150.55 | 138.73 | 51.73 |
| b2_electromagnetic_radiation_2.pdf | Electromagnetic Radiation | B2 | 609 | 1180L | off | 21 | 100.64 | 4.79 | 4.32 | 1.44 | 137.11 | 140.97 | 37.05 |
| b2_first_american_3.pdf | The First American | B2 | 516 | 1180L | on | 20 | 70.83 | 3.54 | 3.27 | 0.81 | 152.84 | 157.59 | 33.66 |
| b2_first_american_3.pdf | The First American | B2 | 516 | 1180L | off | 14 | 55.05 | 3.93 | 3.85 | 0.72 | 135.90 | 134.05 | 27.90 |
| b2_sticky_fingers_4.pdf | Sticky Fingers, Helping Hands | B2 | 727 | 1180L | on | 20 | 95.70 | 4.79 | 4.30 | 1.41 | 162.63 | 169.13 | 39.40 |
| b2_sticky_fingers_4.pdf | Sticky Fingers, Helping Hands | B2 | 727 | 1180L | off | 18 | 82.72 | 4.60 | 4.30 | 1.26 | 168.88 | 169.07 | 43.80 |
| c1_age_of_exploration_1.pdf | The Age of Exploration | C1 | 677 | 1340L | on | 20 | 109.56 | 5.48 | 4.82 | 1.77 | 135.17 | 140.54 | 40.16 |
| c1_age_of_exploration_1.pdf | The Age of Exploration | C1 | 677 | 1340L | off | 15 | 83.35 | 5.56 | 4.87 | 2.49 | 139.29 | 139.01 | 47.74 |
| c1_bee_reading_2.pdf | Worldwide Loss of Bees a Growing Concern | C1 | 688 | 1340L | on | 16 | 79.72 | 4.98 | 4.67 | 1.76 | 154.65 | 147.51 | 56.91 |
| c1_bee_reading_2.pdf | Worldwide Loss of Bees a Growing Concern | C1 | 688 | 1340L | off | 19 | 102.05 | 5.37 | 5.02 | 2.08 | 143.66 | 137.05 | 48.63 |
| c1_native_american_conflicts_3.pdf | Native American Conflicts | C1 | 554 | 1340L | on | 13 | 61.03 | 4.69 | 4.43 | 1.52 | 129.82 | 125.06 | 42.34 |
| c1_native_american_conflicts_3.pdf | Native American Conflicts | C1 | 554 | 1340L | off | 20 | 115.95 | 5.80 | 4.55 | 4.30 | 129.74 | 121.63 | 59.84 |
| c1_walt_disney_4.pdf | Walt Disney Goes to War | C1 | 633 | 1340L | on | 21 | 105.09 | 5.00 | 5.03 | 1.70 | 141.11 | 125.84 | 47.99 |
| c1_walt_disney_4.pdf | Walt Disney Goes to War | C1 | 633 | 1340L | off | 14 | 63.88 | 4.56 | 4.39 | 0.86 | 142.97 | 144.19 | 24.69 |
| c2_noisy_humans_1.pdf | Noisy Humans Drown Out Sounds of Nature in Protected Areas | C2 | 688 | 1500L | on | 23 | 129.66 | 5.64 | 6.03 | 1.62 | 134.80 | 114.10 | 48.92 |
| c2_noisy_humans_1.pdf | Noisy Humans Drown Out Sounds of Nature in Protected Areas | C2 | 688 | 1500L | off | 23 | 120.25 | 5.23 | 5.10 | 1.30 | 139.81 | 134.90 | 36.57 |
| c2_rosa_parks_2.pdf | Rosa Parks: 100th Birthday | C2 | 419 | 1470L | on | 22 | 83.62 | 3.80 | 3.88 | 1.29 | 125.20 | 107.85 | 49.48 |
| c2_rosa_parks_2.pdf | Rosa Parks: 100th Birthday | C2 | 419 | 1470L | off | 21 | 85.45 | 4.07 | 3.57 | 1.80 | 119.84 | 117.37 | 45.91 |

## Per-Text Popup On-Off Differences
Θετικό `duration on-off` σημαίνει ότι το popup-on πήρε περισσότερο χρόνο από το popup-off. Θετικό `WPM on-off` σημαίνει ότι το popup-on ήταν γρηγορότερο σε λέξεις/λεπτό.

| PDF | Level | on n | on mean min | on mean WPM | off n | off mean min | off mean WPM | duration on-off | WPM on-off | faster WPM |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| b2_animals_of_rainforests_1.pdf | B2 | 17 | 4.85 | 157.48 | 19 | 5.02 | 146.57 | -0.17 | 10.91 | on |
| b2_electromagnetic_radiation_2.pdf | B2 | 18 | 4.45 | 150.55 | 21 | 4.79 | 137.11 | -0.35 | 13.44 | on |
| b2_first_american_3.pdf | B2 | 20 | 3.54 | 152.84 | 14 | 3.93 | 135.90 | -0.39 | 16.94 | on |
| b2_sticky_fingers_4.pdf | B2 | 20 | 4.79 | 162.63 | 18 | 4.60 | 168.88 | 0.19 | -6.26 | off |
| c1_age_of_exploration_1.pdf | C1 | 20 | 5.48 | 135.17 | 15 | 5.56 | 139.29 | -0.08 | -4.12 | off |
| c1_bee_reading_2.pdf | C1 | 16 | 4.98 | 154.65 | 19 | 5.37 | 143.66 | -0.39 | 10.98 | on |
| c1_native_american_conflicts_3.pdf | C1 | 13 | 4.69 | 129.82 | 20 | 5.80 | 129.74 | -1.10 | 0.09 | on |
| c1_walt_disney_4.pdf | C1 | 21 | 5.00 | 141.11 | 14 | 4.56 | 142.97 | 0.44 | -1.87 | off |
| c2_noisy_humans_1.pdf | C2 | 23 | 5.64 | 134.80 | 23 | 5.23 | 139.81 | 0.41 | -5.01 | off |
| c2_rosa_parks_2.pdf | C2 | 22 | 3.80 | 125.20 | 21 | 4.07 | 119.84 | -0.27 | 5.36 | on |

## Popup-On Speed Change: Last 2 Sessions vs First 2 Sessions
Για να δούμε αν βελτιωνόταν η ταχύτητα με χρήση του eye-tracker popup-on, ταξινόμησα τα popup-on sessions κάθε user χρονολογικά και σύγκρινα τα πρώτα 2 με τα τελευταία 2. Χρησιμοποιώ threshold **±5 WPM**: πάνω από +5 WPM = improved, κάτω από -5 WPM = slower, ενδιάμεσα = stable/small change.

Users με τουλάχιστον 4 popup-on sessions: **39**.
| result | users | percent | mean WPM change |
| --- | --- | --- | --- |
| Improved popup-on WPM in last 2 vs first 2 | 22 | 56.4% | mean change 35.23 WPM |
| Slower popup-on WPM in last 2 vs first 2 | 13 | 33.3% | mean change -24.06 WPM |
| Stable / small change within +/-5 WPM | 4 | 10.3% | mean change -1.59 WPM |

| user | popup-on n | first2 WPM | last2 WPM | WPM change | first2 min | last2 min | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1059657 | 4 | 132.21 | 110.08 | -22.12 | 5.14 | 6.20 | slower; duration change 1.06 min |
| 1065023 | 4 | 125.24 | 164.31 | 39.07 | 3.96 | 4.13 | improved; duration change 0.17 min |
| 1070729 | 4 | 134.28 | 136.54 | 2.26 | 4.17 | 5.05 | stable; duration change 0.88 min |
| 1080401 | 4 | 93.41 | 79.64 | -13.77 | 6.36 | 8.69 | slower; duration change 2.33 min |
| 1084609 | 4 | 139.86 | 162.27 | 22.41 | 4.31 | 3.83 | improved; duration change -0.48 min |
| 1090053 | 4 | 119.03 | 143.69 | 24.66 | 4.54 | 3.81 | improved; duration change -0.73 min |
| 1093313 | 3 | - | - | - | - | - | not enough popup-on sessions |
| 1093322 | 2 | - | - | - | - | - | not enough popup-on sessions |
| 1093332 | 4 | 83.25 | 129.47 | 46.22 | 7.94 | 5.56 | improved; duration change -2.38 min |
| 1093348 | 4 | 104.87 | 124.79 | 19.92 | 5.18 | 5.09 | improved; duration change -0.09 min |
| 1093379 | 4 | 78.38 | 99.43 | 21.05 | 8.43 | 6.07 | improved; duration change -2.35 min |
| 1093390 | 4 | 116.12 | 112.22 | -3.89 | 5.71 | 5.34 | stable; duration change -0.36 min |
| 1093403 | 4 | 137.76 | 209.13 | 71.37 | 5.01 | 3.36 | improved; duration change -1.65 min |
| 1093413 | 4 | 142.17 | 156.84 | 14.67 | 4.76 | 4.51 | improved; duration change -0.25 min |
| 1093505 | 4 | 183.61 | 126.65 | -56.96 | 3.67 | 3.84 | slower; duration change 0.18 min |
| 1093515 | 3 | - | - | - | - | - | not enough popup-on sessions |
| 1095564 | 4 | 226.17 | 208.37 | -17.80 | 3.10 | 2.75 | slower; duration change -0.35 min |
| 1097463 | 4 | 162.68 | 160.20 | -2.48 | 3.44 | 3.74 | stable; duration change 0.30 min |
| 1100496 | 4 | 151.01 | 125.35 | -25.66 | 4.61 | 4.40 | slower; duration change -0.21 min |
| 1100497 | 4 | 110.18 | 151.50 | 41.31 | 4.62 | 4.08 | improved; duration change -0.55 min |
| 1100613 | 4 | 133.27 | 116.58 | -16.69 | 3.83 | 5.67 | slower; duration change 1.83 min |
| 1100663 | 4 | 123.95 | 144.58 | 20.64 | 4.55 | 4.43 | improved; duration change -0.12 min |
| 1100758 | 4 | 108.12 | 135.19 | 27.06 | 5.21 | 4.22 | improved; duration change -0.99 min |
| 1103080 | 3 | - | - | - | - | - | not enough popup-on sessions |
| 1104782 | 4 | 111.80 | 87.37 | -24.43 | 6.27 | 7.44 | slower; duration change 1.17 min |
| 1104806 | 4 | 126.25 | 103.76 | -22.49 | 5.21 | 6.58 | slower; duration change 1.37 min |
| 1104816 | 4 | 125.91 | 137.28 | 11.37 | 5.68 | 3.99 | improved; duration change -1.69 min |
| 1104818 | 4 | 168.63 | 190.67 | 22.04 | 4.20 | 3.64 | improved; duration change -0.56 min |
| 1108323 | 4 | 145.10 | 179.47 | 34.36 | 4.48 | 3.92 | improved; duration change -0.57 min |
| 1108328 | 3 | - | - | - | - | - | not enough popup-on sessions |
| 1108330 | 3 | - | - | - | - | - | not enough popup-on sessions |
| 1108335 | 4 | 150.61 | 95.36 | -55.25 | 3.85 | 7.40 | slower; duration change 3.55 min |
| 1108339 | 3 | - | - | - | - | - | not enough popup-on sessions |
| 1108344 | 4 | 154.59 | 164.90 | 10.30 | 4.43 | 3.76 | improved; duration change -0.66 min |
| 1108346 | 4 | 151.79 | 183.77 | 31.99 | 3.65 | 3.47 | improved; duration change -0.18 min |
| 1108348 | 4 | 92.76 | 127.26 | 34.50 | 5.85 | 4.42 | improved; duration change -1.43 min |
| 1108349 | 4 | 237.81 | 232.50 | -5.31 | 2.96 | 2.55 | slower; duration change -0.42 min |
| 1108353 | 1 | - | - | - | - | - | not enough popup-on sessions |
| 1108357 | 4 | 122.93 | 112.92 | -10.01 | 3.80 | 5.90 | slower; duration change 2.10 min |
| 1108360 | 5 | 152.99 | 273.90 | 120.91 | 3.93 | 1.86 | improved; duration change -2.06 min |
| 1108364 | 4 | 102.46 | 118.32 | 15.85 | 5.67 | 6.19 | improved; duration change 0.51 min |
| 1108365 | 4 | 190.83 | 228.39 | 37.56 | 3.71 | 2.99 | improved; duration change -0.72 min |
| 1108367 | 4 | 204.64 | 187.58 | -17.06 | 2.90 | 3.99 | slower; duration change 1.09 min |
| 1108382 | 4 | 119.34 | 125.90 | 6.56 | 5.80 | 5.35 | improved; duration change -0.45 min |
| 1108387 | 3 | - | - | - | - | - | not enough popup-on sessions |
| 1112096 | 3 | - | - | - | - | - | not enough popup-on sessions |
| 1112106 | 3 | - | - | - | - | - | not enough popup-on sessions |
| 1112115 | 4 | 178.60 | 153.33 | -25.26 | 3.20 | 4.05 | slower; duration change 0.85 min |
| 1112119c | 3 | - | - | - | - | - | not enough popup-on sessions |
| 1112121 | 4 | 213.99 | 211.72 | -2.27 | 2.45 | 2.95 | stable; duration change 0.50 min |
| 1112139 | 4 | 83.65 | 184.97 | 101.32 | 8.41 | 3.08 | improved; duration change -5.33 min |

Η ερώτηση εδώ είναι συγκεκριμένα για popup-on. Αν ένας user έχει λιγότερα από 4 matched popup-on sessions, δεν υπάρχει αρκετό υλικό για first2/last2 comparison, οπότε δεν βγαίνει συμπέρασμα για learning/adaptation μέσα στο popup-on condition.

## Overall Chronological Speed Change Across All Sessions
Αυτό είναι δευτερεύον check, ανεξάρτητα από popup condition. Συγκρίνει τα πρώτα 2 matched sessions κάθε user με τα τελευταία 2 matched sessions του ίδιου user. Είναι πιο αδύναμο ως συμπέρασμα γιατί ανακατεύει διαφορετικά texts, επίπεδα δυσκολίας και popup conditions.

| result | users | percent |
| --- | --- | --- |
| Improved WPM in last 2 vs first 2 | 31 | 62.0% |
| Slower WPM in last 2 vs first 2 | 13 | 26.0% |
| Stable / small change within +/-5 WPM | 6 | 12.0% |

| user | matched sessions | first2 WPM | last2 WPM | WPM change | interpretation |
| --- | --- | --- | --- | --- | --- |
| 1059657 | 8 | 128.26 | 124.63 | -3.63 | stable |
| 1065023 | 8 | 106.65 | 138.14 | 31.49 | improved |
| 1070729 | 8 | 151.81 | 163.54 | 11.74 | improved |
| 1080401 | 8 | 88.32 | 62.59 | -25.72 | slower |
| 1084609 | 8 | 88.18 | 186.45 | 98.27 | improved |
| 1090053 | 8 | 149.43 | 148.04 | -1.39 | stable |
| 1093313 | 6 | 133.79 | 140.48 | 6.68 | improved |
| 1093322 | 5 | 106.46 | 131.94 | 25.47 | improved |
| 1093332 | 8 | 99.46 | 135.40 | 35.94 | improved |
| 1093348 | 8 | 102.07 | 107.75 | 5.68 | improved |
| 1093379 | 8 | 93.89 | 101.74 | 7.85 | improved |
| 1093390 | 8 | 140.65 | 113.12 | -27.53 | slower |
| 1093403 | 8 | 135.33 | 180.76 | 45.43 | improved |
| 1093413 | 7 | 122.47 | 155.76 | 33.29 | improved |
| 1093505 | 8 | 150.61 | 145.31 | -5.31 | slower |
| 1093515 | 6 | 125.75 | 135.55 | 9.80 | improved |
| 1095564 | 6 | 226.17 | 213.90 | -12.27 | slower |
| 1097463 | 8 | 129.29 | 172.05 | 42.76 | improved |
| 1100496 | 8 | 133.56 | 169.44 | 35.88 | improved |
| 1100497 | 8 | 137.43 | 160.88 | 23.45 | improved |
| 1100613 | 8 | 133.18 | 129.30 | -3.89 | stable |
| 1100663 | 8 | 146.28 | 124.30 | -21.98 | slower |
| 1100758 | 8 | 97.32 | 154.80 | 57.48 | improved |
| 1103080 | 6 | 275.06 | 184.48 | -90.58 | slower |
| 1104782 | 8 | 101.00 | 112.00 | 11.00 | improved |
| 1104806 | 8 | 144.42 | 121.52 | -22.90 | slower |
| 1104816 | 8 | 115.12 | 182.16 | 67.05 | improved |
| 1104818 | 8 | 170.73 | 190.68 | 19.95 | improved |
| 1108323 | 8 | 125.74 | 193.60 | 67.86 | improved |
| 1108328 | 5 | 140.91 | 150.41 | 9.49 | improved |
| 1108330 | 7 | 89.39 | 142.83 | 53.43 | improved |
| 1108335 | 8 | 146.41 | 99.53 | -46.88 | slower |
| 1108339 | 8 | 155.12 | 152.98 | -2.14 | stable |
| 1108344 | 8 | 159.50 | 168.35 | 8.85 | improved |
| 1108346 | 8 | 167.92 | 171.87 | 3.95 | stable |
| 1108348 | 8 | 105.81 | 117.99 | 12.18 | improved |
| 1108349 | 8 | 187.57 | 258.14 | 70.57 | improved |
| 1108357 | 8 | 114.17 | 96.55 | -17.62 | slower |
| 1108360 | 8 | 172.04 | 244.49 | 72.46 | improved |
| 1108364 | 8 | 120.68 | 125.03 | 4.35 | stable |
| 1108365 | 8 | 160.97 | 180.85 | 19.88 | improved |
| 1108367 | 8 | 189.38 | 180.46 | -8.92 | slower |
| 1108382 | 7 | 111.98 | 118.45 | 6.48 | improved |
| 1108387 | 6 | 110.47 | 101.93 | -8.54 | slower |
| 1112096 | 4 | 85.33 | 96.25 | 10.92 | improved |
| 1112106 | 7 | 115.66 | 216.83 | 101.17 | improved |
| 1112115 | 8 | 166.94 | 161.63 | -5.31 | slower |
| 1112119c | 5 | 140.16 | 110.47 | -29.69 | slower |
| 1112121 | 7 | 171.43 | 215.96 | 44.53 | improved |
| 1112139 | 8 | 66.16 | 217.73 | 151.58 | improved |

## Interpretation

- Στο συνολικό descriptive average, το popup-on είναι ελαφρώς πιο γρήγορο από το popup-off, τόσο σε λεπτά όσο και σε WPM.
- Η user-level εικόνα είναι πιο σημαντική από το raw overall mean, γιατί κάθε participant λειτουργεί ως δικό του control. Αν ένας user είναι συνολικά αργός ή γρήγορος, αυτό επηρεάζει και τα δύο conditions του.
- Το popup-off δεν σημαίνει ότι ο eye-tracker δεν δουλεύει. Σημαίνει ότι ο participant δεν βλέπει την άμεση μετάφραση στο σύστημα και πρέπει να χρησιμοποιήσει εξωτερικό εργαλείο, κάτι που λογικά μπορεί να αυξήσει τον χρόνο ανάγνωσης.
- Τα per-text differences είναι απαραίτητα γιατί κάποια κείμενα έχουν διαφορετικό word count και δυσκολία. Η σύγκριση WPM διορθώνει ως ένα βαθμό το διαφορετικό μήκος, αλλά όχι πλήρως τη δυσκολία, το θέμα και την εξοικείωση του user.
- Το first2/last2 popup-on comparison είναι ένδειξη πιθανής εξοικείωσης με το σύστημα. Δεν αποδεικνύει μόνο του learning effect, γιατί τα τελευταία sessions μπορεί να ήταν πιο εύκολα ή διαφορετικού μήκους.

## Output Files

- User popup on/off comparison: `time_analysis_user_popup_comparison.csv`
- Popup-on first2/last2 progress: `time_analysis_popup_on_progress.csv`
- Existing per-session timing stats from the previous export: `quiz_analysis_session_timing_stats.csv`
