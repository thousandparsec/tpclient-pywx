
;--------------------------------
;NSIS Script For pywx-client 

  !include "MUI.nsh"

!macro CreateInternetShortcut FILENAME URL ICONFILE ICONINDEX
WriteINIStr "${FILENAME}.url" "InternetShortcut" "URL" "${URL}"
WriteINIStr "${FILENAME}.url" "InternetShortcut" "IconFile" "${ICONFILE}"
WriteINIStr "${FILENAME}.url" "InternetShortcut" "IconIndex" "${ICONINDEX}"
!macroend

;--------------------------------
;General

  ;Title Of Your Application 
  Name "tpclient-pywx" 
 
  ;Do A CRC Check 
  CRCCheck On 
 
  ;Output File Name 
  OutFile "tpclient-pywx-0.2.0rc2-setup.exe" 
 
  ;The Default Installation Directory 
  InstallDir "$PROGRAMFILES\Thousand Parsec\tpclient-pywx" 

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
  !define MUI_STARTMENUPAGE_REGISTRY_KEY "Software\Thousand Parsec\Client pywx" 
  !define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"
  !define MUI_STARTMENUPAGE_DEFAULTFOLDER "Thousand Parsec\Client pywx"
  !insertmacro MUI_PAGE_STARTMENU Application $STARTMENU_FOLDER

  !insertmacro MUI_PAGE_INSTFILES

  ;Finish Page Configuration
  !define MUI_FINISHPAGE_RUN "$INSTDIR\tpclient-pywx.exe"
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
  WriteRegStr HKCU "Software\Thousand Parsec\tpclient-pywx" "" $INSTDIR

  ;Create the URL handlers
  WriteRegStr HKCR "tp" "" "Thousand Parsec Server"
  WriteRegStr HKCR "tp" "URL Protocol" ""
  WriteRegStr HKCR "tp\shell" "" ""
  WriteRegStr HKCR "tp\shell\open" "" ""
  WriteRegStr HKCR "tp\shell\open\command" "" '"$INSTDIR\tpclient-pywx.exe" "%1"'
  WriteRegStr HKCR "tps" "" "Thousand Parsec Secure Server"
  WriteRegStr HKCR "tps" "URL Protocol" ""
  WriteRegStr HKCR "tps\shell" "" ""
  WriteRegStr HKCR "tps\shell\open" "" ""
  WriteRegStr HKCR "tps\shell\open\command" "" '"$INSTDIR\tpclient-pywx.exe" "%1"'
  WriteRegStr HKCR "tphttp" "" "Thousand Parsec HTTP Tunnel Server"
  WriteRegStr HKCR "tphttp" "URL Protocol" ""
  WriteRegStr HKCR "tphttp\shell" "" ""
  WriteRegStr HKCR "tphttp\shell\open" "" ""
  WriteRegStr HKCR "tphttp\shell\open\command" "" '"$INSTDIR\tpclient-pywx.exe" "%1"'
  WriteRegStr HKCR "tphttps" "" "Thousand Parsec HTTP Tunnel Server"
  WriteRegStr HKCR "tphttps" "URL Protocol" ""
  WriteRegStr HKCR "tphttps\shell" "" ""
  WriteRegStr HKCR "tphttps\shell\open" "" ""
  WriteRegStr HKCR "tphttps\shell\open\command" "" '"$INSTDIR\tpclient-pywx.exe" "%1"'

  ;Store uninstall information
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\tpclient-pywx" \
                 "UninstallString" "$INSTDIR\uninstall.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\tpclient-pywx" \
                 "DisplayName" "Thousand Parsec Client pywx"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\tpclient-pywx" \
                 "DisplayIcon" "$INSTDIR\tpclient-pywx.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\tpclient-pywx" \
                 "DisplayVersion" "0.2.0"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\tpclient-pywx" \
                 "URLInfoAbout" "http://www.thousandparsec.net/tp/"
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\tpclient-pywx" \
                 "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\tpclient-pywx" \
                 "NoRepair" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\tpclient-pywx" \
                 "VersionMajor" 2
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\tpclient-pywx" \
                 "VersionMinor" 0

  ;Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  
  !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
    
    ;Create shortcuts
    CreateDirectory "$SMPROGRAMS\$STARTMENU_FOLDER"
    CreateShortCut "$SMPROGRAMS\$STARTMENU_FOLDER\tpclient-pywx.lnk" "$INSTDIR\tpclient-pywx.exe" "" "$INSTDIR\tpclient-pywx.exe" 0 
    CreateShortCut "$SMPROGRAMS\$STARTMENU_FOLDER\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
	!insertmacro CreateInternetShortcut "$SMPROGRAMS\$STARTMENU_FOLDER\Thousand Parsec Homepage" "http://www.thousandparsec.net/tp/" "$INSTDIR\tpclient-pywx.exe" "0" 
 
  !insertmacro MUI_STARTMENU_WRITE_END

SectionEnd

;--------------------------------
;Descriptions

  ;Language strings
  LangString DESC_Files ${LANG_ENGLISH} "Install tpclient-pywx, a wxWidgets, python based client for Thousand Parsec."

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
  Delete "$SMPROGRAMS\$MUI_TEMP\tpclient-pywx.lnk"
  
  ;Delete empty start menu parent diretories
  StrCpy $MUI_TEMP "$SMPROGRAMS\$MUI_TEMP"
 
  startMenuDeleteLoop:
    RMDir $MUI_TEMP
    GetFullPathName $MUI_TEMP "$MUI_TEMP\.."
    
    IfErrors startMenuDeleteLoopDone
  
    StrCmp $MUI_TEMP $SMPROGRAMS startMenuDeleteLoopDone startMenuDeleteLoop
  startMenuDeleteLoopDone:

  DeleteRegKey HKCR "tp" 
  DeleteRegKey HKCR "tps" 
  DeleteRegKey HKCR "tphttp" 
  DeleteRegKey HKCR "tphttps" 
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\tpclient-pywx"
  DeleteRegKey /ifempty HKCU "Software\Thousand Parsec\Client pywx"
  DeleteRegKey /ifempty HKCU "Software\Thousand Parsec"
SectionEnd

