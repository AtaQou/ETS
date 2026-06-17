# Quiz and Experiment Statistics Report

Αυτό το report ενώνει τα Google Forms quiz exports με το current analysis database. Εστιάζει στο comprehension score, στο `translationOutputMode` (`on/off`), στη συμπεριφορά ανάγνωσης που έχει καταγραφεί στο DB, και στη μεταβολή του SUS μετά από χρήση του συστήματος.

## Important Interpretation Notes

- Σε αυτό το experiment το eye-tracker λειτουργεί και στις δύο συνθήκες.
- Η βασική experimental condition είναι το `translationOutputMode`: `on` σημαίνει ότι ο participant έβλεπε το in-system translation popup κατά την ανάγνωση, ενώ `off` σημαίνει ότι δεν εμφανιζόταν popup και ο participant έπρεπε να χρησιμοποιήσει εξωτερικό εργαλείο/σελίδα μετάφρασης.
- Όταν υπήρχαν πολλά sessions για το ίδιο user/PDF, το quiz response αντιστοιχίστηκε στο session που ταίριαζε καλύτερα χρονικά με το quiz, αποφεύγοντας πολύ σύντομα setup segments όταν υπήρχε πιο πιθανό reading session.
- Αν ένα selected session άλλαξε popup mode μέσα στο ίδιο session, χρησιμοποιείται το final logged mode, επειδή αυτό πιθανότερα αντιστοιχεί στη διορθωμένη ρύθμιση μετά το αρχικό λάθος.
- Αν υπάρχει quiz αλλά δεν βρέθηκε αντίστοιχο DB session, condition γίνεται inferred μόνο όταν ο user έχει ακριβώς 8 unique quiz PDFs και το missing mode προκύπτει μονοσήμαντα από το αναμενόμενο 4-on/4-off balance. Αυτά τα rows χρησιμοποιούνται μόνο για quiz/condition stats, όχι για behavioral correlations.
- Το `showGazeCursor` αναφέρεται χωριστά. Είναι UI setting για το αν φαινόταν ο gaze cursor, όχι η βασική popup-translation condition.
- Για να μειωθεί το bias από τη δυσκολία κάθε PDF, αναφέρονται και raw score percentages και PDF-normalized z-scores. Z-score πάνω από 0 σημαίνει ότι ο participant πήγε καλύτερα από τον μέσο όρο του ίδιου PDF quiz.
- Τα αποτελέσματα είναι descriptive/observational summaries και όχι απόδειξη αιτιότητας. Το condition assignment, missing texts, timing corrections και duplicate setup sessions μπορούν να επηρεάσουν την ερμηνεία.

## Data Coverage

| Metric | Value |
| --- | --- |
| Quiz exports που διαβάστηκαν | 10 |
| Raw quiz responses | 402 |
| Πραγματικά DB-matched user/PDF quiz rows | 377 |
| Inferred condition-only quiz rows | 4 |
| Συνολικά quiz rows που χρησιμοποιούνται στα comprehension stats | 381 |
| Unresolved unmatched quiz responses | 19 |
| Candidate user/PDF pairs στο DB | 379 |
| Unique DB sessions που χρησιμοποιήθηκαν μετά το matching | 377 |
| Participants με usable quiz data | 51 |
| Overall quiz score | n=381, μέσος=78.65, διάμεσος=80.00, ΤΑ=21.77, εύρος=0.00-100.00 |

Τα unresolved unmatched responses είναι κυρίως blank/test IDs ή user/PDF quiz responses χωρίς αντίστοιχο DB session. Πρώτα παραδείγματα:
- `1093515` / `b2_animals_of_rainforests_1.pdf`: 1 response(s)
- `1093515` / `b2_electromagnetic_radiation_2.pdf`: 1 response(s)
- `1112096` / `b2_sticky_fingers_4.pdf`: 1 response(s)
- `110833` / `b2_sticky_fingers_4.pdf`: 1 response(s)
- `1112096` / `c1_age_of_exploration_1.pdf`: 1 response(s)
- `1108328` / `c1_age_of_exploration_1.pdf`: 1 response(s)
- `1093313` / `c1_age_of_exploration_1.pdf`: 1 response(s)
- `1093313` / `c1_bee_reading_2.pdf`: 1 response(s)
- `1108328` / `c1_bee_reading_2.pdf`: 1 response(s)
- `` / `c1_walt_disney_4.pdf`: 1 response(s)
- `1112119` / `c1_walt_disney_4.pdf`: 1 response(s)
- `1108328` / `c2_noisy_humans_1.pdf`: 1 response(s)
- `1093322` / `c2_noisy_humans_1.pdf`: 1 response(s)
- `1108387` / `c2_noisy_humans_1.pdf`: 1 response(s)
- `1112119` / `c2_noisy_humans_1.pdf`: 1 response(s)

## Condition Assignment Check

Το intended design είναι ένα quiz ανά text ανά participant, με 8 usable quiz/text observations ανά participant: 4 popup-on και 4 popup-off.
| Metric | Value |
| --- | --- |
| Participants με usable quiz data | 51 |
| Participants με ακριβώς 8 usable quizzes | 40 |
| Participants με ακριβώς 4 popup-on και 4 popup-off | 38 |
| Participants που θέλουν condition/count review | 13 |
| Rows που επιλέχθηκαν από user/PDFs με multiple candidate sessions | 43 |
| Selected rows όπου το popup mode άλλαξε μέσα στο ίδιο session | 1 |

