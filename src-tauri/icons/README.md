# App Icons

Place your app icons here so that `tauri build` can bundle them.

**Required files** (referenced in `tauri.conf.json`):

- `icon.png` — used for tray icon
- `32x32.png`
- `128x128.png`
- `128x128@2x.png`
- `icon.icns` (macOS)
- `icon.ico` (Windows)

**Generate from a single image:**

```bash
cargo tauri icon path/to/your/icon.png
```

This generates the required sizes and formats. Then move or copy the output into this `icons/` directory.

Replace these placeholders before building for release. See [Tauri icons guide](https://tauri.app/v1/guides/features/icons) for details.
