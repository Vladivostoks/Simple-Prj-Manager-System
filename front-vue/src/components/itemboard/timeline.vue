<!--单项目时间线组件-->
<template>
<el-timeline>
    <el-timeline-item
    v-for="(activity, index) in activities_"
    :key="index"
    :type="activity.type"
    :timestamp="activity.timestamp">
    <span>
    [进展]:{{activity.content}}
    </span>
    <el-divider direction="vertical"></el-divider>
    <span>
    [结果]:{{activity.content}}
    </span>
    <el-button
        size="mini"
        type="primary"
        icon="el-icon-edit"
        :disabled="index"
        @click="openEdit(index)"></el-button>
    <el-button
        size="mini"
        type="danger"
        icon="el-icon-delete"
        :disabled="activities_.length==1?true:false"
        @click="handleDelete(index)"></el-button>
    </el-timeline-item>
</el-timeline>
</template>

<script>
import axios from 'axios'

export default {
    name: 'time_line',
    data(){
        return {
            activities_:[]
        }
    },
    props: {
        /*项目名称 用来从后台获取具体项目的时间线 */
        project_index: {
            type: Object,
            default: function () {
                return { date: 'None',name: "None" }
            }
        },
        /*时间线内容*/
        activities: {
            type: Array,
            default: function () {
                return  [{
                            type : "danger",
                            content: "项目时间线获取失败",
                            timestamp: new Date(Date.parse(new Date().toString()))
                        },
                        {
                            type : "warning",
                            content: "项目时间线获取失败",
                            timestamp: new Date(Date.parse(new Date().toString()))
                        },{
                            type : "primary",
                            content: "项目时间线获取失败",
                            timestamp: new Date(Date.parse(new Date().toString()))
                        },{
                            type : "info",
                            content: "项目时间线获取失败",
                            timestamp: new Date(Date.parse(new Date().toString()))
                        },{
                            type : "success",
                            content: "项目时间线获取失败",
                            timestamp: new Date(Date.parse(new Date().toString()))
                        },{
                            type : "info",
                            content: "项目时间线获取失败",
                            timestamp: new Date(Date.parse(new Date().toString()))
                        }]
            }
        }
    },
    computed: {},
    watch: {},
    methods: {
        openEdit(index){
            alert(index)
        },
        handleDelete(index){
            this.activities_.splice(index,1);
        }
    },
    created() {
        /* axio 从后台获取具体项目的时间线 */
        let self = this;

        axios({
            url:'/'+self.projectName+'/timelineContent',
            method: 'get',
            timeout: 1000,
            responseType: 'json',
            responseEncoding: 'utf8', 
        }).then((res) => {
            self.activities_ = res.data.timelineContent;
        }).catch((err) => {
            //default do nothing
            self.activities_ = self.activities;
        });
    },
    mounted() {},
    updated() {},
    destroyed() {}
}
</script>
