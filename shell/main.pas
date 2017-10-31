unit main;

{$mode objfpc}{$H+}

interface

uses
  Classes,
  SysUtils,
  FileUtil,
  Forms,
  Controls,
  Graphics,
  Dialogs,
  EditBtn,
  StdCtrls,
  Process,
  IniFiles;

type

  { TForm1 }

  TForm1 = class(TForm)
    btnConvertTAGstoCSV: TButton;
    btnConvertWAVtoTAGs: TButton;
    ebFXsFileName: TFileNameEdit;
    ebTAGsFileName: TFileNameEdit;
    Label1: TLabel;
    Label2: TLabel;
    Label3: TLabel;
    meConversionLog: TMemo;
    procedure btnConvertTAGstoCSVClick(Sender: TObject);
    procedure btnConvertWAVtoTAGsClick(Sender: TObject);
    procedure ebFXsFileNameAcceptFileName(Sender: TObject; var Value: String);
    procedure ebTAGsFileNameAcceptFileName(Sender: TObject; var Value: String);
    procedure FormClose(Sender: TObject; var CloseAction: TCloseAction);
    procedure FormCreate(Sender: TObject);
  private
    { private declarations }
    settings: TINIFile;
  public
    { public declarations }
  end;

var
  Form1: TForm1;

implementation

{$R *.lfm}

{ TForm1 }

procedure TForm1.FormCreate(Sender: TObject);
begin
  settings := TINIFile.Create('w2tshell.ini');

  ebFXsFileName.InitialDir := settings.ReadString('wav2time', 'FXsInitialDir', '');
  ebTAGsFileName.InitialDir := settings.ReadString('wav2time', 'TAGsInitialDir', '');
end;

procedure TForm1.FormClose(Sender: TObject; var CloseAction: TCloseAction);
begin
  settings.WriteString('wav2time', 'FXsInitialDir', ExtractFilePath(ebFXsFileName.InitialDir));
  settings.WriteString('wav2time', 'TAGsInitialDir', ExtractFilePath(ebTAGsFileName.InitialDir));

  CloseAction := caFree;
end;

procedure TForm1.ebFXsFileNameAcceptFileName(Sender: TObject; var Value: String);
begin
  ebFXsFileName.InitialDir := ExtractFilePath(Value);
end;

procedure TForm1.ebTAGsFileNameAcceptFileName(Sender: TObject; var Value: String);
begin
  ebTAGsFileName.InitialDir := ExtractFilePath(Value);
end;

procedure TForm1.btnConvertWAVtoTAGsClick(Sender: TObject);
var
  o: string;
begin
  if RunCommand('python.exe', ['wav2time.py ', ebFXsFileName.FileName], o) then
    meConversionLog.Lines.Text := o
  else
    meConversionLog.Lines.Text := 'ERROR';
end;

procedure TForm1.btnConvertTAGstoCSVClick(Sender: TObject);
var
  o: string;
begin
  if RunCommand('python.exe', ['time2csv.py ', ebTAGsFileName.FileName], o) then
    meConversionLog.Lines.Text := o
  else
    meConversionLog.Lines.Text := 'ERROR';
end;

end.

