#include <QCoreApplication>
#include <simplecrypt.h>
#include <QDebug>
#include <iostream>
using namespace std;

int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);
    if (argc != 4)
    {
        qDebug() << "Неверное количество аргуменотов!";
        qDebug() << "Пример запуска расшифровки ./SimpleDimpl -d 88005553535 your_word";
        qDebug() << "Пример запуска зашифровки ./SimpleDimpl -e 88005553535 your_word";
        exit(0);
    }

    long long cryptCode = QString::fromLatin1(argv[2]).toLongLong();
    SimpleCrypt processSimpleCrypt(cryptCode);

    QString userRow = QString::fromLatin1(argv[3]);
    QString resultRow = "";

    if (QString::fromLatin1(argv[1]) == "-d")
    {
        resultRow =  processSimpleCrypt.decryptToString(userRow); //"Расшифрованная строка:     " + processSimpleCrypt.decryptToString(userRow);
    }

    if (QString::fromLatin1(argv[1]) == "-e")
    {
        resultRow = processSimpleCrypt.encryptToString(userRow); //"Зашифрованная строка:     " + processSimpleCrypt.encryptToString(userRow);
    }

    cout << resultRow.toStdString();

    return 0;
}