Participants που δεν ταιριάζουν στο expected 8 total / 4-on / 4-off pattern:
| User | usable quizzes | popup on | popup off | other |
| --- | --- | --- | --- | --- |
| 1093313 | 6 | 3 | 3 | 0 |
| 1093322 | 5 | 2 | 3 | 0 |
| 1093515 | 6 | 3 | 3 | 0 |
| 1108328 | 5 | 3 | 2 | 0 |
| 1108330 | 7 | 3 | 4 | 0 |
| 1108339 | 8 | 3 | 5 | 0 |
| 1108353 | 2 | 1 | 1 | 0 |
| 1108360 | 8 | 5 | 3 | 0 |
| 1108387 | 6 | 3 | 3 | 0 |
| 1112096 | 5 | 4 | 1 | 0 |
| 1112106 | 7 | 3 | 4 | 0 |
| 1112119c | 5 | 3 | 2 | 0 |
| 1112121 | 7 | 4 | 3 | 0 |

Selected session(s) με popup-mode switch μέσα στο ίδιο session. Για το condition label χρησιμοποιήθηκε το final mode:
| User | PDF | start | end | logged modes | used mode |
| --- | --- | --- | --- | --- | --- |
| 1108339 | c1_bee_reading_2.pdf | 2026-05-19T10:30:43.850 | 2026-05-19T10:34:32.105 | off:17, on:14 | off |

### Missing Session Review

