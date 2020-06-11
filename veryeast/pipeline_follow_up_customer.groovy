pipeline{
    agent any

    environment{
        VERYEAST = credentials('veryeast_wife')
        TUJIAN = credentials('tujian')
    }

    parameters{
        string(name: 'follow_up_first_day_interval_today', defaultValue: '0', description: '将要跟进客户的日期距离今天的天数')
        string(name: 'query_follow_up_count_days', defaultValue: '5', description: '自动查询将要跟进日期开始往后的日期 跟进客户数量，限制查询的天数，再往后的没有查询到日期，默认当做客户数量为0')
        string(name: 'max_each_day_follow_up_count', defaultValue: '55', description: '每天可安排的客户最大数量')
    }

    stages{
        stage('follow_up'){
            steps{
                 sh 'export PYTHONPATH=${$WORKSPACE} && python3 ${$WORKSPACE}/veryeast/follow_up_customer.py "$VERYEAST_USR" "$VERYEAST_PSW" "$follow_up_first_day_interval_today" "$query_follow_up_count_days" "$max_each_day_follow_up_count" "$TUJIAN_USR" "$TUJIAN_PSW" '
            }
        }
    }
}