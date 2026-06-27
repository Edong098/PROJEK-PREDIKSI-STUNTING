def get_stunting_interpretation(status, confidence, model_name):
    """
    Returns automated advice and interpretation text based on the prediction status.
    """
    status_lower = str(status).lower().strip()
    
    if 'severely stunted' in status_lower:
        return (
            f"Model memprediksi balita berada pada kategori **Severely Stunted** (Sangat Pendek) "
            f"dengan tingkat keyakinan sebesar **{confidence:.2f}%** menggunakan model **{model_name}**.\n\n"
            f"> [!CAUTION]\n"
            f"> **Rekomendasi Tindakan Segera:**\n"
            f"> 1. Segera lakukan konsultasi dengan Dokter Spesialis Anak atau kunjungi Puskesmas/Rumah Sakit terdekat.\n"
            f"> 2. Berikan intervensi gizi spesifik secara intensif di bawah pengawasan tenaga medis.\n"
            f"> 3. Cek kemungkinan adanya infeksi kronis atau penyakit penyerta lainnya."
        )
    elif 'stunted' in status_lower:
        return (
            f"Model memprediksi balita berada pada kategori **Stunted** (Pendek) "
            f"dengan tingkat keyakinan sebesar **{confidence:.2f}%** menggunakan model **{model_name}**.\n\n"
            f"> [!WARNING]\n"
            f"> **Rekomendasi Tindakan:**\n"
            f"> 1. Rujuk balita ke fasilitas pelayanan kesehatan terdekat untuk pemeriksaan klinis lengkap.\n"
            f"> 2. Evaluasi asupan gizi harian, tingkatkan protein hewani (seperti telur, ikan, susu) dan ASI eksklusif/lanjutan.\n"
            f"> 3. Perbaiki sanitasi lingkungan rumah dan pastikan kebersihan air minum."
        )
    elif 'normal' in status_lower:
        return (
            f"Model memprediksi balita berada pada kategori **Normal** "
            f"dengan tingkat keyakinan sebesar **{confidence:.2f}%** menggunakan model **{model_name}**.\n\n"
            f"> [!NOTE]\n"
            f"> **Keterangan:**\n"
            f"> Berdasarkan karakteristik umur dan tinggi badan yang dimasukkan, kondisi gizi balita berada dalam kategori sehat/ideal.\n"
            f"> Tetap pertahankan pola makan seimbang, jaga kebersihan, serta rutin pantau pertumbuhan di Posyandu setiap bulan."
        )
    elif 'tinggi' in status_lower:
        return (
            f"Model memprediksi balita berada pada kategori **Tinggi** "
            f"dengan tingkat keyakinan sebesar **{confidence:.2f}%** menggunakan model **{model_name}**.\n\n"
            f"> [!TIP]\n"
            f"> **Keterangan:**\n"
            f"> Tinggi badan balita berada di atas rata-rata tinggi anak seusianya. Hal ini umumnya menunjukkan status nutrisi yang sangat baik dan faktor genetik yang optimal.\n"
            f"> Pastikan asupan gizi tetap berimbang demi mendukung perkembangan kognitif dan fisik balita secara keseluruhan."
        )
    else:
        return f"Model memprediksi balita berada pada kategori **{status}** dengan tingkat keyakinan sebesar **{confidence:.2f}%**."
