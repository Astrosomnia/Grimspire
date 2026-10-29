#!/bin/sh
# wrap a source file like claude.ai does, so phone tests get a real viewport
(printf '<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}</style></head><body>\n'; cat "$1"; echo '</body></html>') > "$2"
