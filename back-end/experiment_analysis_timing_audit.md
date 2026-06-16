# Experiment Timing Audit

This report compares the current analysis database with the original database from `deepltest`.
It has two jobs: first, make the timing edits easy to see; second, point to the sessions that still deserve manual checking.

## What Changed

- Manual timing changes to existing non-split sessions: **47**
- Split-created sessions: **40**
- Existing sessions adjusted because of a split: **37**
- Chosen plausible text user/PDF sessions checked for problems: **379**
- Sessions excluded from potential-problem checks because they are checked, manually corrected, or under 4 minutes: **192**
- Open unusual-duration flags after filtering checked sessions: **1**
- Open long-pause flags after filtering checked sessions and translations outside the current start/end window: **30**
- Open repetitive-tail translation flags: **15**

Important: long-pause and repetitive-tail checks use only translations inside the current `startedAt`/`endedAt` window. Translation rows that still exist after a manually shortened `endedAt` are ignored for these problem sections.

Important: potential-problem checks now automatically pass sessions that are under 4 minutes or sessions whose timing you manually changed in the current DB. Split-related sessions are not automatically passed; they can still appear below if they match a problem rule.

## Manual Timing Changes To Existing Sessions

These rows existed in the original `deepltest` database and are not split-related. They are treated as manually corrected and are not listed as potential problems later.

### 1065023 (userID 17) - session `767e4a74-f4ea-4ac5-a52c-a427f6f1a6d8`
This session now contains: c2_rosa_parks_2.pdf (66 stored translations, 65 inside current time window, on).
- Before: 2026-05-18T20:05:27 -> 2026-05-18T20:13:31 (8.07 min).
- After: 2026-05-18T20:05:27 -> 2026-05-18T20:10:12 (4.75 min).
- Change: end moved by -3.32 minutes.

### 1065023 (userID 17) - session `2a604556-49ca-4707-b6f6-2d6138e16d7c`
This session now contains: c2_noisy_humans_1.pdf (70 stored translations, 46 inside current time window, off).
- Before: 2026-05-18T20:13:44 -> 2026-05-19T09:15:31 (781.78 min).
- After: 2026-05-18T20:13:44 -> 2026-05-18T20:19:14 (5.5 min).
- Change: end moved by -776.28 minutes.

### 1080401 (userID 31) - session `d19f64cd-bb4d-4bdd-a59b-31cfc906e642`
This session now contains: b2_first_american_3.pdf (70 stored translations, 70 inside current time window, on).
- Before: 2026-05-25T09:12:00 -> 2026-05-25T09:19:41 (7.68 min).
- After: 2026-05-25T09:12:00 -> 2026-05-25T09:16:51 (4.85 min).
- Change: end moved by -2.83 minutes.

### 1080401 (userID 31) - session `604a8afe-cbad-461c-b0db-78a2c9ed750a`
This session now contains: b2_electromagnetic_radiation_2.pdf (117 stored translations, 114 inside current time window, off).
- Before: 2026-05-25T09:20:03 -> 2026-05-25T10:01:41 (41.63 min).
- After: 2026-05-25T09:20:03 -> 2026-05-25T09:28:43 (8.67 min).
- Change: end moved by -32.97 minutes.

### 1080401 (userID 31) - session `07998834-fb83-475c-a5e4-c2981c6371d6`
This session now contains: c1_native_american_conflicts_3.pdf (270 stored translations, 270 inside current time window, off).
- Before: 2026-05-28T09:52:25 -> 2026-05-28T10:18:13 (25.8 min).
- After: 2026-05-28T09:52:25 -> 2026-05-28T10:07:57 (15.53 min).
- Change: end moved by -10.27 minutes.

### 1084609 (userID 44) - session `1d634156-b062-4155-b2fd-30771a282724`
This session now contains: c1_bee_reading_2.pdf (121 stored translations, 119 inside current time window, off).
- Before: 2026-05-25T18:20:13 -> 2026-05-25T18:33:52 (13.65 min).
- After: 2026-05-25T18:20:13 -> 2026-05-25T18:30:36 (10.38 min).
- Change: end moved by -3.27 minutes.

### 1084609 (userID 44) - session `a329b9b7-7b2a-4d9e-8eb2-8cc9badb749e`
This session now contains: c1_age_of_exploration_1.pdf (45 stored translations, 43 inside current time window, on).
- Before: 2026-05-25T18:34:14 -> 2026-05-25T18:44:44 (10.5 min).
- After: 2026-05-25T18:34:14 -> 2026-05-25T18:40:23 (6.15 min).
- Change: end moved by -4.35 minutes.

### 1093322 (userID 10) - session `c453644c-7b9c-4d36-93ef-a8da76f00adc`
This session now contains: b2_animals_of_rainforests_1.pdf (44 stored translations, 44 inside current time window, off).
- Before: 2026-05-18T15:54:23 -> 2026-05-18T16:07:51 (13.47 min).
- After: 2026-05-18T15:54:23 -> 2026-05-18T16:00:11 (5.8 min).
- Change: end moved by -7.67 minutes.

### 1093322 (userID 10) - session `8ddb2ff7-ca06-497c-82d2-e4974f51de40`
This session now contains: c1_walt_disney_4.pdf (54 stored translations, 48 inside current time window, on).
- Before: 2026-05-20T09:43:44 -> 2026-05-20T09:52:59 (9.25 min).
- After: 2026-05-20T09:43:44 -> 2026-05-20T09:48:58 (5.23 min).
- Change: end moved by -4.02 minutes.

### 1093322 (userID 10) - session `ea531f61-51d7-414e-9adf-8839f7dd0c26`
This session now contains: c1_bee_reading_2.pdf (54 stored translations, 53 inside current time window, off).
- Before: 2026-05-20T09:52:59 -> 2026-05-20T10:01:19 (8.33 min).
- After: 2026-05-20T09:52:59 -> 2026-05-20T09:58:25 (5.43 min).
- Change: end moved by -2.9 minutes.

### 1093322 (userID 10) - session `d0709e17-8b04-4ad0-9887-61cdba5497ee`
This session now contains: b2_sticky_fingers_4.pdf (43 stored translations, 42 inside current time window, off).
- Before: 2026-05-27T09:13:27 -> 2026-05-27T09:20:46 (7.32 min).
- After: 2026-05-27T09:13:27 -> 2026-05-27T09:18:45 (5.3 min).
- Change: end moved by -2.02 minutes.

### 1093348 (userID 39) - session `7dc7ad85-3c80-49a8-87ee-80b727e42556`
This session now contains: c1_bee_reading_2.pdf (39 stored translations, 22 inside current time window, off).
- Before: 2026-05-26T15:02:28 -> 2026-05-26T15:11:05 (8.62 min).
- After: 2026-05-26T15:02:28 -> 2026-05-26T15:08:49 (6.35 min).
- Change: end moved by -2.27 minutes.

### 1093379 (userID 45) - session `0d609472-7b65-482a-bc20-5e0edffb777a`
This session now contains: c1_walt_disney_4.pdf (184 stored translations, 161 inside current time window, on).
- Before: 2026-05-26T10:47:49 -> 2026-05-26T11:00:08 (12.32 min).
- After: 2026-05-26T10:47:49 -> 2026-05-26T10:56:12 (8.38 min).
- Change: end moved by -3.93 minutes.

### 1093379 (userID 45) - session `011fb9da-eb69-428b-8216-bf3e124857c6`
This session now contains: c1_bee_reading_2.pdf (98 stored translations, 93 inside current time window, off).
- Before: 2026-05-26T11:00:20 -> 2026-05-26T11:12:24 (12.07 min).
- After: 2026-05-26T11:00:20 -> 2026-05-26T11:06:28 (6.13 min).
- Change: end moved by -5.93 minutes.

### 1093505 (userID 41) - session `13bc6b94-8791-4212-a001-ab763d578bed`
This session now contains: c1_bee_reading_2.pdf (40 stored translations, 23 inside current time window, off).
- Before: 2026-05-25T16:40:22 -> 2026-05-25T16:48:18 (7.93 min).
- After: 2026-05-25T16:40:22 -> 2026-05-25T16:45:54 (5.53 min).
- Change: end moved by -2.4 minutes.

### 1093515 (userID 27) - session `e5517617-a2d2-404d-a24d-d0b3ca793fe7`
This session now contains: c1_native_american_conflicts_3.pdf (347 stored translations, 304 inside current time window, off).
- Before: 2026-05-21T09:31:39 -> 2026-05-21T09:39:41 (8.03 min).
- After: 2026-05-21T09:31:54 -> 2026-05-21T09:35:51 (3.95 min).
- Change: start moved by 0.25 minutes; end moved by -3.83 minutes.

### 1100758 (userID 36) - session `b9feb6d8-a85f-44b0-a6f9-b49a30597b24`
This session now contains: c1_walt_disney_4.pdf (58 stored translations, 24 inside current time window, on).
- Before: 2026-05-25T13:39:32 -> 2026-05-25T13:52:56 (13.4 min).
- After: 2026-05-25T13:39:32 -> 2026-05-25T13:43:49 (4.28 min).
- Change: end moved by -9.12 minutes.

### 1100758 (userID 36) - session `0b470ee2-68e3-4ff1-a51f-a42bc14041e7`
This session now contains: c2_rosa_parks_2.pdf (84 stored translations, 83 inside current time window, on).
- Before: 2026-05-26T17:06:40 -> 2026-05-26T17:16:01 (9.35 min).
- After: 2026-05-26T17:06:40 -> 2026-05-26T17:12:48 (6.13 min).
- Change: end moved by -3.22 minutes.

### 1108323 (userID 13) - session `a7366305-1b91-4fd3-a077-c22380f1631b`
This session now contains: c2_rosa_parks_2.pdf (33 stored translations, 32 inside current time window, off).
- Before: 2026-05-18T17:22:44 -> 2026-05-18T17:28:26 (5.7 min).
- After: 2026-05-18T17:22:44 -> 2026-05-18T17:25:47 (3.05 min).
- Change: end moved by -2.65 minutes.

### 1108323 (userID 13) - session `9fffa5b8-0b82-426d-805d-c0049bd98060`
This session now contains: b2_animals_of_rainforests_1.pdf (27 stored translations, 27 inside current time window, off).
- Before: 2026-05-19T16:18:48 -> 2026-05-19T16:24:50 (6.03 min).
- After: 2026-05-19T16:20:16 -> 2026-05-19T16:24:50 (4.57 min).
- Change: start moved by 1.47 minutes.

### 1108330 (userID 19) - session `8e022878-6e8d-44c6-b762-112d3673e2f9`
This session now contains: c2_rosa_parks_2.pdf (302 stored translations, 286 inside current time window, off).
- Before: 2026-05-19T09:55:33 -> 2026-05-19T10:04:41 (9.13 min).
- After: 2026-05-19T09:55:33 -> 2026-05-19T10:01:19 (5.77 min).
- Change: end moved by -3.37 minutes.

### 1108330 (userID 19) - session `a1bf0f70-6549-4699-9225-b8c8a404b7e2`
This session now contains: b2_sticky_fingers_4.pdf (30 stored translations, 28 inside current time window, on).
- Before: 2026-05-26T09:05:17 -> 2026-05-26T09:13:09 (7.87 min).
- After: 2026-05-26T09:05:17 -> 2026-05-26T09:10:38 (5.35 min).
- Change: end moved by -2.52 minutes.

### 1108330 (userID 19) - session `993279e2-4f05-4ace-af51-4eaef8c250ba`
This session now contains: b2_first_american_3.pdf (23 stored translations, 21 inside current time window, off).
- Before: 2026-05-26T09:13:24 -> 2026-05-26T09:28:44 (15.33 min).
- After: 2026-05-26T09:13:24 -> 2026-05-26T09:18:12 (4.8 min).
- Change: end moved by -10.53 minutes.

### 1108335 (userID 26) - session `fd864e13-32bf-4819-99de-f47ff44ac346`
This session now contains: c1_native_american_conflicts_3.pdf (33 stored translations, 28 inside current time window, off).
- Before: 2026-05-30T16:54:07 -> 2026-05-30T17:02:14 (8.12 min).
- After: 2026-05-30T16:54:07 -> 2026-05-30T16:58:39 (4.53 min).
- Change: end moved by -3.58 minutes.

### 1108339 (userID 20) - session `a3fc9cf5-eb74-4415-9645-ed76b04722ec`
This session now contains: c2_noisy_humans_1.pdf (56 stored translations, 54 inside current time window, on).
- Before: 2026-05-20T14:46:05 -> 2026-05-20T14:53:21 (7.27 min).
- After: 2026-05-20T14:46:05 -> 2026-05-20T14:51:26 (5.35 min).
- Change: end moved by -1.92 minutes.

### 1108339 (userID 20) - session `aa97c58b-e684-452a-972a-30f63e8e3bc2`
This session now contains: c2_rosa_parks_2.pdf (14 stored translations, 13 inside current time window, off).
- Before: 2026-05-20T14:53:21 -> 2026-05-20T14:57:30 (4.15 min).
- After: 2026-05-20T14:53:21 -> 2026-05-20T14:55:37 (2.27 min).
- Change: end moved by -1.88 minutes.

