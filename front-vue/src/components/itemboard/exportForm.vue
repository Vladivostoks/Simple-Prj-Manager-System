<!--导出选项表单-->
<template>
<el-dialog 
  :title="headLable"
  :show-close="false"
  :visible.sync="formVisible"
  :before-close="handleClose"
  :close-on-click-modal="false"
  width="35vw">
  <el-form :model="form" ref="form" size="mini" :rules="rules">
    <el-form-item label="导出选项" label-width="120px" prop="checkedOption">
        <el-checkbox :indeterminate="isIndeterminate" 
                     v-model="form.checkAll" 
                     @change="handleCheckAllChange">全选</el-checkbox>
        <div style="margin: 15px 0;"></div>
        <el-select
            v-model="form.checkedOption"
            multiple
            filterable
            default-first-option
            style="width:100%"
            placeholder="选择导出列">
            <el-option
                v-for="item in exportOption"
                :key="item"
                :label="item['name']"
                :value="item['name']">
            </el-option>
        </el-select>
    </el-form-item>
    <el-form-item label="过滤/选择" label-width="120px" prop="isChoose">
        <el-switch @change="filterSwitchChange" v-model="form.isChoose"></el-switch>
    </el-form-item>
    <el-form-item label="项目类型过滤/选择" label-width="120px" prop="typeFilter">
        <el-select
            v-model="form.typeFilter"
            multiple
            filterable
            default-first-option
            style="width:100%"
            placeholder="导出相关类型项目">
            <el-option
                v-for="item in typeList"
                :key="item"
                :label="item"
                :value="item">
            </el-option>
        </el-select>
    </el-form-item>
    <el-form-item label="执行人员过滤/选择" label-width="120px" prop="personFilter">
    <el-select
        v-model="form.personFilter"
        multiple
        filterable
        default-first-option
        style="width:100%"
        placeholder="导出相关人员项目">
        <el-option
            v-for="item in personsList"
            :key="item"
            :label="item"
            :value="item">
        </el-option>
    </el-select>
    </el-form-item>
    <el-form-item v-if="isContent" label="按照周导出" label-width="120px" prop="isWeekRange">
        <el-switch v-model="form.isWeekRange"></el-switch>
    </el-form-item>
    <el-form-item v-if="isContent" label="时间戳" label-width="120px" prop="withTimestamp">
        <el-switch v-model="form.withTimestamp"></el-switch>
    </el-form-item>
    <el-form-item v-if="isContent" label="人员名称" label-width="120px" prop="withName">
        <el-switch v-model="form.withName"></el-switch>
    </el-form-item>
    <el-form-item v-if="isContent" label="导出内容区间" label-width="120px" prop="contentTimeRange">
        <el-date-picker
            v-model="form.contentTimeRange"
            type="daterange"
            align="right"
            unlink-panels
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            :picker-options="pickerOptions">
        </el-date-picker>
    </el-form-item>
  </el-form>
  <div slot="footer" class="dialog-footer">
    <el-button @click="Cancel">取 消</el-button>
    <el-button type="primary" @click="Confirm">导出</el-button>
  </div>
</el-dialog>
</template>

<script>
import axios from 'axios'
import {date2shortStr} from '@/assets/js/common.js'
import {deepCopy} from '@/assets/js/common.js'

