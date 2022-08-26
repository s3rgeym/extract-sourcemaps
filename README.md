Extract source maps from a given URL.

Usage:

```bash
./extract_sourcemaps.py <url>
```

How To Search Source Maps:

```bash
httpx -l sites.txt -json -o sourcemaps.json -mr '/app\.[0-9a-f]{8,}\.js"' -mc 200
```

![image](https://user-images.githubusercontent.com/12753171/186840792-7aa436df-6e8f-41b7-94f2-5b3719c53779.png)
