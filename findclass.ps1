param (
    [string]$zipFile,
    [string]$searchTerm
)

# Load the .NET assembly for zip file handling
Add-Type -AssemblyName System.IO.Compression.FileSystem

# Open the zip file and check for the search term
$zipContents = [System.IO.Compression.ZipFile]::OpenRead($zipFile)
$entries = $zipContents.Entries | Select-Object -ExpandProperty FullName

if ($entries -match $searchTerm) {
    Write-Output $zipFile
}

$zipContents.Dispose()