### 1108344 (userID 37) - session `0f2bf24c-64b7-4683-90c1-362df55604ff`
This session now contains: c1_bee_reading_2.pdf (21 stored translations, 18 inside current time window, off).
- Before: 2026-05-26T16:33:29 -> 2026-05-26T16:40:32 (7.05 min).
- After: 2026-05-26T16:33:29 -> 2026-05-26T16:38:30 (5.02 min).
- Change: end moved by -2.03 minutes.

### 1108346 (userID 34) - session `83c9b5c5-6772-473e-a233-04369504584e`
This session now contains: b2_sticky_fingers_4.pdf (4 stored translations, 2 inside current time window, on).
- Before: 2026-05-27T10:23:35 -> 2026-05-27T10:31:24 (7.82 min).
- After: 2026-05-27T10:23:35 -> 2026-05-27T10:27:09 (3.57 min).
- Change: end moved by -4.25 minutes.

### 1108346 (userID 34) - session `6dd314f0-d934-486d-adc4-0e6fa9301449`
This session now contains: c1_native_american_conflicts_3.pdf (27 stored translations, 24 inside current time window, on).
- Before: 2026-05-28T11:03:07 -> 2026-05-28T11:22:53 (19.77 min).
- After: 2026-05-28T11:03:07 -> 2026-05-28T11:06:30 (3.38 min).
- Change: end moved by -16.38 minutes.

### 1108348 (userID 6) - session `cf06b6aa-0f00-4c62-86d1-283a34736f09`
This session now contains: c1_walt_disney_4.pdf (121 stored translations, 107 inside current time window, off).
- Before: 2026-05-18T13:38:09 -> 2026-05-18T13:49:24 (11.25 min).
- After: 2026-05-18T13:38:09 -> 2026-05-18T13:44:20 (6.18 min).
- Change: end moved by -5.07 minutes.

### 1108348 (userID 6) - session `566cc61c-0ac3-4fb6-9256-7f55b55c2fee`
This session now contains: c1_age_of_exploration_1.pdf (180 stored translations, 161 inside current time window, on).
- Before: 2026-05-18T13:49:47 -> 2026-05-18T14:01:53 (12.1 min).
- After: 2026-05-18T13:49:47 -> 2026-05-18T13:55:59 (6.2 min).
- Change: end moved by -5.9 minutes.

### 1108348 (userID 6) - session `1d6df67b-5ccb-43bc-984a-589a3ebe0537`
This session now contains: b2_electromagnetic_radiation_2.pdf (70 stored translations, 70 inside current time window, on).
- Before: 2026-05-20T11:43:08 -> 2026-05-20T11:50:23 (7.25 min).
- After: 2026-05-20T11:43:08 -> 2026-05-20T11:47:50 (4.7 min).
- Change: end moved by -2.55 minutes.

### 1108357 (userID 23) - session `2e35c536-79ff-4a44-9155-7b5e050b15ff`
This session now contains: c2_noisy_humans_1.pdf (114 stored translations, 83 inside current time window, off).
- Before: 2026-05-19T15:19:33 -> 2026-05-19T15:29:14 (9.68 min).
- After: 2026-05-19T15:19:33 -> 2026-05-19T15:25:25 (5.87 min).
- Change: end moved by -3.82 minutes.

### 1108357 (userID 23) - session `9485615f-8d01-4965-b5b0-762221fdc5ef`
This session now contains: c2_rosa_parks_2.pdf (61 stored translations, 59 inside current time window, on).
- Before: 2026-05-19T15:29:31 -> 2026-05-19T15:39:24 (9.88 min).
- After: 2026-05-19T15:29:31 -> 2026-05-19T15:33:17 (3.77 min).
- Change: end moved by -6.12 minutes.

### 1108367 (userID 5) - session `50dd1615-e574-4caf-8db6-37bc70815439`
This session now contains: c1_age_of_exploration_1.pdf (30 stored translations, 29 inside current time window, off).
- Before: 2026-05-18T13:17:56 -> 2026-05-18T13:31:22 (13.43 min).
- After: 2026-05-18T13:17:56 -> 2026-05-18T13:21:11 (3.25 min).
- Change: end moved by -10.18 minutes.

### 1108382 (userID 7) - session `fdb12a6e-aeb5-469a-ba30-51044d0da005`
This session now contains: c1_bee_reading_2.pdf (87 stored translations, 78 inside current time window, on).
- Before: 2026-05-18T14:33:25 -> 2026-05-18T14:45:17 (11.87 min).
- After: 2026-05-18T14:33:25 -> 2026-05-18T14:38:46 (5.35 min).
- Change: end moved by -6.52 minutes.

### 1108382 (userID 7) - session `da1f519a-68f9-4a1c-9e52-af3be8b746ef`
This session now contains: c1_walt_disney_4.pdf (98 stored translations, 58 inside current time window, on).
- Before: 2026-05-21T14:41:17 -> 2026-05-21T14:53:26 (12.15 min).
- After: 2026-05-21T14:41:17 -> 2026-05-21T14:46:26 (5.15 min).
- Change: end moved by -7 minutes.

### 1108387 (userID 18) - session `d4a5f1ff-be4e-4681-98e4-1911db26d8d2`
This session now contains: b2_sticky_fingers_4.pdf (96 stored translations, 91 inside current time window, off).
- Before: 2026-05-19T09:24:21 -> 2026-05-19T09:33:50 (9.48 min).
- After: 2026-05-19T09:24:21 -> 2026-05-19T09:29:58 (5.62 min).
- Change: end moved by -3.87 minutes.

### 1112096 (userID 14) - session `8f0591ce-cbb9-4718-9b3e-0fc0a2bfb978`
This session now contains: b2_animals_of_rainforests_1.pdf (79 stored translations, 79 inside current time window, on).
- Before: 2026-05-18T18:10:52 -> 2026-05-18T18:23:35 (12.72 min).
- After: 2026-05-18T18:10:52 -> 2026-05-18T18:19:08 (8.27 min).
- Change: end moved by -4.45 minutes.

### 1112096 (userID 14) - session `f4c32c0e-5f43-4ba3-a623-d0ffcd49e461`
This session now contains: c2_noisy_humans_1.pdf (45 stored translations, 29 inside current time window, on).
- Before: 2026-05-20T10:16:22 -> 2026-05-20T10:27:11 (10.82 min).
- After: 2026-05-20T10:16:22 -> 2026-05-20T10:21:24 (5.03 min).
- Change: end moved by -5.78 minutes.

### 1112106 (userID 15) - session `ef66d038-9512-4c1e-a3f7-012d8a6f17f6`
This session now contains: c2_rosa_parks_2.pdf (70 stored translations, 44 inside current time window, on).
- Before: 2026-05-18T18:49:34 -> 2026-05-18T18:55:58 (6.4 min).
- After: 2026-05-18T18:49:34 -> 2026-05-18T18:53:32 (3.97 min).
- Change: end moved by -2.43 minutes.

### 1112106 (userID 15) - session `35dc1e38-d6db-417c-b340-2461aac0dc66`
This session now contains: c2_noisy_humans_1.pdf (69 stored translations, 54 inside current time window, off).
- Before: 2026-05-18T18:56:14 -> 2026-05-18T19:16:58 (20.73 min).
- After: 2026-05-18T18:56:14 -> 2026-05-18T19:01:42 (5.47 min).
- Change: end moved by -15.27 minutes.

### 1112119c (userID 33) - session `d7550b5e-6b65-445b-8c5a-cab8ba307c64`
This session now contains: c1_bee_reading_2.pdf (18 stored translations, 16 inside current time window, on).
- Before: 2026-05-27T10:44:03 -> 2026-05-27T10:53:24 (9.35 min).
- After: 2026-05-27T10:44:03 -> 2026-05-27T10:49:15 (5.2 min).
- Change: end moved by -4.15 minutes.

### 1112139 (userID 16) - session `9ad03ea4-153b-4182-9ef1-d4a7f95e1a70`
This session now contains: c1_age_of_exploration_1.pdf (364 stored translations, 345 inside current time window, on).
- Before: 2026-05-18T19:24:18 -> 2026-05-18T19:38:02 (13.73 min).
- After: 2026-05-18T19:24:18 -> 2026-05-18T19:34:09 (9.85 min).
- Change: end moved by -3.88 minutes.

### 1112139 (userID 16) - session `692206b2-426c-43a5-92ea-3733e4e2e4a6`
This session now contains: c1_bee_reading_2.pdf (236 stored translations, 214 inside current time window, off).
- Before: 2026-05-18T19:38:22 -> 2026-05-18T20:01:40 (23.3 min).
- After: 2026-05-18T19:38:22 -> 2026-05-18T19:49:11 (10.82 min).
- Change: end moved by -12.48 minutes.

### 1112139 (userID 16) - session `4e3073ca-cfd1-442f-9c62-343ea363dc69`
This session now contains: c2_rosa_parks_2.pdf (96 stored translations, 95 inside current time window, off).
- Before: 2026-05-19T17:05:06 -> 2026-05-19T17:12:20 (7.23 min).
- After: 2026-05-19T17:05:06 -> 2026-05-19T17:08:38 (3.53 min).
- Change: end moved by -3.7 minutes.

### 1112139 (userID 16) - session `f7691c81-728c-4887-927c-6be72d2247d4`
This session now contains: b2_animals_of_rainforests_1.pdf (79 stored translations, 77 inside current time window, off).
- Before: 2026-05-26T18:27:49 -> 2026-05-26T18:34:38 (6.82 min).
- After: 2026-05-26T18:29:21 -> 2026-05-26T18:34:38 (5.28 min).
- Change: start moved by 1.53 minutes.

## Split-Created And Split-Adjusted Sessions

These are kept separate from manual timing edits. They show what the split created or adjusted without the old before/after timing noise.

