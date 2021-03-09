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
        <el-form-item label="实施进度" prop="percent">
            <el-slider style="width:20vw"
                       v-model="form.percent"></el-slider>
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
        :type="activity.project_status"
        placement="top"
        :timestamp="activity.timestamp+' Author: '+ activity.author+' '+activity.percent+'%'">
        <el-card shadow="hover" style="width:30vw;margin:20px 0;">
            <div style="overflow:hidden;" >
                <div style="float:left;width:10%;">[进展]:</div>
                <pre style="float:left;width:90%;margin:0 0">{{activity.progress_content}}</pre>
            </div>
            <el-divider></el-divider>
            <div style="overflow:hidden;" >
                <div style="float:left;width:10%;">[结果]:</div>
                <pre style="float:left;width:90%;margin:0 0">{{activity.progress_result}}</pre>
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

function date2str(date_input){
    let date_obj = new Date(date_input);
    let year = date_obj.getFullYear();
    let month = date_obj.getMonth() + 1 < 10 ? "0" + (date_obj.getMonth() + 1)
            : date_obj.getMonth() + 1;
    let day = date_obj.getDate() < 10 ? "0" + date_obj.getDate() : date_obj.getDate();
    return (year + "-" + month + "-" + day);
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
                percent:0,
            },
            /* 新增栏状态 */
            addStatus:false,
            /* 时间线活动记录 */
            activities_:[{
                project_status : "danger",
                progress_content: "项目时间线获取失败",
                progress_result: "新增项目结果",
                timestamp: new Date().toString()
            }],
            rules: {
                doneContent: [
                    { required: true, message: '请填写实施内容', trigger: 'blur' },
                    { min: 4, message: '长度需要大于4个字符', trigger: 'blur' }
                ],
                resultContent: [
                    { required: true, message: '请填写实施结果', trigger: 'blur' },
                    { min: 4, message: '长度需要大于4个字符', trigger: 'blur' }
                ],
                percent: [
                    { min: 0, max: 100, type:'integer' ,trigger: 'blur' }
                ]
            }
        }
    },
    props: {
        /*项目名称 用来从后台获取具体项目的时间线 */
        project_uuid: {
            type: String,
            required: true
        },
        /* 当前项目状态,生成新时间线的时候标注使用 */
        project_status: {
            type: String,
            default: "success"
        }
    },
    computed: {},
    watch: {
        addStatus: function(newVal, oldVal) {
            if(newVal)
            {
                this.form.percent = this.activities_[0].percent;
            }
        }
    },
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
                        let data={};
                        let self = this;
                        
                        /*回车换行处理*/
                        data.timestamp = new Date().getTime();
                        data.progress_content = this.form.doneContent;
                        data.progress_result = this.form.resultContent;
                        data.percent = 10;//#TODO
                        console.dir(this.project_status)
                        data.project_status = (this.project_status == "error"?"danger":this.project_status);
                        data.author = getCookie("username");

                        axios({
                            url:'/affair/'+self.project_uuid,
                            method: 'post',
                            timeout: 1000,
                            responseType: 'json',
                            responseEncoding: 'utf8', 
                            headers: {
                                    'Content-Type': 'application/json;charset=UTF-8'
                            },
                            data:data
                        }).then((res) => {
                            if(res.data.message == "插入成功") 
                            {
                                data.timestamp = new Date(data.timestamp).toString();
                                self.activities_.unshift(data);
                                self.closeEdit();
                                self.$message({
                                    type: 'success',
                                    message: '添加时间线成功!'
                                });
                            }
                        }).catch((res)=>{
                            //Do nothing
                            console.dir(res);
                        }); 
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
                //todo axios
                //提交项目变更
                let data = new Object();
                let self = this;

                data.index = this.activities_[index].index_num;
                
                axios({
                    url:'/affair/'+self.project_uuid,
                    method: 'delete',
                    timeout: 1000,
                    responseType: 'json',
                    responseEncoding: 'utf8', 
                    headers: {
                            'Content-Type': 'application/json;charset=UTF-8'
                    },
                    data:data
                }).then((res) => {
                    if(res.data.message == "删除成功") 
                    {
                        self.activities_.splice(index,1);
                        self.$message({
                            type: 'success',
                            message: '删除成功!'
                        });
                    }
                }).catch((res)=>{
                    //Do nothing
                    console.dir(res);
                }); 
            }).catch(() => {
            });
        }
    },
    created() {
        /* axio 从后台获取具体项目的时间线 */
        let self = this;
        let req = new Object();

        req.start_time = new Date(1970,1,1).getTime();
        req.end_time = new Date().getTime();

        axios({
            url:'/affair/'+self.project_uuid,
            method: 'get',
            timeout: 1000,
            responseType: 'json',
            responseEncoding: 'utf8', 
            params: req
        }).then((res) => {
            self.activities_ = res.data;
            for(let i in self.activities_)
            {
                self.activities_[i].timestamp = new Date(self.activities_[i].timestamp).toString();
            }
        }).catch((err) => {
            //default do nothing
            console.dir(err);
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