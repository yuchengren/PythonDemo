pipeline{
    agent any

    environment{
        VERYEAST = credentials('veryeast_wife')
        TUJIAN = credentials('tujian')
        EXECUTE_RESULT_DINGTALK_TOKEN = "a7d885f520f284ccd09561919c8d1c4a3c9fa54d3c3d2b294b0778e3ce5c4574" //执行结果状态的通知
    }

    triggers{
        cron('0 20 * * *')
    }

    options{
        retry(3)
    }

    parameters{
        string(name: 'follow_up_first_day_interval_today', defaultValue: '1', description: '将要跟进客户的日期距离今天的天数')
        string(name: 'query_follow_up_count_days', defaultValue: '5', description: '自动查询将要跟进日期开始往后的日期 跟进客户数量，限制查询的天数，再往后的没有查询到日期，默认当做客户数量为0')
        string(name: 'max_each_day_follow_up_count', defaultValue: '55', description: '每天可安排的客户最大数量')
        string(name: 'max_captcha_recognise_times', defaultValue: '10', description: '验证码最多执行识别的次数')
        booleanParam(name: 'is_tensorflow_recognise_captcha', defaultValue: true, description: '是否用tensorflow做验证码识别')
    }

    stages{
        stage('follow_up'){
            steps{
                 sh 'export PYTHONPATH=${WORKSPACE} && python3 ${WORKSPACE}/veryeast/follow_up_customer.py "$VERYEAST_USR" "$VERYEAST_PSW" "$follow_up_first_day_interval_today" "$query_follow_up_count_days" "$max_each_day_follow_up_count" "$max_captcha_recognise_times" "$is_tensorflow_recognise_captcha" "$TUJIAN_USR" "$TUJIAN_PSW" '
            }
        }
    }

    post {
        failure {
            wrap([$class: 'BuildUser']) {
                sh "export PYTHONPATH=$WORKSPACE && python3 $WORKSPACE/jenkins/execute_result_dingtalk.py ${env.BUILD_USER_ID} ${env.JENKINS_URL} $JOB_NAME $BUILD_ID ${currentBuild.currentResult} $EXECUTE_RESULT_DINGTALK_TOKEN  "
//                 cleanWs()
            }
        }
    }
}