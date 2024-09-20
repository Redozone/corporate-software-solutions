#define BOOST_LOG_DYN_LINK 1

#include <QApplication>
#include <QHttpServer>
#include <QDataStream>
#include <QDateTime>
#include <QTimer>
#include <QTranslator>
#include <QLibraryInfo>
#include <QMetaObject>

#include <stdexcept>
#include <iostream>
#include <functional>
#include <list>

#include "inquirer.h"
#include "pgbackend.h"
#include "../logger/logger_boost_qtwrap.h"
#include "simplecrypt.h"
#include "processhandler.h"
#include "stylist.h"
#include "master.h"
#include "pgbackend_api.h"
#include "shared/constants.h"
#include "multithread_api.h"
#include "configmanager.h"

#define MAIN_TIMER_INTERVAL 1000
#define FAILS_LOG "fails"
#define HTTPSERVER_LOG "http_server"

void checkDatabaseFull(std::shared_ptr<PgBackend> pgbackend, std::shared_ptr<MisterThread<int> > msThread,
                       std::map<std::string, std::string> connectionSettings,
                       QString path, std::string query)
{
    ProcessHandler* processHandler = new ProcessHandler(msThread );
    QStringList params;
    params << QString::fromStdString(connectionSettings["ip"])
            << QString::fromStdString(connectionSettings["port"])
            << QString::fromStdString(connectionSettings["dbName"])
            << path
            << QString::fromStdString(connectionSettings["dbName"]);

    pgbackend->makeRequest(connectionSettings["dbName"], query,
            [=](std::string, std::list<std::string> data )->int{
        int pointer = 0;
        foreach (std::string line, data) {
            QString rawData = QString::fromStdString(line);
            pointer = pointer + rawData.toInt();
        }
        if (pointer == 0)
        {
            logit("Обнаружена нехватка данных в базе данных " + params[2] + ".", QString("process_out") );
            processHandler->addProcess(path+"/recovery_data_iao.sh", params, [=](int ec, QString){
                logit("Попытка произвести запись в схему iao.", "process_out" );
                if (ec == 0) {
                    logit("Записи произведены в базу " + params[2] + ".", "process_out" );
                }
                else {
                    logit("Запись в базу " + params[2] + " провалена.", "process_out" );
                }
            });
        }
        else {logit("База " + params[2] + " уже заполнена.", "process_out" );}
        return 0;
    });
    processHandler->deleteLater();
}

QList<QVariantMap> configurePgBackend(SimpleCrypt &processSimpleCrypt)
{
    QList<QVariantMap> notifications;

    const auto &databases = configManager()->getDatabases();

    for (const QVariant &connectOption : databases) {
        const QVariantMap option = connectOption.toMap();
        std::map<std::string, std::string> connectionSettings;
        for (auto it = option.begin(), end = option.end(); it != end; ++it) {
            connectionSettings[it.key().toStdString()] = it.value().toString().toStdString();
        }
        connectionSettings["password"] = processSimpleCrypt.decryptToString(option.value("password").toString()).toStdString(); // decoding password
        pgbackend()->createPool(connectionSettings);

        checkDatabaseFull(pgbackend(), misterThread(), connectionSettings, QDir::homePath() + "/." + QFileInfo(QCoreApplication::applicationFilePath()).fileName() + "/recovery",
                          JsonAgent::read(QDir::homePath() + "/." + QFileInfo(QCoreApplication::applicationFilePath()).fileName()+"/sql.json").
                          value(QString("check_data_") + QString::fromStdString(connectionSettings["dbName"])).toMap().
                value("SQLRequest").toString().toStdString());

        // Start listening notifications. First - get from DB, second - start listen (in callback)

        if (QString::fromStdString(connectionSettings["notifications"]) == "true")
        {
            auto notificationRequest = JsonAgent::read(QDir::homePath()
                                                       + "/." + QFileInfo(QCoreApplication::applicationFilePath()).fileName()+"/sql.json")
                    .value("get_notification_list").toMap();

            QList<QString> resultKeys;
            const auto resultValueList = notificationRequest.value("ResultValue").toList();
            for (const QVariant &resultValue : resultValueList)
                resultKeys.append(resultValue.toString());

            QString request = "SQLRequest_" + QString::fromUtf8(connectionSettings["dbName"].c_str());

            pgbackend()->makeRequest(connectionSettings["dbName"],
                    notificationRequest.value(request).toString().toStdString(),
                    [&]( std::string, std::list<std::string> data )->int{

                data.push_back("get_columns"); // Хардкод для reportWidget для обхода notify filter
                data.push_back("get_tables"); // Хардкод для reportWidget для обхода notify filter
                data.push_back("get_obj_objekt_vvt"); // Хардкод для reportWidget для обхода notify filter
                data.push_back("get_kka_kat_ts_ka"); // Хардкод для reportWidget для обхода notify filter
                data.push_back("get_bgs_bg_sredstva"); // Хардкод для reportWidget для обхода notify filter
                data.push_back("get_sost_ba_ka"); // Хардкод для reportWidget для обхода notify filter

                QList<QVariantMap> response;
                QString stringSeparator = pgbackend()->separator().c_str();
                for (const std::string &result : data) {
                    QVariantMap map;
                    int i = 0;
                    QString resultString = QString::fromStdString(result);
                    if (resultString.at(resultString.size()- stringSeparator.size()) == stringSeparator) {
                        resultString.chop(stringSeparator.size());
                    }

                    auto const list = resultString.split(stringSeparator);
                    for (const QString &value : list) {
                        map[resultKeys[i]] = QVariant(value);
                        ++i;
                    }
                    response.append(map);
                }

                std::list<std::string> notifyList;
                for (auto map : response) {
                    std::string notify = map.value("trigger_name").toString().toStdString();
                    notifyList.push_back(notify);
                    notifyList.push_back(notify + "_delete");

                    // add the same notification with postfix '_delete'
                    notifications.append(map);
                    map["trigger_name"] = QVariant::fromValue(map.value("trigger_name").toString() + "_delete");

                    notifications.append(map);
                }

                logit((QString("Get notification list : \n ")) +
                      QString::fromStdString(std::accumulate(notifyList.begin(), notifyList.end(), std::string{},
                                                             [](std::string &ss, std::string &s) { return ss.empty() ? s : ss + "," + s; }) ),
                        "pgBackend" );
                pgbackend()->startListen(connectionSettings["dbName"], notifyList);
                return 0;
            }, [&]( std::string tag, std::string data )->int{

                logit("Linten notification fail because cant make request for reading notification list from database, \n message from backend: "
                      + QString::fromStdString(data) + "   "+QString::fromStdString(tag),
                      "pgBackend");
                return 0;
            }, PgBackend::RequestType::Sync, "pgBackend" );
        }
    }

    // add primary keys to empty notifications

    return notifications;
}

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    QApplication::setAttribute(Qt::AA_ForceRasterWidgets, false);
    qApp->setStyleSheet(Stylist::getInstance().getStyle());

    QString locale = QLocale::system().name();

    QTranslator *qtTranslator = new QTranslator(qApp);
    qtTranslator->load("qt_" + locale, QLibraryInfo::location(QLibraryInfo::TranslationsPath));
    qApp->installTranslator(qtTranslator);

    a.setOrganizationName("ssmit");
    a.setOrganizationDomain("ssmit");
    a.setApplicationName("ssmit");

    qRegisterMetaType<QList<QVariantMap>>();

    QString loggerPath = QDir::homePath() + "/." + QFileInfo(QCoreApplication::applicationFilePath()).fileName() + "/log/";
    if (!QDir(loggerPath).exists())
        QDir().mkdir(loggerPath);

    QVariantMap log_map = JsonAgent::read(QDir::homePath() + "/." + QFileInfo(QCoreApplication::applicationFilePath()).fileName()+"/conf_log.json");

    setup_logger(loggerPath, log_map);

    long long cryptCode = JsonAgent::read(QDir::homePath() + "/." + QFileInfo(QCoreApplication::applicationFilePath()).fileName()+"/data.json").value("cryptCode").toLongLong();
    SimpleCrypt processSimpleCrypt(cryptCode);

    qmlRegisterSingletonType<Stylist>("stylist",1,0,"Stylist",stylistQMLProvider);

    pgbackend()->logit = [&](std::string mes, std::string tag, int) {
        //there is may be convertion from pgbackend.log() to logger.log()
        logit(QString::fromStdString(mes), QString::fromStdString(tag));
    };

