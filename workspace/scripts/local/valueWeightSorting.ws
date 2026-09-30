@wrapMethod(W3GuiPlayerInventoryComponent)
function SetInventoryFlashObjectForItem(itemId : SItemUniqueId, out flashObject : CScriptedFlashObject) : void
{
	var itemPrice : int;
	var displayedWeight : float;
	var valueWeight : float;

	wrappedMethod(itemId, flashObject);

	// Merchant prices use a different inventory component; leave that context unchanged.
	if (_shopInvCmp)
	{
		return;
	}

	itemPrice = _inv.GetItemPriceModified(itemId, true);
	// Match guiTooltipComponent.addValueWeightStat, including its displayed-weight rounding.
	displayedWeight = StringToFloat(StrReplace(FloatToStringPrec(_inv.GetItemEncumbrance(itemId), 2), ",", "."), 0.0f);
	valueWeight = 0.0f;
	if (itemPrice >= 0 && displayedWeight > 0.0f)
	{
		valueWeight = (float)itemPrice / displayedWeight;
		valueWeight = (float)RoundMath(valueWeight * 100.0f) / 100.0f;
	}

	// The vanilla "price" field is an unmodified stack total, not the tooltip's unit price.
	flashObject.SetMemberFlashInt("valueWeightPrice", itemPrice);
	flashObject.SetMemberFlashNumber("valueWeightWeight", displayedWeight);
	flashObject.SetMemberFlashNumber("valueWeightRatio", valueWeight);
}
