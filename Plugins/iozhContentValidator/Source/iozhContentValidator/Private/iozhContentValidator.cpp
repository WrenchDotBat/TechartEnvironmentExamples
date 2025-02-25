// Copyright Epic Games, Inc. All Rights Reserved.

#include "iozhContentValidator.h"
#include "iozhContentValidatorStyle.h"
#include "iozhContentValidatorCommands.h"
#include "Misc/MessageDialog.h"
#include "ToolMenus.h"
#include "UObject/SavePackage.h"
#include "Editor/EditorEngine.h"

static const FName iozhContentValidatorTabName("iozhContentValidator");

#define LOCTEXT_NAMESPACE "FiozhContentValidatorModule"

void FiozhContentValidatorModule::StartupModule()
{
	// This code will execute after your module is loaded into memory; the exact timing is specified in the .uplugin file per-module
	
	FiozhContentValidatorStyle::Initialize();
	FiozhContentValidatorStyle::ReloadTextures();

	FiozhContentValidatorCommands::Register();
	
	PluginCommands = MakeShareable(new FUICommandList);

	PluginCommands->MapAction(
		FiozhContentValidatorCommands::Get().PluginAction,
		FExecuteAction::CreateRaw(this, &FiozhContentValidatorModule::PluginButtonClicked),
		FCanExecuteAction());

	UToolMenus::RegisterStartupCallback(FSimpleMulticastDelegate::FDelegate::CreateRaw(this, &FiozhContentValidatorModule::RegisterMenus));

	FCoreUObjectDelegates::OnObjectPreSave.AddUObject(this, &FiozhContentValidatorModule::OnPreSave);

}

/*void FiozhContentValidatorModule::OnPreSave(UObject* InObject, FObjectPreSaveContext InObjectPreSaveContext)
{
}
*/

void FiozhContentValidatorModule::ShutdownModule()
{
	// This function may be called during shutdown to clean up your module.  For modules that support dynamic reloading,
	// we call this function before unloading the module.

	UToolMenus::UnRegisterStartupCallback(this);

	UToolMenus::UnregisterOwner(this);

	FiozhContentValidatorStyle::Shutdown();

	FiozhContentValidatorCommands::Unregister();
}

void FiozhContentValidatorModule::PluginButtonClicked()
{
	// Put your "OnButtonClicked" stuff here
	FText DialogText = FText::Format(
							LOCTEXT("PluginButtonDialogText", "Add code to {0} in {1} to override this button's actions"),
							FText::FromString(TEXT("FiozhContentValidatorModule::PluginButtonClicked()")),
							FText::FromString(TEXT("iozhContentValidator.cpp"))
					   );
	FMessageDialog::Open(EAppMsgType::Ok, DialogText);
}

void FiozhContentValidatorModule::RegisterMenus()
{
	// Owner will be used for cleanup in call to UToolMenus::UnregisterOwner
	FToolMenuOwnerScoped OwnerScoped(this);

	{
		UToolMenu* Menu = UToolMenus::Get()->ExtendMenu("LevelEditor.MainMenu.Window");
		{
			FToolMenuSection& Section = Menu->FindOrAddSection("WindowLayout");
			Section.AddMenuEntryWithCommandList(FiozhContentValidatorCommands::Get().PluginAction, PluginCommands);
		}
	}

	{
		UToolMenu* ToolbarMenu = UToolMenus::Get()->ExtendMenu("LevelEditor.LevelEditorToolBar.PlayToolBar");
		{
			FToolMenuSection& Section = ToolbarMenu->FindOrAddSection("PluginTools");
			{
				FToolMenuEntry& Entry = Section.AddEntry(FToolMenuEntry::InitToolBarButton(FiozhContentValidatorCommands::Get().PluginAction));
				Entry.SetCommandList(PluginCommands);
			}
		}
	}
}

#undef LOCTEXT_NAMESPACE
	
IMPLEMENT_MODULE(FiozhContentValidatorModule, iozhContentValidator)