# Price / Weight - Inventory Tooltip and Sorting

![Price / Weight](media/price-value.png)

Adds a `Price / Weight` value to item tooltips and a matching inventory sort option for **The Witcher 3: Wild Hunt**.

Version 2.0 targets **Remastered**. The previous Next-Gen implementation is preserved on the `next-gen` branch.

The higher the number, the more crowns the item is worth per unit of carry weight. This makes it easier to decide what to keep, sell, or drop without doing the math yourself.

## Links

- [Nexus Mods](https://www.nexusmods.com/witcher3/mods/12874)
- [Steam Workshop](https://steamcommunity.com/sharedfiles/filedetails/?id=3811021371)
- [mod.io](https://mod.io/g/the-witcher-3/m/price-weight)
- [YouTube demo](https://youtu.be/pxSG0zXrIO8)

## Features

- Displays `Price / Weight` in item tooltips.
- Adds `Price / Weight` to the inventory sorting menu.
- Sorts items with the highest value-to-weight ratio first.
- Separates weightless items into a group below weighted items.
- Localized for every language currently supported by The Witcher 3.

## Calculation

```text
Price / Weight = displayed price / displayed weight
```

Example:

```text
1772 / 2.04 = 868.63
```

The calculation uses the price and rounded weight shown in the tooltip. Items with weight but zero price show `0`. Weightless items show no ratio or ratio icon.

![Tooltip calculation example](media/example-1.jpg)

## Sorting

Select `Price / Weight` in the inventory sort dialog. Within each inventory section, weighted items appear first, from highest to lowest ratio, including items with a ratio of `0`.

Weightless items follow in descending price order, starting on a fresh row below the weighted group. Any unused cells at the end of that group stay empty, including when it contains items that occupy two cells vertically.

![Sorting example](media/example-2.jpg)

## Compatibility

This release uses precompiled scripts and replaces inventory tooltip and sorting Flash assets. Script Merger is not required for a standalone installation and cannot combine these compiled files.

Mods that change the same tooltip script functions or inventory Flash assets may require a compatibility patch. Script annotations help compatible script changes work together, but they do not merge Flash assets or make every script replacement compatible.

See [MERGING.md](MERGING.md) for more detailed compatibility notes.

## Installation

1. For **Remastered**, get version 2.0 from [Nexus Mods](https://www.nexusmods.com/witcher3/mods/12874), [Steam Workshop](https://steamcommunity.com/sharedfiles/filedetails/?id=3811021371), or [mod.io](https://mod.io/g/the-witcher-3/m/price-weight). For **Next-Gen**, download the previous-version archive available on the same [Nexus Mods page](https://www.nexusmods.com/witcher3/mods/12874).
2. For a manual install, extract the archive and copy `modPriceWeight` into your `The Witcher 3\Mods` directory. For a subscription install, let the game or platform install it.
3. If you use other inventory UI mods, check their compatibility with this mod and install a matching compatibility patch if available.
4. Launch the game and check an inventory tooltip and the inventory sort dialog.

## Uninstallation

For a manual install, remove `modPriceWeight` from your `Mods` directory. For a subscription install, unsubscribe from the mod.

If you created merged scripts containing files from this mod, remove or regenerate the merge after uninstalling.

## Project Notes

This repository contains edited REDkit source and generated UI assets for the mod. The game uses the cooked and compiled assets, not the raw `.fla` or `.as` files directly.

See [DEVELOPMENT.md](DEVELOPMENT.md) for maintenance notes, Flash font precautions, and the release checklist.
