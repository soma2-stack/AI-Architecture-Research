$ErrorActionPreference = 'Stop'
$dir = Split-Path -Parent $MyInvocation.MyCommand.Path
$csv = Join-Path $dir 'gpu_telemetry.csv'
$stdout = Join-Path $dir 'run.log'
$stderr = Join-Path $dir 'run_stderr.log'
$exitJson = Join-Path $dir 'run_exit.json'
$env:OMP_NUM_THREADS = '1'
$env:MKL_NUM_THREADS = '1'
$env:OPENBLAS_NUM_THREADS = '1'
$env:NUMEXPR_NUM_THREADS = '1'
$header = 'timestamp_local,temperature_c,memory_used_mib,memory_total_mib,gpu_utilization_pct'
Set-Content -LiteralPath $csv -Value $header -Encoding ascii
function Add-Sample {
    $line = & nvidia-smi --query-gpu=temperature.gpu,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits 2>&1
    if ($LASTEXITCODE -ne 0) { throw "nvidia-smi telemetry failure: $line" }
    $parts = ([string]$line).Trim() -split '\s*,\s*'
    if ($parts.Count -lt 4) { throw "Malformed nvidia-smi sample: $line" }
    $stamp = (Get-Date).ToString('o')
    Add-Content -LiteralPath $csv -Value "$stamp,$($parts[0]),$($parts[1]),$($parts[2]),$($parts[3])" -Encoding ascii
    return [pscustomobject]@{Temperature=[double]$parts[0]; UsedMiB=[double]$parts[1]; TotalMiB=[double]$parts[2]; Utilization=[double]$parts[3]}
}
$stopReason = $null
$exitCode = $null
$proc = $null
try {
    $initial = Add-Sample
    if ($initial.Temperature -gt 81) { throw "Preflight temperature $($initial.Temperature)C exceeds the 81C target; run not started." }
    if ($initial.UsedMiB -gt 10240) { throw "Preflight VRAM $($initial.UsedMiB) MiB exceeds 10 GiB; run not started." }
    $python = (Get-Command python).Source
    $proc = Start-Process -FilePath $python -ArgumentList @('-u','run_test3.py') -WorkingDirectory $dir -PassThru -WindowStyle Hidden -RedirectStandardOutput $stdout -RedirectStandardError $stderr
    while ($true) {
        Start-Sleep -Seconds 10
        $proc.Refresh()
        if ($proc.HasExited) { $exitCode = $proc.ExitCode; break }
        $sample = Add-Sample
        if ($sample.Temperature -gt 81) { $stopReason = "Temperature exceeded 81C target ($($sample.Temperature)C); stopped this run before 86C hard limit."; Stop-Process -Id $proc.Id -Force; break }
        if ($sample.UsedMiB -gt 10240) { $stopReason = "GPU memory exceeded 10 GiB ($($sample.UsedMiB) MiB); stopped this run."; Stop-Process -Id $proc.Id -Force; break }
    }
    if ($proc -and !$proc.HasExited) { $proc.Refresh() }
} catch {
    $stopReason = $_.Exception.Message
    if ($proc -and !$proc.HasExited) { Stop-Process -Id $proc.Id -Force }
}
$final = $null
try { $final = Add-Sample } catch { if (!$stopReason) { $stopReason = $_.Exception.Message } }
if ($null -eq $exitCode -and $proc) { $proc.Refresh(); if ($proc.HasExited) { $exitCode = $proc.ExitCode } }
[pscustomobject]@{started=$null -ne $proc; process_id=if($proc){$proc.Id}else{$null}; exit_code=$exitCode; stop_reason=$stopReason; final_temperature_c=if($final){$final.Temperature}else{$null}; final_memory_used_mib=if($final){$final.UsedMiB}else{$null}; telemetry_file='gpu_telemetry.csv'; stdout_file='run.log'; stderr_file='run_stderr.log'} | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $exitJson -Encoding utf8
if ($stopReason) { Write-Error $stopReason; exit 2 }
if ($null -eq $exitCode) { Write-Error 'Experiment did not report an exit code.'; exit 3 }
exit $exitCode
