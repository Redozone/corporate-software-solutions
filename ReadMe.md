## Как создать из папки iso образ
   
Для того, чтобы создать из папки с файлами образ iso, необходимо выполнить следующую команду:
```bash
$ mkisofs -o /path/where/save/your/iso/<iso_name>.iso /path/to/folder/to/iso/<folder>

или

mkisofs -r -V 'db_disk' -o db_disk.iso -m '.git' -r ./db_disk

Пример:
# mkisofs -o /home/diffraction/NIR_integration/disk/docker_denis.iso /home/diffraction/NIR_integration/disk/docker
```

## Записываем образ для правильного получения контрольной суммы через wodim

```bash
root@localhost:~# wodim dev=/dev/sr0 -eject -v /home/diffraction/bibly/ssmit156.last.crtf.lbl.iso - записали
$ md5sum /dev/cdrom - получили контрольную сумму
```

## Как посчитать контрольную сумму
        
проверим, есть ли диск по /dev/sr0
```bash
$ lsblk
```

посмотреть данные logical block size и volume size чтобы рассчитать контрольную сумму диска вставленного в дисковвод (отмонтировать диск надо)
```bash
$ umount /dev/sr0
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

посмотреть контрольную сумму диска (строка со звездочкой)(отмонтировать диск надо)
```bash
$ dd bs=<logical block size> count=<volume size> if=/dev/sr0 conv=notrunc,noerror | md5sum -b
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

Полный цикл получения файла с архивом 9 уровня: 
```bash
$ docker pull 192.168.34.13:5000/stac_start:1.0.5
$ docker image ls
$ docker image save -o stac_start.tar 192.168.34.13:5000/stac_start:1.0.5
$ gzip -9 stac_start.tar
$ du -hs stac_start.tar.*
```

Рабогтаем с диском
eject /dev/sr0 -T
