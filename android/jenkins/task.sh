#!/bin/bash

if ! ${jiagu}
then
    exit 0
fi

typeset -l flavor
flavor=${FLAVOR}
typeset -l buildType
buildType=${BUILD_TYPE}

BUILD_PATH=./app/build
APK_PATH=${BUILD_PATH}/outputs/apk/${flavor}/${buildType} #需要加固的apk路径

BASE=/DevelopTools/360jiagu/jiagu.jar
NAME=513082359@qq.com
PASSWORD=yu8410550
KEY_PATH=./keystore/mkseller.jks #密钥路径
KEY_PASSWORD=hzmk12345678 #密钥密码
ALIAS=mkseller #别名
ALIAS_PASSWORD=hzmk12345678 #别名密码
JIAGU_PATH=${BUILD_PATH}/jiagu  #输出加固包路径


IFS=$(echo -en "\n\b")
echo -en $IFS
apkFileName="*.apk"
for file in `find ${APK_PATH} -name "*.apk"`
do
    apkFileName=`basename ${file}`
    break
done
echo apkFile=${APK_PATH}/${apkFileName}

rm -rf  ${JIAGU_PATH}
mkdir ${JIAGU_PATH}

echo "------jiagu start! ------"

java -jar ${BASE} -version
java -jar ${BASE} -login ${NAME} ${PASSWORD}
java -jar ${BASE} -importsign ${KEY_PATH} ${KEY_PASSWORD} ${ALIAS} ${ALIAS_PASSWORD}
java -jar ${BASE} -showsign
#java -jar ${BASE}/jiagu.jar -importmulpkg ${BASE}/多渠道模板.txt #根据自身情况使用
#java -jar ${BASE} -showmulpkg
java -jar ${BASE} -showconfig
java -jar ${BASE} -jiagu ${APK_PATH}/${apkFileName} ${JIAGU_PATH} -autosign

echo "------ jiagu end!------"

jiaguApkFileName="*.apk"
for file2 in `find ${JIAGU_PATH} -name "*.apk"`
do
    if test -f ${file2}
    then
        jiaguApkFileName=`basename ${file2}`
        break
    fi
done
echo "jiaguApkFileName=${jiaguApkFileName}"
renameJiaguApkFileName="${apkFileName}"
echo "renameJiaguApkFileName=${renameJiaguApkFileName}"
mv ${JIAGU_PATH}/${jiaguApkFileName} ${JIAGU_PATH}/${renameJiaguApkFileName}


if ! ${channel}
then
    exit 0
fi

rm -rf ./app/build/rebuildChannel/*
./gradlew app:reBuildChannel