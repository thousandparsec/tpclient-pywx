
;--------------------------------
;NSIS Script For pywx-client 

  !include "MUI.nsh"

;--------------------------------
;General

  ;Title Of Your Application 
  Name "pywx-client" 
 
  ;Do A CRC Check 
  CRCCheck On 
 
  ;Output File Name 
  OutFile "pywx-client-0.0.6-setup.exe" 
 
  ;The Default Installation Directory 
  InstallDir "$PROGRAMFILES\Thousand Parsec\pywx-client" 

;--------------------------------
;Variables

  Var MUI_TEMP
  Var STARTMENU_FOLDER

;--------------------------------
;Interface Settings

  !define MUI_ABORTWARNING

;  !define MUI_HEADERIMAGE
  
  !define MUI_WELCOMEFINISHPAGE_BITMAP ".\graphics\sidebar.bmp"
  !define MUI_UNWELCOMEFINISHPAGE_BITMAP ".\graphics\sidebar.bmp"

;--------------------------------
;Pages

  !insertmacro MUI_PAGE_WELCOME
  !insertmacro MUI_PAGE_LICENSE ".\COPYING"
  !insertmacro MUI_PAGE_DIRECTORY

  ;Start Menu Folder Page Configuration
  !define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKCU" 
  !define MUI_STARTMENUPAGE_REGISTRY_KEY "Software\Thousand Parsec\pywx-client" 
  !define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"
  !define MUI_STARTMENUPAGE_DEFAULTFOLDER "Thousand Parsec\pywx-client"
  !insertmacro MUI_PAGE_STARTMENU Application $STARTMENU_FOLDER

  !insertmacro MUI_PAGE_INSTFILES

  ;Finish Page Configuration
  !define MUI_FINISHPAGE_RUN "$INSTDIR\main.exe"
  !define MUI_FINISHPAGE_RUN_NOTCHECKED
;  !define MUI_FINISHPAGE_SHOWREADME "$INSTDIR\README"
;  !define MUI_FINISHPAGE_SHOWREADME_NOTCHECKED
  !define MUI_FINISHPAGE_LINK "Thousand Parsec Website"
  !define MUI_FINISHPAGE_LINK_LOCATION "http://www.thousandparsec.net/tp/"
  !insertmacro MUI_PAGE_FINISH
  
  !insertmacro MUI_UNPAGE_WELCOME
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES
  !insertmacro MUI_UNPAGE_FINISH
  
;--------------------------------
;Languages
 
  !insertmacro MUI_LANGUAGE "English"

;--------------------------------
;Installer Sections
 
Section "Files" Files

  SetOutPath "$INSTDIR"
  
  SetCompress Auto 
  SetOverwrite IfNewer 
  File /r "dist\*.*" 
  
  ;Store installation folder
  WriteRegStr HKCU "Software\Thousand Parsec\pywx-client" "" $INSTDIR
  
  ;Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  
  !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
    
    ;Create shortcuts
    CreateDirectory "$SMPROGRAMS\$STARTMENU_FOLDER"
    CreateShortCut "$SMPROGRAMS\$STARTMENU_FOLDER\pywx-client.lnk" "$INSTDIR\main.exe" "" "$INSTDIR\main.exe" 0 
    CreateShortCut "$SMPROGRAMS\$STARTMENU_FOLDER\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
  
  !insertmacro MUI_STARTMENU_WRITE_END

SectionEnd

;--------------------------------
;Descriptions

  ;Language strings
  LangString DESC_Files ${LANG_ENGLISH} "Install pywx-client, a wxWidgets, python based client for Thousand Parsec."

  ;Assign language strings to sections
  !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${Files} $(DESC_Files)
  !insertmacro MUI_FUNCTION_DESCRIPTION_END

;--------------------------------
;Uninstaller Section

Section "Uninstall"
  ;Delete Files 
  RmDir /r "$INSTDIR" 

  !insertmacro MUI_STARTMENU_GETFOLDER Application $MUI_TEMP
    
  Delete "$SMPROGRAMS\$MUI_TEMP\Uninstall.lnk"
  Delete "$SMPROGRAMS\$MUI_TEMP\pywx-client.lnk"
  
  ;Delete empty start menu parent diretories
  StrCpy $MUI_TEMP "$SMPROGRAMS\$MUI_TEMP"
 
  startMenuDeleteLoop:
    RMDir $MUI_TEMP
    GetFullPathName $MUI_TEMP "$MUI_TEMP\.."
    
    IfErrors startMenuDeleteLoopDone
  
    StrCmp $MUI_TEMP $SMPROGRAMS startMenuDeleteLoopDone startMenuDeleteLoop
  startMenuDeleteLoopDone:

  DeleteRegKey /ifempty HKCU "Software\Thousand Parsec\pywx-client"
  DeleteRegKey /ifempty HKCU "Software\Thousand Parsec"
SectionEnd

