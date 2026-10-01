# Compatibility and Source Integration Notes

Version 2.0 targets Remastered and ships precompiled scripts plus compiled Flash assets. A standalone installation does not require Script Merger. Combining it with another inventory mod can still require a compatibility patch.

## Current Package

`PriceWeight.w3edit` sets `useLooseScripts` to `false`. The inspected packed output contains `content/precompiled.rsblob`, with no loose `content/scripts` directory.

| Component | Implementation | Compatibility boundary |
| --- | --- | --- |
| Tooltip data | Edited `W3TooltipComponent` in `scripts/game/gui/_old/components/guiTooltipComponent.ws` | Includes direct changes to vanilla methods; it is not entirely implemented with annotations. |
| Sorting data | `scripts/local/valueWeightSorting.ws` wraps `W3GuiPlayerInventoryComponent.SetInventoryFlashObjectForItem` | Calls `wrappedMethod` and supplies displayed price, weight, and ratio to Flash. Compatible wrappers can compose, but behavior still needs testing together. |
| Tooltip and inventory presentation | `componentslib.redswf` and `panel_inventory.redswf` | Replaces compiled UI resources. WitcherScript annotations do not merge these assets. |

## Flash Asset Conflicts

These resources are replaced by the mod:

```text
gameplay/gui_new/swf/common/componentslib.redswf
gameplay/gui_new/swf/inventory/panel_inventory.redswf
```

If another mod provides the same resource, load order selects a version; it does not combine the UI changes. Losing `componentslib.redswf` can remove or break the ratio icon. Losing `panel_inventory.redswf` can remove the sorting option, sorting logic, or weightless grouping.

A compatibility patch must integrate both mods' relevant Flash/ActionScript changes and rebuild the affected assets. Script Merger cannot automatically do that.

## For Players

1. Install the Remastered version of this mod.
2. Check compatibility before combining it with other inventory or tooltip mods.
3. Use a patch built for the exact mod versions when one is available. Changing load order may select one mod's behavior while losing the other's.
4. Check the tooltip, Price / Weight sorting, and weightless grouping in game.

## For Authors Building a Compatibility Patch

Source files relevant to integration:

```text
scripts/game/gui/_old/components/guiTooltipComponent.ws
scripts/local/valueWeightSorting.ws
gameplay/gui_new/fla/witcher3/menus/common/componentslib.fla
gameplay/gui_new/fla/witcher3/menus/inventory/menuinventory.fla
gameplay/gui_new/actionscript/red/game/witcher3/menus/inventory_menu/MenuInventory.as
gameplay/gui_new/actionscript/red/game/witcher3/slots/SlotsListGrid.as
gameplay/gui_new/actionscript/red/game/witcher3/slots/ItemDataStub.as
```

Preserve `addValueWeightStat` and its calls after the vanilla price stat in inventory and merchant contexts. The helper uses displayed weight, keeps localization key `mod_valueweight_price_weight`, shows `0` for zero-price weighted items, and hides the ratio for weightless items. Keep the sorting wrapper and its Flash data fields as well.

Source-level text merging can help author a combined implementation, but the result must be rebuilt and tested in the intended package. The notes recommend loose scripts on PC for traditional edited vanilla files, and annotations or minimal class extensions for precompiled mods. Switching this project's packaging or refactoring its tooltip requires a separate implementation and validation task; the current build settings have not been changed.

For future compatibility work, investigate moving the tooltip changes into small wrappers or class extensions. That may reduce script conflicts; it will not remove the separate Flash asset conflicts.

Preserve the font setup and run the Ukrainian exporter after the final cook, as described in [DEVELOPMENT.md](DEVELOPMENT.md).
