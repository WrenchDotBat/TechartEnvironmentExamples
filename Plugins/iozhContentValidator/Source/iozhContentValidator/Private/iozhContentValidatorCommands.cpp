// Copyright Epic Games, Inc. All Rights Reserved.

#include "iozhContentValidatorCommands.h"

#define LOCTEXT_NAMESPACE "FiozhContentValidatorModule"

void FiozhContentValidatorCommands::RegisterCommands()
{
	UI_COMMAND(PluginAction, "iozhContentValidator", "Execute iozhContentValidator action", EUserInterfaceActionType::Button, FInputChord());
}

#undef LOCTEXT_NAMESPACE