Ο παρακάτω πίνακας εξηγεί γιατί κάποια quiz rows δεν έγιναν απλό DB match. Τα `used_with_inferred_condition` μπήκαν στα quiz/condition stats με inferred `on/off`. Τα `not_used_no_user_pdf_session` δεν μπήκαν στα stats γιατί δεν μπορούσε να βγει ασφαλές PDF-specific condition.
Συμπέρασμα για τα ΑΜ με λιγότερα από 8 usable rows: στις περισσότερες περιπτώσεις το quiz υπάρχει στο Google Forms, αλλά στο current DB δεν υπάρχει `translation_events` row με το ίδιο user και το ίδιο PDF. Όταν το 4-on/4-off balance έκανε το missing condition μονοσήμαντο, το quiz κρατήθηκε ως inferred condition-only row.
| User | PDF | quiz time | status | condition | reason | nearby DB evidence |
| --- | --- | --- | --- | --- | --- | --- |
| 1093313 | c1_age_of_exploration_1.pdf | 2026/05/21 9:49:35 π.μ. GMT+3 | not_used_no_user_pdf_session |  | Υπάρχει quiz response, αλλά στο current DB δεν υπάρχει text session με ίδιο user και ίδιο PDF. | Δεν βρέθηκε κοντινό session στο DB για την ίδια ημέρα. |
| 1093313 | c1_bee_reading_2.pdf | 2026/05/21 9:54:33 π.μ. GMT+3 | not_used_no_user_pdf_session |  | Υπάρχει quiz response, αλλά στο current DB δεν υπάρχει text session με ίδιο user και ίδιο PDF. | Δεν βρέθηκε κοντινό session στο DB για την ίδια ημέρα. |
| 1093322 | c2_noisy_humans_1.pdf | 2026/05/25 10:48:03 π.μ. GMT+3 | not_used_no_user_pdf_session |  | Υπάρχει quiz response, αλλά στο current DB δεν υπάρχει text session με ίδιο user και ίδιο PDF. | Δεν βρέθηκε κοντινό session στο DB για την ίδια ημέρα. |
| 1093322 | c2_rosa_parks_2.pdf | 2026/05/25 10:54:21 π.μ. GMT+3 | not_used_no_user_pdf_session |  | Υπάρχει quiz response, αλλά στο current DB δεν υπάρχει text session με ίδιο user και ίδιο PDF. | Δεν βρέθηκε κοντινό session στο DB για την ίδια ημέρα. |
| 1093515 | b2_electromagnetic_radiation_2.pdf | 2026/05/25 6:57:11 μ.μ. GMT+3 | not_used_no_user_pdf_session |  | Υπάρχει quiz response, αλλά στο current DB δεν υπάρχει text session με ίδιο user και ίδιο PDF. | Δεν βρέθηκε κοντινό session στο DB για την ίδια ημέρα. |
| 1093515 | b2_animals_of_rainforests_1.pdf | 2026/05/25 7:04:43 μ.μ. GMT+3 | not_used_no_user_pdf_session |  | Υπάρχει quiz response, αλλά στο current DB δεν υπάρχει text session με ίδιο user και ίδιο PDF. | Δεν βρέθηκε κοντινό session στο DB για την ίδια ημέρα. |
| 1095564 | c2_rosa_parks_2.pdf | 2026/05/25 5:11:10 μ.μ. GMT+3 | used_with_inferred_condition | off | Ο user είχε 8 unique quiz PDFs και 4 popup-on / 2 popup-off DB-matched sessions. Για να συμπληρωθεί το αναμενόμενο 4-on/4-off, το missing PDF ταξινομήθηκε ως `off`. | 2026-05-25T17:04:45->2026-05-25T17:04:47 docs=NO_TRANSLATION_EVENTS modes=on events=0 reason=manual_disconnect; 2026-05-25T17:04:51->2026-05-25T17:07:29 docs=eye_tracking_validation_simple_2pages.pdf modes=on... |
| 1095564 | b2_electromagnetic_radiation_2.pdf | 2026/05/28 3:23:13 μ.μ. GMT+3 | used_with_inferred_condition | off | Ο user είχε 8 unique quiz PDFs και 4 popup-on / 2 popup-off DB-matched sessions. Για να συμπληρωθεί το αναμενόμενο 4-on/4-off, το missing PDF ταξινομήθηκε ως `off`. | 2026-05-28T15:18:36->2026-05-28T15:18:45 docs=NO_TRANSLATION_EVENTS modes=on events=0 reason=translation_output_mode_changed; 2026-05-28T15:18:45->2026-05-28T15:21:37 docs=NO_TRANSLATION_EVENTS modes=on events=0... |
| 1103080 | c1_walt_disney_4.pdf | 2026/06/04 3:47:05 μ.μ. GMT+3 | used_with_inferred_condition | off | Ο user είχε 8 unique quiz PDFs και 4 popup-on / 3 popup-off DB-matched sessions. Για να συμπληρωθεί το αναμενόμενο 4-on/4-off, το missing PDF ταξινομήθηκε ως `off`. | 2026-06-04T15:35:54->2026-06-04T15:39:38 docs=c1_age_of_exploration_1.pdf modes=on events=8 reason=manual_disconnect; 2026-06-04T15:41:40->2026-06-04T15:41:46 docs=NO_TRANSLATION_EVENTS modes=on events=0... |
| 1108328 | c1_age_of_exploration_1.pdf | 2026/05/19 6:55:57 μ.μ. GMT+3 | not_used_no_user_pdf_session |  | Υπάρχει quiz response, αλλά στο current DB δεν υπάρχει text session με ίδιο user και ίδιο PDF. | 2026-05-19T18:35:48->2026-05-19T18:36:07 docs=NO_TRANSLATION_EVENTS modes=on events=0 reason=manual_disconnect; 2026-05-19T18:38:34->2026-05-19T18:39:59.672 docs=eye_tracking_validation_simple_2pages.pdf modes=on... |
| 1108328 | c1_bee_reading_2.pdf | 2026/05/21 10:55:21 π.μ. GMT+3 | not_used_no_user_pdf_session |  | Υπάρχει quiz response, αλλά στο current DB δεν υπάρχει text session με ίδιο user και ίδιο PDF. | 2026-05-21T10:08:52->2026-05-21T10:10:47 docs=eye_tracking_validation_simple_2pages.pdf modes=on events=5 reason=translation_output_mode_changed; 2026-05-21T10:10:47->2026-05-21T10:10:51 docs=NO_TRANSLATION_EVENTS... |
| 1108328 | c2_noisy_humans_1.pdf | 2026/05/25 10:13:56 π.μ. GMT+3 | not_used_no_user_pdf_session |  | Υπάρχει quiz response, αλλά στο current DB δεν υπάρχει text session με ίδιο user και ίδιο PDF. | Δεν βρέθηκε κοντινό session στο DB για την ίδια ημέρα. |
| 1108328 | c2_rosa_parks_2.pdf | 2026/05/25 10:19:04 π.μ. GMT+3 | not_used_no_user_pdf_session |  | Υπάρχει quiz response, αλλά στο current DB δεν υπάρχει text session με ίδιο user και ίδιο PDF. | Δεν βρέθηκε κοντινό session στο DB για την ίδια ημέρα. |
| 1108382 | c2_rosa_parks_2.pdf | 2026/05/19 2:57:08 μ.μ. GMT+3 | used_with_inferred_condition | off | Ο user είχε 8 unique quiz PDFs και 4 popup-on / 3 popup-off DB-matched sessions. Για να συμπληρωθεί το αναμενόμενο 4-on/4-off, το missing PDF ταξινομήθηκε ως `off`. | 2026-05-19T14:58:41->2026-05-19T14:58:48 docs=c2_noisy_humans_1.pdf modes=on events=1 reason=manual_disconnect; 2026-05-19T14:59:44->2026-05-19T15:05:59 docs=c2_noisy_humans_1.pdf modes=on events=103... |
| 1108387 | c2_noisy_humans_1.pdf | 2026/05/26 9:42:55 π.μ. GMT+3 | not_used_no_user_pdf_session |  | Υπάρχει quiz response, αλλά στο current DB δεν υπάρχει text session με ίδιο user και ίδιο PDF. | Δεν βρέθηκε κοντινό session στο DB για την ίδια ημέρα. |
| 1108387 | c2_rosa_parks_2.pdf | 2026/05/26 9:51:18 π.μ. GMT+3 | not_used_no_user_pdf_session |  | Υπάρχει quiz response, αλλά στο current DB δεν υπάρχει text session με ίδιο user και ίδιο PDF. | Δεν βρέθηκε κοντινό session στο DB για την ίδια ημέρα. |
| 1112096 | b2_sticky_fingers_4.pdf | 2026/05/18 6:32:30 μ.μ. GMT+3 | not_used_no_user_pdf_session |  | Υπάρχει quiz response, αλλά στο current DB δεν υπάρχει text session με ίδιο user και ίδιο PDF. | 2026-05-18T18:06:55->2026-05-18T18:10:52 docs=eye_tracking_validation_simple_2pages.pdf modes=on events=56 reason=document_changed; 2026-05-18T18:10:52->2026-05-18T18:19:08 docs=b2_animals_of_rainforests_1.pdf... |
| 1112096 | c1_age_of_exploration_1.pdf | 2026/05/19 2:09:11 μ.μ. GMT+3 | not_used_no_user_pdf_session |  | Υπάρχει quiz response, αλλά στο current DB δεν υπάρχει text session με ίδιο user και ίδιο PDF. | 2026-05-19T13:43:47->2026-05-19T13:43:58 docs=NO_TRANSLATION_EVENTS modes=off events=2 reason=manual_disconnect; 2026-05-19T13:44:00->2026-05-19T13:44:08 docs=NO_TRANSLATION_EVENTS modes=on events=0... |
| 1112119c | c2_noisy_humans_1.pdf | 2026/05/26 10:21:35 π.μ. GMT+3 | not_used_no_user_pdf_session |  | Υπάρχει quiz response, αλλά στο current DB δεν υπάρχει text session με ίδιο user και ίδιο PDF. | Δεν βρέθηκε κοντινό session στο DB για την ίδια ημέρα. |
| 1112119c | c2_rosa_parks_2.pdf | 2026/05/26 10:29:20 π.μ. GMT+3 | not_used_no_user_pdf_session |  | Υπάρχει quiz response, αλλά στο current DB δεν υπάρχει text session με ίδιο user και ίδιο PDF. | Δεν βρέθηκε κοντινό session στο DB για την ίδια ημέρα. |
| 1112119c | c1_walt_disney_4.pdf | 2026/05/27 10:43:02 π.μ. GMT+3 | not_used_no_user_pdf_session |  | Υπάρχει quiz response, αλλά στο current DB δεν υπάρχει text session με ίδιο user και ίδιο PDF. | 2026-05-27T10:44:03->2026-05-27T10:49:15 docs=c1_bee_reading_2.pdf modes=on events=18 reason=manual_disconnect |