- 1065023 (userID 17) | `68948df4-2969-4b5d-996f-2248850e0d44` | eye_tracking_validation_simple_2pages.pdf | 2026-05-19T17:57:50 -> 2026-05-19T18:00:11.824 (2.36 min) | output off | split 1/2 from `68948df4-2969-4b5d-996f-2248850e0d44`
- 1065023 (userID 17) | `4d4c37eb-07b0-4011-9c23-6211ed43d82a` | b2_electromagnetic_radiation_2.pdf | 2026-05-19T18:00:25.369 -> 2026-05-19T18:04:44.381 (4.32 min) | output off | split 2/2 from `68948df4-2969-4b5d-996f-2248850e0d44`
- 1093322 (userID 10) | `0823c0ab-65f4-42b7-8b3d-28d3ec50b5d1` | eye_tracking_validation_simple_2pages.pdf | 2026-05-18T15:41:22 -> 2026-05-18T15:45:50.855 (4.48 min) | output on | split 1/2 from `0823c0ab-65f4-42b7-8b3d-28d3ec50b5d1`
- 1093322 (userID 10) | `db27365f-b25d-4bec-9931-e7463ac1291c` | b2_electromagnetic_radiation_2.pdf | 2026-05-18T15:46:51.470 -> 2026-05-18T15:53:38.526 (6.78 min) | output on | split 2/2 from `0823c0ab-65f4-42b7-8b3d-28d3ec50b5d1`
- 1093348 (userID 39) | `2b5c0846-a850-48b5-8467-b6e736bc5a6a` | eye_tracking_validation_simple_2pages.pdf | 2026-05-25T15:37:41 -> 2026-05-25T15:38:45.406 (1.07 min) | output on | split 1/3 from `2b5c0846-a850-48b5-8467-b6e736bc5a6a`
- 1093348 (userID 39) | `6c5c45fb-5383-4047-aa17-ad1a68387a72` | c2_rosa_parks_2.pdf | 2026-05-25T15:38:58.256 -> 2026-05-25T15:43:52 (4.9 min) | output on | split 2/3 from `2b5c0846-a850-48b5-8467-b6e736bc5a6a`
- 1093348 (userID 39) | `7f84e707-ff3d-4c85-890b-82f784a0f030` | c2_noisy_humans_1.pdf | 2026-05-25T15:46:21.220 -> 2026-05-25T15:52:09 (5.8 min) | output off | split 3/3 from `2b5c0846-a850-48b5-8467-b6e736bc5a6a`
- 1093403 (userID 9) | `e2067df6-37eb-48c5-bb7b-fdbe820cd4c6` | eye_tracking_validation_simple_2pages.pdf | 2026-05-18T15:11:57 -> 2026-05-18T15:14:38.910 (2.7 min) | output on | split 1/2 from `e2067df6-37eb-48c5-bb7b-fdbe820cd4c6`
- 1093403 (userID 9) | `cabb8f46-b750-4913-95de-54d1d12d1874` | c2_noisy_humans_1.pdf | 2026-05-18T15:15:01.583 -> 2026-05-18T15:20:19 (5.29 min) | output on | split 2/2 from `e2067df6-37eb-48c5-bb7b-fdbe820cd4c6`
- 1093403 (userID 9) | `385c0cd6-9d40-4ed4-8bfd-007f7211cd66` | eye_tracking_validation_simple_2pages.pdf | 2026-05-19T10:59:16 -> 2026-05-19T11:00:04.009 (0.8 min) | output on | split 1/2 from `385c0cd6-9d40-4ed4-8bfd-007f7211cd66`
- 1093403 (userID 9) | `4e499daf-a2d5-481a-aded-d175bc5d53a1` | c1_bee_reading_2.pdf | 2026-05-19T11:00:22 -> 2026-05-19T11:05:06 (4.73 min) | output on | split 2/2 from `385c0cd6-9d40-4ed4-8bfd-007f7211cd66`
- 1093403 (userID 9) | `e887bbb7-f415-41c2-8d96-e109b720dc7b` | eye_tracking_validation_simple_2pages.pdf | 2026-05-21T10:59:21 -> 2026-05-21T10:59:49.333 (0.47 min) | output on | split 1/3 from `e887bbb7-f415-41c2-8d96-e109b720dc7b`
- 1093403 (userID 9) | `f9929859-4faf-47d9-a7b3-de9c08ff01d5` | c1_age_of_exploration_1.pdf | 2026-05-21T11:00:54 -> 2026-05-21T11:04:19 (3.42 min) | output on | split 2/3 from `e887bbb7-f415-41c2-8d96-e109b720dc7b`
- 1093403 (userID 9) | `b5588a67-bdd1-49f9-a693-d884bea21035` | c1_walt_disney_4.pdf | 2026-05-21T11:07:02 -> 2026-05-21T11:10:54 (3.87 min) | output off | split 3/3 from `e887bbb7-f415-41c2-8d96-e109b720dc7b`
- 1093413 (userID 49) | `01e0b116-a272-4136-8bc0-d5dde3e638e1` | eye_tracking_validation_simple_2pages.pdf | 2026-05-28T13:37:16 -> 2026-05-28T13:40:18.817 (3.05 min) | output on | split 1/2 from `01e0b116-a272-4136-8bc0-d5dde3e638e1`
- 1093413 (userID 49) | `a2a4732f-b342-417f-ba6a-1c623c2ad711` | c1_walt_disney_4.pdf | 2026-05-28T13:40:33.162 -> 2026-05-28T13:44:28.160 (3.92 min) | output on | split 2/2 from `01e0b116-a272-4136-8bc0-d5dde3e638e1`
- 1093515 (userID 27) | `a38397e6-637e-4cfa-a848-263738dfa62e` | eye_tracking_validation_simple_2pages.pdf | 2026-05-21T09:18:21 -> 2026-05-21T09:19:13.455 (0.87 min) | output on | split 1/2 from `a38397e6-637e-4cfa-a848-263738dfa62e`
- 1093515 (userID 27) | `977369c8-c045-493f-881c-f2af4301a6a0` | c1_walt_disney_4.pdf | 2026-05-21T09:20:51.334 -> 2026-05-21T09:26:33 (5.69 min) | output on | split 2/2 from `a38397e6-637e-4cfa-a848-263738dfa62e`
- 1097463 (userID 12) | `5cab1f9b-6f9b-411d-8c8e-cec9137cb4c0` | c1_age_of_exploration_1.pdf | 2026-05-18T16:42:57 -> 2026-05-18T16:49:37 (6.67 min) | output off | split 1/2 from `5cab1f9b-6f9b-411d-8c8e-cec9137cb4c0`
- 1097463 (userID 12) | `28dc08ef-0dbc-49c9-b691-d4e878127daf` | c1_bee_reading_2.pdf | 2026-05-18T16:51:20.336 -> 2026-05-18T16:51:40.457 (0.34 min) | output off | split 2/2 from `5cab1f9b-6f9b-411d-8c8e-cec9137cb4c0`
- 1097463 (userID 12) | `0b59ef93-0b3f-44af-9a48-66431c7d3af3` | eye_tracking_validation_simple_2pages.pdf | 2026-05-19T12:51:45 -> 2026-05-19T12:52:09.400 (0.41 min) | output on | split 1/2 from `0b59ef93-0b3f-44af-9a48-66431c7d3af3`
- 1097463 (userID 12) | `f015d424-f98d-4ee7-8175-d51e6db43085` | c2_rosa_parks_2.pdf | 2026-05-19T12:52:25.469 -> 2026-05-19T12:54:55.095 (2.49 min) | output on | split 2/2 from `0b59ef93-0b3f-44af-9a48-66431c7d3af3`
- 1097463 (userID 12) | `8b353cbd-e017-4462-937e-5e69156e5823` | eye_tracking_validation_simple_2pages.pdf | 2026-05-20T13:26:23 -> 2026-05-20T13:29:10.592 (2.79 min) | output on | split 1/2 from `8b353cbd-e017-4462-937e-5e69156e5823`
- 1097463 (userID 12) | `8f295f4e-1dda-4f6d-9392-28f1bfdd42f3` | b2_animals_of_rainforests_1.pdf | 2026-05-20T13:30:05 -> 2026-05-20T13:34:17 (4.2 min) | output off | split 2/2 from `8b353cbd-e017-4462-937e-5e69156e5823`
- 1100663 (userID 24) | `e35ed4a6-d332-46bd-bf66-f92ea7982bbc` | eye_tracking_validation_simple_2pages.pdf | 2026-05-19T15:44:49 -> 2026-05-19T15:49:12.828 (4.4 min) | output on | split 1/2 from `e35ed4a6-d332-46bd-bf66-f92ea7982bbc`
- 1100663 (userID 24) | `c67658ac-80d9-4d50-9563-28621df3fcd0` | c1_bee_reading_2.pdf | 2026-05-19T15:50:06.570 -> 2026-05-19T15:54:22.252 (4.26 min) | output on | split 2/2 from `e35ed4a6-d332-46bd-bf66-f92ea7982bbc`
- 1103080 (userID 35) | `809491b1-34bf-4007-ba9a-abdc95ad8f83` | eye_tracking_validation_simple_2pages.pdf | 2026-05-25T12:15:14 -> 2026-05-25T12:18:36.111 (3.37 min) | output on | split 1/2 from `809491b1-34bf-4007-ba9a-abdc95ad8f83`
- 1103080 (userID 35) | `0cf369b9-aeef-45af-96ed-1e7bb674c354` | c1_bee_reading_2.pdf | 2026-05-25T12:19:06.684 -> 2026-05-25T12:21:20.976 (2.24 min) | output on | split 2/2 from `809491b1-34bf-4007-ba9a-abdc95ad8f83`
- 1108323 (userID 13) | `71ed7bc5-21ec-4c01-87d1-4fd17d22cce8` | eye_tracking_validation_simple_2pages.pdf | 2026-05-18T17:09:56 -> 2026-05-18T17:12:39.593 (2.73 min) | output on | split 1/2 from `71ed7bc5-21ec-4c01-87d1-4fd17d22cce8`
- 1108323 (userID 13) | `501ccebc-659a-487d-bcb1-53a03738da89` | c2_noisy_humans_1.pdf | 2026-05-18T17:13:05.444 -> 2026-05-18T17:19:07 (6.03 min) | output on | split 2/2 from `71ed7bc5-21ec-4c01-87d1-4fd17d22cce8`
- 1108328 (userID 25) | `c2098d66-bff1-4e58-bb75-74b7565a5fc2` | eye_tracking_validation_simple_2pages.pdf | 2026-05-19T18:38:34 -> 2026-05-19T18:39:59.672 (1.43 min) | output on | split 1/2 from `c2098d66-bff1-4e58-bb75-74b7565a5fc2`
- 1108328 (userID 25) | `88537952-da97-4422-86c8-225f22dda44a` | c1_native_american_conflicts_3.pdf | 2026-05-19T18:40:42.321 -> 2026-05-19T18:45:02.817 (4.34 min) | output on | split 2/2 from `c2098d66-bff1-4e58-bb75-74b7565a5fc2`
- 1108330 (userID 19) | `35f2c97a-a0f3-44b8-9d3e-e7e9ab7db6fb` | eye_tracking_validation_simple_2pages.pdf | 2026-05-20T12:30:38 -> 2026-05-20T12:33:44.865 (3.11 min) | output on | split 1/2 from `35f2c97a-a0f3-44b8-9d3e-e7e9ab7db6fb`
- 1108330 (userID 19) | `bafcd784-a5ac-4479-94b3-8e3849e16d7a` | c1_walt_disney_4.pdf | 2026-05-20T12:34:31.278 -> 2026-05-20T12:39:12.635 (4.69 min) | output on | split 2/2 from `35f2c97a-a0f3-44b8-9d3e-e7e9ab7db6fb`
- 1108335 (userID 26) | `3cd284fd-d5f6-4d14-b957-8dd8b2fd05ba` | eye_tracking_validation_simple_2pages.pdf | 2026-05-20T12:02:58 -> 2026-05-20T12:04:34.510 (1.61 min) | output on | split 1/2 from `3cd284fd-d5f6-4d14-b957-8dd8b2fd05ba`
- 1108335 (userID 26) | `efb89a1f-43b7-4aa7-bce0-fdb7fce482d7` | c2_rosa_parks_2.pdf | 2026-05-20T12:05:09.284 -> 2026-05-20T12:07:44.980 (2.59 min) | output on | split 2/2 from `3cd284fd-d5f6-4d14-b957-8dd8b2fd05ba`
- 1108335 (userID 26) | `3ff87ec6-1b0b-4818-9c93-ba39a6293173` | eye_tracking_validation_simple_2pages.pdf | 2026-05-21T12:32:43 -> 2026-05-21T12:34:22.970 (1.67 min) | output on | split 1/2 from `3ff87ec6-1b0b-4818-9c93-ba39a6293173`
- 1108335 (userID 26) | `674593f0-fce2-446a-9bba-280ff8983ac6` | b2_animals_of_rainforests_1.pdf | 2026-05-21T12:34:29.502 -> 2026-05-21T12:39:36.785 (5.12 min) | output on | split 2/2 from `3ff87ec6-1b0b-4818-9c93-ba39a6293173`
- 1108339 (userID 20) | `e9e0e884-d50d-4f25-93ff-54c56c622565` | eye_tracking_validation_simple_2pages.pdf | 2026-05-19T10:21:19 -> 2026-05-19T10:23:16.707 (1.96 min) | output on | split 1/2 from `e9e0e884-d50d-4f25-93ff-54c56c622565`
- 1108339 (userID 20) | `5f1f9665-8d3d-4ede-a943-d6fe4d9ec18d` | c1_walt_disney_4.pdf | 2026-05-19T10:24:22.302 -> 2026-05-19T10:25:22.937 (1.01 min) | output on | split 2/2 from `e9e0e884-d50d-4f25-93ff-54c56c622565`
- 1108339 (userID 20) | `9d4aeaa8-dcb9-46df-9849-690d0083dbd4` | c1_walt_disney_4.pdf | 2026-05-19T10:25:27 -> 2026-05-19T10:30:21.052 (4.9 min) | output off | split 1/2 from `9d4aeaa8-dcb9-46df-9849-690d0083dbd4`
- 1108339 (userID 20) | `110e438b-035d-45a0-b8d6-52a659dc0160` | c1_bee_reading_2.pdf | 2026-05-19T10:30:43.850 -> 2026-05-19T10:34:32.105 (3.8 min) | output off | split 2/2 from `9d4aeaa8-dcb9-46df-9849-690d0083dbd4`
- 1108344 (userID 37) | `c1423ce4-1960-4064-a87a-82820ec927a1` | eye_tracking_validation_simple_2pages.pdf | 2026-05-25T14:11:12 -> 2026-05-25T14:14:01.900 (2.83 min) | output on | split 1/2 from `c1423ce4-1960-4064-a87a-82820ec927a1`
- 1108344 (userID 37) | `31b88f10-7ab7-49d5-b0b4-0d27912b9d7d` | c2_noisy_humans_1.pdf | 2026-05-25T14:14:17.159 -> 2026-05-25T14:18:30.815 (4.23 min) | output on | split 2/2 from `c1423ce4-1960-4064-a87a-82820ec927a1`
- 1108348 (userID 6) | `4983fd09-cb5d-4efe-a425-55d047099a7b` | eye_tracking_validation_simple_2pages.pdf | 2026-05-19T11:30:33 -> 2026-05-19T11:31:39.129 (1.1 min) | output on | split 1/3 from `4983fd09-cb5d-4efe-a425-55d047099a7b`
- 1108348 (userID 6) | `e9c7f8af-da33-4507-b792-bc9e2831a1f4` | c2_rosa_parks_2.pdf | 2026-05-19T11:32:04.890 -> 2026-05-19T11:37:34 (5.49 min) | output on | split 2/3 from `4983fd09-cb5d-4efe-a425-55d047099a7b`
- 1108348 (userID 6) | `9bdf2d24-49fd-4b98-a123-564ac1939171` | c2_noisy_humans_1.pdf | 2026-05-19T11:40:24.695 -> 2026-05-19T11:48:46.978 (8.37 min) | output off | split 3/3 from `4983fd09-cb5d-4efe-a425-55d047099a7b`
- 1108348 (userID 6) | `b9144d1a-69bd-4013-8829-88342758e631` | eye_tracking_validation_simple_2pages.pdf | 2026-05-20T11:30:08 -> 2026-05-20T11:30:53.117 (0.75 min) | output on | split 1/2 from `b9144d1a-69bd-4013-8829-88342758e631`
- 1108348 (userID 6) | `e0d4706d-e7b7-41af-9741-829957381e17` | b2_sticky_fingers_4.pdf | 2026-05-20T11:31:19.903 -> 2026-05-20T11:39:23.854 (8.07 min) | output off | split 2/2 from `b9144d1a-69bd-4013-8829-88342758e631`
- 1108348 (userID 6) | `b4ed17d5-65a7-43f4-9bd7-8c07824e59a2` | eye_tracking_validation_simple_2pages.pdf | 2026-05-21T11:56:51 -> 2026-05-21T11:57:29.447 (0.64 min) | output on | split 1/2 from `b4ed17d5-65a7-43f4-9bd7-8c07824e59a2`
- 1108348 (userID 6) | `b8575b1f-516d-4a3e-84fd-f5353dfc5f59` | b2_first_american_3.pdf | 2026-05-21T11:57:54 -> 2026-05-21T12:02:02 (4.13 min) | output on | split 2/2 from `b4ed17d5-65a7-43f4-9bd7-8c07824e59a2`
- 1108349 (userID 21) | `dc8e45f9-040f-4d23-b0a6-d351fe09aacf` | eye_tracking_validation_simple_2pages.pdf | 2026-05-20T16:07:01 -> 2026-05-20T16:08:48.304 (1.79 min) | output on | split 1/2 from `dc8e45f9-040f-4d23-b0a6-d351fe09aacf`
- 1108349 (userID 21) | `bef55ca2-5d56-4fc9-b046-3c2167b769e4` | c2_noisy_humans_1.pdf | 2026-05-20T16:09:27.368 -> 2026-05-20T16:12:10.201 (2.71 min) | output on | split 2/2 from `dc8e45f9-040f-4d23-b0a6-d351fe09aacf`
- 1108360 (userID 8) | `fe2b8212-295b-4b20-8a21-91182c4034f5` | eye_tracking_validation_simple_2pages.pdf | 2026-05-18T14:49:53 -> 2026-05-18T14:52:47.515 (2.91 min) | output on | split 1/2 from `fe2b8212-295b-4b20-8a21-91182c4034f5`
- 1108360 (userID 8) | `5a05fc3f-a734-4209-bc88-0122e615b055` | c1_age_of_exploration_1.pdf | 2026-05-18T14:52:54.588 -> 2026-05-18T14:57:32.134 (4.63 min) | output on | split 2/2 from `fe2b8212-295b-4b20-8a21-91182c4034f5`
- 1108360 (userID 8) | `cf5eb027-4825-412e-9485-3879d4ff4811` | b2_first_american_3.pdf | 2026-05-20T15:15:27 -> 2026-05-20T15:18:40.915 (3.23 min) | output on | split 1/2 from `cf5eb027-4825-412e-9485-3879d4ff4811`
- 1108360 (userID 8) | `2456cda2-6e02-4f02-ab19-9d491eae66a9` | b2_animals_of_rainforests_1.pdf | 2026-05-20T15:19:38.585 -> 2026-05-20T15:24:24.212 (4.76 min) | output on | split 2/2 from `cf5eb027-4825-412e-9485-3879d4ff4811`
- 1108367 (userID 5) | `6d9d323a-9bbe-4c82-bdf9-16f6b46f9f5d` | eye_tracking_validation_simple_2pages.pdf | 2026-05-18T13:06:14 -> 2026-05-18T13:09:04.273 (2.84 min) | output on | split 1/2 from `6d9d323a-9bbe-4c82-bdf9-16f6b46f9f5d`
- 1108367 (userID 5) | `8a219f9b-9b6a-40b7-9282-87ee0a630283` | c1_native_american_conflicts_3.pdf | 2026-05-18T13:10:26 -> 2026-05-18T13:13:41 (3.25 min) | output on | split 2/2 from `6d9d323a-9bbe-4c82-bdf9-16f6b46f9f5d`
- 1108367 (userID 5) | `379fff7c-d051-48dd-bdb9-01fca0306263` | eye_tracking_validation_simple_2pages.pdf | 2026-05-19T12:00:47 -> 2026-05-19T12:02:32.945 (1.77 min) | output on | split 1/2 from `379fff7c-d051-48dd-bdb9-01fca0306263`
- 1108367 (userID 5) | `729d4cdb-ae13-4f26-839f-dcee0f478870` | b2_electromagnetic_radiation_2.pdf | 2026-05-19T12:02:45.761 -> 2026-05-19T12:05:18.679 (2.55 min) | output on | split 2/2 from `379fff7c-d051-48dd-bdb9-01fca0306263`
- 1108367 (userID 5) | `b305bdaa-c42a-4971-8adc-42e7f4eed5f5` | eye_tracking_validation_simple_2pages.pdf | 2026-05-20T16:26:00 -> 2026-05-20T16:26:40.491 (0.67 min) | output on | split 1/2 from `b305bdaa-c42a-4971-8adc-42e7f4eed5f5`
- 1108367 (userID 5) | `b9f7064b-5a49-4eff-9d8d-5fc78817b342` | c2_noisy_humans_1.pdf | 2026-05-20T16:27:07.539 -> 2026-05-20T16:30:04.825 (2.95 min) | output on | split 2/2 from `b305bdaa-c42a-4971-8adc-42e7f4eed5f5`
- 1108382 (userID 7) | `9b862d6c-1462-4c7d-9ccb-7bf772224eb4` | c1_age_of_exploration_1.pdf | 2026-05-18T14:24:04 -> 2026-05-18T14:31:10 (7.1 min) | output off | split 1/2 from `9b862d6c-1462-4c7d-9ccb-7bf772224eb4`
- 1108382 (userID 7) | `35e99ced-ff7f-40ad-ab11-f7c2c1fb1c15` | c1_bee_reading_2.pdf | 2026-05-18T14:33:06.331 -> 2026-05-18T14:33:21.726 (0.26 min) | output off | split 2/2 from `9b862d6c-1462-4c7d-9ccb-7bf772224eb4`
- 1108382 (userID 7) | `518260d4-dd98-4ef6-ace2-116ba25e323d` | eye_tracking_validation_simple_2pages.pdf | 2026-05-20T14:09:38 -> 2026-05-20T14:10:52.496 (1.24 min) | output on | split 1/2 from `518260d4-dd98-4ef6-ace2-116ba25e323d`
- 1108382 (userID 7) | `c2f6a674-25d4-47d4-86dd-07d96caa064e` | b2_animals_of_rainforests_1.pdf | 2026-05-20T14:11:31.893 -> 2026-05-20T14:17:04.090 (5.54 min) | output on | split 2/2 from `518260d4-dd98-4ef6-ace2-116ba25e323d`
- 1108382 (userID 7) | `81ef1e12-b0bd-42b8-94ba-ac9adf27e623` | eye_tracking_validation_simple_2pages.pdf | 2026-05-21T14:32:04 -> 2026-05-21T14:32:25.171 (0.35 min) | output off | split 1/2 from `81ef1e12-b0bd-42b8-94ba-ac9adf27e623`
- 1108382 (userID 7) | `537be0cb-b5d6-4a09-b61b-2f906dec92a9` | c1_native_american_conflicts_3.pdf | 2026-05-21T14:32:46.321 -> 2026-05-21T14:37:38 (4.86 min) | output off | split 2/2 from `81ef1e12-b0bd-42b8-94ba-ac9adf27e623`
- 1112106 (userID 15) | `3a8243f0-1719-43f8-aee3-a485ada32d19` | eye_tracking_validation_simple_2pages.pdf | 2026-05-19T17:16:30 -> 2026-05-19T17:17:55.479 (1.42 min) | output off | split 1/2 from `3a8243f0-1719-43f8-aee3-a485ada32d19`
- 1112106 (userID 15) | `4f8f18f6-90df-4301-8181-14bc91882bb4` | c1_bee_reading_2.pdf | 2026-05-19T17:19:54.115 -> 2026-05-19T17:24:31.070 (4.62 min) | output off | split 2/2 from `3a8243f0-1719-43f8-aee3-a485ada32d19`
- 1112121 (userID 11) | `b1c7ca69-7307-4be3-bdc6-e3fc987a89a3` | eye_tracking_validation_simple_2pages.pdf | 2026-05-19T16:38:51 -> 2026-05-19T16:39:29.615 (0.64 min) | output on | split 1/2 from `b1c7ca69-7307-4be3-bdc6-e3fc987a89a3`
- 1112121 (userID 11) | `b1506ee1-4692-4a64-a3c1-cacfeb78cfeb` | c1_walt_disney_4.pdf | 2026-05-19T16:39:48.460 -> 2026-05-19T16:42:40.917 (2.87 min) | output on | split 2/2 from `b1c7ca69-7307-4be3-bdc6-e3fc987a89a3`
- 1112121 (userID 11) | `1a669bd6-6ddb-42cd-91f3-1960f3dd82ff` | eye_tracking_validation_simple_2pages.pdf | 2026-05-21T16:07:41 -> 2026-05-21T16:07:44.529 (0.06 min) | output on | split 1/2 from `1a669bd6-6ddb-42cd-91f3-1960f3dd82ff`
- 1112121 (userID 11) | `eb0d35b5-e405-4b36-a5c7-9bd4060c2e3e` | b2_animals_of_rainforests_1.pdf | 2026-05-21T16:08:16.162 -> 2026-05-21T16:11:01.020 (2.75 min) | output on | split 2/2 from `1a669bd6-6ddb-42cd-91f3-1960f3dd82ff`
- 1112139 (userID 16) | `c0fe3c20-5c53-46f6-8fb3-01fa71441a1a` | eye_tracking_validation_simple_2pages.pdf | 2026-05-19T16:52:57 -> 2026-05-19T16:53:40.220 (0.72 min) | output on | split 1/2 from `c0fe3c20-5c53-46f6-8fb3-01fa71441a1a`
- 1112139 (userID 16) | `cadfd23b-96c0-47b0-aa16-52010d70275a` | c2_noisy_humans_1.pdf | 2026-05-19T16:54:12.090 -> 2026-05-19T17:01:10.617 (6.98 min) | output on | split 2/2 from `c0fe3c20-5c53-46f6-8fb3-01fa71441a1a`

