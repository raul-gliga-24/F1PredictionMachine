param(
    [Parameter(Mandatory = $true)]
    [int]$Season,
    
    [Parameter(Mandatory = $true)]
    [int]$Round,
    
    [switch]$Save
)

$url = "http://localhost:8000/api/predictions/pre-race/$Season/$Round"

Write-Host "Fetching F1 Prediction for Season $Season, Round $Round..." -ForegroundColor Cyan

try {
   
    $response = Invoke-RestMethod -Uri $url -Method Post -ErrorAction Stop
    $json = $response | ConvertTo-Json -Depth 10
    
    Write-Host "`nPrediction Result:" -ForegroundColor Green
    Write-Host $json
    
    if ($Save) {
        $dir = "predictions"
        if (-not (Test-Path -Path $dir)) {
            New-Item -ItemType Directory -Path $dir | Out-Null
        }
        $outFile = "$dir/round_${Round}_${Season}.json"
        
        $json | Out-File -FilePath $outFile -Encoding utf8
        Write-Host "`n[SUCCESS] Prediction saved to $outFile" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "Error calling API: $($_.Exception.Message)" -ForegroundColor Red
}
