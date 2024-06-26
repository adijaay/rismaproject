from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from surat_menyurat.models import SuratMasuk, SuratKeluar
from surat_menyurat.forms import FormSuratMasuk, FormSuratKeluar
import os
from django.db.models import Q
from datetime import datetime

@login_required
def home(request):
  data_surat_masuk = SuratMasuk.objects.exclude(status='Diproses bidang terkait').count()
  data_surat_keluar = SuratKeluar.objects.exclude(status='Sudah dikirim').count()
  return render(request, 'home.html', {
    'data_surat_masuk': data_surat_masuk,
    'data_surat_keluar': data_surat_keluar
  })

def login_redirect(request):
  return redirect('login')

@login_required
def surat_masuk_list(request):
  query = request.GET.get('q')
  start_date = request.GET.get('start_date')
  end_date = request.GET.get('end_date')

  filters =Q()

  if start_date:
      start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%d-%m-%Y')
  
  if end_date:
      end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%d-%m-%Y')

  if query:
      filters &= (Q(nomor__icontains=query) |
                  Q(perihal__icontains=query) |
                  Q(pengirim__icontains=query) |
                  Q(deskripsi__icontains=query))

  if start_date:
      filters &= Q(tgl_masuk__gte=start_date)
  
  if end_date:
      filters &= Q(tgl_masuk__lte=end_date)

  data = SuratMasuk.objects.exclude(status='Diproses bidang terkait').filter(filters).order_by('-id')

  return render(request, "surat/surat_masuk_list.html", {
      'data': data,
      'query': query,
      'start_date': start_date,
      'end_date': end_date
  })

@login_required
def surat_masuk_delete(request, id):
  surat_masuk = get_object_or_404(SuratMasuk, pk=id)
  surat_masuk.delete()
  if surat_masuk.file_path:
        old_file_path = os.path.join(settings.MEDIA_ROOT, surat_masuk.file_path.name)
        if os.path.exists(old_file_path):
            os.remove(old_file_path)
  return redirect('surat:surat_masuk_list')

@login_required
def surat_masuk_edit(r, id):
  if r.POST:
    form = FormSuratMasuk(r.POST or None, r.FILES)
    id = r.POST['id']
    surat_masuk = get_object_or_404(SuratMasuk, pk=id)
    if form.is_valid():
      surat_masuk.nomor = form.cleaned_data['nomor']
      surat_masuk.tgl_surat = form.cleaned_data['tgl_surat']
      surat_masuk.perihal = form.cleaned_data['perihal']
      surat_masuk.pengirim = form.cleaned_data['pengirim']
      surat_masuk.deskripsi = form.cleaned_data['deskripsi']
      surat_masuk.tgl_masuk = form.cleaned_data['tgl_masuk']
      surat_masuk.status = form.cleaned_data['status']
      if 'file_path' in r.FILES:
          if surat_masuk.file_path:
              old_file_path = os.path.join(settings.MEDIA_ROOT, surat_masuk.file_path.name)
              if os.path.exists(old_file_path):
                  os.remove(old_file_path)
          surat_masuk.file_path = r.FILES['file_path']

      surat_masuk.save(force_update=True)
      return redirect('surat:surat_masuk_list')
    return render(r, 'surat/surat_masuk_form_edit.html', {'form':form, 'id':id})

  surat_masuk = get_object_or_404(SuratMasuk, pk=id)
  form = FormSuratMasuk(initial={
          'nomor':surat_masuk.nomor,
          'tgl_surat':surat_masuk.tgl_surat,
          'perihal':surat_masuk.perihal,
          'pengirim':surat_masuk.pengirim,
          'deskripsi':surat_masuk.deskripsi,
          'tgl_masuk':surat_masuk.tgl_masuk,
          'status':surat_masuk.status,
          'file_path': surat_masuk.file_path
        })
  return render(r, 'surat/surat_masuk_form_edit.html', {'form':form, 'id':surat_masuk.id})

@login_required
def surat_masuk_form(request):
    form = FormSuratMasuk(request.POST or None, request.FILES)
    if request.POST:
        if form.is_valid():
            form.save(commit=True)
            return redirect('surat:surat_masuk_list')

        return render(request, "surat/surat_masuk_form_new.html", {
            'form': form
        })

    return render(request, "surat/surat_masuk_form_new.html", {
        'form': form
    })

@login_required
def surat_keluar_form(request):
  form = FormSuratKeluar(request.POST, request.FILES)
  if request.POST:
    if form.is_valid():
      form.save(commit=True)

      return redirect('surat:surat_keluar_list')

    return render(request, "surat/surat_keluar_form_new.html", {
      'form': form
    })

  return render(request, "surat/surat_keluar_form_new.html", {
    'form': form
  })

@login_required
def surat_keluar_list(request):
  query = request.GET.get('q')
  start_date = request.GET.get('start_date')
  end_date = request.GET.get('end_date')

  filters =Q()

  if start_date:
      start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%d-%m-%Y')
  
  if end_date:
      end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%d-%m-%Y')

  if query:
      filters &= (Q(nomor__icontains=query) |
                  Q(perihal__icontains=query) |
                  Q(pengirim__icontains=query) |
                  Q(deskripsi__icontains=query))

  if start_date:
      filters &= Q(tgl_keluar__gte=start_date)
  
  if end_date:
      filters &= Q(tgl_keluar__lte=end_date)

  data = SuratKeluar.objects.exclude(status='Sudah dikirim').filter(filters).order_by('-id')

  return render(request, "surat/surat_keluar_list.html", {
      'data': data,
      'query': query,
      'start_date': start_date,
      'end_date': end_date
  })