## Duplicate Same-PDF Sessions: Which One Was Treated As Real

When the same user had multiple sessions for the same PDF, the audit treated the session with the most in-window translations as the real one. If translations tied, it used the longer session. The ignored rows are usually setup/test sessions.

- 1059657 (userID 53) | b2_sticky_fingers_4.pdf | kept: 2026-06-02T15:49:06 5.2m 58 in-window translations on | ignored: 2026-06-02T15:48:42 0.4m 1 in-window translations off
- 1065023 (userID 17) | b2_electromagnetic_radiation_2.pdf | kept: 2026-05-19T18:00:25.369 4.32m 36 in-window translations off | ignored: 2026-05-19T18:06:24 0.33m 1 in-window translations off
- 1093313 (userID 28) | b2_first_american_3.pdf | kept: 2026-06-03T10:28:40 2.87m 181 in-window translations on | ignored: 2026-06-03T10:27:43 0.95m 28 in-window translations off
- 1093313 (userID 28) | b2_sticky_fingers_4.pdf | kept: 2026-06-04T10:18:05 7.5m 239 in-window translations on | ignored: 2026-06-04T10:17:48 0.28m 21 in-window translations off
- 1093322 (userID 10) | b2_electromagnetic_radiation_2.pdf | kept: 2026-05-18T15:46:51.470 6.78m 57 in-window translations on | ignored: 2026-05-27T09:21:12 4.4m 35 in-window translations on; 2026-05-27T09:20:58 0.23m 1 in-window translations off
- 1093332 (userID 54) | b2_sticky_fingers_4.pdf | kept: 2026-06-04T10:04:14 5.63m 47 in-window translations on | ignored: 2026-06-04T10:03:56 0.3m 4 in-window translations off
- 1093379 (userID 45) | b2_first_american_3.pdf | kept: 2026-05-29T09:24:16 4.88m 106 in-window translations on | ignored: 2026-05-29T09:23:48 0.47m 6 in-window translations off
- 1093379 (userID 45) | c2_rosa_parks_2.pdf | kept: 2026-05-27T13:02:59 4.82m 68 in-window translations off | ignored: 2026-05-27T12:58:35 4.4m 5 in-window translations on
- 1093390 (userID 55) | b2_electromagnetic_radiation_2.pdf | kept: 2026-06-02T11:14:44 6.38m 363 in-window translations on | ignored: 2026-06-02T11:14:38 0.1m 1 in-window translations off
- 1093413 (userID 49) | c1_walt_disney_4.pdf | kept: 2026-05-28T13:40:33.162 3.92m 26 in-window translations on | ignored: 2026-05-28T13:48:43 0.2m 1 in-window translations on
- 1093505 (userID 41) | b2_animals_of_rainforests_1.pdf | kept: 2026-05-28T14:37:46 3.75m 18 in-window translations on | ignored: 2026-05-28T14:37:32 0.23m 5 in-window translations off
- 1093505 (userID 41) | c1_native_american_conflicts_3.pdf | kept: 2026-06-03T15:40:50 0.72m 16 in-window translations off | ignored: 2026-06-03T15:41:33 3.82m 9 in-window translations on
- 1097463 (userID 12) | c1_bee_reading_2.pdf | kept: 2026-05-18T16:51:46 4.38m 65 in-window translations on | ignored: 2026-05-18T16:51:20.336 0.34m 6 in-window translations off
- 1097463 (userID 12) | c2_noisy_humans_1.pdf | kept: 2026-05-19T12:58:23 4.55m 47 in-window translations off | ignored: 2026-05-19T12:58:12 0.18m 1 in-window translations on
- 1100613 (userID 52) | b2_animals_of_rainforests_1.pdf | kept: 2026-05-29T16:14:36 5.58m 24 in-window translations off | ignored: 2026-05-29T16:14:26 0.17m 1 in-window translations on
- 1100613 (userID 52) | c1_bee_reading_2.pdf | kept: 2026-06-05T10:36:44 5.68m 44 in-window translations on | ignored: 2026-06-05T10:36:30 0.23m 1 in-window translations off
- 1100758 (userID 36) | c2_rosa_parks_2.pdf | kept: 2026-05-26T17:06:40 6.13m 83 in-window translations on | ignored: 2026-05-26T17:00:00 0.83m 14 in-window translations off; 2026-05-26T17:00:50 1.8m 13 in-window translations on; 2026-05-26T17:05:29 0.17m 1 in-window translations on; 2026-05-26T17:02:41 0.08m 1 in-window translations on
- 1103080 (userID 35) | c2_noisy_humans_1.pdf | kept: 2026-06-02T16:27:32 3.67m 18 in-window translations off | ignored: 2026-06-02T16:26:30 1.03m 9 in-window translations on
- 1104782 (userID 56) | b2_electromagnetic_radiation_2.pdf | kept: 2026-06-05T09:53:13 5.12m 35 in-window translations off | ignored: 2026-06-05T09:52:23 0.83m 3 in-window translations on
- 1104818 (userID 40) | c1_age_of_exploration_1.pdf | kept: 2026-05-27T14:47:16 4.07m 21 in-window translations on | ignored: 2026-05-27T14:46:54 0.37m 4 in-window translations off
- 1108328 (userID 25) | b2_animals_of_rainforests_1.pdf | kept: 2026-05-30T12:38:33 4.5m 39 in-window translations on | ignored: 2026-05-30T12:38:14 0.32m 3 in-window translations off
- 1108330 (userID 19) | b2_first_american_3.pdf | kept: 2026-05-26T09:13:24 4.8m 21 in-window translations off | ignored: 2026-05-26T09:13:14 0.17m 1 in-window translations on
- 1108330 (userID 19) | c2_noisy_humans_1.pdf | kept: 2026-05-19T10:04:56 6.48m 409 in-window translations on | ignored: 2026-05-26T09:04:37 0.58m 3 in-window translations on
- 1108339 (userID 20) | c1_bee_reading_2.pdf | kept: 2026-05-19T10:30:43.850 3.8m 31 in-window translations off | ignored: 2026-05-19T10:34:49 1.97m 12 in-window translations on
- 1108339 (userID 20) | c1_walt_disney_4.pdf | kept: 2026-05-19T10:25:27 4.9m 13 in-window translations off | ignored: 2026-05-19T10:24:22.302 1.01m 6 in-window translations on
- 1108346 (userID 34) | c1_age_of_exploration_1.pdf | kept: 2026-05-26T11:16:08 3.5m 3 in-window translations off | ignored: 2026-05-26T11:15:38 0.35m 1 in-window translations off
- 1108348 (userID 6) | c1_age_of_exploration_1.pdf | kept: 2026-05-18T13:49:47 6.2m 161 in-window translations on | ignored: 2026-05-18T13:49:29 0.3m 1 in-window translations off
- 1108360 (userID 8) | b2_sticky_fingers_4.pdf | kept: 2026-06-03T15:23:06 3.58m 29 in-window translations off | ignored: 2026-06-03T15:22:39 0.45m 1 in-window translations on
- 1108360 (userID 8) | c2_noisy_humans_1.pdf | kept: 2026-05-25T15:16:26 2.87m 8 in-window translations off | ignored: 2026-05-25T15:16:08 0.3m 2 in-window translations on
- 1108364 (userID 38) | b2_first_american_3.pdf | kept: 2026-05-28T12:37:10 4.85m 33 in-window translations off | ignored: 2026-05-28T12:35:47 1.38m 2 in-window translations on
- 1108364 (userID 38) | c2_rosa_parks_2.pdf | kept: 2026-05-27T12:00:00 3.65m 36 in-window translations off | ignored: 2026-05-27T12:09:21 1.42m 1 in-window translations off
- 1108365 (userID 48) | c1_native_american_conflicts_3.pdf | kept: 2026-06-02T16:00:02 0.92m 24 in-window translations on | ignored: 2026-06-02T16:00:57 2.92m 7 in-window translations off
- 1108367 (userID 5) | b2_sticky_fingers_4.pdf | kept: 2026-05-21T11:40:16 3.32m 14 in-window translations off | ignored: 2026-05-21T11:39:43 0.55m 2 in-window translations on
- 1108367 (userID 5) | c1_age_of_exploration_1.pdf | kept: 2026-05-18T13:17:56 3.25m 29 in-window translations off | ignored: 2026-05-18T13:17:27 0.48m 4 in-window translations on
- 1108382 (userID 7) | c1_bee_reading_2.pdf | kept: 2026-05-18T14:33:25 5.35m 78 in-window translations on | ignored: 2026-05-18T14:33:06.331 0.26m 1 in-window translations off
- 1108382 (userID 7) | c2_noisy_humans_1.pdf | kept: 2026-05-19T14:59:44 6.25m 103 in-window translations on | ignored: 2026-05-19T14:58:41 0.12m 1 in-window translations on
- 1108387 (userID 18) | c1_native_american_conflicts_3.pdf | kept: 2026-05-20T13:01:52 5.87m 128 in-window translations on | ignored: 2026-05-20T12:59:50 2.03m 3 in-window translations on
- 1112096 (userID 14) | c2_noisy_humans_1.pdf | kept: 2026-05-20T10:16:22 5.03m 29 in-window translations on | ignored: 2026-05-20T10:14:44 1.63m 6 in-window translations off
- 1112106 (userID 15) | c1_native_american_conflicts_3.pdf | kept: 2026-05-19T17:28:53 2.18m 5 in-window translations off | ignored: 2026-05-19T17:31:04 1.03m 4 in-window translations on
- 1112115 (userID 51) | b2_electromagnetic_radiation_2.pdf | kept: 2026-06-04T14:06:08 4.05m 19 in-window translations on | ignored: 2026-06-04T14:13:08 3.43m 13 in-window translations off
- 1112121 (userID 11) | c2_rosa_parks_2.pdf | kept: 2026-05-18T16:25:05 2.02m 28 in-window translations on | ignored: 2026-05-18T16:23:52 1.22m 7 in-window translations off
- 1112139 (userID 16) | b2_first_american_3.pdf | kept: 2026-05-26T18:37:50 2.57m 29 in-window translations on | ignored: 2026-05-26T18:37:38 0.2m 4 in-window translations off
- 1112139 (userID 16) | c2_rosa_parks_2.pdf | kept: 2026-05-19T17:05:06 3.53m 95 in-window translations off | ignored: 2026-05-19T17:04:23 0.72m 11 in-window translations on

