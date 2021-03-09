<template>
<el-container style="height: 87vh;">
    <el-header height="60px">
        <el-col :span="6" style="align-items:left;">
            <el-menu :default-active="table_status"
                     v-model="table_status"
                     mode="horizontal"
                     @select="selectItemWithStatus"
                     background-color="#545c64"
                     text-color="#fff"
                     active-text-color="#ffd04b">
                <el-menu-item index="create">本周新增</el-menu-item>
                <el-menu-item index="incomplete">未完成</el-menu-item>
                <el-menu-item index="complete">历史已完成</el-menu-item>
            </el-menu>
        </el-col>
        <el-col :span="10"
                class="timerange"
                v-if="table_status=='create'">
            <el-date-picker v-model="weekRange"
                            type="week"
                            disabled
                            format="yyyy 第 WW 周"
                            placeholder="选择周">
            </el-date-picker>
        </el-col>
        <el-col :span="10"
                class="timerange"
                v-if="table_status=='incomplete'">
        </el-col>
        <el-col :span="10"
                class="timerange"
                v-if="table_status=='complete'">
            <el-switch  style="display: block;padding: 20px"
                        active-text="最后更新时间"
                        inactive-text="创建时间"
                        @change="rangeTypeChange()"
                        v-model="isUpdateTime">
            </el-switch>
            <el-date-picker v-if="isUpdateTime"
                            v-model="weekRange"
                            @change="timeRangeChange()"
                            type="week"
                            format="自yyyy 第 WW 周"
                            placeholder="选择周">
            </el-date-picker>
            <el-date-picker v-else
                            v-model="weekRange"
                            type="daterange"
                            @change="timeRangeChange()"
                            range-separator="至"
                            start-placeholder="开始日期"
                            end-placeholder="结束日期">
            </el-date-picker>
        </el-col>
        <el-col :span="7" class="timerange">
            <el-button
                size="mini"
                type="info"
                @click="exportItem()">导出当前记录</el-button>
            <el-button
                size="mini"
                type="success"
                v-show="table_status!='complete'">提交项目记录</el-button>
            <el-button
                size="mini"
                type="primary"
                v-show="table_status=='create'"
                @click="creatNewitem()">新建项目记录</el-button>
        </el-col>
        <el-col :span="1"> 
        </el-col>
    </el-header>
    <el-main>
        <el-table
            :data="tableData"
            height="100%"
            :key="tableKey"
            :header-cell-style="headStyle"
            :row-class-name="tableRowClassName"
            v-loading="loading"
            element-loading-text="加载中"
            element-loading-spinner="el-icon-loading"
            element-loading-background="rgba(0, 0, 0, 0.8)"
            style="width: 100%">
            <el-table-column type="expand">
                <template slot-scope="scope">
                    <self-timeline 
                    :project_uuid="scope.row.uuid"
                    :project_status="getSchemeType(scope.$index,scope.row)"
                    :project_index="scope.row.uuid">
                    </self-timeline>
                </template>
            </el-table-column>
            <el-table-column
                min-width="3%"
                type="index"
                >
            </el-table-column>
            <el-table-column
                prop="creat_date"
                min-width="6%"
                label="创建日期">
            </el-table-column>
            <el-table-column
                prop="region"
                min-width="5%"
                :filters="regionOpt"
                :filter-method="tableFilter"
                label="区域">
            </el-table-column>
            <el-table-column
                prop="prjname"
                min-width="8%"
                label="项目名称">
            </el-table-column>
            <el-table-column
                min-width="5%"
                prop="prjtype"
                :filters="typeOpt"
                :filter-method="tableFilter"
                label="项目类型">
                <template slot-scope="scope">
                    <el-tag 
                    disable-transitions
                    type="info"
                    size="small"
                    style="margin: 1px;"
                    v-for="item in scope.row.prjtype"
                    :key="item">
                        {{ item }}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column
                prop="brief"
                min-width="17%"
                label="原始需求/反馈">
                <template slot-scope="scope">
                <pre>{{ scope.row.brief }}</pre>
                </template>
            </el-table-column>
            <el-table-column
                prop="svnurl"
                min-width="10%"
                label="svn/git地址">
            </el-table-column>
            <el-table-column
                min-width="8%"
                label="已执行/预计时间(周)">
                <template slot-scope="scope">
                    <el-alert
                    :description="getSchemeStr(scope.$index, scope.row)"
                    :closable="false"
                    center
                    style="padding: 2px 8px;"
                    :type="getSchemeType(scope.$index, scope.row)">
                    </el-alert>
                </template>
            </el-table-column>
            <el-table-column
                min-width="10%"
                prop="status"
                :filters="statusOpt"
                :filter-method="tableFilter"
                label="执行状态">
                <template slot-scope="scope">
                    <self-processline 
                    :percent="scope.row.percent"
                    :status="scope.row.status">
                    </self-processline>
                </template>
            </el-table-column>
            <el-table-column
                min-width="14%"
                prop="duty_persons"
                :filters="personOpt"
                :filter-method="tableFilter"
                label="当前处理人员">
                <template slot-scope="scope">
                    <el-tag 
                    disable-transitions
                    size="small"
                    style="margin: 1px;"
                    v-for="item in scope.row.duty_persons"
                    :key="item">
                        {{ item }}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column
                min-width="6%"
                prop="relate_persons"
                :filters="relationOpt"
                :filter-method="tableFilter"
                label="关联人员">
                <template slot-scope="scope">
                    <el-tag 
                    disable-transitions 
                    type="warning"
                    size="small"
                    style="margin: 1px;"
                    v-for="item in scope.row.relate_persons"
                    :key="item">
                        {{ item }}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column 
                min-width="9%"
                align="right">
                <template slot="header" slot-scope="scope">
                    <el-input
                    v-model="search"
                    size="mini"
                    @keyup.enter.native="searchViaKeyword(search,scope)"
                    placeholder="输入关键字搜索"/>
                </template>
                <template slot-scope="scope">
                    <el-button
                    size="mini"
                    :disabled="table_status=='complete'"
                    @click="affairEdit(scope.$index, scope.row)">Edit</el-button>
                    <el-button
                    size="mini"
                    type="danger"
                    :disabled="table_status!='create'"
                    @click="affairDelete(scope.$index, scope.row)">Delete</el-button>
                </template>
            </el-table-column>
        </el-table>
        <item-edit 
            v-if="open_dialog"
            @dialog-close="dialogClose"
            @dialog-submit="dialogSubmit"
            :editIndex="editIndex"
            :value="editDefault"></item-edit>
    </el-main>
    <el-footer height="40px">
        <el-pagination
         layout="prev, pager, next"
         :page-size="2"
         :total="tableData.length">
        </el-pagination>
    </el-footer>