## Quiz Performance by Difficulty Level
| Level | n | Μέσο % | Διάμεσος % | ΤΑ | Εύρος |
| --- | --- | --- | --- | --- | --- |
| B2 | 148 | 81.53 | 80.00 | 18.66 | 20.00-100.00 |
| C1 | 141 | 82.98 | 80.00 | 19.11 | 20.00-100.00 |
| C2 | 92 | 67.39 | 80.00 | 26.14 | 0.00-100.00 |

## Quiz Performance by PDF
| PDF | Level | n | Μέσο % | Διάμεσος % | ΤΑ |
| --- | --- | --- | --- | --- | --- |
| b2_animals_of_rainforests_1.pdf | B2 | 36 | 82.41 | 83.33 | 19.50 |
| b2_electromagnetic_radiation_2.pdf | B2 | 40 | 69.50 | 80.00 | 20.25 |
| b2_first_american_3.pdf | B2 | 34 | 87.65 | 80.00 | 13.04 |
| b2_sticky_fingers_4.pdf | B2 | 38 | 87.89 | 90.00 | 14.36 |
| c1_age_of_exploration_1.pdf | C1 | 35 | 84.00 | 80.00 | 15.94 |
| c1_bee_reading_2.pdf | C1 | 35 | 89.14 | 100.00 | 16.34 |
| c1_native_american_conflicts_3.pdf | C1 | 34 | 82.35 | 90.00 | 21.89 |
| c1_walt_disney_4.pdf | C1 | 37 | 76.76 | 80.00 | 20.28 |
| c2_noisy_humans_1.pdf | C2 | 46 | 80.00 | 80.00 | 19.78 |
| c2_rosa_parks_2.pdf | C2 | 46 | 54.78 | 60.00 | 25.80 |

## Popup On vs Off ανά PDF

Εδώ συγκρίνεται κάθε κείμενο μόνο με τον εαυτό του: τι ποσοστό σωστών απαντήσεων είχαν οι participants όταν το ίδιο PDF διαβάστηκε με popup `on` σε σχέση με popup `off`. Αυτό είναι πιο καθαρό από το overall comparison, γιατί η δυσκολία του PDF μένει σταθερή μέσα σε κάθε row.
| PDF | Level | on n | on μέσο % | off n | off μέσο % | on-off | d | ερμηνεία |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| b2_animals_of_rainforests_1.pdf | B2 | 17 | 84.31 | 19 | 80.70 | 3.61 | 0.183 | ουσιαστικά μικρή/ουδέτερη διαφορά; usable n |
| b2_electromagnetic_radiation_2.pdf | B2 | 18 | 67.78 | 22 | 70.91 | -3.13 | -0.153 | ουσιαστικά μικρή/ουδέτερη διαφορά; usable n |
| b2_first_american_3.pdf | B2 | 20 | 87.00 | 14 | 88.57 | -1.57 | -0.119 | ουσιαστικά μικρή/ουδέτερη διαφορά; usable n |
| b2_sticky_fingers_4.pdf | B2 | 20 | 91.00 | 18 | 84.44 | 6.56 | 0.463 | πιθανό benefit με popup-on; usable n |
| c1_age_of_exploration_1.pdf | C1 | 20 | 82.00 | 15 | 86.67 | -4.67 | -0.292 | ουσιαστικά μικρή/ουδέτερη διαφορά; usable n |
| c1_bee_reading_2.pdf | C1 | 16 | 90.00 | 19 | 88.42 | 1.58 | 0.095 | ουσιαστικά μικρή/ουδέτερη διαφορά; usable n |
| c1_native_american_conflicts_3.pdf | C1 | 13 | 86.15 | 21 | 80.00 | 6.15 | 0.280 | πιθανό benefit με popup-on; usable n |
| c1_walt_disney_4.pdf | C1 | 22 | 76.36 | 15 | 77.33 | -0.97 | -0.047 | ουσιαστικά μικρή/ουδέτερη διαφορά; usable n |
| c2_noisy_humans_1.pdf | C2 | 23 | 78.26 | 23 | 81.74 | -3.48 | -0.175 | ουσιαστικά μικρή/ουδέτερη διαφορά; usable n |
| c2_rosa_parks_2.pdf | C2 | 23 | 54.78 | 23 | 54.78 | 0.00 | 0.000 | ουσιαστικά μικρή/ουδέτερη διαφορά; usable n |

Σύντομη ανάγνωση: το μεγαλύτερο positive difference υπέρ του popup-on είναι στο `b2_sticky_fingers_4.pdf` με 6.56 percentage points. Το μεγαλύτερο negative difference είναι στο `c1_age_of_exploration_1.pdf` με -4.67 percentage points, δηλαδή καλύτερο score στο popup-off/external translation.
Με threshold ±5 percentage points: 2 PDFs δείχνουν πιθανό benefit υπέρ popup-on, 0 PDFs δείχνουν πιθανό benefit υπέρ popup-off/external translation, και 8 PDFs είναι πρακτικά ουδέτερα.

## Popup Translation Output: On vs Off

Αυτή είναι η βασική experimental comparison. Και στις δύο περιπτώσεις το eye-tracker ήταν ενεργό. `on` σημαίνει ότι ο participant έβλεπε το translation popup μέσα στο reading system. `off` σημαίνει ότι έπρεπε να μεταφράσει εξωτερικά, π.χ. με Google Translate.
| Popup mode | n | Μέσο % | Διάμεσος % | ΤΑ | Μέσο PDF-z | Διάμεσος PDF-z |
| --- | --- | --- | --- | --- | --- | --- |
| on | 192 | 78.92 | 80.00 | 22.20 | 0.008 | 0.160 |
| off | 189 | 78.38 | 80.00 | 21.37 | -0.008 | 0.047 |

