// Copyright Epic Games, Inc. All Rights Reserved.

#include "iozhContentValidatorStyle.h"
#include "iozhContentValidator.h"
#include "Framework/Application/SlateApplication.h"
#include "Styling/SlateStyleRegistry.h"
#include "Slate/SlateGameResources.h"
#include "Interfaces/IPluginManager.h"
#include "Styling/SlateStyleMacros.h"

#define RootToContentDir Style->RootToContentDir

TSharedPtr<FSlateStyleSet> FiozhContentValidatorStyle::StyleInstance = nullptr;

void FiozhContentValidatorStyle::Initialize()
{
	if (!StyleInstance.IsValid())
	{
		StyleInstance = Create();
		FSlateStyleRegistry::RegisterSlateStyle(*StyleInstance);
	}
}

void FiozhContentValidatorStyle::Shutdown()
{
	FSlateStyleRegistry::UnRegisterSlateStyle(*StyleInstance);
	ensure(StyleInstance.IsUnique());
	StyleInstance.Reset();
}

FName FiozhContentValidatorStyle::GetStyleSetName()
{
	static FName StyleSetName(TEXT("iozhContentValidatorStyle"));
	return StyleSetName;
}


const FVector2D Icon16x16(16.0f, 16.0f);
const FVector2D Icon20x20(20.0f, 20.0f);

TSharedRef< FSlateStyleSet > FiozhContentValidatorStyle::Create()
{
	TSharedRef< FSlateStyleSet > Style = MakeShareable(new FSlateStyleSet("iozhContentValidatorStyle"));
	Style->SetContentRoot(IPluginManager::Get().FindPlugin("iozhContentValidator")->GetBaseDir() / TEXT("Resources"));

	Style->Set("iozhContentValidator.PluginAction", new IMAGE_BRUSH_SVG(TEXT("PlaceholderButtonIcon"), Icon20x20));
	return Style;
}

void FiozhContentValidatorStyle::ReloadTextures()
{
	if (FSlateApplication::IsInitialized())
	{
		FSlateApplication::Get().GetRenderer()->ReloadTextureResources();
	}
}

const ISlateStyle& FiozhContentValidatorStyle::Get()
{
	return *StyleInstance;
}
