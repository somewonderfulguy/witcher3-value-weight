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

- Bump version in `PriceWeight.w3edit`.
- Update `CHANGELOG.md`.
- Cook/package the mod.
- Test a manual install from the packaged archive.
- Test Steam Workshop upload/subscription if publishing there.
- Run Script Merger or confirm expected conflicts.
- Verify tooltip and sorting in English.
- Smoke-test Polish plus one CJK/Arabic/Korean language for font safety.
- Check that `componentslib.redswf` does not contain `Times New Roman`.
- Update screenshots/video if UI changed.
- Update Nexus/Steam descriptions if behavior, installation notes, or known issues changed.