</el-container>
</template>

<script>
import axios from 'axios'
import item_edit from '@/components/itemboard/dialog'
import time_line from '@/components/itemboard/timeline'
import process_line from '@/components/itemboard/progressline'

function timestrToNum(timestr) {
    let date = new Date(timestr);
    let Y = date.getFullYear();
    let M = (date.getMonth()+1 < 10 ? '0'+(date.getMonth()+1):date.getMonth()+1);
    let D = (date.getDate()< 10 ? '0'+date.getDate():date.getDate());
    return Y+M+D;
}

function date2str(date_input){
    let date_obj = new Date(date_input);
    let year = date_obj.getFullYear();
    let month = date_obj.getMonth() + 1 < 10 ? "0" + (date_obj.getMonth() + 1)
            : date_obj.getMonth() + 1;
    let day = date_obj.getDate() < 10 ? "0" + date_obj.getDate() : date_obj.getDate();
    return (year + "-" + month + "-" + day);
}

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

/*获取当前生效时间段*/
function getTimeRange(data_range)
{
    let ret = new Object();

    //时间范围
    ret.start_time = date2str(data_range[0]);
    ret.end_time = date2str(data_range[1]);

    return ret;
}

/* 生成uuid */
function uuid() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
        return v.toString(16);
    });
}

