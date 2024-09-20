#-------------------------------------------------
#
# Project created by QtCreator 2018-01-26T11:34:31
#
#-------------------------------------------------

QT += core gui xml sql network quickwidgets qml quick charts httpserver location printsupport

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = ssmit-156

#QMAKE_EXTRA_TARGETS += copy_configs
#PRE_TARGETDEPS += copy_configs
#copy_configs.commands = mkdir -p ~/.$$TARGET/ && touch ~/.$$TARGET/config.probuf && mkdir -p ~/.$$TARGET/log/ && mv ~/.$$TARGET/config.probuf ~/.$$TARGET/log/ &&rm -f ~/.$$TARGET/*.* && mv ~/.$$TARGET/log/config.probuf ~/.$$TARGET/ && cp -s $$PWD/source/configs/* ~/.$$TARGET/
#copy_configs.CONFIG = phony

VERSION = 1.0.0
DEFINES += APP_VERSION=\\\"$$VERSION\\\"

TEMPLATE = app
CONFIG += c++20 qml_debug qtquickcompiler

LIBS += -lprotobuf-lite -lboost_system -lballistics -lboost_thread -lboost_chrono -lboost_locale -lpq -lX11 -lboost_log -lboost_log_setup -lboost_filesystem
LIBS += -lstdc++

INCLUDEPATH += ./protobuf \
    ./functional \
    ./gui \
    ./gui/tcuWidget \
    ./analytics \
    ./database \
    ./gui/configCreator \
    ./functional/iao_sost \
    ./gui/satelliteScheme \
    ./gui/groundcontrolscheme \
    ./gui/maininterface \
    ./gui/noticeWidget \
    ./gui/radialBar \
    ./functional/configManager \
    ./reportPrinter \
    ./gui/groundSpecialComplex \
    ./gui/reportPrinter \
    ./gui/estimationTehCon \
    ../../logger \
    ../../configmanager \
    ../../pgbackend/src \
    ../../simplecrypt/contrib/include

SOURCES += main.cpp \
    ../../simplecrypt/contrib/src/simplecrypt.cpp \
    database/inquirer.cpp \
    functional/iao_sost/statusaccount.cpp \
    functional/iao_sost/treeitem.cpp \
    functional/iao_sost/treemodel.cpp \
    functional/processhandler.cpp \
    functional/master.cpp \
    functional/mccmonitor.cpp \
    functional/notifyworker.cpp \
    gui/configCreator/configselector.cpp \
    gui/configCreator/dragwidget.cpp \
    gui/configCreator/dropwidget.cpp \
    gui/configCreator/interfaceconfigurator.cpp \
    gui/configCreator/nodekeeper.cpp \
    gui/configCreator/previewwidget.cpp \
    gui/configCreator/serializerconstructor.cpp \
    gui/estimationTehCon/estimationmodel.cpp \
    gui/estimationTehCon/estimationwidget.cpp \
    gui/groundSpecialComplex/groundspecialcomplex.cpp \
    gui/groundSpecialComplex/listmapmodel.inl \
    gui/noticeWidget/noticemodel.cpp \
    gui/reportPrinter/reportprinter.cpp \
    gui/groundSpecialComplex/trackmodel.cpp \
    gui/groundSpecialComplex/unitmodel.cpp \
    gui/maininterface/maininterface.cpp \
    gui/noticeWidget/noticewidget.cpp \
    gui/reportPrinter/reportwaitindicator.cpp \
    gui/reportWidget/historymodel.cpp \
    gui/reportWidget/proxymodel.cpp \
    gui/reportWidget/reportmodel.cpp \
    gui/reportWidget/reportwidget.cpp \
    gui/satelliteScheme/satellitescheme.cpp \
    gui/satelliteScheme/satellitesmodel.cpp \
    gui/screenconfig/screenconfig.cpp \
    gui/ssmitmessage.cpp \
    gui/statisticCharts/callout.cpp \
    gui/statisticCharts/chart.cpp \
    gui/statisticCharts/statisticcharts.cpp \
    gui/statisticCharts/view.cpp \
    gui/tcuWidget/tcuwidget.cpp \
    gui/controlbutton.cpp \
    gui/tabdialog.cpp \
    gui/testwidget.cpp \
    gui/transparentwindow.cpp \
    ../../configmanager/configmanager.cpp \
    ../../configmanager/jsonagent.cpp \
    ../../pgbackend/src/pgbackend.cpp \
    gui/tcuWidget/seancetreemodel.cpp \
    gui/tcuWidget/seancenode.cpp \
    protobuf/configuration.pb.cc \
    gui/noticeWidget/proxyModel.cpp \
    gui/radialBar/radialbar.cpp \
    functional/datahandler.cpp \
    functional/convertor.cpp \
    functional/handler_satellitesstates.cpp

