Extract source maps from a given URL.

Usage:

```bash
./extract_sourcemaps.py <url>
```

How To Search Source Maps:

```bash
httpx -l sites.txt -json -o sourcemaps.json -mr '/app\.[0-9a-f]{8,}\.js"' -mc 200
```

![image](https://user-images.githubusercontent.com/12753171/186857622-7bd4378b-2861-4a9e-9428-b8deae6a3f98.png)
