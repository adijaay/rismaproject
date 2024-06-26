1. Clone dari repo **git clone https://github.com/adijaay/rismaproject.git**
2. Masuk ke project **cd rismaproject**
3. Membuat dan mengaktifkan environment
   - ****pip install virtualenv**** (_bagi yang belum install virtualenv_)
   - **virtualenv env** jika terdapat dua versi python yakni python2 dan python3 bisa lebih spesifik ke versi python yang kita inginkan dengan menggunakan command **virtualenv -p python3 env**
   - **source env/bin/activate** = Linux/MAc OS
   - **env\Script\activate** = windows
4. Install django terbaru **pip install django** (file dependensi sengaja tidak diexport karena saat ini dependensi hanya django saja)
5. Migrate database
   - Silahkan menuju ke file **manage.py** dengan command **cd administrasi**
   - Jalankan perintah inisialisasi database dengan command **python manage.py migrate**
6. Buat user baru **python manage.py createsuperuser**
7. Jalankan server/program **python manage.py runserver**
8. Terimakasih
