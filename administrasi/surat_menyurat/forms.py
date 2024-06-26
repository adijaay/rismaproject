from django import forms
from surat_menyurat.models import  SuratMasuk, SuratKeluar

class FormSuratMasuk(forms.ModelForm):
  class Meta:
    model = SuratMasuk
    exclude = ('id', )

  def __init__(self, *args, **kwargs):
    super(FormSuratMasuk, self).__init__(*args, **kwargs)
    for visible in self.visible_fields():
      visible.field.widget.attrs['class'] = 'form-control'
    
class FormSuratKeluar(forms.ModelForm):
  class Meta:
    model = SuratKeluar
    exclude = ('id', )

  def __init__(self, *args, **kwargs):
    super(FormSuratKeluar, self).__init__(*args, **kwargs)
    for visible in self.visible_fields():
      visible.field.widget.attrs['class'] = 'form-control'
      