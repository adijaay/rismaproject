from django.db import models
from django.utils.translation import gettext_lazy as _

class Surat(models.Model):
  nomor         = models.CharField(max_length=255, blank=False, null=False)
  tgl_surat     = models.CharField(
                  _("Tanggal surat"),
                  help_text=_('Tanggal di dalam isi surat'),
                  max_length=255, blank=False, null=False)
  perihal       = models.CharField(max_length=255, blank=False, null=False)
  pengirim      = models.CharField(
                  help_text=_('Orang atau jasa yang mengantar surat'),
                  max_length=255, blank=True, null=True)
  deskripsi     = models.TextField(blank=True, null=True)
  file_path     = models.FileField(blank=True, null=True, upload_to='surat_menyurat/medias/')

class SuratMasuk(Surat):
  STATUS_MASUK = (
    ('Baru Masuk', 'Masuk'),
    ('Diproses ke Kepala Dinas', 'Diproses ke Kepala Dinas'),
    ('Diproses ke Sekretaris Dinas', 'Diproses ke Sekretaris Dinas'),
    ('Diproses bidang terkait', 'Diproses Bidang Terkait'),
  )
  tgl_masuk     = models.CharField(
                  _("Tanggal masuk"),
                  help_text=_('Tanggal masuk surat ke kantor'),
                  max_length=255, blank=False, null=False)
  status        = models.CharField(max_length=255, choices=STATUS_MASUK)
  created       = models.DateTimeField(auto_now=False, auto_now_add=True)
  updated       = models.DateTimeField(auto_now=True, auto_now_add=False)

  def __str__(self):
    return self.nomor

class SuratKeluar(Surat):
  STATUS_KELUAR = (
    ('Sudah Dikirim', 'Sudah Dikirim'),
    ('Diproses ke Kepala Dinas', 'Diproses ke Kepala Dinas'),
    ('Diproses ke Sekretaris Dinas', 'Diproses ke Sekretaris Dinas'),
    ('Diproses bidang terkait', 'Diproses Bidang Terkait'),
  )
  tgl_keluar        = models.CharField(
                      _("Tanggal keluar"),
                      help_text=_('Tanggal keluar surat dari kantor'),
                      max_length=255, blank=False, null=False)
  status            = models.CharField(max_length=255, choices=STATUS_KELUAR)
  created           = models.DateTimeField(auto_now=False, auto_now_add=True)
  updated           = models.DateTimeField(auto_now=True, auto_now_add=False)

  def __str__(self):
    return self.nomor
