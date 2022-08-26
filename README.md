Extract source maps from a given URL.

Usage:

```bash
./extract_sourcemaps.py <url>
```

How To Search Source Maps:

```bash
httpx -l sites.txt -json -o sourcemaps.json -mr '/app\.[0-9a-f]{8,}\.js"' -mc 200
```
