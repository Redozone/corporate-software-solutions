#!/bin/bash

### объявить функцию запуска с пропуском
declare -f skip_runme
function skip_runme()
{
    [ -x "${1}" ] \
	&& runme $@ "${SKIP_KEY}"
}

### объявить функцию запуска
declare -f runme
function runme()
{   
    [ -x "${1}" ] \
    && $@
}

### объявить функцию запуска с параметром
declare -f cndtnl_execme
function cndtnl_execme()
{
    [ "${SKIP_FLAG}" = "${SKIP_KEY}" ] \
        && return 0
    [ -x "${1}" ] \
	&& execme $@
}

### объявить функцию запуска c замещением
declare -f execme
function execme()
{
    [ -x "${1}" ] \
	&& exec $@
}

### дописать contributed директорию к списку поиска библиотек
declare -x LD_LIBRARY_PATH=/usr/share/ssmit-156/contrib:${LD_LIBRARY_PATH}

### переключить версию Qt
declare -rx QT_SELECT=Qt5.15.2

### приписать бинари парсека к пути их поиска
declare -x PATH=/usr/lib/parsec/bin:$PATH

### предварительный бинарь
declare -r PREBIN="/usr/bin/password_setter.sh"

### окончательный бинарь
declare -r EXEBIN="/usr/bin/ssmit-156"

### путь до папки с конфигом кассы
declare -r CASA_HOME="/usr/share/casa-svc/.casa-service"

### определить директории для копирования конфигурации
declare -r USERCFGDIR="$(getent passwd $( /usr/bin/id -u ) | cut -d: -f6)/.ssmit-156"
declare -r TMPLCFGDIR="/usr/share/ssmit-156/configs"

### параметры работы скрипта
declare -a POSITIONAL_ARGS
declare    SKIP_FLAG="--no-skip"
declare -r SKIP_KEY="--skip"

### List of config files
declare -ra CFGLIST=( \
                      'groundSCColors.json' \
		      'conf_log.json' \
		      'data.json' \
		      'sql.json' \
		      'database.config' \
		      'settings.config' \
		      'refresh.sh' \
		      'xrandr.sh' \
		      'config.probuf' \
		      'chartConfig.json' \
		    )

### список wrappers
declare -ra WRPLIST=( '/usr/bin/ssmit-training-156.sh' \
		      '/usr/bin/trackwriter_service.sh' \
		    )
		    
### List of dirs to create
declare -ra DIRLIST=( 'log' 'recovery' 'cache_here_map' )

### List of dirs to copy
declare -ra DIRCPLIST=( 'recovery' 'cache_here_map' )

### Парсер аргументов командной строки
while [ $# -gt 0 ]; do
  case $1 in
    "${SKIP_KEY}")
      SKIP_FLAG="${SKIP_KEY}"
      shift
      ;;
    *)
      POSITIONAL_ARGS+=("$1")      
      shift
      ;;
  esac
done
set -- "${POSITIONAL_ARGS[@]}"

### создать недостающие директории
for THEDIR in "${DIRLIST[@]}"
do
    [ -d "${USERCFGDIR}/${THEDIR}" ] \
	|| mkdir -p "${USERCFGDIR}/${THEDIR}"
done

### скопировать директории с содержимым согласно списка
for THEDIR in "${DIRCPLIST[@]}"
do
    [ -z "$(find "${USERCFGDIR}/${THEDIR}" -empty -prune)" ] \
        || cp "${TMPLCFGDIR}/${THEDIR}/"* "${USERCFGDIR}/${THEDIR}/"
done

### скопировать конфиги согласно списка
for THECFG in "${CFGLIST[@]}"
do
    [ -f "${USERCFGDIR}/${THECFG}" ] \
	|| cp "${TMPLCFGDIR}/${THECFG}" "${USERCFGDIR}/"
done

### установка текущего пароля доступа
runme "${PREBIN}" "${USERCFGDIR}/settings.config"

### установка пароля для casa-service
runme "${PREBIN}" "${CASA_HOME}/settings.config"

### запустить wrappers согласно списка
for WRAPPER in "${WRPLIST[@]}"
do
    skip_runme "${WRAPPER}"
done

#### запустить приложение
cndtnl_execme "${EXEBIN}" $@
