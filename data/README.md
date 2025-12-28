# Reference Images Directory

## Setup Instructions

1. **Add Reference Images**: Place your Pokemon card reference images in this `reference_images/` folder.

2. **Naming Convention**: Name your image files to match the card names in `cards_database.csv`:
   - Example: `Pikachu VMAX.jpg` or `Pikachu VMAX.png`
   - Use underscores or hyphens for spaces: `Pikachu_VMAX.jpg` or `Pikachu-VMAX.jpg`
   - Case doesn't matter, but try to match the database names

3. **Image Quality**: For best detection results:
   - Use high-resolution images (at least 800x600 pixels)
   - Ensure good lighting and contrast
   - Remove backgrounds if possible
   - Use clear, focused photos

4. **Supported Formats**: PNG, JPG, JPEG

## Example Structure

```
data/
├── cards_database.csv
├── README.md
└── reference_images/
    ├── Pikachu VMAX.jpg
    ├── Charizard GX.png
    ├── Mewtwo EX.jpg
    └── ...
```