//    example:
//    notifications.append(QVariantMap({ {"trigger_name", "get_telemetry"},
//                                       {"time_triggers_keys", "start, end"},
//                                       {"primary_keys", "payload"}
//                                     }));

    std::shared_ptr<QTimer> mainTimer = std::make_shared<QTimer>();
    Inquirer inquirer;
    Master master(mainTimer);

    QObject::connect(&inquirer,  &Inquirer::sendNotificationData,
                     &master, &Master::resolveNotification);

    QObject::connect(&master, &Master::sendNotification,
                     &inquirer, &Inquirer::makeRequest);

    master.runWidgets();

    misterThread()->create_service_thread([&]() -> int {
        auto notifications = configurePgBackend(processSimpleCrypt);
        master.setNotifications(notifications);
        //NOTE: функция ниже на самом деле сигнал, который вызывает makePipeline.
        //если вызывать напрямую, то обработчики нотификаций почемуто не пеерсылают данные из БД на
        //виджеты.
        master.ready();
        return 0;
    });

    mainTimer->start(MAIN_TIMER_INTERVAL);

    QHttpServer httpServer;
    httpServer.route("/", QHttpServerRequest::Method::POST, [&inquirer](const QHttpServerRequest &req) {

        auto track = QJsonDocument::fromJson(req.body()).toVariant().toList();

        QList<QMap<QString,QVariant>> outTrack;

        for (auto &t : track) {
            outTrack.append(qvariant_cast<QMap<QString,QVariant>>(t));
        }

        emit inquirer.sendNotificationData("tracks_for_satellites", QVariant::fromValue(outTrack));

        return QHttpServerResponder::StatusCode::Ok;
    });

    const QString httpIp = configManager()->getProperty("http_server", "ip");
    QHostAddress httpAddress;
    if (httpIp == "ip4"){
        httpAddress = QHostAddress::AnyIPv4;
    } else if (httpIp == "*") {
        httpAddress = QHostAddress::Any;
    } else {
        httpAddress = QHostAddress(httpIp);
    }

    const QString port = configManager()->getProperty("http_server", "port");
    qint16 httpPort = !port.isEmpty() ? port.toInt() : DEFAULT_HTTP_SERVER_PORT;

    const auto listenPort = httpServer.listen(httpAddress, httpPort);
    if (!listenPort) {
        logit("HttpServer failed to listen on a port.", FAILS_LOG);
    }
    logit(QString("Running http server on http://%1:%2")
          .arg(httpAddress.toString(), QString::number(listenPort)), HTTPSERVER_LOG);


    return a.exec();
}
