// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "Framework/Commands/Commands.h"
#include "iozhContentValidatorStyle.h"

class FiozhContentValidatorCommands : public TCommands<FiozhContentValidatorCommands>
{
public:

	FiozhContentValidatorCommands()
		: TCommands<FiozhContentValidatorCommands>(TEXT("iozhContentValidator"), NSLOCTEXT("Contexts", "iozhContentValidator", "iozhContentValidator Plugin"), NAME_None, FiozhContentValidatorStyle::GetStyleSetName())
	{
	}

	// TCommands<> interface
	virtual void RegisterCommands() override;

public:
	TSharedPtr< FUICommandInfo > PluginAction;
};
