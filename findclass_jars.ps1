# param (
#     [string]$repositoryPath,
#     [string]$className
# )

# $jarFiles = Get-ChildItem -Path $repositoryPath -Recurse -Filter '*.jar'

# foreach ($jarFile in $jarFiles) {
#     & .\findclass.ps1 $jarFile.FullName $className
# }

param (
    [string]$repositoryPath,
    [string]$className
)

$currentScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$findClassScriptPath = Join-Path -Path $currentScriptDir -ChildPath 'findclass.ps1'

$jarFiles = Get-ChildItem -Path $repositoryPath -Recurse -Filter '*.jar'

foreach ($jarFile in $jarFiles) {
    & $findClassScriptPath $jarFile.FullName $className
}
