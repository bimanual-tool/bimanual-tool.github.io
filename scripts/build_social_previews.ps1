# Typeset 1200 x 630 social cards using the unchanged workshop logo.
# Requires Windows and System.Drawing; no additional packages are needed.
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$repoRoot = Split-Path $PSScriptRoot -Parent
$logo = [System.Drawing.Image]::FromFile((Join-Path $repoRoot 'assets/bidextool-logo.png'))
$navy = [System.Drawing.ColorTranslator]::FromHtml('#172942')
$muted = [System.Drawing.ColorTranslator]::FromHtml('#626975')
$paper = [System.Drawing.ColorTranslator]::FromHtml('#fffdfa')

function Add-CardText {
    param($Graphics, [string]$Text, [float]$X, [float]$Y, [string]$Family, [float]$Size, [System.Drawing.FontStyle]$Style, $Color)
    $font = [System.Drawing.Font]::new($Family, $Size, $Style, [System.Drawing.GraphicsUnit]::Pixel)
    $brush = [System.Drawing.SolidBrush]::new($Color)
    $Graphics.DrawString($Text, $font, $brush, $X, $Y, [System.Drawing.StringFormat]::GenericTypographic)
    $font.Dispose()
    $brush.Dispose()
}

try {
    foreach ($kind in @('on-psyduck-social', 'bidextool-social')) {
        $bitmap = [System.Drawing.Bitmap]::new(1200, 630)
        $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
        try {
            $graphics.Clear($paper)
            $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
            $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
            $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
            $graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
            $regular = [System.Drawing.FontStyle]::Regular
            $bold = [System.Drawing.FontStyle]::Bold
            Add-CardText $graphics 'BiDexTool  /  CoRL 2026' 70 45 'Segoe UI' 19 $bold $navy
            $accent = [System.Drawing.Pen]::new([System.Drawing.ColorTranslator]::FromHtml('#e9b83b'), 5)
            $graphics.DrawLine($accent, 70, 92, 120, 92)
            $accent.Dispose()
            if ($kind -eq 'on-psyduck-social') {
                Add-CardText $graphics 'On Psyduck' 67 145 'Georgia' 74 $regular $navy
                Add-CardText $graphics '论·可达鸭' 72 249 'SimSun' 38 $regular $navy
                Add-CardText $graphics 'A workshop reflection' 72 340 'Segoe UI' 25 $regular $navy
                Add-CardText $graphics 'Two hands, a paintbrush,' 72 389 'Segoe UI' 22 $regular $muted
                Add-CardText $graphics 'and a few questions that remain.' 72 422 'Segoe UI' 22 $regular $muted
                Add-CardText $graphics 'Runfa Blark Li  ·  November 17, 2026' 72 526 'Segoe UI' 17 $regular $muted
            } else {
                Add-CardText $graphics 'BiDexTool' 67 145 'Georgia' 78 $regular $navy
                Add-CardText $graphics 'Bimanual Dexterous' 72 258 'Segoe UI' 30 $bold $navy
                Add-CardText $graphics 'Tool Use' 72 299 'Segoe UI' 30 $bold $navy
                Add-CardText $graphics 'Workshop reflection' 72 385 'Segoe UI' 23 $regular $muted
                Add-CardText $graphics 'Full recording · Talks · Papers' 72 421 'Segoe UI' 23 $regular $muted
                Add-CardText $graphics 'November 12, 2026  ·  Austin, Texas' 72 526 'Segoe UI' 17 $regular $muted
            }
            $scale = [Math]::Min(421.0 / $logo.Width, 472.0 / $logo.Height)
            $w = [float]($logo.Width * $scale)
            $h = [float]($logo.Height * $scale)
            $graphics.DrawImage($logo, [System.Drawing.RectangleF]::new(681, 68, $w, $h))
            $line = [System.Drawing.Pen]::new([System.Drawing.ColorTranslator]::FromHtml('#e6e7e9'), 1)
            $graphics.DrawLine($line, 70, 568, 1130, 568)
            $line.Dispose()
            $target = Join-Path $repoRoot ('assets/' + $kind + '.png')
            $bitmap.Save($target, [System.Drawing.Imaging.ImageFormat]::Png)
            Write-Output ('Built ' + $kind + '.png')
        } finally {
            $graphics.Dispose()
            $bitmap.Dispose()
        }
    }
} finally {
    $logo.Dispose()
}
