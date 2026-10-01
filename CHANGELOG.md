# Changelog

All notable user-facing changes to this mod are documented here.

## [Unreleased]

### Version 2.0 — Remastered

- Restored tooltip and inventory sorting support for Remastered.
- Fixed Price / Weight ordering and ordinary Price sorting to use the displayed item price.
- Separated weightless items onto a fresh row below weighted items when sorting by Price / Weight, including grids with mixed item sizes.
- Show `0` for zero-price weighted items and hide the ratio for weightless items.
- Restored localization for all 18 supported languages, including Ukrainian.

## [1.0.0] - 2026-09-13

Initial public release.

### Added

- Added `Price / Weight` to item tooltips.
- Added a new `Price / Weight` option to the inventory sorting menu.
- Added sorting by highest value-to-weight ratio first.
- Added a custom tooltip icon for the new value.
- Added localization for every language currently supported by The Witcher 3.
- Added `N/A` display for positive-price items with zero weight.
- Added merge and compatibility notes for Script Merger users.

### Fixed

- Made the displayed ratio use the same rounded weight shown in the tooltip, so visible calculations stay consistent.
- Restored runtime-shared Flash font handling so Chinese, Japanese, Korean, Arabic, Turkish, Polish, and other localized tooltip text render correctly.

### Known Limitations

- Weapon sorting may not always look perfectly left-to-right because the vanilla inventory grid packs mixed item sizes after sorting. The displayed `Price / Weight` values remain correct.