Raw popup-on μείον popup-off μέση διαφορά: **0.55 percentage points**; independent-groups Cohen's d = **0.025**.
PDF-normalized popup-on μείον popup-off μέση διαφορά: **0.017 z-score units**.

### Popup Mode by Level
| Level | Popup | n | Μέσο % | Διάμεσος % | ΤΑ |
| --- | --- | --- | --- | --- | --- |
| B2 | on | 75 | 82.84 | 80.00 | 18.52 |
| B2 | off | 73 | 80.18 | 80.00 | 18.83 |
| C1 | on | 71 | 82.82 | 80.00 | 19.51 |
| C1 | off | 70 | 83.14 | 80.00 | 18.85 |
| C2 | on | 46 | 66.52 | 70.00 | 27.02 |
| C2 | off | 46 | 68.26 | 80.00 | 25.50 |

### Within-Participant Popup Comparison
Participants με popup-on και popup-off quiz rows: **51**.
Μέση within-participant διαφορά popup-on μείον popup-off: **1.22 percentage points**; διάμεσος **0.00**; paired Cohen's d = **0.081**.
Users με υψηλότερο score στο popup-on / ίσο / υψηλότερο στο popup-off: **23 / 8 / 20**.
| Level | paired users | Μέσο on-off | Διάμεσος | ΤΑ | paired d |
| --- | --- | --- | --- | --- | --- |
| B2 | 48 | 3.60 | 1.66 | 19.26 | 0.187 |
| C1 | 44 | -0.68 | 0.00 | 16.62 | -0.041 |
| C2 | 46 | -1.74 | 0.00 | 37.67 | -0.046 |

### Largest Individual Popup Differences
Θετικές τιμές σημαίνουν ότι ο participant είχε υψηλότερο score με το in-system popup. Αρνητικές τιμές σημαίνουν υψηλότερο score όταν χρησιμοποιούσε εξωτερική μετάφραση.
| User | popup-on μέσο % | popup-off μέσο % | on-off |
| --- | --- | --- | --- |
| 1112096 | 48.33 | 0.00 | 48.33 |
| 1100758 | 60.00 | 90.00 | -30.00 |
| 1097463 | 65.00 | 90.83 | -25.83 |
| 1104816 | 95.83 | 70.00 | 25.83 |
| 1065023 | 60.00 | 85.00 | -25.00 |
| 1070729 | 70.00 | 95.00 | -25.00 |
| 1093403 | 70.00 | 45.00 | 25.00 |
| 1108365 | 95.00 | 70.00 | 25.00 |
| 1084609 | 95.00 | 71.67 | 23.33 |
| 1112119c | 100.00 | 80.00 | 20.00 |
| 1108364 | 80.00 | 60.00 | 20.00 |
| 1093515 | 80.00 | 100.00 | -20.00 |
| 1104818 | 100.00 | 80.83 | 19.17 |
| 1093322 | 70.00 | 88.89 | -18.89 |
| 1112106 | 46.67 | 65.00 | -18.33 |

## Eye-Tracker and Gaze-Cursor Fields

Όλα τα πραγματικά DB-matched quiz/session rows έχουν tracker connection: **377 / 377**. Rows χωρίς tracker connection: **0**.
Αυτό επιβεβαιώνει ότι οι συνθήκες popup-on και popup-off είναι και οι δύο eye-tracker sessions. Τα inferred condition-only rows δεν μετριούνται εδώ, επειδή δεν έχουν πραγματικό DB session row.

### Gaze Cursor Visible vs Hidden
| Gaze cursor | n | Μέσο % | Διάμεσος % | ΤΑ | Μέσο PDF-z |
| --- | --- | --- | --- | --- | --- |
| visible | 281 | 78.71 | 80.00 | 21.37 | -0.018 |
| hidden | 96 | 78.65 | 80.00 | 22.81 | 0.028 |

Raw visible-minus-hidden μέση διαφορά: **0.06 percentage points**. Αυτό πρέπει να ερμηνευτεί μόνο ως UI/gaze-cursor comparison. Η βασική experimental condition παραμένει το popup translation on/off.

### Gaze Dwell Time Before Translation
Το `baseGazeSamples / 300` δίνει περίπου τον χρόνο gaze dwell σε δευτερόλεπτα πριν επιλεγεί μια λέξη για μετάφραση.
| Dwell sec | n | Μέσο % | Διάμεσος % | ΤΑ |
| --- | --- | --- | --- | --- |
| 0.13 | 5 | 84.00 | 80.00 | 8.94 |
| 0.20 | 23 | 73.91 | 80.00 | 17.51 |
| 0.75 | 5 | 46.67 | 40.00 | 12.47 |
| 1.00 | 181 | 78.16 | 80.00 | 22.44 |
| 1.17 | 8 | 90.00 | 100.00 | 15.12 |
| 1.33 | 11 | 80.30 | 100.00 | 28.30 |
| 1.50 | 131 | 81.20 | 80.00 | 19.91 |

## Behavioural Correlations

| Variable | n | Pearson r με score | Spearman rho |
| --- | --- | --- | --- |
| Διάρκεια ανάγνωσης σε λεπτά | 377 | -0.041 | -0.039 |
| Πλήθος μεταφράσεων | 377 | -0.121 | -0.184 |
| Unique translated source words | 377 | -0.118 | -0.172 |
| Μεταφράσεις ανά λεπτό | 377 | -0.116 | -0.234 |
| Μέγιστο κενό ανάμεσα σε μεταφράσεις, sec | 377 | 0.020 | 0.079 |
| Quiz delay μετά το session, λεπτά | 377 | -0.185 | -0.198 |
| Gaze dwell seconds | 377 | 0.089 | 0.124 |

## Change Over Time

