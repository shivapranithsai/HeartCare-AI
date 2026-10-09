$ErrorActionPreference = "Stop"
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $docPath = "C:\Users\shiva\Downloads\heart-failure-prediction\Testing_Report_HeartCare_AI.docx"
    $pdfPath = "C:\Users\shiva\Downloads\heart-failure-prediction\Testing_Report_HeartCare_AI.pdf"
    
    Write-Host "Opening document: $docPath"
    $doc = $word.Documents.Open($docPath)
    
    Write-Host "Exporting to PDF: $pdfPath"
    # 17 = wdExportFormatPDF
    $doc.ExportAsFixedFormat($pdfPath, 17)
    
    $doc.Close([ref]0)
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
    Write-Host "SUCCESS: PDF created at $pdfPath"
} catch {
    Write-Host "ERROR: $($_.Exception.Message)"
    exit 1
}
