<!--导出选项表单-->
<template>
<el-dialog 
  :title="headLable"
  :show-close="false"
  :visible.sync="formVisible"
  :before-close="handleClose"
  :close-on-click-modal="false"
  width="30vw">
  <el-form :model="form" ref="form" size="mini" :rules="rules">
    <el-form-item label="导出选项" label-width="100px" prop="checkedOption">
        <el-checkbox :indeterminate="isIndeterminate" 
                     v-model="form.checkAll" 
                     @change="handleCheckAllChange">全选</el-checkbox>
        <div style="margin: 15px 0;"></div>
        <el-checkbox-group v-model="form.checkedOption" 
                           @change="exportOptChange">
            <el-checkbox v-for="opt in exportOption" :label="opt['name']" :key="opt['name']">{{ opt['name'] }}</el-checkbox>
        </el-checkbox-group>
    </el-form-item>
    <el-form-item v-if="isContent" label="按照周导出" label-width="100px" prop="isWeekRange">
        <el-switch v-model="form.isWeekRange"></el-switch>
    </el-form-item>
    <el-form-item v-if="isContent" label="导出内容区间" label-width="100px" prop="contentTimeRange">
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
import {date2shortStr} from '@/assets/js/common.js'

export default {
    name: 'exportOptionForm',
    data() {
        let checkOpt = (rule, value, callback)=>{
            if(value.length<=0) {
                callback(new Error('至少需要选择一项'));
            }
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
            /* 输入输出表单 */
            form: {
                /* 全选 */
                checkAll: true,
                /* 表格列勾选项 */
                checkedOption:[],
                /* 按照周划分导出 */
                isWeekRange: true,
                /* 导出时间范围 */
                contentTimeRange:[new Date(0),new Date()]
            },
            /* 输入校验规则 */
            rules: {
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
        exportOptChange(val) {
            let checkedCount = val.length;
            let total_opt_num = 0;

            for(let key in this.exportOption)
            {
                total_opt_num++;
            }
            this.checkAll = checkedCount === total_opt_num;
            this.isIndeterminate = checkedCount > 0 && checkedCount < total_opt_num;

            if(this.form.checkedOption.indexOf("具体内容") > -1)
            {
                this.isContent = true;
            }
            else
            {
                this.isContent = false;
            }
        },
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
                    let columns = this.exportOption;
                    let dateRange = [new Date(1970,0,0),new Date()];

                    //根据表单选择项，重新更新
                    for(let key in columns)
                    {
                        if(!(this.form.checkedOption.indexOf(columns[key].name) > -1))
                        {
                            delete columns[key];
                        }
                        else
                        {
                            //需要将具体内容这列替换成具体到时间列
                            if(this.form.checkedOption.indexOf("具体内容") > -1 
                                && columns[key].name == "具体内容")
                            {
                                dateRange[0] = columns[key].dateRange[0].getTime() >
                                                this.form.contentTimeRange[0].getTime()?
                                                columns[key].dateRange[0]:this.form.contentTimeRange[0];
                                if(this.form.isWeekRange)
                                {
                                    //导出时间从本周结束开始
                                    let DayOfWeek = this.form.contentTimeRange[1].getDay(); //今天本周的第几天
                                    let Day = this.form.contentTimeRange[1].getDate(); //当前日
                                    let Month = this.form.contentTimeRange[1].getMonth(); //当前月
                                    let Year = this.form.contentTimeRange[1].getFullYear(); //当前年

                                    dateRange[1] = new Date(Year, Month, Day - DayOfWeek+7);
                                }
                                else
                                {
                                    dateRange[1] = this.form.contentTimeRange[1];
                                }

                                //起始时间从当前项目中最早的开始算
                                for(let date = dateRange[1];date.getTime()>=dateRange[0].getTime();)
                                {
                                    //按照每天划分
                                    let nowDay = date.getDate();
                                    let nowMonth = date.getMonth();
                                    let nowYear = date.getFullYear();
                                    let timeName;
                                    let nextDate;

                                    if(this.form.isWeekRange)
                                    {
                                        timeName = date2shortStr(new Date(nowYear, nowMonth, nowDay - 7));
                                    }
                                    else
                                    {
                                        timeName = date2shortStr(date);
                                    }

                                    columns[timeName]=new Object();
                                    columns[timeName].name = timeName;
                                    columns[timeName].wpx = 160;

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

                    //执行导出动作                
                    this.exportAction(columns,dateRange);

                    this.$emit("dialog-submit");
                } else {
                    return false;
                }
            });
        }
    },
    created() {},
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