## Potential Problems: Daily Text Pattern

Expected pattern: on a valid experiment day, a user should normally have two texts of the same prefix (`b2`, `c1`, or `c2`).

- 1093322 (userID 10) on 2026-05-27 for `b2`: expected 2 B2 texts on this day, found 1. Docs found: b2_sticky_fingers_4.pdf.
- 1095564 (userID 42) on 2026-05-25 for `c2`: expected 2 C2 texts on this day, found 1. Docs found: c2_noisy_humans_1.pdf.
- 1095564 (userID 42) on 2026-05-28 for `b2`: expected 2 B2 texts on this day, found 1. Docs found: b2_animals_of_rainforests_1.pdf.
- 1103080 (userID 35) on 2026-06-04 for `c1`: expected 2 C1 texts on this day, found 1. Docs found: c1_age_of_exploration_1.pdf.
- 1108328 (userID 25) on 2026-05-19 for `c1`: expected 2 C1 texts on this day, found 1. Docs found: c1_native_american_conflicts_3.pdf.
- 1108382 (userID 7) on 2026-05-19 for `c2`: expected 2 C2 texts on this day, found 1. Docs found: c2_noisy_humans_1.pdf.
- 1112096 (userID 14) on 2026-05-18 for `b2`: expected 2 B2 texts on this day, found 1. Docs found: b2_animals_of_rainforests_1.pdf.
- 1112096 (userID 14) on 2026-05-19 for `c1`: expected 2 C1 texts on this day, found 1. Docs found: c1_native_american_conflicts_3.pdf.
- 1112096 (userID 14) on 2026-05-21 for `c1`: expected 2 C1 texts on this day, found 1. Docs found: c1_walt_disney_4.pdf.
- 1112119c (userID 33) on 2026-05-27 for `c1`: expected 2 C1 texts on this day, found 1. Docs found: c1_bee_reading_2.pdf.
- 1112121 (userID 11) on 2026-05-19 for `c1`: expected 2 C1 texts on this day, found 1. Docs found: c1_walt_disney_4.pdf.

## Potential Problems: User Does Not Have Exactly 8 Texts

- 1093313 (userID 28): 6 chosen text PDFs instead of 8. Docs: b2_animals_of_rainforests_1.pdf, b2_electromagnetic_radiation_2.pdf, b2_first_american_3.pdf, b2_sticky_fingers_4.pdf, c2_noisy_humans_1.pdf, c2_rosa_parks_2.pdf.
- 1093322 (userID 10): 5 chosen text PDFs instead of 8. Docs: b2_animals_of_rainforests_1.pdf, b2_electromagnetic_radiation_2.pdf, b2_sticky_fingers_4.pdf, c1_bee_reading_2.pdf, c1_walt_disney_4.pdf.
- 1093515 (userID 27): 6 chosen text PDFs instead of 8. Docs: c1_age_of_exploration_1.pdf, c1_bee_reading_2.pdf, c1_native_american_conflicts_3.pdf, c1_walt_disney_4.pdf, c2_noisy_humans_1.pdf, c2_rosa_parks_2.pdf.
- 1095564 (userID 42): 6 chosen text PDFs instead of 8. Docs: b2_animals_of_rainforests_1.pdf, b2_first_american_3.pdf, b2_sticky_fingers_4.pdf, c1_bee_reading_2.pdf, c1_walt_disney_4.pdf, c2_noisy_humans_1.pdf.
- 1103080 (userID 35): 7 chosen text PDFs instead of 8. Docs: b2_first_american_3.pdf, b2_sticky_fingers_4.pdf, c1_age_of_exploration_1.pdf, c1_bee_reading_2.pdf, c1_native_american_conflicts_3.pdf, c2_noisy_humans_1.pdf, c2_rosa_parks_2.pdf.
- 1108328 (userID 25): 5 chosen text PDFs instead of 8. Docs: b2_animals_of_rainforests_1.pdf, b2_electromagnetic_radiation_2.pdf, b2_first_american_3.pdf, b2_sticky_fingers_4.pdf, c1_native_american_conflicts_3.pdf.
- 1108353 (userID 22): 2 chosen text PDFs instead of 8. Docs: c1_age_of_exploration_1.pdf, c1_native_american_conflicts_3.pdf.
- 1108382 (userID 7): 7 chosen text PDFs instead of 8. Docs: b2_animals_of_rainforests_1.pdf, b2_electromagnetic_radiation_2.pdf, c1_age_of_exploration_1.pdf, c1_bee_reading_2.pdf, c1_native_american_conflicts_3.pdf, c1_walt_disney_4.pdf, c2_noisy_humans_1.pdf.
- 1108387 (userID 18): 6 chosen text PDFs instead of 8. Docs: b2_electromagnetic_radiation_2.pdf, b2_sticky_fingers_4.pdf, c1_age_of_exploration_1.pdf, c1_bee_reading_2.pdf, c1_native_american_conflicts_3.pdf, c1_walt_disney_4.pdf.
- 1112096 (userID 14): 5 chosen text PDFs instead of 8. Docs: b2_animals_of_rainforests_1.pdf, c1_native_american_conflicts_3.pdf, c1_walt_disney_4.pdf, c2_noisy_humans_1.pdf, c2_rosa_parks_2.pdf.
- 1112119c (userID 33): 5 chosen text PDFs instead of 8. Docs: b2_animals_of_rainforests_1.pdf, b2_electromagnetic_radiation_2.pdf, b2_first_american_3.pdf, b2_sticky_fingers_4.pdf, c1_bee_reading_2.pdf.
- 1112121 (userID 11): 7 chosen text PDFs instead of 8. Docs: b2_animals_of_rainforests_1.pdf, b2_electromagnetic_radiation_2.pdf, b2_first_american_3.pdf, b2_sticky_fingers_4.pdf, c1_walt_disney_4.pdf, c2_noisy_humans_1.pdf, c2_rosa_parks_2.pdf.

## Checked Long-Duration Sessions: No Open Timing Fix Needed

These are the sessions already checked or accepted by you. This now includes the former unusual-duration entries from the previous lines 717-764. They are not treated as open duration or long-pause errors below.

### Still Above 8 Minutes, But Checked/Accepted