@login_required
def surat_keluar_delete(request, id):
  surat_keluar = get_object_or_404(SuratKeluar, pk=id)
  surat_keluar.delete()
  if surat_keluar.file_path:
        old_file_path = os.path.join(settings.MEDIA_ROOT, surat_keluar.file_path.name)
        if os.path.exists(old_file_path):
            os.remove(old_file_path)
  return redirect('surat:surat_keluar_list')

@login_required
def surat_keluar_edit(r, id):
  if r.POST:
    form = FormSuratKeluar(r.POST or None, r.FILES)
    id = r.POST['id']
    surat_keluar = get_object_or_404(SuratKeluar, pk=id)
    if form.is_valid():
      surat_keluar.nomor = form.cleaned_data['nomor']
      surat_keluar.tgl_surat = form.cleaned_data['tgl_surat']
      surat_keluar.perihal = form.cleaned_data['perihal']
      surat_keluar.pengirim = form.cleaned_data['pengirim']
      surat_keluar.deskripsi = form.cleaned_data['deskripsi']
      surat_keluar.tgl_keluar = form.cleaned_data['tgl_keluar']
      surat_keluar.status = form.cleaned_data['status']
      if 'file_path' in r.FILES:
          if surat_keluar.file_path:
              old_file_path = os.path.join(settings.MEDIA_ROOT, surat_keluar.file_path.name)
              if os.path.exists(old_file_path):
                  os.remove(old_file_path)
          surat_keluar.file_path = r.FILES['file_path']

      surat_keluar.save(force_update=True)
      return redirect('surat:surat_keluar_list')
    return render(r, 'surat/surat_keluar_form_edit.html', {'form':form, 'id':id})

  surat_keluar = get_object_or_404(SuratKeluar, pk=id)
  form = FormSuratKeluar(initial={
          'nomor':surat_keluar.nomor,
          'tgl_surat':surat_keluar.tgl_surat,
          'perihal':surat_keluar.perihal,
          'pengirim':surat_keluar.pengirim,
          'deskripsi':surat_keluar.deskripsi,
          'tgl_keluar':surat_keluar.tgl_keluar,
          'status':surat_keluar.status,
          'file_path': surat_keluar.file_path
        })
  return render(r, 'surat/surat_keluar_form_edit.html', {'form':form, 'id':surat_keluar.id})

@login_required
def arsip_surat_masuk_list(request):
  query = request.GET.get('q')
  start_date = request.GET.get('start_date')
  end_date = request.GET.get('end_date')

  filters = Q(status='Diproses bidang terkait')

  if start_date:
      start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%d-%m-%Y')
  
  if end_date:
      end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%d-%m-%Y')

  if query:
      filters &= (Q(nomor__icontains=query) |
                  Q(perihal__icontains=query) |
                  Q(pengirim__icontains=query) |
                  Q(deskripsi__icontains=query) |
                  Q(status__icontains=query))

  if start_date:
      filters &= Q(tgl_masuk__gte=start_date)
  
  if end_date:
      filters &= Q(tgl_masuk__lte=end_date)

  data = SuratMasuk.objects.filter(filters).order_by('-id')

  return render(request, "surat/arsip_surat_masuk_list.html", {
      'data': data,
      'query': query,
      'start_date': start_date,
      'end_date': end_date
  })

@login_required
def arsip_surat_masuk_delete(request, id):
    surat_masuk = get_object_or_404(SuratMasuk, pk=id)
    surat_masuk.delete()
    
    if surat_masuk.file_path:
        old_file_path = os.path.join(settings.MEDIA_ROOT, surat_masuk.file_path.name)
        if os.path.exists(old_file_path):
            os.remove(old_file_path)
    
    return redirect('surat:arsip_surat_masuk_list')

@login_required
def arsip_surat_keluar_list(request):
    query = request.GET.get('q')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    filters = Q(status='Sudah dikirim')

    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%d-%m-%Y')
    
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%d-%m-%Y')

    if query:
        filters &= (Q(nomor__icontains=query) |
                    Q(perihal__icontains=query) |
                    Q(pengirim__icontains=query) |
                    Q(deskripsi__icontains=query) |
                    Q(status__icontains=query))

    if start_date:
        filters &= Q(tgl_keluar__gte=start_date)
    
    if end_date:
        filters &= Q(tgl_keluar__lte=end_date)

    data = SuratKeluar.objects.filter(filters).order_by('-id')

    return render(request, "surat/arsip_surat_keluar_list.html", {
        'data': data,
        'query': query,
        'start_date': start_date,
        'end_date': end_date
    })

@login_required
def arsip_surat_keluar_delete(request, id):
  surat_keluar = get_object_or_404(SuratKeluar, pk=id)
  surat_keluar.delete()
  if surat_keluar.file_path:
        old_file_path = os.path.join(settings.MEDIA_ROOT, surat_keluar.file_path.name)
        if os.path.exists(old_file_path):
            os.remove(old_file_path)
  return redirect('surat:arsip_surat_keluar_list')