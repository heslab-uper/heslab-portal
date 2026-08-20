# HESLab Portal — situs

Repositori ini memuat **keluaran situs**, bukan kode pembangkitnya.

Seluruh berkas HTML di sini dihasilkan otomatis oleh pembangkit situs statis
berbasis Python yang dijalankan di komputer laboratorium, lalu dicerminkan ke
repositori ini dan disajikan melalui GitHub Pages.

**Jangan menyunting berkas HTML di sini secara manual.** Perubahan apa pun akan
tertimpa pada pembaruan otomatis berikutnya.

Situs: <https://heslab-uper.github.io/heslab-portal/>

---

## Isi

| Lintasan | Isi | Frekuensi pembaruan |
|---|---|---|
| `/` | Beranda, empat dasbor | saat ada perubahan |
| `/rainfall/` | Animasi hujan 24 jam terakhir | tiap jam |
| `/rainfall/harian/{now,nrt,standard}/` | Laporan hujan harian per kabupaten/kota | tiap hari |
| `/rainfall/dasarian/{now,nrt,standard}/` | Akumulasi hujan dasarian multi-tahun | tiap bulan |
| `/fews/`, `/streamflow/`, `/drought/` | Modul dalam penyiapan | — |
| `/assets/geo/` | Geometri administrasi tersederhanakan | saat ada pemekaran wilayah |

Setiap berkas HTML bersifat mandiri: gaya dan data tertanam di dalamnya.
Satu-satunya berkas bersama adalah geometri kabupaten/kota di `assets/geo/`,
yang sengaja dipisah karena berukuran besar dan tidak berubah.

---

## Sumber data

Estimasi curah hujan berasal dari **JAXA Global Rainfall Watch (GSMaP)**,
Earth Observation Research Center, JAXA — <https://sharaku.eorc.jaxa.jp/GSMaP/>

Nilai per kabupaten/kota adalah **rata-rata areal** sel grid 0,1° (± 11 km) di
dalam poligon administrasi, bukan pengukuran penakar hujan di satu titik.
Rata-rata areal meredam puncak hujan lokal secara sistematis; angka pada portal
ini tidak menggantikan pengamatan permukaan.

Atribusi lengkap, tingkat kematangan tiap produk, dan keterbatasannya tercantum
pada kaki setiap halaman Rainfall Monitoring.

Batas wilayah administrasi: BPS / Badan Informasi Geospasial.

---

## Status dan penggunaan

Portal ini disusun untuk keperluan **riset dan edukasi**. Informasi peringatan
dini resmi tetap mengacu pada BMKG dan instansi berwenang.

Angka pada portal dapat berubah tanpa pemberitahuan seiring pembaruan produk
satelit — khususnya untuk produk near-real-time yang belum terkoreksi penakar.

---

## Riwayat commit

Riwayat repositori ini terdiri atas commit otomatis dan **tidak memiliki nilai
arsip**. Seluruh isi dapat dibangun ulang dari repositori kode. Karena itu
riwayat dapat dipangkas sewaktu-waktu bila ukurannya membesar, tanpa kehilangan
informasi apa pun.

---

## Laboratorium

Hydro-Environmental Systems Laboratory (HESLab)
Program Studi Teknik Sipil, Universitas Pertamina

Surel: heslab@universitaspertamina.ac.id
Website laboratorium: <https://www.heslab-uper.com>