- 1108353 (userID 22) | c1_native_american_conflicts_3.pdf | 18.15 min | 2026-05-19T14:29:37 | output off | session `37e1840d-3839-41db-977c-02a4e68b71c2`
- 1080401 (userID 31) | c1_native_american_conflicts_3.pdf | 15.53 min | 2026-05-28T09:52:25 | output off | session `07998834-fb83-475c-a5e4-c2981c6371d6`
- 1080401 (userID 31) | c1_age_of_exploration_1.pdf | 13.18 min | 2026-05-30T12:49:49 | output off | session `b3099ed7-3994-418f-8476-b491182f79b5`
- 1100758 (userID 36) | c1_native_american_conflicts_3.pdf | 11.85 min | 2026-05-25T13:53:08 | output off | session `2c2c3aad-9857-4fee-8f3a-bdfd2063f1aa`
- 1112139 (userID 16) | c1_bee_reading_2.pdf | 10.82 min | 2026-05-18T19:38:22 | output off | session `692206b2-426c-43a5-92ea-3733e4e2e4a6`
- 1084609 (userID 44) | c1_bee_reading_2.pdf | 10.38 min | 2026-05-25T18:20:13 | output off | session `1d634156-b062-4155-b2fd-30771a282724`
- 1112139 (userID 16) | c1_age_of_exploration_1.pdf | 9.85 min | 2026-05-18T19:24:18 | output on | session `9ad03ea4-153b-4182-9ef1-d4a7f95e1a70`
- 1080401 (userID 31) | c2_rosa_parks_2.pdf | 9.37 min | 2026-05-29T17:31:33 | output off | session `a7bec24a-22e8-4476-af16-469f3c6e95e7`
- 1080401 (userID 31) | c1_bee_reading_2.pdf | 9.32 min | 2026-05-30T13:07:03 | output on | session `cc47959e-863c-4698-adde-8b842bb345a0`
- 1108353 (userID 22) | c1_age_of_exploration_1.pdf | 8.73 min | 2026-05-19T14:20:37 | output on | session `6317d0ef-9a87-4488-a2ac-184c157ecbe3`
- 1080401 (userID 31) | b2_electromagnetic_radiation_2.pdf | 8.67 min | 2026-05-25T09:20:03 | output off | session `604a8afe-cbad-461c-b0db-78a2c9ed750a`
- 1093379 (userID 45) | c2_noisy_humans_1.pdf | 8.47 min | 2026-05-27T12:46:19 | output on | session `21ac03fb-e7ea-4f6f-982d-e3b4992ca4c0`
- 1093379 (userID 45) | c1_walt_disney_4.pdf | 8.38 min | 2026-05-26T10:47:49 | output on | session `0d609472-7b65-482a-bc20-5e0edffb777a`
- 1108348 (userID 6) | c2_noisy_humans_1.pdf | 8.37 min | 2026-05-19T11:40:24.695 | output off | session `9bdf2d24-49fd-4b98-a123-564ac1939171`
- 1112096 (userID 14) | b2_animals_of_rainforests_1.pdf | 8.27 min | 2026-05-18T18:10:52 | output on | session `8f0591ce-cbb9-4718-9b3e-0fc0a2bfb978`
- 1108387 (userID 18) | c1_bee_reading_2.pdf | 8.15 min | 2026-06-04T11:35:05 | output on | session `d1dc375c-d963-4e1d-95fb-a30c415b0e11`
- 1093332 (userID 54) | c1_walt_disney_4.pdf | 8.12 min | 2026-05-30T17:22:21 | output on | session `07ac5aba-7fc6-4d0b-93f0-f3638b276ab5`
- 1108335 (userID 26) | b2_sticky_fingers_4.pdf | 8.08 min | 2026-06-04T12:03:29 | output on | session `41f5df45-3138-4fd8-b45f-3df505ea402d`
- 1108348 (userID 6) | b2_sticky_fingers_4.pdf | 8.07 min | 2026-05-20T11:31:19.903 | output off | session `e0d4706d-e7b7-41af-9741-829957381e17`
- 1080401 (userID 31) | c2_noisy_humans_1.pdf | 8.05 min | 2026-05-29T17:46:09 | output on | session `84e8c4d2-d3fa-4e11-9698-adcd196924eb`

### Checked/Accepted Or Fixed Below 8 Minutes

- 1093313 (userID 28) | b2_sticky_fingers_4.pdf | current 7.5 min | 2026-06-04T10:18:05 | output on | session `e69041c2-44d3-42e0-9987-f23d126eeb68`
- 1084609 (userID 44) | c2_noisy_humans_1.pdf | current 7 min | 2026-05-26T13:36:03 | output off | session `444fb265-0faa-4fcc-85f0-35322a297345`
- 1108357 (userID 23) | c1_age_of_exploration_1.pdf | current 6.77 min | 2026-06-03T10:03:43 | output on | session `60007f9e-ac83-4d02-8bd7-c957edf73d3b`
- 1097463 (userID 12) | c1_age_of_exploration_1.pdf | current 6.67 min | 2026-05-18T16:42:57 | output off | session `5cab1f9b-6f9b-411d-8c8e-cec9137cb4c0`
- 1093390 (userID 55) | b2_electromagnetic_radiation_2.pdf | current 6.38 min | 2026-06-02T11:14:44 | output on | session `ada13f59-b046-4c93-a5f7-b09b9cab5948`
- 1093348 (userID 39) | c1_bee_reading_2.pdf | current 6.35 min | 2026-05-26T15:02:28 | output off | session `7dc7ad85-3c80-49a8-87ee-80b727e42556`
- 1108382 (userID 7) | c2_noisy_humans_1.pdf | current 6.25 min | 2026-05-19T14:59:44 | output on | session `1a1eeaaa-8726-434a-9360-dcbef482e911`
- 1108348 (userID 6) | c1_age_of_exploration_1.pdf | current 6.2 min | 2026-05-18T13:49:47 | output on | session `566cc61c-0ac3-4fb6-9256-7f55b55c2fee`
- 1108348 (userID 6) | c1_walt_disney_4.pdf | current 6.18 min | 2026-05-18T13:38:09 | output off | session `cf06b6aa-0f00-4c62-86d1-283a34736f09`
- 1084609 (userID 44) | c1_age_of_exploration_1.pdf | current 6.15 min | 2026-05-25T18:34:14 | output on | session `a329b9b7-7b2a-4d9e-8eb2-8cc9badb749e`
- 1093379 (userID 45) | c1_bee_reading_2.pdf | current 6.13 min | 2026-05-26T11:00:20 | output off | session `011fb9da-eb69-428b-8216-bf3e124857c6`
- 1100758 (userID 36) | c2_rosa_parks_2.pdf | current 6.13 min | 2026-05-26T17:06:40 | output on | session `0b470ee2-68e3-4ff1-a51f-a42bc14041e7`
- 1108323 (userID 13) | c2_noisy_humans_1.pdf | current 6.03 min | 2026-05-18T17:13:05.444 | output on | session `501ccebc-659a-487d-bcb1-53a03738da89`
- 1108357 (userID 23) | c2_noisy_humans_1.pdf | current 5.87 min | 2026-05-19T15:19:33 | output off | session `2e35c536-79ff-4a44-9155-7b5e050b15ff`
- 1093322 (userID 10) | b2_animals_of_rainforests_1.pdf | current 5.8 min | 2026-05-18T15:54:23 | output off | session `c453644c-7b9c-4d36-93ef-a8da76f00adc`
- 1093348 (userID 39) | c2_noisy_humans_1.pdf | current 5.8 min | 2026-05-25T15:46:21.220 | output off | session `7f84e707-ff3d-4c85-890b-82f784a0f030`
- 1108330 (userID 19) | c2_rosa_parks_2.pdf | current 5.77 min | 2026-05-19T09:55:33 | output off | session `8e022878-6e8d-44c6-b762-112d3673e2f9`
- 1093515 (userID 27) | c1_walt_disney_4.pdf | current 5.69 min | 2026-05-21T09:20:51.334 | output on | session `977369c8-c045-493f-881c-f2af4301a6a0`
- 1108387 (userID 18) | b2_sticky_fingers_4.pdf | current 5.62 min | 2026-05-19T09:24:21 | output off | session `d4a5f1ff-be4e-4681-98e4-1911db26d8d2`
- 1093505 (userID 41) | c1_bee_reading_2.pdf | current 5.53 min | 2026-05-25T16:40:22 | output off | session `13bc6b94-8791-4212-a001-ab763d578bed`
- 1065023 (userID 17) | c2_noisy_humans_1.pdf | current 5.5 min | 2026-05-18T20:13:44 | output off | session `2a604556-49ca-4707-b6f6-2d6138e16d7c`
- 1112106 (userID 15) | c2_noisy_humans_1.pdf | current 5.47 min | 2026-05-18T18:56:14 | output off | session `35dc1e38-d6db-417c-b340-2461aac0dc66`
- 1093322 (userID 10) | c1_bee_reading_2.pdf | current 5.43 min | 2026-05-20T09:52:59 | output off | session `ea531f61-51d7-414e-9adf-8839f7dd0c26`
- 1108339 (userID 20) | c2_noisy_humans_1.pdf | current 5.35 min | 2026-05-20T14:46:05 | output on | session `a3fc9cf5-eb74-4415-9645-ed76b04722ec`
- 1108382 (userID 7) | c1_bee_reading_2.pdf | current 5.35 min | 2026-05-18T14:33:25 | output on | session `fdb12a6e-aeb5-469a-ba30-51044d0da005`
- 1093403 (userID 9) | c2_noisy_humans_1.pdf | current 5.29 min | 2026-05-18T15:15:01.583 | output on | session `cabb8f46-b750-4913-95de-54d1d12d1874`
- 1093322 (userID 10) | c1_walt_disney_4.pdf | current 5.23 min | 2026-05-20T09:43:44 | output on | session `8ddb2ff7-ca06-497c-82d2-e4974f51de40`
- 1112119c (userID 33) | c1_bee_reading_2.pdf | current 5.2 min | 2026-05-27T10:44:03 | output on | session `d7550b5e-6b65-445b-8c5a-cab8ba307c64`
- 1108382 (userID 7) | c1_walt_disney_4.pdf | current 5.15 min | 2026-05-21T14:41:17 | output on | session `da1f519a-68f9-4a1c-9e52-af3be8b746ef`
- 1093390 (userID 55) | c1_bee_reading_2.pdf | current 5.03 min | 2026-05-30T17:52:59 | output on | session `05a90b22-e2f0-4c72-a0f1-bc78419358cd`
- 1112096 (userID 14) | c2_noisy_humans_1.pdf | current 5.03 min | 2026-05-20T10:16:22 | output on | session `f4c32c0e-5f43-4ba3-a623-d0ffcd49e461`
- 1112119c (userID 33) | b2_sticky_fingers_4.pdf | current 5.03 min | 2026-05-25T11:34:16 | output on | session `b7613186-3756-445b-aba2-c3839f33c4bf`
- 1108344 (userID 37) | c1_bee_reading_2.pdf | current 5.02 min | 2026-05-26T16:33:29 | output off | session `0f2bf24c-64b7-4683-90c1-362df55604ff`
- 1093348 (userID 39) | c2_rosa_parks_2.pdf | current 4.9 min | 2026-05-25T15:38:58.256 | output on | session `6c5c45fb-5383-4047-aa17-ad1a68387a72`
- 1108330 (userID 19) | b2_first_american_3.pdf | current 4.8 min | 2026-05-26T09:13:24 | output off | session `993279e2-4f05-4ace-af51-4eaef8c250ba`
- 1108323 (userID 13) | b2_animals_of_rainforests_1.pdf | current 4.57 min | 2026-05-19T16:20:16 | output off | session `9fffa5b8-0b82-426d-805d-c0049bd98060`
- 1108335 (userID 26) | c1_native_american_conflicts_3.pdf | current 4.53 min | 2026-05-30T16:54:07 | output off | session `fd864e13-32bf-4819-99de-f47ff44ac346`
- 1104806 (userID 50) | b2_electromagnetic_radiation_2.pdf | current 4.4 min | 2026-05-29T14:01:34 | output on | session `8ca23e63-d7e8-4cfa-bb87-78fa478943f4`
- 1100758 (userID 36) | c1_walt_disney_4.pdf | current 4.28 min | 2026-05-25T13:39:32 | output on | session `b9feb6d8-a85f-44b0-a6f9-b49a30597b24`
- 1112106 (userID 15) | c2_rosa_parks_2.pdf | current 3.97 min | 2026-05-18T18:49:34 | output on | session `ef66d038-9512-4c1e-a3f7-012d8a6f17f6`
- 1108357 (userID 23) | c2_rosa_parks_2.pdf | current 3.77 min | 2026-05-19T15:29:31 | output on | session `9485615f-8d01-4965-b5b0-762221fdc5ef`
- 1108346 (userID 34) | b2_sticky_fingers_4.pdf | current 3.57 min | 2026-05-27T10:23:35 | output on | session `83c9b5c5-6772-473e-a233-04369504584e`
- 1108346 (userID 34) | c1_native_american_conflicts_3.pdf | current 3.38 min | 2026-05-28T11:03:07 | output on | session `6dd314f0-d934-486d-adc4-0e6fa9301449`
- 1103080 (userID 35) | c1_bee_reading_2.pdf | current 2.24 min | 2026-05-25T12:19:06.684 | output on | session `0cf369b9-aeef-45af-96ed-1e7bb674c354`

## Potential Problems: Unusual Duration

These are duration flags after excluding checked sessions, manually corrected non-split sessions, and sessions under 4 minutes.

### 1104782 (userID 56) - c1_native_american_conflicts_3.pdf
Session `1d3eb6cd-7d71-4be9-93e3-f7f1f0fbb1ed` started at 2026-06-04T13:43:22 and lasts 7.95 min. Output mode is on and it has 140 in-window translations (140 stored total).
- Why to check it: above global high threshold for output `on` (7.95m vs median 4.52m).
checked
## Potential Problems: Output Mode Pattern Looks Reversed

