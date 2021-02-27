<!--单项目时间线组件-->
<template>
<el-timeline>
    <el-timeline-item
    type="info"
    placement="top"
    icon="el-icon-plus"
    :timestamp="new Date().toString()">
    <el-form v-if="addStatus" :rules="rules" ref="contentform" :model="form" label-width="80px">
        <el-form-item label="实施内容" prop="doneContent">
            <el-input
            type="textarea"
            size="medium"
            :autosize="{ minRows: 1, maxRows: 3}"
            placeholder="输入项目进度记录实施内容"
            style="width:20vw"
            v-model="form.doneContent">
            </el-input>
        </el-form-item>
        <el-form-item label="实施结果" prop="resultContent">
            <el-input
            type="textarea"
            size="medium"
            :autosize="{ minRows: 1, maxRows: 3}"
            placeholder="输入项目进度记录实施结果"
            style="width:20vw"
            v-model="form.resultContent">
            </el-input>
        </el-form-item>
    </el-form>
    <el-button
        size="mini"
        :type="addStatus?'success':'primary'"
        :icon="addStatus?'el-icon-check':'el-icon-edit'"
        @click="openEdit('contentform')">{{ addStatus?'':'新增时间线记录'}}</el-button>
    <el-button v-if="addStatus"
        size="mini"
        type="danger"
        icon="el-icon-close"
        @click="closeEdit"></el-button>
    </el-timeline-item>

    <el-timeline-item
        v-for="(activity, index) in activities_"
        :key="index"
        :type="activity.type"
        placement="top"
        :timestamp="activity.timestamp">
        <el-card shadow="hover" style="width:30vw;margin:20px 0;">
            <div style="overflow:hidden;" >
                <div style="float:left;width:10%;">[进展]:</div>
                <pre style="float:left;width:90%;margin:0 0">{{activity.done}}</pre>
            </div>
            <el-divider></el-divider>
            <div style="overflow:hidden;" >
                <div style="float:left;width:10%;">[结果]:</div>
                <pre style="float:left;width:90%;margin:0 0">{{activity.result}}</pre>
            </div>
        </el-card>
        <el-button
            size="mini"
            type="danger"
            icon="el-icon-delete"
            @click="handleDelete(index)"></el-button>
    </el-timeline-item>
</el-timeline>
</template>

<script>
import axios from 'axios'

function getCookie(cname)
{
    let name = cname + "=";
    let ca = document.cookie.split(';');

    for(let i=0; i<ca.length; i++) 
    {
        let c = ca[i].trim();
        if (c.indexOf(name)==0) return c.substring(name.length,c.length);
    }
    return "";
}

export default {
    name: 'time_line',
    data(){
        return {
            /* 新增时间线内容 */
            form:{
                contentStaus:'',
                doneContent:'',
                resultContent:'',
            },
            /* 新增栏状态 */
            addStatus:false,
            /* 时间线活动记录 */
            activities_:[],
            rules: {
                doneContent: [
                    { required: true, message: '请填写实施内容', trigger: 'blur' },
                    { min: 4, message: '长度需要大于4个字符', trigger: 'blur' }
                ],
                resultContent: [
                    { required: true, message: '请填写实施结果', trigger: 'blur' },
                    { min: 4, message: '长度需要大于4个字符', trigger: 'blur' }
                ]
            }
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
        /* 当前项目状态,生成新时间线的时候标注使用 */
        projectStatus: {
            type: String,
            default: "success"
        },
        /*时间线内容*/
        activities: {
            type: Array,
            default: function () {
                return  [{
                            type : "danger",
                            done: "项目时间线获取失败",
                            result: "新增项目结果",
                            timestamp: new Date().toString()
                        },
                        {
                            type : "warning",
                            done: "项目时间线获取失败",
                            result: "新增项目结果",
                            timestamp: new Date().toString()
                        },{
                            type : "primary",
                            done: "项目时间线获取失败",
                            result: "新增项目结果",
                            timestamp: new Date().toString()
                        },{
                            type : "info",
                            done: "项目时间线获取失败",
                            result: "新增项目结果",
                            timestamp: new Date().toString()
                        },{
                            type : "success",
                            done: "项目时间线获取失败项目时间线获取失败项目时间线获取失败项目时间线获取失败项目时间线获取失败项目时间线获取失败项目时间线获取失败项目时间线获取失败项目时间线获取失败项目时间线获取失败项目时间线获取失败项目时间线获取失败项目时间线获取失败项目时间线获取失败项目时间线获取失败项目时间线获取失败",
                            result: "新增项目结果",
                            timestamp: new Date().toString()
                        },{
                            type : "info",
                            done: "项目时间线获取失败",
                            result: "新增项目结果",
                            timestamp: new Date().toString()
                        }
                ]
            }
        }
    },
    computed: {},
    watch: {},
    methods: {
        closeEdit(){
            //切换编辑状态
            this.addStatus = !this.addStatus;
            
            this.form.contentStaus = '';
            this.form.doneContent = '';
            this.form.resultContent = '';
        },
        openEdit(formValue){
            if(this.addStatus)
            {
                this.$refs[formValue].validate((valid) => {
                    console.dir(valid);
                    if (valid)
                    {
                        let new_data={};

                        new_data.type = (this.projectStatus == "error"?"danger":this.projectStatus);
                        /*回车换行处理*/
                        new_data.done = this.form.doneContent;
                        new_data.result = this.form.resultContent;
                        new_data.timestamp = new Date().toString() +" Author: "+ getCookie("username");

                        this.activities_.unshift(new_data);
                        this.closeEdit();
                    }
                    else
                    {
                        return false;
                    }
                });
            }
            else
            {
                this.closeEdit();
            }
        },
        handleDelete(index){
            this.$confirm('此操作将删除此条时间线记录,是否执行?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                this.activities_.splice(index,1);
                this.$message({
                    type: 'success',
                    message: '删除成功!'
                });
            }).catch(() => {
            });
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

<style scoped>
    /* pre 自动换行 */
    pre {
        white-space: pre-wrap;
        word-wrap: break-word;
    }
</style>