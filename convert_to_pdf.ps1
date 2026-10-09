$ErrorActionPreference = "Stop"
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $docPath = "C:\Users\shiva\Downloads\heart-failure-prediction\HeartCare_AI_Final_Year_Project_Report.docx"
    $pdfPath = "C:\Users\shiva\Downloads\heart-failure-prediction\HeartCare_AI_Final_Year_Project_Report.pdf"
    $doc = $word.Documents.Open($docPath)
    # 17 represents wdExportFormatPDF / SaveAs format
    $doc.ExportAsFixedFormat($pdfPath, 17)
    $doc.Close([ref]0)
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
    Write-Host "SUCCESS: PDF created at $pdfPath"
} catch {
    Write-Host "NOTICE: $($_.Exception.Message)"
}