- 1059657 (userID 53): median output-on time 5.69 min, median output-off time 4.9 min. Why suspicious: output off should usually be slower, but this user is faster with off.
- 1090053 (userID 47): median output-on time 4.52 min, median output-off time 4.4 min. Why suspicious: output off should usually be slower, but this user is faster with off.
- 1093332 (userID 54): median output-on time 5.63 min, median output-off time 4.58 min. Why suspicious: output off should usually be slower, but this user is faster with off.
- 1093379 (userID 45): median output-on time 6.07 min, median output-off time 5.02 min. Why suspicious: output off should usually be slower, but this user is faster with off.
- 1093390 (userID 55): median output-on time 5.34 min, median output-off time 5.06 min. Why suspicious: output off should usually be slower, but this user is faster with off.
- 1100496 (userID 46): median output-on time 4.63 min, median output-off time 4.55 min. Why suspicious: output off should usually be slower, but this user is faster with off.
- 1100613 (userID 52): median output-on time 5.65 min, median output-off time 4.57 min. Why suspicious: output off should usually be slower, but this user is faster with off.
- 1104782 (userID 56): median output-on time 6.64 min, median output-off time 4.68 min. Why suspicious: output off should usually be slower, but this user is faster with off.
- 1104806 (userID 50): median output-on time 6.33 min, median output-off time 5.57 min. Why suspicious: output off should usually be slower, but this user is faster with off.
- 1104816 (userID 29): median output-on time 4.93 min, median output-off time 4.15 min. Why suspicious: output off should usually be slower, but this user is faster with off.
- 1108335 (userID 26): median output-on time 5.92 min, median output-off time 4.73 min. Why suspicious: output off should usually be slower, but this user is faster with off.
- 1108364 (userID 38): median output-on time 5.67 min, median output-off time 4.85 min. Why suspicious: output off should usually be slower, but this user is faster with off.
- 1108387 (userID 18): median output-on time 6.26 min, median output-off time 6.05 min. Why suspicious: output off should usually be slower, but this user is faster with off.

## Potential Problems: Long Pauses Inside A Session

These are long-pause cases after filtering out checked sessions, manually corrected non-split sessions, sessions under 4 minutes, and translation events outside the current corrected session start/end window.

### 1112115 (userID 51) - b2_sticky_fingers_4.pdf
- Session `1bb13253-9e5e-424f-b220-d3ec72ea27a2`, duration 4.03 min, output on, 6 in-window translations (6 stored total).
- Why to check it: largest in-window gap between translations is 120.85s while the median gap is 27.67s; gap is over one minute.
- Largest gap ends at 2026-06-02T11:45:48.239Z, around text `available, -> commodities`.

### 1093322 (userID 10) - b2_electromagnetic_radiation_2.pdf
- Session `db27365f-b25d-4bec-9931-e7463ac1291c`, duration 6.78 min, output on, 57 in-window translations (57 stored total).
- Why to check it: largest in-window gap between translations is 118.96s while the median gap is 2.93s; gap is over one minute.
- Largest gap ends at 2026-05-18T12:53:38.526Z, around text `images -> Even`.

### 1108365 (userID 48) - c1_walt_disney_4.pdf
- Session `cb3c547f-82c3-4cb6-94cc-a08635a5e2e8`, duration 4.53 min, output off, 14 in-window translations (14 stored total).
- Why to check it: largest in-window gap between translations is 112.29s while the median gap is 6.54s; gap is over one minute.
- Largest gap ends at 2026-06-03T10:11:14.312Z, around text `Meanwhile, -> produced`.

### 1112115 (userID 51) - c2_noisy_humans_1.pdf
- Session `002ae749-6080-4cf5-bdb1-b2d966318f7c`, duration 4.38 min, output off, 13 in-window translations (13 stored total).
- Why to check it: largest in-window gap between translations is 105.86s while the median gap is 11.77s; gap is over one minute.
- Largest gap ends at 2026-05-29T12:35:58.936Z, around text `approximated -> musicologist`.

### 1108360 (userID 8) - c1_age_of_exploration_1.pdf
- Session `5a05fc3f-a734-4209-bc88-0122e615b055`, duration 4.63 min, output on, 8 in-window translations (8 stored total).
- Why to check it: largest in-window gap between translations is 104.75s while the median gap is 19.04s; gap is over one minute.
- Largest gap ends at 2026-05-18T11:57:31.767Z, around text `objects -> explored,`.

### 1093348 (userID 39) - c1_native_american_conflicts_3.pdf
- Session `0399a479-315e-42b8-84e3-e5524a976365`, duration 5.12 min, output off, 15 in-window translations (15 stored total).
- Why to check it: largest in-window gap between translations is 101.81s while the median gap is 11.48s; gap is over one minute.
- Largest gap ends at 2026-06-04T12:05:46.944Z, around text `America -> slew`.

### 1100497 (userID 30) - b2_electromagnetic_radiation_2.pdf
- Session `d822699f-42ed-4cd2-bb0b-c926b459da8a`, duration 5.02 min, output on, 6 in-window translations (6 stored total).
- Why to check it: largest in-window gap between translations is 98.61s while the median gap is 12.65s; gap is over one minute.
- Largest gap ends at 2026-05-21T14:52:14.714Z, around text `electromagnetic -> gain`.

### 1104816 (userID 29) - c2_noisy_humans_1.pdf
- Session `14f605e4-8639-41bf-9536-7ce2f87f8c8f`, duration 6.43 min, output on, 25 in-window translations (25 stored total).
- Why to check it: largest in-window gap between translations is 98.14s while the median gap is 4.24s; gap is over one minute.
- Largest gap ends at 2026-05-21T14:25:47.754Z, around text `overflights -> "Nature`.

### 1104818 (userID 40) - b2_sticky_fingers_4.pdf
- Session `d1280697-9b46-49b5-93a2-7bb5fae5f23d`, duration 4.22 min, output on, 7 in-window translations (7 stored total).
- Why to check it: largest in-window gap between translations is 96.37s while the median gap is 19.18s; gap is over one minute.
- Largest gap ends at 2026-05-25T13:19:41.652Z, around text `cacao -> adhere`.

### 1100496 (userID 46) - c2_noisy_humans_1.pdf
- Session `64590fb2-c90b-43de-b6ab-c754218973bc`, duration 4.53 min, output off, 11 in-window translations (11 stored total).
- Why to check it: largest in-window gap between translations is 89.4s while the median gap is 8.6s; gap is over one minute.
- Largest gap ends at 2026-05-29T07:44:34.950Z, around text `areas -> scare`.

### 1100497 (userID 30) - b2_animals_of_rainforests_1.pdf
- Session `36061f30-752f-4ab6-a808-3ddd89255df3`, duration 4.65 min, output off, 17 in-window translations (17 stored total).
- Why to check it: largest in-window gap between translations is 86.13s while the median gap is 2.37s; gap is over one minute.
- Largest gap ends at 2026-05-21T14:44:05.981Z, around text `two -> mostly`.

### 1100758 (userID 36) - b2_sticky_fingers_4.pdf
- Session `2d8eccca-1f6a-474c-bd5d-cf9269ea480d`, duration 4 min, output off, 31 in-window translations (31 stored total).
- Why to check it: largest in-window gap between translations is 85.5s while the median gap is 2.38s; gap is over one minute.
- Largest gap ends at 2026-05-27T12:37:30.376Z, around text `pods -> designated`.

### 1100497 (userID 30) - c1_age_of_exploration_1.pdf
- Session `19291736-7952-4190-a618-ec329989161b`, duration 4.58 min, output on, 19 in-window translations (19 stored total).
- Why to check it: largest in-window gap between translations is 85.25s while the median gap is 4.79s; gap is over one minute.
- Largest gap ends at 2026-05-27T08:05:52.833Z, around text `interests, -> helpedexplorers`.

### 1093332 (userID 54) - c2_rosa_parks_2.pdf
- Session `44940a1f-4c02-458f-bdcc-31d8d7ea224d`, duration 4.62 min, output off, 34 in-window translations (34 stored total).
- Why to check it: largest in-window gap between translations is 84.67s while the median gap is 2.92s; gap is over one minute.
- Largest gap ends at 2026-06-03T08:02:39.144Z, around text `transformed -> seamstress`.

### 1093348 (userID 39) - c1_walt_disney_4.pdf
- Session `ed4be697-e0ed-47aa-beda-f28aa983c3b9`, duration 5.9 min, output on, 79 in-window translations (79 stored total).
- Why to check it: largest in-window gap between translations is 84.46s while the median gap is 1.29s; gap is over one minute.
- Largest gap ends at 2026-06-04T12:19:56.136Z, around text `maintaining -> accorded`.

### 1108346 (userID 34) - c1_bee_reading_2.pdf
- Session `adaefc3a-0e9d-4a74-9e74-fff84911f56b`, duration 4.55 min, output on, 16 in-window translations (16 stored total).
- Why to check it: largest in-window gap between translations is 83.5s while the median gap is 0.12s; gap is over one minute.
- Largest gap ends at 2026-05-26T08:23:47.845Z, around text `essential -> According`.

### 1104782 (userID 56) - b2_animals_of_rainforests_1.pdf
- Session `defb93d4-dd2c-4e6b-8a5f-275b39bad1db`, duration 6.37 min, output on, 68 in-window translations (68 stored total).
- Why to check it: largest in-window gap between translations is 75.89s while the median gap is 1.26s; gap is over one minute.
- Largest gap ends at 2026-06-03T09:48:25.870Z, around text `living -> thrive.`.

### 1065023 (userID 17) - c1_bee_reading_2.pdf
- Session `27d90b52-af7b-44d8-9f34-abaae29f3f1e`, duration 5.73 min, output off, 52 in-window translations (52 stored total).
- Why to check it: largest in-window gap between translations is 75.56s while the median gap is 2.74s; gap is over one minute.
- Largest gap ends at 2026-05-20T14:46:36.626Z, around text `changes -> importance`.

### 1100758 (userID 36) - c2_noisy_humans_1.pdf
- Session `9903e67f-dc23-4e52-a966-6567e5a657a8`, duration 6.75 min, output off, 40 in-window translations (40 stored total).
- Why to check it: largest in-window gap between translations is 74.52s while the median gap is 5.41s; gap is over one minute.
- Largest gap ends at 2026-05-26T14:21:42.308Z, around text `restorative -> ReadWorks’`.

### 1093403 (userID 9) - c1_native_american_conflicts_3.pdf
- Session `9ee81d15-c631-4762-8998-4e512736898c`, duration 6.13 min, output off, 74 in-window translations (74 stored total).
- Why to check it: largest in-window gap between translations is 74.21s while the median gap is 2.5s; gap is over one minute.
- Largest gap ends at 2026-05-19T08:10:36.077Z, around text `presence -> smallpox.`.

### 1100758 (userID 36) - b2_animals_of_rainforests_1.pdf
- Session `e7791fca-1908-479e-b272-ed52b93b3052`, duration 4.38 min, output off, 22 in-window translations (22 stored total).
- Why to check it: largest in-window gap between translations is 72.34s while the median gap is 3.96s; gap is over one minute.
- Largest gap ends at 2026-05-28T11:13:12.576Z, around text `sparrows -> climates`.

### 1108387 (userID 18) - c1_age_of_exploration_1.pdf
- Session `d74317ae-a09d-48a7-9786-7943e8d87649`, duration 6.8 min, output off, 104 in-window translations (104 stored total).
- Why to check it: largest in-window gap between translations is 68.77s while the median gap is 1.8s; gap is over one minute.
- Largest gap ends at 2026-05-20T10:14:45.761Z, around text `interests, -> navigators`.

### 1104816 (userID 29) - c1_native_american_conflicts_3.pdf
- Session `11a245c4-bff0-4bfb-89ac-867e38116682`, duration 4.65 min, output on, 41 in-window translations (41 stored total).
- Why to check it: largest in-window gap between translations is 67.47s while the median gap is 0.43s; gap is over one minute.
- Largest gap ends at 2026-05-28T14:08:13.321Z, around text `materials. -> dramatically`.

### 1108382 (userID 7) - b2_electromagnetic_radiation_2.pdf
- Session `877604a0-9ac6-469b-b28a-8ff975833258`, duration 6.53 min, output off, 55 in-window translations (55 stored total).
- Why to check it: largest in-window gap between translations is 63.74s while the median gap is 3.55s; gap is over one minute.
- Largest gap ends at 2026-05-20T11:24:31.320Z, around text `slinky. -> radio`.

### 1093413 (userID 49) - b2_sticky_fingers_4.pdf
- Session `d16c8a0c-eec7-40a7-9e83-91b200671633`, duration 4.43 min, output on, 22 in-window translations (22 stored total).
- Why to check it: largest in-window gap between translations is 62.22s while the median gap is 2.88s; gap is over one minute.
- Largest gap ends at 2026-05-30T10:38:34.531Z, around text `ReadWorks -> harvested`.

### Long-Pause Entries From Previous Report Now Filtered Out

These were in the previous long-pause section but are no longer open long-pause flags because they were checked, manually corrected, under 4 minutes, or because the suspicious gap is outside the current corrected start/end window.

