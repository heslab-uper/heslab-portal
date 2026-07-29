# HESLab Portal — GH Pages + Manual Plotly HTML

## Cara kerja (ringkas)

1. Anda menulis figure Plotly seperti biasa (`go.Figure(...)`).
2. `site/build_site.py` mengubah tiap figure jadi **fragment HTML** (bukan halaman utuh),
   lalu menyisipkannya ke `site/templates/base.html` — satu template yang berisi
   header, navigasi, dan styling untuk SELURUH situs.
3. Hasilnya ditulis ke folder `docs/` — ini folder yang akan disajikan GitHub Pages.
4. GitHub Actions (`.github/workflows/deploy.yml`) menjalankan langkah 1–3 otomatis
   setiap ada push, setiap hari jam 05:00 WIB, atau saat Anda klik "Run workflow" manual.

## Setup GitHub Pages (dilakukan SEKALI saja, manual di web GitHub)

1. Push repo ini ke GitHub.
2. Buka **Settings → Pages**.
3. Di "Build and deployment" → **Source: Deploy from a branch**.
4. Pilih branch `main`, folder **`/docs`**.
5. Simpan. Situs akan hidup di `https://<username>.github.io/<repo-name>/` dalam 1-2 menit.

Setelah ini, Anda **tidak perlu mengulang setup** — setiap kali `docs/` berubah
(lewat Actions atau push manual), GitHub Pages otomatis republish.

## Menambah halaman baru

Cukup tambahkan blok baru di `build_site.py` (atau file Python terpisah yang
mengimpor `render_page` dan `ContentBlock` dari `build_site.py`):

```python
from build_site import render_page, ContentBlock
import plotly.graph_objects as go

fig = go.Figure(...)

render_page(
    output_path="rainfall/monthly.html",   # -> docs/rainfall/monthly.html
    title="Rainfall Monitoring — Bulanan",
    section="rainfall",                    # menyorot menu nav yang aktif
    blocks=[ContentBlock(fig, card_title="Curah Hujan Bulanan")],
)
```

Anda TIDAK perlu menulis HTML baru. Template dan CSS sudah menangani layout,
navigasi, dan tampilan responsif secara otomatis.

## Mengatur layout beberapa chart dalam satu halaman

`ContentBlock(fig, size=...)` menerima:
- `"full"`  → chart selebar halaman (default)
- `"half"`  → dua chart berdampingan
- `"third"` → tiga chart berdampingan

```python
render_page(
    output_path="rainfall/daily.html",
    title="Rainfall — Harian",
    section="rainfall",
    blocks=[
        ContentBlock(fig_map, size="full"),
        ContentBlock(fig_spi, size="half", card_title="SPI"),
        ContentBlock(fig_rank, size="half", card_title="Ranking"),
    ],
)
```

## Mengubah warna/tampilan situs

Edit satu file saja: `site/assets/style.css` (variabel warna ada di bagian
`:root` paling atas). Perubahan ini otomatis berlaku ke SEMUA halaman karena
semua halaman memuat file CSS yang sama.

## Catatan penting

- **Jangan** gunakan `fig.write_html()` langsung ke folder `docs/` untuk chart
  individual — itu akan membuat halaman berdiri sendiri tanpa nav/header/footer
  situs Anda. Selalu lewat `render_page()` + `ContentBlock`.
- `include_plotlyjs=False` di `ContentBlock` sengaja dipakai karena Plotly.js
  sudah dimuat SEKALI di `templates/base.html` lewat CDN — ini membuat setiap
  halaman jauh lebih ringan (tidak mengunduh ulang library ~3MB per chart).
- Skrip ini belum saya jalankan di sandbox ini karena tidak ada akses jaringan
  untuk `pip install`. Sintaksnya sudah saya verifikasi (`py_compile` sukses),
  tapi jalankan `pip install -r requirements.txt && python site/build_site.py`
  di komputer Anda untuk konfirmasi output visualnya sebelum push pertama kali.
