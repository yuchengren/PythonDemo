pipeline{
    agent any

    options {
        buildDiscarder logRotator(artifactDaysToKeepStr: '14', artifactNumToKeepStr: '20', daysToKeepStr: '14', numToKeepStr: '20')
    }

    environment{
        VERYEAST = credentials('veryeast_wife')
        TUJIAN = credentials('tujian')
        VERYEAST_PROPERTIES_FILE = "/root/PycharmProjects/PythonDemo/veryeast/config/veryeast.properties"
    }

    parameters{
        extendedChoice(
                defaultValue: '3',
                description: '所属公海',
                multiSelectDelimiter: ',',
                name: 'BELONG_PUBLIC_SEA',
                quoteValue: false,
                saveJSONParameterToFile: false,
                type: 'PT_RADIO',
                propertyFile: "/root/PycharmProjects/PythonDemo/veryeast/config/veryeast.properties",
                propertyKey: 'BELONG_PUBLIC_SEA_INDEX',
                descriptionPropertyFile: "/root/PycharmProjects/PythonDemo/veryeast/config/veryeast.properties",
                descriptionPropertyKey: 'BELONG_PUBLIC_SEA_NAME',
                visibleItemCount: 5)
        extendedChoice(
                defaultValue: '0',
                description: '客户来源',
                multiSelectDelimiter: ',',
                name: 'CUSTOMER_SOURCE',
                quoteValue: false,
                saveJSONParameterToFile: false,
                type: 'PT_RADIO',
                propertyFile: "/root/PycharmProjects/PythonDemo/veryeast/config/veryeast.properties",
                propertyKey: 'CUSTOMER_SOURCE_INDEX',
                descriptionPropertyFile: "/root/PycharmProjects/PythonDemo/veryeast/config/veryeast.properties",
                descriptionPropertyKey: 'CUSTOMER_SOURCE_NAME',
                visibleItemCount: 5)
        string(name: 'GET_IN_CUSTOMER_NAMES', defaultValue: '', description: '揽入客户的名称，多个客户以英文逗号分隔')
        string(name: 'GET_IN_FREQUENCY', defaultValue: '0.01', description: '点击揽入的频率，即每隔多少秒点击一次')
        string(name: 'max_captcha_recognise_times', defaultValue: '10', description: '验证码最多执行识别的次数')
        booleanParam(name: 'is_tensorflow_recognise_captcha', defaultValue: true, description: '是否用tensorflow做验证码识别')
    }

    stages{
        stage('follow_up'){
            steps{
                 sh 'export PYTHONPATH=${WORKSPACE} && python3 ${WORKSPACE}/veryeast/get_in_customer.py "$VERYEAST_USR" "$VERYEAST_PSW" "$BELONG_PUBLIC_SEA" "$CUSTOMER_SOURCE" "$GET_IN_CUSTOMER_NAMES" "$GET_IN_FREQUENCY" "$max_captcha_recognise_times" "$is_tensorflow_recognise_captcha" "$TUJIAN_USR" "$TUJIAN_PSW" '
            }
        }
    }
}