- 1093390 (userID 55) | c1_bee_reading_2.pdf | session `05a90b22-e2f0-4c72-a0f1-bc78419358cd` | already checked/accepted in the duration review list.
- 1104806 (userID 50) | c2_noisy_humans_1.pdf | session `117bf0e4-f2d7-4ea3-b8d6-49ec7552efdd` | largest in-window gap is now 35.66s, below the open long-pause threshold or no longer a top case.
- 1100496 (userID 46) | b2_animals_of_rainforests_1.pdf | session `1688a594-18d5-4ec2-8a55-c766ee99b034` | largest in-window gap is now 53.64s, below the open long-pause threshold or no longer a top case.
- 1108382 (userID 7) | c2_noisy_humans_1.pdf | session `1a1eeaaa-8726-434a-9360-dcbef482e911` | already checked/accepted in the duration review list.
- 1093313 (userID 28) | c2_rosa_parks_2.pdf | session `2b9fb871-1cc9-4176-8ee5-44ea771ed554` | largest in-window gap is now 47.24s, below the open long-pause threshold or no longer a top case.
- 1097463 (userID 12) | b2_first_american_3.pdf | session `4b81c5c9-b5e1-408e-9cfc-117eb4e17ac9` | largest in-window gap is now 54.54s, below the open long-pause threshold or no longer a top case.
- 1100663 (userID 24) | c2_rosa_parks_2.pdf | session `4e0b9023-94c1-4f57-b7a6-2370b8e8cb51` | largest in-window gap is now 56.05s, below the open long-pause threshold or no longer a top case.
- 1112139 (userID 16) | c2_rosa_parks_2.pdf | session `4e3073ca-cfd1-442f-9c62-343ea363dc69` | already manually corrected in the current DB.
- 1093403 (userID 9) | c1_bee_reading_2.pdf | session `4e499daf-a2d5-481a-aded-d175bc5d53a1` | largest in-window gap is now 53.01s, below the open long-pause threshold or no longer a top case.
- 1093515 (userID 27) | c1_bee_reading_2.pdf | session `5f09d6fb-00d7-4a69-b80e-265b19a26762` | largest in-window gap is now 30.02s, below the open long-pause threshold or no longer a top case.
- 1093390 (userID 55) | b2_first_american_3.pdf | session `693d5a52-5784-42ab-b7ee-eb7288c0c31c` | largest in-window gap is now 49.88s, below the open long-pause threshold or no longer a top case.
- 1093348 (userID 39) | c2_rosa_parks_2.pdf | session `6c5c45fb-5383-4047-aa17-ad1a68387a72` | already checked/accepted in the duration review list.
- 1112115 (userID 51) | c1_age_of_exploration_1.pdf | session `6fa727dd-1679-4778-adb4-9dc5a661718d` | largest in-window gap is now 37.93s, below the open long-pause threshold or no longer a top case.
- 1108367 (userID 5) | b2_animals_of_rainforests_1.pdf | session `75cec1ad-74b6-4061-b074-04d2e6124387` | largest in-window gap is now 54.12s, below the open long-pause threshold or no longer a top case.
- 1108328 (userID 25) | c1_native_american_conflicts_3.pdf | session `88537952-da97-4422-86c8-225f22dda44a` | largest in-window gap is now 54.77s, below the open long-pause threshold or no longer a top case.
- 1097463 (userID 12) | b2_animals_of_rainforests_1.pdf | session `8f295f4e-1dda-4f6d-9392-28f1bfdd42f3` | largest in-window gap is now 24.13s, below the open long-pause threshold or no longer a top case.
- 1093390 (userID 55) | b2_electromagnetic_radiation_2.pdf | session `ada13f59-b046-4c93-a5f7-b09b9cab5948` | already checked/accepted in the duration review list.
- 1112115 (userID 51) | c1_walt_disney_4.pdf | session `b6a00409-fb6f-4afb-91b5-7547d7ac56a8` | largest in-window gap is now 57.1s, below the open long-pause threshold or no longer a top case.
- 1112119c (userID 33) | b2_sticky_fingers_4.pdf | session `b7613186-3756-445b-aba2-c3839f33c4bf` | already checked/accepted in the duration review list.
- 1108348 (userID 6) | b2_first_american_3.pdf | session `b8575b1f-516d-4a3e-84fd-f5353dfc5f59` | largest in-window gap is now 27.47s, below the open long-pause threshold or no longer a top case.
- 1100663 (userID 24) | c1_bee_reading_2.pdf | session `c67658ac-80d9-4d50-9563-28621df3fcd0` | largest in-window gap is now 41.92s, below the open long-pause threshold or no longer a top case.
- 1112139 (userID 16) | c2_noisy_humans_1.pdf | session `cadfd23b-96c0-47b0-aa16-52010d70275a` | largest in-window gap is now 53.01s, below the open long-pause threshold or no longer a top case.
- 1065023 (userID 17) | c1_walt_disney_4.pdf | session `e02ead73-7b83-4931-863c-5153f1f7c8e7` | largest in-window gap is now 32.66s, below the open long-pause threshold or no longer a top case.
- 1112139 (userID 16) | b2_animals_of_rainforests_1.pdf | session `f7691c81-728c-4887-927c-6be72d2247d4` | already manually corrected in the current DB.
- 1093403 (userID 9) | c1_age_of_exploration_1.pdf | session `f9929859-4faf-47d9-a7b3-de9c08ff01d5` | current duration is under 4 minutes, accepted by the current review rule.

## Potential Problems: Repetitive Translations At Session End

These cases look for many repeated translations in the final 120 seconds of the current corrected session window. This can indicate that the user was no longer reading/scrolling the PDF and was repeatedly looking at another page or translation source. Checked sessions, manually corrected non-split sessions, and sessions under 4 minutes are excluded.

### 1093313 (userID 28) - c2_rosa_parks_2.pdf
- Session `2b9fb871-1cc9-4176-8ee5-44ea771ed554`, duration 5.9 min, output on, 173 in-window translations.
- Tail signal: 122 translations in the final 120s, 74 unique normalized words, duplicate ratio 39.34%, most repeated word `montgomery` appears 5 times, last 10 events have 8 unique words.
- Last tail words: Americans, enduring, thousand, thirty-seventh., legacy,, legacy,, legacy,, acts, Rosa, anniversary.

### 1112139 (userID 16) - c2_noisy_humans_1.pdf
- Session `cadfd23b-96c0-47b0-aa16-52010d70275a`, duration 6.98 min, output on, 259 in-window translations.
- Tail signal: 102 translations in the final 120s, 68 unique normalized words, duplicate ratio 33.33%, most repeated word `recording` appears 5 times, last 10 events have 7 unique words.
- Last tail words: listened, listened, tape, recording, natural, natural, sounds, recovered, disturbing, listened.

### 1097463 (userID 12) - b2_first_american_3.pdf
- Session `4b81c5c9-b5e1-408e-9cfc-117eb4e17ac9`, duration 4.32 min, output on, 78 in-window translations.
- Tail signal: 59 translations in the final 120s, 32 unique normalized words, duplicate ratio 45.76%, most repeated word `american` appears 7 times, last 10 events have 9 unique words.
- Last tail words: ounce, Postmaster, represent, Postmaster, America, important, Ambassador, Pennsylvania., prevention, famous.

### 1108346 (userID 34) - c1_bee_reading_2.pdf
- Session `adaefc3a-0e9d-4a74-9e74-fff84911f56b`, duration 4.55 min, output on, 16 in-window translations.
- Tail signal: 13 translations in the final 120s, 4 unique normalized words, duplicate ratio 69.23%, most repeated word `larkspur` appears 7 times, last 10 events have 2 unique words.
- Last tail words: larkspur,, particular, particular, larkspur,, larkspur,, larkspur,, particular, particular, larkspur,, larkspur,.

### 1100663 (userID 24) - c2_rosa_parks_2.pdf
- Session `4e0b9023-94c1-4f57-b7a6-2370b8e8cb51`, duration 4.85 min, output on, 103 in-window translations.
- Tail signal: 37 translations in the final 120s, 22 unique normalized words, duplicate ratio 40.54%, most repeated word `pledge` appears 5 times, last 10 events have 6 unique words.
- Last tail words: enduring, observe, enduring, enduring, two, two, enduring, hereunto, Independence, February.

### 1093390 (userID 55) - b2_first_american_3.pdf
- Session `693d5a52-5784-42ab-b7ee-eb7288c0c31c`, duration 5.17 min, output on, 95 in-window translations.
- Tail signal: 26 translations in the final 120s, 16 unique normalized words, duplicate ratio 38.46%, most repeated word `london` appears 7 times, last 10 events have 8 unique words.
- Last tail words: London,, colony,, opposed, represent, every, everyone, everyone, positions, positions, Pennsylvania..

### 1104806 (userID 50) - c2_noisy_humans_1.pdf
- Session `117bf0e4-f2d7-4ea3-b8d6-49ec7552efdd`, duration 6.03 min, output on, 69 in-window translations.
- Tail signal: 28 translations in the final 120s, 17 unique normalized words, duplicate ratio 39.29%, most repeated word `restorative` appears 6 times, last 10 events have 5 unique words.
- Last tail words: surroundings,, psychologists., quickly, quickly, restorative, restorative, restorative, restorative, restorative, disturbing.

### 1100663 (userID 24) - c1_bee_reading_2.pdf
- Session `c67658ac-80d9-4d50-9563-28621df3fcd0`, duration 4.26 min, output on, 61 in-window translations.
- Tail signal: 28 translations in the final 120s, 18 unique normalized words, duplicate ratio 35.71%, most repeated word `enhancementtargeted` appears 6 times, last 10 events have 6 unique words.
- Last tail words: beekeeping, beekeeping, pest, enhancement...targeted, enhancement...targeted, pest, imperative, beekeeping, ensure, food.

### 1065023 (userID 17) - c1_walt_disney_4.pdf
- Session `e02ead73-7b83-4931-863c-5153f1f7c8e7`, duration 4.07 min, output on, 50 in-window translations.
- Tail signal: 25 translations in the final 120s, 16 unique normalized words, duplicate ratio 36%, most repeated word `insignia` appears 6 times, last 10 events have 8 unique words.
- Last tail words: surprising,, insignia, insignia, insignia, "mosquito, appropriate, Supplies, world-famous, "Flying, million.

### 1112115 (userID 51) - c1_age_of_exploration_1.pdf
- Session `6fa727dd-1679-4778-adb4-9dc5a661718d`, duration 4.87 min, output off, 45 in-window translations.
- Tail signal: 13 translations in the final 120s, 7 unique normalized words, duplicate ratio 46.15%, most repeated word `developing` appears 6 times, last 10 events have 5 unique words.
- Last tail words: governments, developing, developing, developing, developing, developing, developing, Longitude, explored,, improved.

### 1108328 (userID 25) - c1_native_american_conflicts_3.pdf
- Session `88537952-da97-4422-86c8-225f22dda44a`, duration 4.34 min, output on, 28 in-window translations.
- Tail signal: 19 translations in the final 120s, 10 unique normalized words, duplicate ratio 47.37%, most repeated word `relationships` appears 4 times, last 10 events have 6 unique words.
- Last tail words: weapons,, weapons,, miles, miles, weapons,, weapons,, scrambling, share, reinforcements, time..

### 1100496 (userID 46) - b2_animals_of_rainforests_1.pdf
- Session `1688a594-18d5-4ec2-8a55-c766ee99b034`, duration 4.63 min, output on, 31 in-window translations.
- Tail signal: 23 translations in the final 120s, 14 unique normalized words, duplicate ratio 39.13%, most repeated word `hemisphere` appears 5 times, last 10 events have 7 unique words.
- Last tail words: predators., Hemisphere,, Hemisphere,, Hemisphere,, Hemisphere,, destroy, biodiversity, skins., mining, habitats.

### 1108367 (userID 5) - b2_animals_of_rainforests_1.pdf
- Session `75cec1ad-74b6-4061-b074-04d2e6124387`, duration 5.03 min, output on, 22 in-window translations.
- Tail signal: 13 translations in the final 120s, 7 unique normalized words, duplicate ratio 46.15%, most repeated word `likely` appears 4 times, last 10 events have 7 unique words.
- Last tail words: cannot, especially, likely, planet,, especially, likely, especially, mining, ecosystems, jaguars.

### 1093515 (userID 27) - c1_bee_reading_2.pdf
- Session `5f09d6fb-00d7-4a69-b80e-265b19a26762`, duration 5.05 min, output off, 57 in-window translations.
- Tail signal: 22 translations in the final 120s, 16 unique normalized words, duplicate ratio 27.27%, most repeated word `pesticide` appears 5 times, last 10 events have 8 unique words.
- Last tail words: bees, honey, pesticide, pesticide, profitable,", resistant, enhancement...targeted, pesticide, management, improved.

### 1112115 (userID 51) - c1_walt_disney_4.pdf
- Session `b6a00409-fb6f-4afb-91b5-7547d7ac56a8`, duration 4.05 min, output on, 20 in-window translations.
- Tail signal: 16 translations in the final 120s, 11 unique normalized words, duplicate ratio 31.25%, most repeated word `insignia` appears 5 times, last 10 events have 5 unique words.
- Last tail words: emblems., insignia, surprising,, insignia, insignia, insignia, famous, famous, insignia, torpedo.