export default {
    name: 'exportOptionForm',
    data() {
        let checkOpt = (rule, value, callback)=>{
            // if(value.length<=0) {
            //     callback(new Error('至少需要选择一项'));
            // }
            callback();
            return true;
        }

        return {
            /* 表单可见状态 */
            formVisible: true,
            /* 导出具体内容 */
            isContent: true,
            /* 默认全选,选项不为未知 */
            isIndeterminate:false,
            /* 项目类型列表 */
            typeList:[],
            /* 项目人员列表 */
            personsList:[],
            /* 输入输出表单 */
            form: {
                /* 是否开启选择(关闭为过滤) */
                isChoose:false,
                /* 类型过滤 */
                typeFilter:[],
                /* 人员过滤 */
                personFilter:[],
                /* 全选 */
                checkAll: true,
                /* 表格列勾选项 */
                checkedOption:[],
                /* 按照周划分导出 */
                isWeekRange: true,
                /* 内容导出携带时间戳 */
                withTimestamp: true,
                /* 内容导出携带姓名 */
                withName: true,
                /* 导出时间范围 */
                contentTimeRange:[new Date(0),new Date()]
            },
            /* 输入校验规则 */
            rules: {
                typeFilter: [
                    { required: true, validator: checkOpt, trigger: 'blur' }
                ],
                personFilter: [
                    { required: true, validator: checkOpt, trigger: 'blur' }
                ],
                checkedOption: [
                    { required: true, validator: checkOpt, trigger: 'blur' }
                ]
            },
            /* 日期区间快捷选项 */
            pickerOptions: {
                shortcuts: [{
                    text: '最近一周',
                    onClick(picker) {
                        const end = new Date();
                        const start = new Date();
                        start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
                        picker.$emit('pick', [start, end]);
                    }
                }, {
                    text: '最近一个月',
                    onClick(picker) {
                        const end = new Date();
                        const start = new Date();
                        start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
                        picker.$emit('pick', [start, end]);
                    }
                }, {
                    text: '最近三个月',
                    onClick(picker) {
                        const end = new Date();
                        const start = new Date();
                        start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
                        picker.$emit('pick', [start, end]);
                    }
                }, {
                    text: '至今所有',
                    onClick(picker) {
                        const end = new Date();
                        const start = new Date();
                        start.setTime(0);
                        picker.$emit('pick', [start, end]);
                    }
                }]
            }
        }
    },
    props: {
        /*标题*/
        headLable:{
            type: String,
            required: true,
        },
        /*如果是编辑需要传入被编辑值*/
        exportOption:{
            type: Object,
            default: null,
            validator: function (value) {
                //todo:入参校验
                return true
            }
        },
        /* 必要的导出动作实现 */
        exportAction:{
            type: Function,
            required: true,
        }
    },
    components: {},
    computed: {},
    watch: {},
    methods: {
        /**
         * @description: 修改默认过滤/选择选项
         */
        filterSwitchChange()
        {
            if(this.form.isChoose)
            {
                this.form.typeFilter = this.typeList;
                this.form.personFilter = this.personsList
            }
        },
        /**
         * @description: 从后台获取对应选项范围
         * @param {String} opt 获取选项名称
         * @return {Array} 选项数组
         */
        getOption(opt)
        {
            return new Promise(function(resolve,reject){
                axios({
                    url:'/option',
                    method: 'get',
                    timeout: 5000,
                    responseType: 'json',
                    responseEncoding: 'utf8', 
                    params: {'option_name':opt}
                }).then((res) => {
                    resolve(res.data.option);
                }).catch((error)=>{
                    reject(error);
                }); 
            })
        },
        /**
         * @description: 全选导出项目
         * @param {Boolean} val 是否全选
         */         
        handleCheckAllChange(val) {
            if(val)
            {
                for(let key in this.exportOption)
                {
                    this.form.checkedOption.push(this.exportOption[key]["name"]);
                }

                this.isContent = true;
            }
            else
            {
                this.form.checkedOption = [];
            }
            this.isIndeterminate = false;
        },
        /**
         * @description: 导出选项修改触发
         * @param {Array} val 修改后到值
         */    
        // exportOptChange(val) {
        //     let checkedCount = val.length;
        //     let total_opt_num = 0;

        //     for(let key in this.exportOption)
        //     {
        //         total_opt_num++;
        //     }
        //     this.checkAll = checkedCount === total_opt_num;
        //     this.isIndeterminate = checkedCount > 0 && checkedCount < total_opt_num;

        //     if(this.form.checkedOption.indexOf("具体内容") > -1)
        //     {
        //         this.isContent = true;
        //     }
        //     else
        //     {
        //         this.isContent = false;
        //     }
        // },
        /**
         * @description: 对话关闭钩子函数
         * @param {Object} done 关闭动作回调
         */
        handleClose(done) {
            this.formVisible = false;
            this.$emit("dialog-close")
            .then(() => {
                done();
            })
            .catch(() => {});
        },
        /**
         * @description: 取消导出
         * @event dialog-close 导出取消事件
         */
        Cancel(){
            this.formVisible = false;
            this.$emit("dialog-close");
        },
        /**
         * @description: 确认导出项
         * @event dialog-submit 确认导出事件
         */
        Confirm(){
            this.$refs['form'].validate((valid) => {
                if (valid) {
                    this.formVisible = false;
                    let dateRange = [new Date(1970,0,0),new Date()];
                    let columns = new Object();
                    
                    //按照checkedOption排列 根据表单选择项，重新更新
                    for(let i in this.form.checkedOption)
                    {
                        for(let key in this.exportOption)
                        {
                            if(this.exportOption[key].name == this.form.checkedOption[i])
                            {
                                columns[key] = this.exportOption[key];
                                if(columns[key]["name"] == "具体内容")
                                {
                                    //需要将具体内容这列替换成具体到时间列
                                    let wpx = columns[key].wpx;
                                    let alignment = columns[key].alignment;

                                    dateRange[0] = columns[key].dateRange[0].getTime() >
                                                    this.form.contentTimeRange[0].getTime()?
                                                    columns[key].dateRange[0]:this.form.contentTimeRange[0];
                                    if(this.form.isWeekRange)
                                    {
                                        //导出时间从开始日所在周开始日开始，结束日所在周最后一日结束
                                        let DayOfWeek = this.form.contentTimeRange[1].getDay(); //今天本周的第几天
                                        let Day = this.form.contentTimeRange[1].getDate(); //当前日
                                        let Month = this.form.contentTimeRange[1].getMonth(); //当前月
                                        let Year = this.form.contentTimeRange[1].getFullYear(); //当前年

                                        dateRange[1] = new Date(Year, Month, Day - DayOfWeek+7);

                                        DayOfWeek = dateRange[0].getDay(); //今天本周的第几天
                                        Day = dateRange[0].getDate(); //当前日
                                        Month = dateRange[0].getMonth(); //当前月
                                        Year = dateRange[0].getFullYear(); //当前年

                                        dateRange[0] = new Date(Year, Month, Day - DayOfWeek);
                                    }
                                    else
                                    {
                                        dateRange[1] = this.form.contentTimeRange[1];
                                    }

                                    //起始时间从当前项目中最早的开始算,前开后闭区间
                                    for(let date = dateRange[1];date.getTime()>dateRange[0].getTime();)
                                    {
                                        //按照每天划分
                                        let nowDay = date.getDate();
                                        let nowMonth = date.getMonth();
                                        let nowYear = date.getFullYear();
                                        let timeName;
                                        let nextDate;

                                        if(this.form.isWeekRange)
                                        {
                                            timeName = date2shortStr(new Date(nowYear, nowMonth, nowDay-2));
                                        }
                                        else
                                        {
                                            timeName = date2shortStr(date);
                                        }

                                        columns[timeName]=new Object();
                                        columns[timeName].name = timeName;
                                        columns[timeName].wpx = wpx;
                                        columns[timeName].alignment = alignment;

                                        if(this.form.isWeekRange)
                                        {
                                            nextDate = new Date(nowYear, nowMonth, nowDay-7);
                                        }
                                        else
                                        {
                                            nextDate = new Date(nowYear, nowMonth, nowDay-1);
                                        }

                                        columns[timeName].dateRange = [nextDate,date];
                                        date=nextDate;
                                    }
                                    delete columns[key];
                                }
                            }
                        }
                    }
 
                    //执行导出动作                
                    this.exportAction(columns,dateRange,
                                      this.form.typeFilter,
                                      this.form.personFilter,
                                      this.form.isChoose,
                                      this.form.withTimestamp,
                                      this.form.withName
                                      );

                    this.$emit("dialog-submit");
                } else {
                    return false;
                }
            });
        }
    },
    created() {
        //初始化选项,默认全选
        this.getOption("prjtype_opt").then((data)=>{
            this.typeList = data;
        });
        this.getOption("dutyperson_opt").then((data)=>{
            this.personsList = data;
        });
    },
    mounted() {
        //deep copy
        if(this.exportOption != null)
        {
            for(let key in this.exportOption)
            {
                this.form.checkedOption.push(this.exportOption[key]["name"]);
            }
        }
        this.formVisible = true;
    },
    updated() {
    },
    destroyed() {}
}
</script>

<style scoped>
    .el-form-item{
        text-align: left;
    }
</style>