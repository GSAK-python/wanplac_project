[33mb13de06[m[33m ([m[1;36mHEAD[m[33m, [m[1;32mmaster[m[33m)[m Dodanie whitenoise non static do installed apps
[33m8ab2154[m Poprawienie gitignore
[33md2672fd[m[33m ([m[1;31morigin/master[m[33m, [m[1;31mheroku/master[m[33m)[m Dodanie celery i celery ebat do Procfile
[33m09d87e1[m Usuniecie migracji i zrobienie ich ponownie
[33m393167f[m Bez migracji
[33m2d7592e[m APP1 - ponowne dodanie email (POSGRE)
[33m8176565[m Dodanie WhiteNoise
[33m55e1228[m Zmiana na STATICFILES_DIRS
[33m7d138aa[m Zmiana w ALLOWED_HOSTS
[33mdafed93[m Zmiana w Procfile
[33m140e01b[m Ponowne usuniecie migracji ale w models jest exact_time
[33ma3f96db[m Dodanie exact_time
[33mf9d1f38[m DB modify
[33m2bcbd5e[m Wyczyszenie migracji po za init.py
[33m3eaca19[m Usuniecie daty z app1.DateList
[33m8a1fc52[m Usuniecie wszystkich migracji
[33m15fda89[m Poprawana kolejnosci migracji
[33mce53e55[m Poprawna kolejnosci migracji
[33m3bf9768[m Poprawa kolejnosci w migracjach
[33m704025a[m Usuniecie migracji z exact_time
[33mb264c47[m Usuniecie exact_time z calego projektu
[33m2465d0c[m USE_TZ=True
[33mfde01f3[m Settings static
[33m5adb721[m Settings ciag dalszy
[33mf3da49a[m Zmiana w STATIC_ROOT oraz STATICFILES_DIR
[33m4c284be[m Dodanie blank=True, null=True do kazdego pola z auto_now_add
[33m042eabd[m Zmiana USE_TZ na False
[33m15e2c29[m dodanie requiremetns.txt
[33m65fb005[m usuniecie requiremetns.txt
[33mbeb40d4[m test test.txt
[33mdd78766[m Zamiana procfile
[33m2184042[m Heroku zmiana procfile
[33m0d72bc0[m Upgrade python do 3.8.2
[33me92ec23[m Pliki do heroku - ponowna proba
[33md1147e0[m Merge branch 'master' of https://github.com/GSAK-python/wanplac_project
[33m5773e59[m Nowy Procfile
[33m4d4829f[m[33m ([m[1;31mheroku/masterbranch[m[33m)[m Nowy plik procfile
[33m68b1cc0[m Requiremetns.txt
[33m400e692[m[33m ([m[1;32mmsater[m[33m)[m Update requiremets.txt
[33ma45b1b8[m[33m ([m[1;32morigin[m[33m)[m Zmiana w requiremetns.txt
[33m4460fa8[m Zmiana pliku requirements-dev.txt
[33mfec1f81[m Zmiana w requirements-dev.txt
[33md43355c[m Zmiana pliku procfile
[33m38ad037[m Zmiania ustawien do static w settings
[33m65b5d5b[m Zmiana pliku runtime.txt
[33m05f9910[m Dodanie plikow HEROKU oraz wstepny navbar
[33m2803ec2[m Dodanie stylu COLLAPSE w ListView Twoje Zamowienia
[33m9749d2a[m Historia rezerwacji, filtr wg booking_id oraz exact_time co do sekundy
[33m356066e[m Dodanie listy z historia zamowien plus dodatkowy kod (wczesniejszy proby z ListView w template oraz main_page.view). W nastepnym commitcie bedzie to wyczyszczone
[33m5397830[m Dodanie wszystkich nowych funckjonalnosci z APP1 do CP i APP2
[33m31218b2[m Dodanie pola z numerem telefonu do APP1
[33mbbb790d[m Dodanie dyanmicznych formsetow do wszystkich aplikacji oraz dodanie dodatkowych ValidationError do formularza
[33md299b84[m APP1 - optymalizacja dodawania i usuwania dodatkowyh kajakow. Jeszcze jeden blad do naprawy
[33m3c2d3b7[m APP1 - dodanie danyamicznych formsetow dodowania kajakow oraz ich usuwania
[33m31b7ece[m Dodano zabezpieczenie przed wprowadzeniem wiekszej ilosci kajakow niz jest dostpenych
[33ma784ba4[m Dodana przerwa technincza na kazdy dzien od 12 do 12.30
[33m5f98d42[m Dodanie pliku JS do odswiezania strona o konkretnych godzinach
[33md748e73[m Trzy aplikacje - poprawienie booking_change_date() w APP2
[33m739cd1a[m Trzy aplikacje - poprawka do return_kayak_store() w kazdej apce
[33mb16c789[m Trzy aplikacje - jedna na kazdy z trzech dni - DZIALA
[33m0aca80d[m Od tego commita wprowadzam trzecia appke - APP1
[33m22bff12[m Upade APP2 do stanu CLIENT_PANEL, poprawana funckji booking_dates_limit()
[33mf370a07[m Automatyczna zmiana daty dziala!!!
[33m7f1e7ec[m Dodano nowy model z DateField, DateList jest to kontroli strony z odnosnikami to formularzy, drugi do kontroli rezerwacji dat
[33m2e40977[m pole date jako one2one field
[33m1ca9c62[m Proby uzyskania daty formularza takiej samej jak data wyboru dnia
[33m9f8c6b3[m change_date() oraz return_kayak_store() w CP i APP2 dzialaja jak nalezy, popraawne zmienianie dat w main_page
[33mcb0886d[m Poprawne działanie change_date i return_kayak_store w CP i APP2 - CELERY BEAT
[33maf15e85[m Poprawienie funkcji get_current_data
[33m25dab1e[m Testowanie funkcji change_date i return_kayak_store w apce client_panel
[33maf2a91c[m Ustawienie Celery Beat, sprawdzanie dzialanie funckcji periodic task na baze danych (db_test_func).
[33mb97db17[m Dodanie funkcji sprawdzania statusu kajakow w tasks.py (shared_task). Ustawienie Celery pod Win10
[33m4a25bed[m Data w formularzach zmienia sie w zaleznosci od aktualnego dnia, stworzenie funkcji i wrzucenie jej do atrubutu deafult
[33m7119369[m Trzy apki - strona startowa ma odnosniki do odpowiedniego formularza w zaleznosci od dzisiejszej daty
[33ma8d1d13[m Trzy apki - client_panel - pole data jest tylko informacyjne, zmiana schematu na jeden formset
[33m27729cc[m Dodanie trzeciej apki, dwie takie same i na nich bede dalej pracowac jako dwie rozne daty
[33m9b67c21[m Dwie apki - logowanie dziala, nie wlaczylem RABBITA
[33m2123f06[m Dwie apki - dodanie strony startowej ktora ma odnosiniki do apek
[33mb3ea4bc[m Dwie apki
[33m797248a[m Jenda apka, dwa formsety, kombinowanie z nowym modelem
[33m41a2d69[m Od tego commita zaczynam robic wersje z wieloma apkami oraz formularzami
[33m586d5f1[m Dodanie nowego modelu Term
[33mb7f3d6a[m Celery ciag dalszy
[33m77c214d[m Dodanie celery
[33meac159a[m Stworzenie szablonu bazowego. Dodanie mozliwosci dodadnia nowego wiersza w formularzu rezerwacji. Modyfikacja BookingCreateView
[33m21535bf[m Formularz rezerwacji zostaje zapisany
[33mc8bebe9[m Dodanie error_message do formularzy w foderze registration
[33md6a8858[m Dodanie formularza rejestracji
[33mbcfdbf9[m Utowrzenie systemu do resetowania hasla. Testowanie systemu poprzez EmailBackend(setting)
[33m8cdd239[m Dodanie widokow resetowania hasla
[33m1b61f7d[m Dodanie ekranu logowania
[33m836dc94[m Dodanie strony login
[33m7f73e13[m "Dodanie pliku .gitignore"
[33mc67c120[m 001 - dodanie modeli, wstepny formularz rezerwacji