Τα rows μπήκαν σε χρονολογική σειρά με βάση το matched DB session start time. Για inferred condition-only rows, όπου δεν υπάρχει DB session time, χρησιμοποιείται το quiz timestamp. Το raw score change είναι χρήσιμο, αλλά το PDF-normalized z-score change είναι ασφαλέστερο επειδή το πρώτο και τελευταίο text μπορεί να μην έχουν ίδια δυσκολία.
| Metric | Value |
| --- | --- |
| Users με τουλάχιστον 2 usable quiz rows | 51 |
| First quiz to last quiz raw change | n=51, μέσος=12.03, διάμεσος=3.33, ΤΑ=27.91, εύρος=-40.00-100.00 |
| First quiz to last quiz PDF-z change | n=51, μέσος=0.36, διάμεσος=0.20, ΤΑ=1.27, εύρος=-2.72-3.03 |
| Early half to late half raw change | n=51, μέσος=6.81, διάμεσος=7.50, ΤΑ=14.73, εύρος=-46.66-36.66 |
| Early half to late half PDF-z change | n=51, μέσος=0.16, διάμεσος=0.20, ΤΑ=0.60, εύρος=-1.16-1.41 |
| Complete 8-quiz users: early half to late half PDF-z change | n=40, μέσος=0.18, διάμεσος=0.22, ΤΑ=0.55, εύρος=-1.16-1.41 |
| PDF-z improved / unchanged / declined, all users | 31 / 0 / 20 |
| PDF-z improved / unchanged / declined, complete users | 25 / 0 / 15 |

Οι μεγαλύτερες individual early-to-late μεταβολές μετά από PDF normalization:
| User | quizzes | early z | late z | late-early z | first PDF | last PDF |
| --- | --- | --- | --- | --- | --- | --- |
| 1093332 | 8 | -0.817 | 0.589 | 1.406 | c1_walt_disney_4.pdf | b2_electromagnetic_radiation_2.pdf |
| 1093322 | 5 | -0.638 | 0.754 | 1.392 | b2_electromagnetic_radiation_2.pdf | b2_sticky_fingers_4.pdf |
| 1108357 | 8 | -0.660 | 0.659 | 1.319 | c2_noisy_humans_1.pdf | c1_native_american_conflicts_3.pdf |
| 1093379 | 8 | 0.703 | -0.459 | -1.162 | c1_walt_disney_4.pdf | c1_age_of_exploration_1.pdf |
| 1112096 | 5 | -1.312 | -2.461 | -1.149 | b2_animals_of_rainforests_1.pdf | c1_walt_disney_4.pdf |
| 1103080 | 8 | -0.331 | 0.647 | 0.978 | c1_bee_reading_2.pdf | c1_walt_disney_4.pdf |
| 1080401 | 8 | -0.972 | -0.099 | 0.873 | b2_first_american_3.pdf | c1_bee_reading_2.pdf |
| 1090053 | 8 | -0.145 | 0.697 | 0.842 | b2_sticky_fingers_4.pdf | c1_bee_reading_2.pdf |
| 1112106 | 7 | -1.044 | -0.218 | 0.826 | c2_rosa_parks_2.pdf | b2_electromagnetic_radiation_2.pdf |
| 1100496 | 8 | -0.190 | -0.999 | -0.809 | b2_first_american_3.pdf | b2_electromagnetic_radiation_2.pdf |
| 1108328 | 5 | -0.288 | 0.497 | 0.786 | c1_native_american_conflicts_3.pdf | b2_animals_of_rainforests_1.pdf |
| 1112115 | 8 | -0.617 | 0.086 | 0.702 | c2_noisy_humans_1.pdf | b2_animals_of_rainforests_1.pdf |

## Hardest Quiz Questions

Οι ερωτήσεις με τα χαμηλότερα average question scores στα usable responses. Αυτό βοηθά να εντοπιστούν comprehension items που ήταν γενικά δύσκολα, ανεξάρτητα από το system condition.
| PDF | Level | n | Μέσο question % | Question |
| --- | --- | --- | --- | --- |
| b2_electromagnetic_radiation_2.pdf | B2 | 40 | 17.50 | What does the author list in the passage? |
| c2_rosa_parks_2.pdf | C2 | 46 | 30.43 | What was the direct effect of Rosa Park’s civil disobedience? |
| c1_walt_disney_4.pdf | C1 | 37 | 32.43 | . Read these sentences from the text: “An important factor ensuring America’s ultimate victory over the Axis Powers in W |
| c2_rosa_parks_2.pdf | C2 | 46 | 36.96 | Through the Montgomery Bus Boycott, African-Americans showed they were tired of being treated as inferior to white Ameri |
| c2_rosa_parks_2.pdf | C2 | 46 | 50.00 | What was the main reason why President Obama gave this speech? |
| c1_age_of_exploration_1.pdf | C1 | 35 | 54.29 | Limited knowledge of world geography was a problem for early exploration. What evidence from the passage supports this c |
| b2_animals_of_rainforests_1.pdf | B2 | 36 | 55.56 | Tropical rainforests have optimal conditions for many animal species. What evidence from the text supports this conclusi |
| b2_sticky_fingers_4.pdf | B2 | 38 | 60.53 | What is this passage mostly about? |
| b2_first_american_3.pdf | B2 | 34 | 61.76 | Who were the “founding fathers”? |
| c2_noisy_humans_1.pdf | C2 | 46 | 65.22 | Noise pollution can be harmful to wildlife in protected areas. What evidence from the text supports this conclusion? |
| c1_native_american_conflicts_3.pdf | C1 | 34 | 67.65 | Read these sentences from the text. The consequences of European arrival to North America negatively affected the relati |
| c1_bee_reading_2.pdf | C1 | 35 | 68.57 | In the article, Kevin Hackett, the national program leader for the bee and pollination program at the U.S. Department of |
| c1_native_american_conflicts_3.pdf | C1 | 34 | 70.59 | Read these sentences from the text. The relationships Native American tribes had built with each other became tenuous as |
| c2_noisy_humans_1.pdf | C2 | 46 | 73.91 | What is the main idea of this article? |
| c2_rosa_parks_2.pdf | C2 | 46 | 73.91 | What is this passage mostly about? |

