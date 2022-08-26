Extract source maps from a given URL. Test on Vue.js and React apps.

Use pyenv to install latest python version and make it global.

Install requirements if needed.

Usage:

```bash
./extract_sourcemaps.py [OPTIONS] <target url>
./extract_sourcemaps.py -h
```

How To Search Source Maps:

```bash
httpx -l sites.txt -json -o sourcemaps.json -mr '/app\.[0-9a-f]{8,}\.js"' -mc 200
```

![image](https://user-images.githubusercontent.com/12753171/186984737-d64efb73-1700-4e48-8242-e8d806ab78ce.png)
