# Development Notes

Notes for maintaining and releasing this mod.

## Flash Font Trap

The inventory tooltip icon lives in `componentslib.fla`, but republishing that file can easily break tooltip fonts.

Keep these font symbols using the stock runtime-shared setup from `gfxfontlib.swf`:

```text
$BoldFont
$NormalFont
$ItalicFont
```

Do not embed PF Din directly into `componentslib` for release. Adobe Animate's `All` character range only embeds glyphs available in PF Din. That may work for Latin text, but it breaks or partially breaks localized tooltip text for Chinese, Japanese, Korean, Arabic, and Turkish.

Known-good release rule:

```text
Import for runtime sharing: on
Export for runtime sharing: off
Export for ActionScript: off
Export in frame 1: off
URL: gfxfontlib.swf
```

Also make sure no text fields were silently changed to `TimesNewRomanPSMT`. The generated `componentslib.redswf` should not contain `Times New Roman`.

After editing `componentslib.fla`:

1. Publish `componentslib.swf` from Adobe Animate.
2. Import the SWF in REDkit as Flash SWF to recreate `componentslib.redswf`.
3. Cook/package.
4. Test at least English, Polish, Turkish, Arabic, Japanese, Korean, Simplified Chinese, and Traditional Chinese.

## Release Checklist

### Ukrainian Strings on the Current REDkit Build

The REDkit executable inspected on 2026-09-30 exports a fixed 17-language list
that omits UA. Adding UA to the database registry does not extend that list.
The project's Ukrainian translation is already stored under
`mod_valueweight_price_weight`; keep this as the source of truth.

Use this order for every build: **cook in REDkit → export Ukrainian → install or archive the packed mod**.

After the final cook, run from the project directory:

```powershell
py -3 tools/export_ukrainian_strings.py --write
```

This adds only `packed/mods/modpriceweight/content/ua.w3strings`. It does not
cook the project, install the mod, or launch the game. Without `--write`, the
helper validates the database and native Arabic output without writing a file.
It targets Remastered v164 UTF-8 strings and preserves the native key hash and
the project's string ID. It exports only the Price / Weight label.

Do not cook again between running the helper and installing or archiving.
Re-cooking removes the supplemental file, so run the helper again after each cook.
Dmitriy confirmed on 2026-10-01 that exporting and then installing directly from
`packed` displays the Ukrainian label correctly in game.

Automated Workshop/mod.io upload can involve another cook; preservation of this supplemental file during those
upload flows has not been verified.

### General Release Checks

- Bump version in `PriceWeight.w3edit`.
- Update `CHANGELOG.md`.
- Cook/package the mod.
- Run the Ukrainian export helper after the final cook and include `ua.w3strings` in the package.
- Test a manual install from the packaged archive.
- Test Steam Workshop upload/subscription if publishing there.
- Check overlapping tooltip functions and inventory Flash assets; test any compatibility patch with the actual precompiled package. Script Merger is not a repair path for this release's compiled files.
- Verify tooltip and sorting in English.
- Smoke-test Polish plus one CJK/Arabic/Korean language for font safety.
- Check that `componentslib.redswf` does not contain `Times New Roman`.
- Update screenshots/video if UI changed.
- Update Nexus/Steam descriptions if behavior, installation notes, or known issues changed.
