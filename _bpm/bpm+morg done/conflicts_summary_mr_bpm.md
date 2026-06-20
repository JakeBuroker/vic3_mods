# Morgenroete + BPM conflict audit (Victoria 3 1.13)

Load order used for this audit:

1. Community Mod Framework
2. Morgenroete
3. Better Politics Mod
4. This compatch

## Source baseline

- Community Mod Framework `1.56.0` (`3a892d8`, 2026-06-06)
- Morgenroete `2.8.2 Allemao` (`b399b44`, 2026-06-19)
- Better Politics Mod `2.5.32` (`b90f1da`, 2026-06-13)
- Victoria 3 `1.13.*`

The repository's `tools/scan_conflicts.py` found 28 duplicate top-level identifiers across the two mods. Most are additive on-actions or wrapper keys, not destructive conflicts. Only the cases below require compatch content.

## Required fixes

### `common/achievement_groups.txt`

This is the only exact file-path overlap. Victoria 3 loads BPM's whole file after Morgenroete's file, so BPM otherwise removes Morgenroete's achievement groups and omits newer vanilla achievements.

The compatch file is rebuilt from Morgenroete's current 1.13 file, which contains the complete current vanilla list and all Morgenroete groups, plus BPM's `bpm_achievements` group.

### `morgenrote_is_active`

- Morgenroete defines `REPLACE_OR_CREATE:morgenrote_is_active = { always = yes }`.
- BPM's compatibility fallback later defines `morgenrote_is_active = { always = no }`.

The compatch restores `always = yes` in a late-loading scripted-trigger file.

### Swedish Bernadotte templates

BPM replaces these five templates after Morgenroete has injected or replaced its flavor fields:

- `swe_karl_johan_bernadotte_template`
- `swe_oscar_bernadotte_template`
- `swe_charles_bernadotte_template`
- `swe_oscar_ii_bernadotte_template`
- `swe_gustaf_v_bernadotte_template`

The compatch keeps BPM's interest-group and ideology choices while restoring Morgenroete's ruler traits, custom DNA, and related flavor fields. The merged templates were rebuilt from the current source definitions rather than copied from the 1.12 patch.

## Conflict removed upstream

### `mass_propaganda`

This no longer needs a compatch override.

- Morgenroete injects `elgar_mass_culture_tech` into `unlocking_technologies`.
- BPM 2.5.32 now only injects `country_institution_culture_max_investment_add = 1` into the technology's modifier.

BPM no longer replaces the whole technology, so Morgenroete's prerequisite survives the configured load order. The old `zzzz_bpm_mr_society_technologies_patch.txt` was removed to avoid injecting the same prerequisite twice.

## Reviewed duplicates that need no patch

### On-actions

The scanner reports 14 shared on-action names, including monthly, yearly, technology-acquired, revolution, secession, and country-release hooks. Victoria 3 combines definitions from separate on-action files; these are expected additive registrations, not overwrites.

### History wrapper keys

`CHARACTERS`, `COUNTRIES`, and `GLOBAL` are file-format wrapper keys repeated across many files. They are scanner false positives.

### Other compatibility fallbacks

`JKFP_is_active_trigger`, `WCR_is_active_trigger`, and `basileia_is_active` are `always = no` fallbacks in both mods. Their duplicate definitions agree and do not require intervention.

## Scope

This patch resolves confirmed file overwrites and late `REPLACE` conflicts. It deliberately does not rebalance laws, parties, political movements, or interest groups.
