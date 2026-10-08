# BundleWP blog images

Featured images for bundlewp.com blog posts, drawn with code (SVG) using the free Lucide icon set (ISC licence). No AI image tools, no paid APIs.

## How a new image is made (for the daily blog task)

1. `cd tools && npm install && cd ..` (and `pip install playwright pillow && python3 -m playwright install chromium` if missing)
2. Write a NEW scene script `tools/scenes/<post-slug>.py` that draws **what the post is actually about** using `tools/kit.py`. Look at the existing scenes first.
3. `python3 tools/render_scene.py tools/scenes/<post-slug>.py blog/<yyyy>/<mm>/<post-slug>.webp`, open the `.preview.png`, fix anything that overlaps or looks wrong, then commit the `.webp` and the scene script.

## Design rules

- **Show the post's real scenario**, not a generic icon pattern. Ask: what would this look like on a real screen or desk? Examples:
  - expense tracking → receipts flowing into a dashboard (donut, bars, ledger table) on a laptop
  - product data extraction → online-store product cards → scan → spreadsheet
  - calculator website → a website grid of calculator tools + phone view
  - Google Maps leads → map with business pins + popup → contact list with phone/email
  - billing/POS → till screen with invoice, printed receipt, barcode, stock boxes, card payment
  - WooCommerce automation → order cards moving through a pipeline with gears/automation arrows, cart recovery email
  - CRM / lead nurturing → contact cards, email/WhatsApp chat bubbles, timeline of follow-ups, funnel
  - WordPress speed/security → browser with speed gauge, shield, lock, backup cloud
- **Vary the layout** — never reuse the previous 3 posts' layout (left-to-right flow, single big device, device + phone, before/after split, map + list, dashboard close-up, desk scene with documents, pipeline/stages…).
- **Vary the palette** — light: mint, sky, peach, lilac, sand; dark: midnight, forest, plum, ember. Don't repeat the palette of the last 2 images.
- **No words or numbers** in the image (the blog card shows the title). No fake brand logos.
- Keep the main subject inside x 120–1080, y 60–570; leave the top-left corner (x<260, y<100) fairly empty because the theme puts a "LATEST" badge there.

## Kit parts (`tools/kit.py`)

background(style: blobs|grid|dots|both) · box · lines · pill · circle · icon(name) · badge(icon) · arrow · sparkles ·
browser · laptop · phone · pos_terminal · bars · line_chart · donut · table · receipt · document · product_card ·
map_panel(pins) · pin · person · contact_row · gear. Lucide icon names: https://lucide.dev/icons
