$npm_path = npm bin
$env:Path += ";" + $npm_path
Invoke-Expression("" + $args)
