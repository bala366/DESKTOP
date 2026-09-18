[Setup]
AppId={{9D7A7391-62D1-4C67-A861-62E0E9CF21B8}
AppName=Carteira de Clientes - Casarão do Campo
AppVersion=1.0
DefaultDirName={autopf}\CasaraoDoCampo\CarteiraClientes
DefaultGroupName=Casarão do Campo
OutputDir=installer
OutputBaseFilename=INSTALADOR_CARTEIRA_CASARAO_DESKTOP
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=lowest
UninstallDisplayName=Carteira de Clientes - Casarão do Campo
[Files]
Source: "dist\CarteiraCasarao.exe"; DestDir: "{app}"; Flags: ignoreversion
[Icons]
Name: "{autodesktop}\Carteira de Clientes - Casarão do Campo"; Filename: "{app}\CarteiraCasarao.exe"
Name: "{group}\Carteira de Clientes - Casarão do Campo"; Filename: "{app}\CarteiraCasarao.exe"
Name: "{group}\Desinstalar Carteira de Clientes"; Filename: "{uninstallexe}"
[Run]
Filename: "{app}\CarteiraCasarao.exe"; Description: "Abrir Carteira de Clientes"; Flags: nowait postinstall skipifsilent