export default {
  name: 'tempItemPage',
  data() {
        return {
            /* 表格加载 */
            loading: false,
            /* 当前列表展示时间 */
            weekRange: new Date(),
            isUpdateTime: false,
            /* 通知 */
            notifyPromise:Promise.resolve(),
            /* 修改此变量来更新表格 */
            tableKey: Math.random(),
            /*打开编辑或者展示框*/
            editIndex: false,
            editDefault:{},     //  打开编辑框时候的默认参数
            open_dialog: false,
            /*检索显示内容*/
            search: '',
            /*当前展示当前表单类型 默认为本周新增*/
            table_status:"create",
            /*展示列表*/
            tableData:[/*{
                uuid: '2e0e322a-503a-47fd-b28b-3a1202b55502',
                creat_date: '2021-02-19',
                prjname: 'xx区域xx项目',
                brief: '客户反馈xx问题/客户新增xx需求',
                region: '西安',
                period: 20,
                percent: 80,
                status: '执行中',
                relate_persons: ['Ayden.Shu'],
                duty_persons: ['Ayden.Shu',"shuzhengyang"]
            }*/]
        }
    },
    props: {},
    components: {
        "self-timeline":time_line,
        "self-processline":process_line,
        "item-edit":item_edit
    },
    computed: {
        statusOpt(){
            let index_t;
            let set = new Set();
            let ret = [];

            /* 生成当前项目状态集合 */
            for(index_t in this.tableData)
            {
                if(this.tableData[index_t].status != null)
                {
                    set.add(this.tableData[index_t].status);
                }
            }

            let array = Array.from(set);

            for(index_t in array)
            {
                let pair={
                    text: array[index_t],
                    value: array[index_t],
                };

                ret.push(pair);
            }
            return ret;
        },
        typeOpt(){
            let index_t;
            let index_p;
            let set = new Set();
            let ret = [];

            /* 生成当前项目类型集合 */
            for(index_t in this.tableData)
            {
                for(index_p in this.tableData[index_t].prjtype)
                {
                    set.add(this.tableData[index_t].prjtype[index_p]);
                }
            }

            let array = Array.from(set);

            for(index_p in array)
            {
                let pair={
                    text: array[index_p],
                    value: array[index_p],
                };

                ret.push(pair);
            }

            return ret; 
        },
        regionOpt(){
            let index_t;
            let set = new Set();
            let ret = [];

            /* 生成当前项目区域集合 */
            for(index_t in this.tableData)
            {
                set.add(this.tableData[index_t].region);
            }

            let array = Array.from(set);

            for(index_t in array)
            {
                let pair={
                    text: array[index_t],
                    value: array[index_t],
                };

                ret.push(pair);
            }

            return ret; 
        },
        personOpt(){
            let index_t;
            let index_p;
            let set = new Set();
            let ret = [];

            /* 生成当前表格执行人员集合 */
            for(index_t in this.tableData)
            {
                for(index_p in this.tableData[index_t].duty_persons)
                {
                    set.add(this.tableData[index_t].duty_persons[index_p]);
                }
            }

            let array = Array.from(set);

            for(index_p in array)
            {
                let pair={
                    text: array[index_p],
                    value: array[index_p],
                };

                ret.push(pair);
            }

            return ret; 
        },
        relationOpt(){
            let index_t;
            let index_p;
            let set = new Set();
            let ret = [];

            /* 生成当前表格关联人员集合 */
            for(index_t in this.tableData)
            {
                for(index_p in this.tableData[index_t].relate_persons)
                {
                    set.add(this.tableData[index_t].relate_persons[index_p]);
                }
            }

            let array = Array.from(set);

            for(index_p in array)
            {
                let pair={
                    text: array[index_p],
                    value: array[index_p],
                };

                ret.push(pair);
            }

            return ret; 
        }
    },
    watch: {},
    methods: {
        headStyle({row, column, rowIndex, columnIndex}){
            return {height: "20px",background: "#303133"};
        },
        /* 按照内容检索字段*/
        searchViaKeyword(search,scope){

        },
        /*表单状态指示*/
        tableRowClassName({row, rowIndex}) {
            //获取对应数组中项目最后更新时间
            if (rowIndex === 1) {
                return 'warning-row';
            } else if (rowIndex === 3) {
                return 'success-row';
            }
            return '';
        },
        /* 选择过滤器 */
        tableFilter(value, row, column){
            const property = column['property'];
            return row[property].includes(value);
        },
        /* 通知函数封装 */
        notify(msg_option) {
            this.notifyPromise = this.notifyPromise.then(this.$nextTick).then(()=>{
                this.$notify(msg_option);
            });
        },
        /* 获取执行进度和当前进度比较字符串 */
        getSchemeType(index,row){
            let cur_timestamp = new Date().getTime();
            let start_timestamp = new Date(row.creat_date).getTime();

            let week = (cur_timestamp - start_timestamp) / (1000 * 60 * 60 * 24 * 7);

            week = Math.ceil(week);

            if(week > row.period)
            {
                return "error"
            }
            else if(week >= (row.period-1))
            {
                return "warning"
            }
            
            return "success";
        },
        /* 获取规划字符串 */
        getSchemeStr(index,row){
            let cur_timestamp = new Date().getTime();
            let start_timestamp = new Date(row.creat_date).getTime();

            let week = (cur_timestamp - start_timestamp) / (1000 * 60 * 60 * 24 * 7);

            if(week<1)
            {
                week = 1;
            }
            else
            {
                week = Math.ceil(week);
            }

            return `${week}周/${row.period}周`;
        },
        /* 时间选择创建时间还是最后更新时间 */
        rangeTypeChange(){
            //值变化且原来是数组
            if(this.isUpdateTime)
            {
                this.weekRange = this.weekRange[0];
            }
            else
            {
                let now = new Date(this.weekRange);//当前日期
                let nowDayOfWeek = now.getDay(); //今天本周的第几天
                let nowDay = now.getDate(); //当前日
                let nowMonth = now.getMonth(); //当前月
                let nowYear = now.getFullYear(); //当前年

                this.weekRange = new Array();
                this.weekRange[0] = new Date(nowYear, nowMonth, nowDay - nowDayOfWeek+1);
                this.weekRange[1] = new Date(nowYear, nowMonth, nowDay + (8 - nowDayOfWeek));
            }
        },
        /* 时间选择器产生变化,需要更新表单 */
        timeRangeChange(){
            let time_range=new Array();

            console.dir(this.weekRange);
            if(!this.isUpdateTime)
            {
                /* 重新触发检索过程 */
                time_range = this.weekRange;
            }
            else
            {
                let nowDayOfWeek = this.weekRange.getDay(); //今天本周的第几天
                let nowDay = this.weekRange.getDate(); //当前日
                let nowMonth = this.weekRange.getMonth(); //当前月
                let nowYear = this.weekRange.getFullYear(); //当前年

                time_range[0] = new Date(nowYear, nowMonth, nowDay - nowDayOfWeek-7);
                time_range[1] = new Date(nowYear, nowMonth, nowDay - nowDayOfWeek-1);
            }
            
            /* 重新触发检索过程 */
            this.affairGet(getTimeRange(time_range),this.table_status);
        },
        /* 项目类型产生变化,需要更新表单 */
        selectItemWithStatus(index,indexPath){
            this.table_status = index;
            let time_range = new Array(2);
            let self = this;

            //一周认为是周日开始，周六结束,区间前闭后开
            if(index === "create")
            {
                // 时间生成为当前周的
                let now = new Date();//当前日期
                let nowDayOfWeek = now.getDay(); //今天本周的第几天
                let nowDay = now.getDate(); //当前日
                let nowMonth = now.getMonth(); //当前月
                let nowYear = now.getFullYear(); //当前年

                time_range[0] = new Date(nowYear, nowMonth, nowDay - nowDayOfWeek+1);
                time_range[1] = new Date(nowYear, nowMonth, nowDay + (8 - nowDayOfWeek));
                console.dir(time_range[0].toString())
                console.dir(time_range[1].toString())
            }
            else if(index === "incomplete")
            {
                // 时间跨度为本周前未完成
                time_range[0] = new Date(1970, 1, 1);

                let now = new Date();//当前日期
                let nowDayOfWeek = now.getDay(); //今天本周的第几天
                let nowDay = now.getDate(); //当前日
                let nowMonth = now.getMonth(); //当前月
                let nowYear = now.getFullYear(); //当前年

                time_range[1] = new Date(nowYear, nowMonth, nowDay - nowDayOfWeek+1);
                console.dir(time_range[0].toString())
                console.dir(time_range[1].toString())
            }
            else if(index === "complete")
            {
                // 默认为最后更新时间,会去修改weekRange
                this.isUpdateTime = true;

                // 默认时间为上周完成的
                let now = new Date();//当前日期
                let nowDayOfWeek = now.getDay(); //今天本周的第几天
                let nowDay = now.getDate(); //当前日
                let nowMonth = now.getMonth(); //当前月
                let nowYear = now.getFullYear(); //当前年

                time_range[0] = new Date(nowYear, nowMonth, nowDay - nowDayOfWeek-6);
                time_range[1] = new Date(nowYear, nowMonth, nowDay - nowDayOfWeek+1);
                console.dir(time_range[0].toString())
                console.dir(time_range[1].toString())
            }
            /* week设置为一周最后周日时间 */
            this.weekRange = time_range[1];
            
            /* 重新触发检索过程 */
            this.affairGet(getTimeRange(time_range),index).then((res)=>{
                /* 生成提示信息 */
                for(let index in self.tableData)
                {
                    let data = self.tableData[index];

                    if(data.status == "已完成" || data.status == "已终止")
                    {
                        continue;
                    }

                    let cur_timestamp = new Date().getTime();
                    let start_timestamp = new Date(data.creat_date).getTime();
                    let week = (cur_timestamp - start_timestamp) / (1000 * 60 * 60 * 24 * 7);

                    week = Math.ceil(week);
                    if(week > data.period)
                    {
                        //弹框提示
                        this.notify({
                            title: '超期提示',
                            type: 'error',
                            duration: 4500,
                            message: `项目<${data.prjname}> 已经超过规划时间，请及时处理`
                        });
                    }
                    else if(week >= (data.period-1))
                    {
                        //弹框提示
                        this.notify({
                            title: '即将超期',
                            type: 'warning',
                            duration: 2500,
                            message: `项目<${data.prjname}> 即将超期，请及时处理`
                        });
                    }
                }
            }).catch((res)=>{
                console.dir(res);
            });
        },
        /* 触发表单更新 */
        affairGet(data_range,table_status){
            //触发检索
            let self = this;
            let req = data_range;

            if(table_status === "incomplete")
            {
                req.iscomplete = false;
            }
            else if(table_status === "complete")
            {
                req.iscomplete = true;
                req.isupdatetime = this.isUpdateTime;
            }

            req.username = getCookie("username");
            req.userprop = getCookie("userprop");

            this.loading = true;

            return new Promise(function (resolve, reject) {
                axios({
                    url:'/affair',
                    method: 'get',
                    timeout: 1000,
                    responseType: 'json',
                    responseEncoding: 'utf8', 
                    params: req
                }).then((res) => {
                    self.tableData = res.data;
                    self.loading = false;
                    resolve();
                }).catch((error)=>{
                    reject(error);
                }); 
            });
        },
        /* 对话框关闭事件 */
        dialogClose(){
            this.open_dialog = false;
        },
        /* 对话框提交事件 */
        dialogSubmit(new_data,uuid)
        {
            //编辑数据更新
            this.affairPut(new_data).then((res)=>{
                if(res)
                {
                    if(uuid)
                    {
                        // 修改
                        for(let i=0; i<this.tableData.length; i++) 
                        {
                            if(this.tableData[i].uuid == uuid)
                            {
                                this.tableData[i] = new_data;
                            }
                        }
                        this.$message.success('修改记录成功!');
                    }
                    else
                    {
                        //生成uuid
                        new_data.uuid = uuid();
                        console.dir(new_data);
                        //新增
                        this.tableData.unshift(new_data);
                        this.$message.success('新增记录成功!');
                    }

                    //更新数据,并关闭
                    this.tableKey = Math.random();
                }
                else
                {
                    //报错
                    this.$message.warning('提交记录失败!');
                }

                this.open_dialog = false;
            }).catch((res)=>{
                // 异常
                console.dir(res);
                this.$message.error('服务器跑路了～');
            })
        },
        /*单条目创建*/
        creatNewitem(){
            /*无索引*/
            this.editIndex = -1;
            this.editDefault = {
                creat_date: date2str(new Date()),
                prjname: '',
                prjtype: [],
                brief: '',
                region: '',
                period: 1,
                percent: 0,
                status: '执行中',
                duty_persons: [getCookie("username")]
            };
            this.open_dialog = true;
        },
        /*单条目编辑*/
        affairEdit(index,row){
            //给进索引
            this.editIndex = index;
            //设置默认值
            this.editDefault = row;
            //弹编辑窗口
            this.open_dialog = true;
        },
        /*单条目删除*/
        affairDelete(index,row){
            this.$confirm('此操作将删除此条项目记录,是否执行?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                console.dir(123123123);
                let req = new Object();

                req.uuid = row.uuid;
                axios({
                    url:'/affair',
                    method: 'delete',
                    timeout: 1000,
                    responseType: 'json',
                    responseEncoding: 'utf8', 
                    headers: {
                            'Content-Type': 'application/json;charset=UTF-8'
                    },
                    data: req
                }).then((res) => {
                    //如果成功
                    if(res.data.message == "删除成功")
                    {
                        this.$message({
                            type: 'success',
                            message: `删除成功!`
                        });

                        for(let i=0; i<this.tableData.length; i++) 
                        {
                            if(this.tableData[i].uuid == row.uuid)
                            {
                                this.tableData.splice(i,1);
                            }
                        }
                    }
                }).catch((error)=>{
                    //Do nothing
                    console.dir(error);
                }); 
            }).catch(() => {
            });
        },
        /* 提交项目记录 */
        affairPut(single_affair){
            return new Promise(function (resolve, reject) {
                //提交项目变更
                axios({
                    url:'/affair',
                    method: 'put',
                    timeout: 1000,
                    responseType: 'json',
                    responseEncoding: 'utf8', 
                    headers: {
                            'Content-Type': 'application/json;charset=UTF-8'
                    },
                    data:single_affair
                }).then((res) => {
                    if(res.data.message == "插入成功") 
                    {
                        resolve(true);
                    }
                    else{
                        resolve(false);
                    }
                }).catch((res)=>{
                    //Do nothing
                    reject(res);
                }); 
            });
        },
        /* 导出当前记录 */
        exportItem(){
            alert("todo 导出");
        }
    },
    created() {},
    mounted() {
        let indexPath;

        this.selectItemWithStatus(this.table_status,indexPath);
    },
    updated() {},
    destroyed() {}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    .el-header {
        color: #333;
        background-color:#545c64;
        padding: 0px;
    }
    .el-header > .el-col{
        height: 100%;
    }
    .el-header .timerange{
        display:flex;
        justify-content:center;/*主轴上居中*/
        align-items:center;/*侧轴上居中*/
        color:#fff;
    }
    
    .el-menu,.el-menu-item {
        height: 100%;
    }

    /* pre标签自动换行 */
    pre {
        white-space: pre-wrap;
        word-wrap: break-word;
    }

    .el-aside {
        background-color: #6db4fa;
        color: #333;
        text-align: center;
        line-height: 200px;
    }
    .el-main {
        background-color: #c2d6ec;
        color: #333;
        display:inline-block;
        padding:1px 0 0 0 ;
        height:fit-content;
    }

    .el-table .warning-row {
        background: #E6A23C;
    }

    .el-table .success-row {
        background: #67C23A;
    }

    /* 滚动条空出的th和其它标题栏背景一致 */
    .el-table >>> .gutter
    {
        border-bottom: 1px solid #EBEEF5;
        background: #303133;
    }

    .el-footer {
        background-color: #545c64;
        color: #007ffd;
        text-align: center;
        line-height: 40px;
    }

    /* 修改分页器按键背景 */
    .el-pagination{
        padding: 0 0;
    }

    .el-pagination >>> button,.el-pagination >>> button:disabled,.el-pagination >>> li{
        background-color: #545c64;
    }

    .el-pagination >>> li.active{
        color: #83baf0;
    }

</style>
