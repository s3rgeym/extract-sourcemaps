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

## Assets

React:

```js
var _path, _path2

function _extends() {
  _extends =
    Object.assign ||
    function (target) {
      for (var i = 1; i < arguments.length; i++) {
        var source = arguments[i]
        for (var key in source) {
          if (Object.prototype.hasOwnProperty.call(source, key)) {
            target[key] = source[key]
          }
        }
      }
      return target
    }
  return _extends.apply(this, arguments)
}

import * as React from 'react'

function SvgAddFile(props) {
  return /*#__PURE__*/ React.createElement(
    'svg',
    _extends(
      {
        width: 24,
        height: 24,
        fill: 'none',
        xmlns: 'http://www.w3.org/2000/svg',
      },
      props,
    ),
    _path ||
      (_path = /*#__PURE__*/ React.createElement('path', {
        d: 'M18.75 21H5.249a.75.75 0 01-.75-.75V3.75a.75.75 0 01.75-.75h9l5.25 5.25v12a.75.75 0 01-.75.75z',
        stroke: '#359D9E',
        strokeWidth: 1.5,
        strokeLinecap: 'round',
        strokeLinejoin: 'round',
      })),
    _path2 ||
      (_path2 = /*#__PURE__*/ React.createElement('path', {
        d: 'M14.25 3v5.25h5.25M9.75 14.25h4.5M12 12v4.5',
        stroke: '#359D9E',
        strokeWidth: 1.5,
        strokeLinecap: 'round',
        strokeLinejoin: 'round',
      })),
  )
}

export default __webpack_public_path__ + '96d8a036093d833f8b176896735c931f.svg'
export { SvgAddFile as ReactComponent }
```