## SUS Usability Change

Το SUS υπολογίστηκε με την standard 0-100 formula: τα odd items δίνουν `response - 1`, τα even items δίνουν `5 - response`, και το άθροισμα πολλαπλασιάζεται με 2.5. Υψηλότερο score σημαίνει καλύτερη perceived usability.
| Metric | Value |
| --- | --- |
| Valid matched SUS submissions | 101 |
| Participants με paired first/last SUS | 50 |
| First SUS | n=50, μέσος=79.20, διάμεσος=80.00, ΤΑ=9.68, εύρος=50.00-100.00 |
| Second SUS | n=50, μέσος=80.85, διάμεσος=82.50, ΤΑ=9.74, εύρος=52.50-100.00 |
| Change second-first | n=50, μέσος=1.65, διάμεσος=2.50, ΤΑ=8.43, εύρος=-17.50-27.50 |
| Paired Cohen's d for SUS change | 0.196 |
| Improved / unchanged / declined | 26 / 7 / 17 |
| First SUS >= 68 | 44 / 50 |
| Second SUS >= 68 | 44 / 50 |

### SUS Item-Level Change
Τα item scores παρακάτω είναι ήδη direction-corrected, άρα υψηλότερο σημαίνει πάντα καλύτερη αξιολόγηση.
| Item | First mean | Second mean | Mean change | Statement |
| --- | --- | --- | --- | --- |
| 1 | 2.52 | 2.80 | 0.28 | Θα ήθελα να χρησιμοποιώ συχνά αυτό το σύστημα υποστήριξης ανάγνωσης με eye-tracker. |
| 2 | 3.58 | 3.68 | 0.10 | Βρήκα το σύστημα αδικαιολόγητα πολύπλοκο στη χρήση του. |
| 3 | 2.96 | 3.14 | 0.18 | Θεώρησα ότι το σύστημα ήταν εύκολο στη χρήση κατά την ανάγνωση του κειμένου. |
| 4 | 3.34 | 3.34 | 0.00 | Πιστεύω ότι θα χρειαζόμουν βοήθεια από κάποιον ειδικό για να μπορέσω να χρησιμοποιήσω το σύστημα απο |
| 5 | 2.84 | 2.84 | 0.00 | Θεώρησα ότι οι λειτουργίες του συστήματος, όπως η ανίχνευση βλέμματος, οι μεταφράσεις και το vocabul |
| 6 | 2.68 | 2.82 | 0.14 | Θεώρησα ότι υπήρχε ασυνέπεια στον τρόπο που λειτουργούσε το σύστημα κατά την ανάγνωση. |
| 7 | 3.46 | 3.44 | -0.02 | Πιστεύω ότι οι περισσότεροι χρήστες θα μπορούσαν να μάθουν να χρησιμοποιούν αυτό το σύστημα γρήγορα. |
| 8 | 3.40 | 3.48 | 0.08 | Θεώρησα ότι το σύστημα ήταν δύσχρηστο κατά τη διάρκεια της ανάγνωσης. |
| 9 | 3.12 | 3.08 | -0.04 | Ένιωσα σιγουριά όταν χρησιμοποιούσα το σύστημα. |
| 10 | 3.78 | 3.72 | -0.06 | Χρειάστηκε να μάθω πολλά πράγματα πριν μπορέσω να χρησιμοποιήσω αποτελεσματικά το σύστημα. |

## Participant Background

| Metric | Value |
| --- | --- |
| Demographic rows | 54 |
| Matched demographic rows | 51 |
| Age | n=51, μέσος=21.86, διάμεσος=22.00, ΤΑ=1.82, εύρος=20.00-28.00 |

### Gender
| Response | n |
| --- | --- |
| Άνδρας | 30 |
| Γυναίκα | 21 |

### Self-rated English level
| Response | n |
| --- | --- |
| C2 | 28 |
| Β2 | 11 |
| C1 | 11 |
| Β1 | 1 |

### Translation tool use frequency
| Response | n |
| --- | --- |
| Μερικές φορές | 23 |
| Σπάνια | 17 |
| Συχνά | 9 |
| Πολύ συχνά | 2 |

### Reported reading/learning difficulty
| Response | n |
| --- | --- |
| Όχι | 50 |
| Ναι | 1 |

### Quiz Score by Self-Rated English Level
| English level | participants | Μέσο user quiz % | Διάμεσος | ΤΑ |
| --- | --- | --- | --- | --- |
| C1 | 11 | 74.45 | 72.92 | 13.55 |
| C2 | 28 | 83.01 | 84.00 | 7.85 |
| Β1 | 1 | 75.00 | 75.00 | - |
| Β2 | 11 | 71.56 | 80.00 | 16.83 |

## Per-Participant Summary

