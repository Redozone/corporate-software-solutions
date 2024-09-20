#!/bin/bash
#export PGPASSWORD=qwerty    password

conf_path=$1
release="$(lsb_release -r)"
echo $release
if [[ $release != *"1.6"* ]]; then
    echo "Wrong operation system"
    exit 0
fi
system_pass=$PGPASSWORD
#exec xterm
if [ "${system_pass}"x == "x" ]; then
    echo "Empty PGPASSWORD"
    exit 0
fi
#echo $system_pass

OUTPUT=""
flag=0

while [ $flag -lt 1 ]
do
  OUTPUT="$(/usr/bin/SimpleDimpl -e 88005553535 $system_pass)"
  if [[ $OUTPUT != *"/"* ]]; then
    flag=2
  fi
done

change_row(){
  config=$1
  find_source=$2
  pass=$3
  old_string=""
  new_string=""
  while IFS= read -r line;
  do
    if [[ $line == *"$find_source"* ]]; then
        old_string=$line
        new_string="$find_source\"$pass\""
    fi
  done < ${conf_path}

  stick="\\\\\\"
  old_stick="${old_string/\\/"$stick"}"
  new_stick="${new_string/\\/"$stick"}"
  
  if [[ $config == *".json"* ]]; then
    sed -i "s/${old_string}/            ${new_string},/g" ${config}
  else
    sed -i 's/'$old_stick'/'$new_stick'/g' ${config}
  fi
}

change_row $conf_path "comm_c\password=" $OUTPUT
change_row $conf_path "bmaz\password=" $OUTPUT
change_row $conf_path "\"password\": " $OUTPUT

