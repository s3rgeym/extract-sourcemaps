Extract source maps from a given URL.

Usage:

```bash
./extract_sourcemaps.py <url>
```

How To Search Source Maps:

```bash
httpx -l sites.txt -json -o sourcemaps.json -mr '/app\.[0-9a-f]{8,}\.js"' -mc 200
```

![image](https://user-images.githubusercontent.com/12753171/186984737-d64efb73-1700-4e48-8242-e8d806ab78ce.png)