Το πλήρες per-participant table γράφτηκε στο `quiz_analysis_user_summary.csv`. Παρακάτω φαίνονται τα πρώτα rows.
| User | quizzes | Μέσο % | Popup on % | Popup off % | On-off | SUS change |
| --- | --- | --- | --- | --- | --- | --- |
| 1059657 | 8 | 90.0 | 90.0 | 90.0 | 0.0 | -10.0 |
| 1065023 | 8 | 72.5 | 60.0 | 85.0 | -25.0 | 5.0 |
| 1070729 | 8 | 82.5 | 70.0 | 95.0 | -25.0 | 0.0 |
| 1080401 | 8 | 67.5 | 65.0 | 70.0 | -5.0 | 10.0 |
| 1084609 | 8 | 83.33 | 95.0 | 71.67 | 23.33 | 2.5 |
| 1090053 | 8 | 87.5 | 90.0 | 85.0 | 5.0 | 12.5 |
| 1093313 | 6 | 80.0 | 73.33 | 86.67 | -13.33 | -17.5 |
| 1093322 | 5 | 81.33 | 70.0 | 88.89 | -18.89 | 0.0 |
| 1093332 | 8 | 72.92 | 75.83 | 70.0 | 5.83 | 5.0 |
| 1093348 | 8 | 90.0 | 90.0 | 90.0 | 0.0 | 2.5 |
| 1093379 | 8 | 85.0 | 80.0 | 90.0 | -10.0 | 5.0 |
| 1093390 | 8 | 80.0 | 80.0 | 80.0 | 0.0 | 7.5 |
| 1093403 | 8 | 57.5 | 70.0 | 45.0 | 25.0 | -2.5 |
| 1093413 | 8 | 80.0 | 80.0 | 80.0 | 0.0 | -7.5 |
| 1093505 | 8 | 90.0 | 90.0 | 90.0 | 0.0 | -2.5 |
| 1093515 | 6 | 90.0 | 80.0 | 100.0 | -20.0 | -7.5 |
| 1095564 | 8 | 82.92 | 85.83 | 80.0 | 5.83 | -2.5 |
| 1097463 | 8 | 77.92 | 65.0 | 90.83 | -25.83 | 15.0 |
| 1100496 | 8 | 67.5 | 70.0 | 65.0 | 5.0 | 2.5 |
| 1100497 | 8 | 87.92 | 85.0 | 90.83 | -5.83 | -12.5 |
| 1100613 | 8 | 85.83 | 85.0 | 86.67 | -1.67 | 0.0 |
| 1100663 | 8 | 85.0 | 85.0 | 85.0 | 0.0 | 0.0 |
| 1100758 | 8 | 75.0 | 60.0 | 90.0 | -30.0 | 12.5 |
| 1103080 | 8 | 82.5 | 80.0 | 85.0 | -5.0 | -7.5 |
| 1104782 | 8 | 46.25 | 47.5 | 45.0 | 2.5 | -2.5 |

## Main Conclusions and Hypotheses

- Η popup condition **δεν έδειξε ουσιαστικό overall comprehension-score advantage**. Η raw διαφορά popup-on μείον popup-off ήταν 0.55 percentage points, και η PDF-normalized διαφορά ήταν 0.017 z-score units.
- Τα individual responses ήταν ετερογενή: 23 users είχαν καλύτερο μέσο score με popup, 20 είχαν καλύτερο μέσο score με external translation, και 8 ήταν ίσοι με βάση τα condition means.
- Η δυσκολία του text φαίνεται να είχε μεγαλύτερη επίδραση από το popup mode. Το χαμηλότερο-scoring PDF ήταν το `c2_rosa_parks_2.pdf` με 54.78%, ενώ το υψηλότερο-scoring PDF ήταν το `c1_bee_reading_2.pdf` με 89.14%.
- Ανά level, οι observed means ήταν B2: 81.53%, C1: 82.98%, C2: 67.39%. Το C2 average πέφτει αρκετά λόγω του `c2_rosa_parks_2.pdf`, άρα τα level effects πρέπει να συζητηθούν μαζί με individual text effects.
- Στο per-PDF comparison η εικόνα είναι μικτή: 2 PDFs έχουν διαφορά τουλάχιστον +5 points υπέρ popup-on, 0 PDFs έχουν διαφορά τουλάχιστον -5 points υπέρ popup-off/external translation, και 8 PDFs είναι εντός ±5 points.
- Δεν υπάρχει ισχυρή ένδειξη για μεγάλο learning/practice improvement στα quiz scores με την πάροδο του χρόνου. Η early-to-late PDF-normalized μεταβολή είχε μέσο 0.159 z-score units, με 31 users να βελτιώνονται και 20 να μειώνονται.
- Τα behavioural correlations με το score ήταν weak. Το translation count και τα translations per minute ήταν ελαφρώς αρνητικά, κάτι που πιθανότερα σημαίνει ότι readers με χαμηλότερη κατανόηση χρειάζονταν περισσότερη μεταφραστική υποστήριξη, όχι ότι η μετάφραση προκάλεσε χαμηλότερο score.
- Το SUS usability ήταν ήδη υψηλό και αυξήθηκε ελαφρά με τη χρήση. Το mean SUS change ήταν 1.65 points, κάτι που δείχνει ότι το σύστημα παρέμεινε αποδεκτό μετά από επαναλαμβανόμενη χρήση αντί να γίνεται πιο κουραστικό/frustrating.
- Για πιο ισχυρά statistical claims θα χρειαζόταν mixed-effects model με participant και PDF ως random effects. Τα descriptive statistics εδώ παραμένουν χρήσιμα γιατί δείχνουν το βασικό pattern: οι διαφορές στο score φαίνεται να οδηγούνται περισσότερο από participant/text variation παρά από το popup-on versus popup-off μόνο.

## Data Quality Notes

- User/PDF pairs με duplicate quiz responses όπου επιλέχθηκε ένα response με βάση timestamp proximity: **2**.
- Τα matched quiz rows με accepted/split timing corrections χρησιμοποιούν τις current analysis DB values. Αν κάποιο session end time είναι ακόμη λάθος, τα duration-based correlations μπορούν να αλλάξουν.
- Τα popup condition labels προέρχονται από το `translationOutputMode`. Για sessions με multiple candidate DB segments, το matching χρησιμοποιεί το quiz timestamp και αποφεύγει short setup segments όπου είναι δυνατό.
- Τα inferred condition-only rows δεν δημιουργούν νέο session και δεν αλλάζουν το DB. Απλώς κρατούν το quiz score στο condition analysis όταν το 4-on/4-off balance κάνει το missing condition μονοσήμαντο.

## Output Files

- Joined quiz/session data: `quiz_analysis_joined.csv`
- Per-participant summary: `quiz_analysis_user_summary.csv`
- SUS paired data: `quiz_analysis_sus_paired.csv`
- Question-level statistics: `quiz_analysis_question_stats.csv`
- Missing-session review: `quiz_analysis_missing_session_review.csv`
- PDF condition comparison: `quiz_analysis_pdf_condition_comparison.csv`
