param(
    [ValidateRange(1, 65535)]
    [int]$Port = 8000
)

$projectRoot = [IO.Path]::GetFullPath($PSScriptRoot)
$templatesRoot = Join-Path $projectRoot "templates"
$contentTypes = @{
    ".css"  = "text/css; charset=utf-8"
    ".html" = "text/html; charset=utf-8"
    ".js"   = "application/javascript; charset=utf-8"
    ".jpeg" = "image/jpeg"
    ".jpg"  = "image/jpeg"
    ".md"   = "text/markdown; charset=utf-8"
    ".png"  = "image/png"
    ".svg"  = "image/svg+xml"
    ".webp" = "image/webp"
}

function Send-Response {
    param(
        [Parameter(Mandatory)]
        [System.Net.HttpListenerResponse]$Response,
        [Parameter(Mandatory)]
        [byte[]]$Body,
        [Parameter(Mandatory)]
        [string]$ContentType,
        [int]$StatusCode = 200
    )

    $Response.StatusCode = $StatusCode
    $Response.ContentType = $ContentType
    $Response.Headers["Cache-Control"] = "no-store"
    $Response.ContentLength64 = $Body.Length
    $Response.OutputStream.Write($Body, 0, $Body.Length)
    $Response.OutputStream.Close()
}

function Get-LocalContentIndex {
    $keys = @(
        Get-ChildItem -LiteralPath $templatesRoot -Recurse -File -Filter "*.md" |
            ForEach-Object {
                $_.FullName.Substring($projectRoot.Length + 1).Replace("\", "/")
            } |
            Sort-Object
    )
    $json = ConvertTo-Json -InputObject $keys -Compress
    return "window.CONTENT_INDEX = Object.freeze($json);`n"
}

$listener = [System.Net.HttpListener]::new()
$listener.Prefixes.Add("http://127.0.0.1:$Port/")

try {
    $listener.Start()
    Write-Host ""
    Write-Host "Local preview: http://127.0.0.1:$Port" -ForegroundColor Green
    Write-Host "Refresh the page after changing Markdown files. Press Ctrl+C to stop."
    Write-Host ""

    while ($listener.IsListening) {
        $context = $listener.GetContext()
        try {
            $urlPath = [Uri]::UnescapeDataString($context.Request.Url.AbsolutePath)
            if ($urlPath -eq "/content-index.js") {
                $body = [Text.Encoding]::UTF8.GetBytes((Get-LocalContentIndex))
                Send-Response -Response $context.Response -Body $body `
                    -ContentType "application/javascript; charset=utf-8"
                continue
            }

            $relativePath = $urlPath.TrimStart("/")
            if ([string]::IsNullOrWhiteSpace($relativePath)) {
                $relativePath = "index.html"
            }

            $filePath = [IO.Path]::GetFullPath((Join-Path $projectRoot $relativePath))
            $insideProject = $filePath.Equals($projectRoot, [StringComparison]::OrdinalIgnoreCase) -or
                $filePath.StartsWith("$projectRoot\", [StringComparison]::OrdinalIgnoreCase)

            if (-not $insideProject -or -not (Test-Path -LiteralPath $filePath -PathType Leaf)) {
                $body = [Text.Encoding]::UTF8.GetBytes("Not found")
                Send-Response -Response $context.Response -Body $body `
                    -ContentType "text/plain; charset=utf-8" -StatusCode 404
                continue
            }

            $extension = [IO.Path]::GetExtension($filePath).ToLowerInvariant()
            $contentType = $contentTypes[$extension]
            if (-not $contentType) {
                $contentType = "application/octet-stream"
            }
            Send-Response -Response $context.Response -Body ([IO.File]::ReadAllBytes($filePath)) `
                -ContentType $contentType
        }
        catch {
            Write-Warning $_
            if ($context.Response.OutputStream.CanWrite) {
                $body = [Text.Encoding]::UTF8.GetBytes("Local preview error")
                Send-Response -Response $context.Response -Body $body `
                    -ContentType "text/plain; charset=utf-8" -StatusCode 500
            }
        }
    }
}
finally {
    try {
        $listener.Stop()
        $listener.Close()
    }
    catch {
        # The listener can already be disposed when startup itself fails.
    }
}
