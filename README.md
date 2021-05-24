# ProtocolInetTask

# 1) PortScan
* прикрепил различные скриншоты, в которых демонстрируется, что все 6 требуемых протоколов распознаются
- выводит список открытых TCP портов (используется soccet.connect() - если успех = порт открыт)
- список открытых UDP портов (используется soccet.recvfrom и sendto, посколько UDP не гарантирует доставку)
- многопоточность присутствует (время работы заметно ускорено, import threading)
- распознавание всех 6-ти прикладных протоколов (NTP/DNS/SMTP/POP3/IMAP/HTTP)
 # ЗАПУСК 
  python3 index.py <*имя хоста*> <*опционально*> 
  - -t - сканировать tcp, 
  - -u - сканировать udp, 
  - -p - выбор диапазона портов

- *на скриншотах видны примеры запуска
 
P.S. для проверки корректности поиска использовал тулзу nMap (на некоторых скриншотах видно)


# 2) HTTP-Api

Прикрепляю скрипт, решающий первый (1) таск в задаче http-api (фото в макс. разрешении из выбранного альбома ВК)
+ скриншоты работы программы (авторизация, как и требовалось, через OAuth)

 # ЗАПУСК 
  python3 main.py
  + далее всё в интерактивном режиме спрашивает скрипт
  + прочтите справку для корректной работы со скриптом: python3 main.py -h