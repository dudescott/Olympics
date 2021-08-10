Attribute VB_Name = "Transformer"
Option Explicit

Sub transform_data()
    
    Dim home As Workbook: Set home = ActiveWorkbook
    Dim r As Long, c As Integer
    ' follow instructions by Dan White on Automation Error
    ' https://stackoverflow.com/questions/40625618/automation-error-2146232576-80131700-on-creating-an-array
    Dim lines As Object: Set lines = CreateObject("System.Collections.ArrayList")
    With Application
        .ScreenUpdating = False: .Calculation = xlCalculationManual
    End With
    
    With Sheets("Data")
        Dim code As String, year As Integer, pop As LongLong
        For r = 5 To 270
            code = .Cells(r, 2).Value2
            For c = 5 To 65
                year = .Cells(4, c).Value2
                pop = .Cells(r, c).Value2
                lines.Add Array(code, year, pop)
            Next c
        Next r
    End With
    
    With Sheets.Add
        .name = "Population"
        .[A1:C1].Value2 = Array("Country Code", "Year", "Population")
        Dim line As Variant
        r = 2
        For Each line In lines
            .Range("A" & r & ":C" & r).Value2 = line
            r = r + 1
        Next line
        .Move
        Application.Dialogs(xlDialogSaveAs).Show "population.csv", xlCSV
    End With
    
    With Application
        .ScreenUpdating = True: .Calculation = xlCalculationAutomatic
    End With
    
    MsgBox "The population.csv file has been created.", vbOKOnly, "Success"

End Sub