HEADERS  += \
    ../../logger/logger_boost.h \
    ../../logger/logger_boost_qtwrap.h \
    ../../pgbackend/src/misterthread.h \
    ../../simplecrypt/contrib/include/simplecrypt.h \
    database/inquirer.h \
    functional/iao_sost/iaoconnectionoptions.h \
    functional/iao_sost/statusaccount.h \
    functional/iao_sost/treeitem.h \
    functional/iao_sost/treemodel.h \
    functional/multithread_api.h \
    functional/pipeline.h \
    gui/estimationTehCon/estimationmodel.h \
    gui/estimationTehCon/estimationwidget.h \
    gui/groundSpecialComplex/groundspecialcomplex.h \
    gui/groundSpecialComplex/listmapmodel.h \
    gui/noticeWidget/noticemodel.h \
    gui/reportPrinter/reportprinter.h \
    gui/groundSpecialComplex/trackmodel.h \
    gui/groundSpecialComplex/unitmodel.h \
    gui/reportPrinter/reportwaitindicator.h \
    gui/reportWidget/historymodel.h \
    gui/reportWidget/proxymodel.h \
    gui/reportWidget/reportmodel.h \
    gui/reportWidget/reportwidget.h \
    gui/satelliteScheme/satellitesmodel.h \
    gui/ssmitmessage.h \
    gui/statisticCharts/callout.h \
    gui/statisticCharts/chart.h \
    gui/statisticCharts/statisticcharts.h \
    gui/statisticCharts/view.h \
    gui/statisticCharts/wrapper.h \
    gui/tcuWidget/seancenode.h \
    gui/tcuWidget/seancetreemodel.h \
    functional/binarytree.h \
    functional/functions.h \
    functional/master.h \
    functional/mccmonitor.h \
    functional/notifyworker.h \
    functional/processhandler.h \
    functional/stylist.h \
    functional/widgetinterfaces.h \
    gui/configCreator/configselector.h \
    gui/configCreator/dragwidget.h \
    gui/configCreator/dropwidget.h \
    gui/configCreator/interfaceconfigurator.h \
    gui/configCreator/nodekeeper.h \
    gui/configCreator/previewwidget.h \
    gui/configCreator/serializerconstructor.h \
    gui/maininterface/maininterface.h \
    gui/noticeWidget/noticewidget.h \
    gui/satelliteScheme/satellitescheme.h \
    gui/screenconfig/screenconfig.h \
    gui/tcuWidget/tcuwidget.h \
    gui/controlbutton.h \
    gui/tabdialog.h \
    gui/testwidget.h \
    gui/transparentwindow.h \
    ../../configmanager/configmanager.h \
    ../../configmanager/jsonagent.h \
    ../../pgbackend/src/pgbackend.h \
    protobuf/configuration.pb.h \
    gui/noticeWidget/proxyModel.h \
    gui/radialBar/radialbar.h \
    functional/cacheprovider.h \
    functional/convertor.h \
    functional/datahandler.h \
    functional/handler_satellitesstates.h \
    functional/handler_ballistic.h \
    functional/handlers.h \
    functional/pgbackend_api.h \
    shared/constants.h

FORMS    += gui/maininterface/maininterface.ui \
    gui/configCreator/configselector.ui \
    gui/configCreator/interfaceconfigurator.ui \
    gui/screenconfig/screenconfig.ui \

DISTFILES += \
    gui/groundSpecialComplex/doc/images/itemview_transitions.jpg \
    protobuf/configuration.proto \
    source/configs/settings.config

RESOURCES += \
    qml.qrc \
    resource.qrc
