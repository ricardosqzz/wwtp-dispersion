# ENTRADA: JSON indicado em ListaArquivos, com docx e pdf para cada documento.
# SAÍDA: PDF nativo do Word para conferência da paginação e figuras; documentos são abertos apenas para leitura.
# CAMINHOS: definidos no JSON; não fecha documentos do usuário, somente a instância criada por este script.
param([Parameter(Mandatory=$true)][string]$ListaArquivos)
$ErrorActionPreference='Stop'
$items=Get-Content -LiteralPath $ListaArquivos -Raw -Encoding UTF8 | ConvertFrom-Json
$word=New-Object -ComObject Word.Application
$word.Visible=$false
$word.DisplayAlerts=0
try {
 foreach($item in $items) {
  $source=[System.IO.Path]::GetFullPath([string]$item.docx)
  $target=[System.IO.Path]::GetFullPath([string]$item.pdf)
  $document=$word.Documents.Open($source,$false,$true,$false)
  try {$document.Repaginate();$document.ExportAsFixedFormat($target,17,$false,0,0,1,1,0,$true,$true,1);Write-Output "WORD_PDF $target"}
  finally {$document.Close(0)}
 }
} finally {$word.Quit()}
