# Merge and Compatibility Notes

This mod changes the inventory tooltip and inventory sorting UI. If you use other inventory UI mods, run Script Merger after installing or updating mods.

## Files Changed By This Mod

Script conflict:

```text
scripts\game\gui\_old\components\guiTooltipComponent.ws
```

Compiled Flash UI conflicts:

```text
gameplay\gui_new\swf\common\componentslib.redswf
gameplay\gui_new\swf\inventory\panel_inventory.redswf
```

Source files used to build the Flash UI, included only for reference in the project source:

```text
gameplay\gui_new\fla\witcher3\menus\common\componentslib.fla
gameplay\gui_new\fla\witcher3\menus\inventory\menuinventory.fla
gameplay\gui_new\actionscript\red\game\witcher3\menus\inventory_menu\MenuInventory.as
gameplay\gui_new\actionscript\red\game\witcher3\slots\SlotsListGrid.as
```

## Script Merger

Script Merger can detect conflicts and create merged files for text/script conflicts. For this mod, the useful merge target is:

```text
scripts\game\gui\_old\components\guiTooltipComponent.ws
```

When merging this file, keep this mod's added `valueweight` tooltip stat near the vanilla price tooltip stat. The important additions are:

```text
addGFxItemStat( propsList, "valueweight", ..., "mod_valueweight_price_weight" );
```

and, for zero-weight items with a positive price:

```text
GetLocStringByKeyExt( "mod_valueweight_not_applicable" )
```

If the merge keeps the script code but the icon is missing, the Flash UI conflict was not resolved in favor of this mod.

## Non-Text UI Conflicts

Script Merger cannot automatically merge compiled Flash UI assets such as `.redswf`. If another mod also changes either of these files, one mod's file will win by load order:

```text
gameplay\gui_new\swf\common\componentslib.redswf
gameplay\gui_new\swf\inventory\panel_inventory.redswf
```

Effects of losing those files:

- If `componentslib.redswf` is overridden by another mod, the tooltip value/weight row may show a missing/incorrect icon.
- If `panel_inventory.redswf` is overridden by another mod, the `Price / Weight` sort option may be missing or the sort dialog may behave incorrectly.

If another mod edits the same inventory Flash files, a real compatibility patch must be built from both mods' Flash/ActionScript changes. Load order alone can only choose which mod's UI file wins.

## Recommended User Steps

1. Install this mod.
2. Install any other mods.
3. Run Script Merger.
4. Merge `guiTooltipComponent.ws` if Script Merger reports a conflict.
5. For `.redswf` conflicts, choose the UI mod whose inventory screen you want to win, or use a compatibility patch made for the exact pair of mods.
6. Launch the game and check an inventory tooltip and the inventory sort dialog.

