<!--单项目时间线组件-->
<template>
<el-timeline>
    <el-timeline-item
    type="info"
    placement="top"
    icon="el-icon-plus"
    v-if="isEditable"
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
            v-if="isEditable && (index == 0)"
            size="mini"
            type="danger"
            icon="el-icon-delete"
            @click="handleDelete(index)"></el-button>
    </el-timeline-item>
</el-timeline>
</template>

<script>
import axios from 'axios'
import {getCookie} from '@/assets/js/common.js'

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
            activities_:[],
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
        },
        /* 是否可编辑时间线 */
        isEditable:{
            type: Boolean,
            default: true

        }
    },
    computed: {},
    watch: {
        addStatus: function(newVal, oldVal) {
            if(newVal)
            {
                if(this.activities_.length>0)
                {
                    this.form.percent = this.activities_[0].percent;
                }
            }
        }
    },
    methods: {
        /**
         * @description: 获取规定时间范围内到某个事务到时间线
         * @param {String} uuid 查询项目uuid
         * @param {Array} dateRange 起始时间和结束时间Date对象数组 
         * @return {Promise} 查询动作
         */
        getLineContent(uuid,dateRange)
        {
            let req = new Object();

            req.start_time = dateRange[0].getTime();
            req.end_time = dateRange[1].getTime();
            return new Promise(function (resolve, reject) {
                axios({
                    url:'/affair/'+uuid,
                    method: 'get',
                    timeout: 5000,
                    responseType: 'json',
                    responseEncoding: 'utf8', 
                    params: req
                }).then((res) => {
                    if(res.data.length > 0 || self.isEditable == true)
                    {
                        resolve(res.data);
                    }
                    else
                    {
                        resolve(res.data);
                    }
                }).catch((err) => {
                    reject(err);
                });
            });
        },
        /**
         * @description: 将时间线内容数组转换成一串长字符串
         * @param {Array} contentData 时间线数组
         * @param {Array} dateRange 起始时间和结束时间Date对象数组 
         * @return {String} 时间线文本
         */
        line2Text(contentData,DateRange,withTimeStamp,withName){
            let text = "";
            
            //只取时间范围内到
            for(let i in contentData)
            {
                if(contentData[i].timestamp >= DateRange[0].getTime()
                    && contentData[i].timestamp < DateRange[1].getTime())
                {
                    //合成内容包括实施&结果
                    if(withTimeStamp && withName)
                    {
                        text += new Date(contentData[i].timestamp).toISOString()+"("+contentData[i].author+")"+":\n";
                    }
                    else if(withName)
                    {
                        text += contentData[i].author+":\n";

                    }
                    else if(withTimeStamp)
                    {
                        text += new Date(contentData[i].timestamp).toISOString()+":\n";
                    }
                    text += contentData[i].progress_content
                    if(!text.endsWith("\n"))
                    {
                        text += "\n";
                    }
                    text += contentData[i].progress_result;
                    if(i != (contentData.length-1))
                    {
                        if(!text.endsWith("\n"))
                        {
                            text += "\n";
                        }
                    }
                }
            }
            return text;
        },
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
                if(this.activities_.length>0
                   && (this.form.percent < this.activities_[0].percent))
                {
                    //进度未满而切换状态到已完成，需要禁止
                    this.$message({
                        type: 'error',
                        message: "新时间线记录进度不能降低",
                    });
                }
                else
                {
                    this.$refs[formValue].validate((valid) => {
                        if (valid)
                        {
                            let data={};
                            let self = this;
                        
                            /*回车换行处理*/
                            data.timestamp = new Date().getTime();
                            data.progress_content = this.form.doneContent;
                            data.progress_result = this.form.resultContent;
                            data.percent = this.form.percent;
                            data.project_status = (this.project_status == "error"?"danger":this.project_status);
                            data.author = getCookie("username");

                            axios({
                                url:'/affair/'+self.project_uuid,
                                method: 'post',
                                timeout: 5000,
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
                                    data.index_num = res.data.index_num;
                                    self.activities_.unshift(data);
                                    self.closeEdit();
                                    self.$message({
                                        type: 'success',
                                        message: '添加时间线成功!'
                                    });

                                    //弹出当前更新百分比
                                    this.$emit("timeline-submit",self.project_uuid,data.percent);
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
                    timeout: 5000,
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
                        //弹出当前更新百分比
                        this.$emit("timeline-submit",self.project_uuid,
                                                     self.activities_.length>0?self.activities_[0].percent:0);
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
        let dateRange = [new Date(1970,1,1),new Date()];

        this.getLineContent(this.project_uuid,dateRange).then((data) => {
            this.activities_ = data;

            for(let i in this.activities_)
            {
                this.activities_[i].timestamp = new Date(this.activities_[i].timestamp).toString();
            }
        }).catch((err) => {
            //default do nothing
            this.$message({
                type: 'error',
                message: err
            });
            this.activities_ = [{
                                    timestamp:new Date().toString(),
                                    author:getCookie("username"),
                                    percent:0,
                                    project_status:"danger",
                                    progress_content:"获取项目执行记录失败",
                                    progress_result:"获取暂无项目结果记录失败"
                                }];
            for(let i in this.activities_)
            {
                this.activities_[i].timestamp = new Date(this.activities_[i].timestamp).toString();
            }
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