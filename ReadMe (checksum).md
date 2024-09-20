## Как создать из папки iso образ
   
Для того, чтобы создать из папки с файлами образ iso, необходимо выполнить следующую команду:
```bash
$ mkisofs -o /path/where/save/your/iso/<iso_name>.iso /path/to/folder/to/iso/<folder>

Пример:
# mkisofs -o /home/diffraction/NIR_integration/disk/docker_denis.iso /home/diffraction/NIR_integration/disk/docker
```

## Как посчитать контрольную сумму
        
проверим, есть ли диск по /dev/sr0
```bash
$ lsblk
```

посмотреть данные logical block size и volume size чтобы рассчитать контрольную сумму диска вставленного в дисковвод (отмонтировать диск не надо)
```bash
$ isoinfo dev=/dev/sr0 -d
```

посмотреть данные logical block size  и volume size чтобы рассчитать контрольную сумму образа
```bash
$ isoinfo -d -i <iso_name>.iso
```

посмотреть контрольную сумму образа <iso_name>.iso (строка со звездочкой)
```bash
$ dd bs=<logical block size> count=<volume size> if=/path/where/save/your/iso/<iso_name>.iso | md5sum -b
```

посмотреть контрольную сумму диска (строка со звездочкой)
```bash
$ dd dev=/dev/sr0 bs=<logical block size> count=<volume size> conv=notrunc,noerror | md5sum -b
```



## Тарим с максимальным сжатием

Выполним такую команду:
```bash
$ tar cvf - /path/to/folder/for/tar | gzip -9 -> /name/file/with/path/.tar.gz
```

Чтобы потом запустить (laod) такой докер, надо выполнить немного другую команду:
```bash
$ cat $PWD/stac_docker.tar.gz | docker import - <your_docker_image_name> (в инструкции тогда это <your_docker_image_name> должно совпадать с командой запуска)
```

