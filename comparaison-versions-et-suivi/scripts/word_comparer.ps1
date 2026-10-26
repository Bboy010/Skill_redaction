<#
word_comparer.ps1 : produit, avec Microsoft Word (Windows),
  1) le PDF de la version finale ;
  2) le document avec suivi des modifications : version de référence -> version finale.

Les deux documents sources sont ouverts en LECTURE SEULE.
Le script affiche l'empreinte MD5 de la version finale avant et après : elles doivent être identiques.

Fermez les fichiers dans Word avant de lancer le script.

Usage (PowerShell) :
  .\word_comparer.ps1 -Reference "C:\chemin\soumis.docx" -Finale "C:\chemin\final.docx" `
                      -Pdf "C:\chemin\final.pdf" -Suivi "C:\chemin\final_suivi.docx"
Options :
  -Auteur  "Authors"   nom affiché pour les révisions (évite d'afficher le nom du compte Windows)
  -SansPdf             ne pas produire le PDF
#>
param(
    [Parameter(Mandatory = $true)][string]$Reference,
    [Parameter(Mandatory = $true)][string]$Finale,
    [string]$Pdf,
    [Parameter(Mandatory = $true)][string]$Suivi,
    [string]$Auteur = "Authors",
    [switch]$SansPdf
)

$Reference = (Resolve-Path $Reference).Path
$Finale = (Resolve-Path $Finale).Path
$avant = (Get-FileHash $Finale -Algorithm MD5).Hash

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    if (-not $SansPdf) {
        if (-not $Pdf) { throw "Indiquez -Pdf ou utilisez -SansPdf" }
        $doc = $word.Documents.Open($Finale, $false, $true)     # (chemin, ConfirmConversions, ReadOnly)
        $doc.ExportAsFixedFormat($Pdf, 17)                     # 17 = PDF
        Write-Output ("PDF : " + $Pdf + " (" + $doc.ComputeStatistics(2) + " pages)")
        $doc.Close($false)
    }
    $o = $word.Documents.Open($Reference, $false, $true)
    $r = $word.Documents.Open($Finale, $false, $true)
    # CompareDocuments(Original, Revised, Destination=2 (nouveau document), Granularité=1 (mot), ... , Auteur)
    $cmp = $word.CompareDocuments($o, $r, 2, 1, $true, $true, $true, $true, $true, $true, $true, $true, $true, $true, $Auteur)
    $cmp.SaveAs2($Suivi, 16)                                   # 16 = .docx
    Write-Output ("Document suivi : " + $Suivi + " (" + $cmp.Revisions.Count + " révisions)")
    $cmp.Close($false); $o.Close($false); $r.Close($false)
}
finally {
    $word.Quit()
}
$apres = (Get-FileHash $Finale -Algorithm MD5).Hash
Write-Output ("Version finale inchangée : " + ($avant -eq $apres))
