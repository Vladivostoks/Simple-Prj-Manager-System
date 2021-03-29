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
                v-show="table_status=='create'">
            <el-date-picker v-model="weekRange"
                            type="week"
                            disabled
                            value-format="timestamp"
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
                v-show="table_status=='complete'">
            <el-switch  style="display: block;padding: 20px"
                        active-text="最后更新时间"
                        inactive-text="创建时间"
                        v-model="week_switch"
                        @change="rangeTypeChange()">
            </el-switch>
            <el-date-picker v-show="isUpdateTime"
                            v-model="weekRange"
                            @change="timeRangeChange()"
                            type="week"
                            format="自yyyy 第 WW 周"
                            placeholder="选择周">
            </el-date-picker>
            <el-date-picker v-show="!isUpdateTime"
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
                type="success"
                v-show="table_status=='create'"
                @click="easyExport()">一键导出</el-button>
            <el-button
                size="mini"
                type="primary"
                v-show="table_status=='create'"
                @click="creatNewitem()">新建项目记录</el-button>
            <el-button
                size="mini"
                type="success"
                @click="curpageExport()">导出当前显示项目</el-button>
        </el-col>
        <el-col :span="1"> 
        </el-col>
    </el-header>
    <el-main>
        <el-table
            ref="data_table"
            :data="show_data"
            height="100%"
            :key="tableKey"
            :cell-style="cellStyle"
            :header-cell-style="headercellStyle"
            v-loading="loading"
            element-loading-text="加载中"
            element-loading-spinner="el-icon-loading"
            element-loading-background="rgba(0, 0, 0, 0.8)"
            style="width: 100%">
            <el-table-column type="expand">
                <template v-slot="scope">
                    <self-timeline 
                    @timeline-submit="timelineSubmit"
                    :isEditable="table_status!='complete'"
                    :project_uuid="scope.row.uuid"
                    :project_status="getSchemeType(scope.$index,scope.row)"
                    :project_index="scope.row.uuid">
                    </self-timeline>
                </template>
            </el-table-column>
            <el-table-column
                min-width="1%"
                type="index">
            </el-table-column>
            <el-table-column
                prop="create_date"
                min-width="6%"
                label="创建日期">
                <template v-slot="scope">
                    <div style="display:none">{{scope.row.uuid}}</div>
                {{ date2str(new Date(scope.row.create_date)) }}
                </template>
            </el-table-column>
            <el-table-column
                prop="region"
                min-width="5%"
                :filters="regionOpt"
                :filter-method="tableFilter"
                label="区域">
            </el-table-column>
            <el-table-column
                prop="prjmodel"
                min-width="5%"
                :filters="modelOpt"
                :filter-method="tableFilter"
                label="产品型号">
                <template v-slot="scope">
                    <el-tag 
                    disable-transitions
                    type="info"
                    size="small"
                    style="margin: 1px;"
                    v-for="item in scope.row.prjmodel"
                    :key="item">
                        {{ item }}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column
                prop="prjname"
                min-width="10%"
                label="项目名称">
            </el-table-column>
            <el-table-column
                min-width="7%"
                prop="prjtype"
                :filters="typeOpt"
                :filter-method="tableFilter"
                label="项目类型">
                <template v-slot="scope">
                    <el-tag 
                    disable-transitions
                    type="danger"
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
                <template v-slot="scope">
                <pre>{{ scope.row.brief }}</pre>
                </template>
            </el-table-column>
            <el-table-column
                prop="svnurl"
                min-width="10%"
                label="svn/git地址">
            </el-table-column>
            <el-table-column
                prop="period"
                min-width="8%"
                label="已执行/预计时间">
                <template v-slot="scope">
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
                min-width="8%"
                prop="status"
                :filters="statusOpt"
                :filter-method="tableFilter"
                label="执行状态">
                <template v-slot="scope">
                    <self-processline 
                    :percent="scope.row.percent"
                    :status="scope.row.status">
                    </self-processline>
                </template>
            </el-table-column>
            <el-table-column
                min-width="8%"
                prop="duty_persons"
                :filters="personOpt"
                :filter-method="tableFilter"
                label="当前处理人员">
                <template v-slot="scope">
                    <el-tag 
                    disable-transitions
                    type="success"
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
                <template v-slot="scope">
                    <el-tag 
                    disable-transitions 
                    size="small"
                    style="margin: 1px;"
                    v-for="item in scope.row.relate_persons"
                    :key="item">
                        {{ item }}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column 
                min-width="10%"
                align="right">
                <template v-slot:header>
                    <el-input v-model="search"
                              size="mini"
                              style="width:140px;margin-left:10px;"
                              @keyup.enter.native="filterWithKeyWords(search)"
                              :filter-method="tableFilter"
                              placeholder="输入搜索关键字"/>
                </template>
                <template v-slot:default="scope">
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
        <export-option v-if="open_export_dialog"
                       @dialog-close="exportOptSubmit"
                       @dialog-submit="exportOptSubmit"
                       :headLable="exportLabel"
                       :exportAction="exportAction"
                       :exportOption="exportOption"
        ></export-option>
    </el-main>
    <el-footer height="40px">
        <el-pagination
         layout="prev, pager, next"
         :page-size="2"
         :total="show_data.length">
        </el-pagination>
    </el-footer>
</el-container>
</template>

<script>
import XLSX from 'xlsx'
import XLSXStyle from 'xlsx-style'
import path from 'path'
import { saveAs } from 'file-saver'
import axios from 'axios'
import item_edit from '@/components/itemboard/dialog'
import time_line from '@/components/itemboard/timeline'
import process_line from '@/components/itemboard/progressline'
import exportOptionForm from '@/components/itemboard/exportForm'
import {getCookie,creatUuid,date2shortStr} from '@/assets/js/common.js'
import { exportExcel } from '@/assets/js/exportExcel.js'

/**
 * worksheet转成ArrayBuffer
 * @param {worksheet} s xlsx库中的worksheet
 * @returns {ArrayBuffer}
 */
function s2ab(s) {
    if (typeof ArrayBuffer !== 'undefined') {
        const buf = new ArrayBuffer(s.length)
        const view = new Uint8Array(buf)
        for (let i = 0; i !== s.length; ++i) {
        view[i] = s.charCodeAt(i) & 0xFF
        }
        return buf
    } else {
        const buf = new Array(s.length)
        for (let i = 0; i !== s.length; ++i) {
        buf[i] = s.charCodeAt(i) & 0xFF
        }
        return buf
    }
}

/**
 * 获取当前生效时间段
 * @param {Array} data_range timestamp array with size2 
 * @return {Object} 起始时间结束时间对
 */
function getTimeRange(data_range)
{
    let ret = new Object();

    //时间范围
    //ret.start_time = date2str(data_range[0]);
    //ret.end_time = date2str(data_range[1]);
    console.dir(new Date(data_range[0]))
    console.dir(new Date(data_range[1]))

    ret.start_time = data_range[0];
    ret.end_time = data_range[1];

    return ret;
}

/**
 * 递归查询
 * @param {Array/String/Object} dst_obj 待查询数组或者对象
 * @param {String} contet 模式串
 * @return {Boolean} 是否查询到
 */
function str_search(dst_obj,content)
{
    if(typeof(dst_obj) == "string")
    {
        return (dst_obj.search(content) != -1);
    }
    else if(typeof(dst_obj) == "object" 
            || typeof(dst_obj) == "array")
    {
        for(let key in dst_obj)
        {
            if(str_search(dst_obj[key],content))
            {
                return true;
            }
        }
    }
    else
    {
        //不支持的类型,直接跳过
        return false;
    }
}

/**
 * @description: 
 * @param {*} index
 * @param {*} row
 * @return {*}
 */
function getSchemeStrwithDate(period,date){
    let cur_timestamp = new Date().getTime();
    let start_timestamp = new Date(date).getTime();

    let week = (cur_timestamp - start_timestamp) / (1000 * 60 * 60 * 24 * 7);

    if(week<1)
    {
        week = 1;
    }
    else
    {
        week = Math.ceil(week);
    }

    return `${week}周/${period}周`;
}

/**
 * @description: 创建选项
 * @param {*} object
 * @param {*} key
 * @return {*}
 */
function createOpt(object,key){
    let index_t;
    let index_p;
    let set = new Set();
    let ret = [];

    /* 生成当前项目区域集合 */
    for(index_t in object)
    {
        if(Object.prototype.toString.call(object)=='[object Array]')
        {
            for(index_p in object[index_t][key])
            {
                set.add(object[index_t][key][index_p]);
            }
        }
        else
        {
            if(object[index_t][key] != null)
            {
                set.add(object[index_t][key]);
            }
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
}

export default {
  name: 'tempItemPage',
  data() {
        return {
            /* 表格加载 */
            loading: false,
            /* 当前列表展示时间 */
            weekRange: new Date(),
            /* 开关状态显示 */
            week_switch: true,
            isUpdateTime: true,
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
            /*缓存列表*/
            total_data:[],
            /*显示列表*/
            show_data:[{
                uuid: '2e0e322a-503a-47fd-b28b-3a1202b55502',
                create_date: new Date().getTime(),
                prjmodel: [],
                prjname: 'xx区域xx项目',
                brief: '客户反馈xx问题/客户新增xx需求',
                region: '西安',
                period: 20,
                percent: 80,
                status: '执行中',
                relate_persons: ['Ayden.Shu'],
                duty_persons: ['Ayden.Shu',"shuzhengyang"]
            }],
            /* 导出对话框 */
            open_export_dialog:false,
            /* 导出对话框标题 */
            exportLabel: "",
            /* 导出动作(闭包函数) */
            exportAction: ()=>{},
            /* 导出选项 */
            exportOption:[]
        }
    },
    props: {},
    components: {
        "self-timeline":time_line,
        "self-processline":process_line,
        "item-edit":item_edit,
        "export-option":exportOptionForm
    },
    computed: {
        statusOpt(){
            return createOpt(this.show_data,"status");
        },
        typeOpt(){
            return createOpt(this.show_data,"prjtype");
        },
        regionOpt(){
            return createOpt(this.show_data,"region");
        },
        modelOpt(){
            return createOpt(this.show_data,"prjmodel");
        },
        personOpt(){
            return createOpt(this.show_data,"duty_persons");
        },
        relationOpt(){
            return createOpt(this.show_data,"relate_persons");
        }
    },
    watch: {},
    methods: {
        //创建时间展示
        date2str:date2shortStr,
        /**
         * @description: 表头样式
         * @return {Object} 样式描述
         */
        headercellStyle({row, column, rowIndex, columnIndex}){
            return {height: "20px",background: "#303133"};
        },
        /**
         * @description: 表头样式
         * @return {Object} 样式描述
         */
        cellStyle({row, column, rowIndex, columnIndex}){
            let date = new Date();
            let nowDayOfWeek = date.getDay(); //今天本周的第几天
            let nowDay = date.getDate(); //当前日
            let nowMonth = date.getMonth(); //当前月
            let nowYear = date.getFullYear(); //当前年

            date = new Date(nowYear, nowMonth, nowDay - nowDayOfWeek+1);

            if(row.lastupdate_date<date.getTime() || row.percent == 0)
            {
                return {background: "#C6E2FF"};
            }
        },
        /* 按照内容只展示检索字段 */
        filterWithKeyWords(search){
            console.dir("search:"+search);
            this.loading = true;
            if(search !== "")
            {
                let show_data=[];

                for(let i in this.total_data)
                {
                    if(str_search(this.total_data[i],search))
                    {
                        show_data.push(this.total_data[i]);
                    }
                }

                this.show_data = show_data;
                console.dir(this.show_data);
            }
            else
            {
                this.show_data = this.total_data;
                console.dir(this.show_data);
            }
            this.tableKey = Math.random();
            this.loading = false;
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
            let start_timestamp = new Date(row.create_date).getTime();

            let week = (cur_timestamp - start_timestamp) / (1000 * 60 * 60 * 24 * 7);

            week = Math.ceil(week);

            if(week > row.period)
            {
                return "error"
            }
            else if(week >= row.period)
            {
                return "warning"
            }
            
            return "success";
        },
        /* 获取规划字符串 */
        getSchemeStr(index,row){
            return getSchemeStrwithDate(row.period,row.create_date);
        },
        /* 时间选择创建时间还是最后更新时间 */
        rangeTypeChange(){
            //值变化且原来是数组
            if(!this.isUpdateTime)
            {
                this.weekRange = this.weekRange[0];
            }
            else
            {
                let date = new Date(this.weekRange);//当前日期
                let nowDayOfWeek = date.getDay(); //今天本周的第几天
                let nowDay = date.getDate(); //当前日
                let nowMonth = date.getMonth(); //当前月
                let nowYear = date.getFullYear(); //当前年

                this.weekRange = new Array();
                this.weekRange[0] = new Date(nowYear, nowMonth, nowDay - nowDayOfWeek+1);
                this.weekRange[1] = new Date(nowYear, nowMonth, nowDay + (8 - nowDayOfWeek));
            }
            this.isUpdateTime = !this.isUpdateTime;
        },
        /* 时间选择器产生变化,需要更新表单 */
        timeRangeChange(){
            let time_range = new Array();
            let self = this;

            if(!this.isUpdateTime)
            {
                /* 重新触发检索过程 */
                time_range = this.weekRange;
            }
            else
            {
                let date = new Date(this.weekRange);
                let nowDayOfWeek = date.getDay(); //今天本周的第几天
                let nowDay = date.getDate(); //当前日
                let nowMonth = date.getMonth(); //当前月
                let nowYear = date.getFullYear(); //当前年

                time_range[0] = new Date(nowYear, nowMonth, nowDay - nowDayOfWeek+1);
                time_range[1] = new Date(nowYear, nowMonth, nowDay + (8 - nowDayOfWeek));
            }
            
            for(let i in time_range)
            {
                time_range[i] = time_range[i].getTime();
            }

            /* 重新触发检索过程 */
            this.loading = true;
            this.affairGet(getTimeRange(time_range),this.table_status,this.isUpdateTime).then((data)=>{
                self.loading = false;
                self.total_data = data;
                self.show_data = self.total_data;
            });
        },
        /* 时间线更新 */
        timelineSubmit(uuid,percent){
            // 联动项目更新
            for(let i=0; i<this.show_data.length; i++) 
            {
                if(this.show_data[i].uuid == uuid)
                {
                    this.show_data[i].percent = percent;
                    this.affairPut(this.show_data[i]).then(()=>{
                        //更新数据显示
                        this.tableKey = Math.random();
                    });
                    break;
                }
            }
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

                time_range[0] = new Date(nowYear, nowMonth, nowDay - nowDayOfWeek+1).getTime();
                time_range[1] = new Date(nowYear, nowMonth, nowDay + (8 - nowDayOfWeek)).getTime();
            }
            else if(index === "incomplete")
            {
                // 时间跨度为本周前未完成
                time_range[0] = new Date(1970, 1, 1).getTime();

                let now = new Date();//当前日期

                time_range[1] = now.getTime();
            }
            else if(index === "complete")
            {
                // 默认为最后更新时间为检索条件
                this.isUpdateTime = true;
                this.week_switch = true;

                // 默认时间为上周完成的
                let now = new Date();//当前日期
                let nowDayOfWeek = now.getDay(); //今天本周的第几天
                let nowDay = now.getDate(); //当前日
                let nowMonth = now.getMonth(); //当前月
                let nowYear = now.getFullYear(); //当前年

                time_range[0] = new Date(nowYear, nowMonth, nowDay - nowDayOfWeek+1).getTime();
                time_range[1] = new Date(nowYear, nowMonth, nowDay + (8 - nowDayOfWeek)).getTime();
            }
            /* week设置为一周最后周日时间 */
            this.weekRange = new Date(time_range[0]);
            
            /* 重新触发检索过程 */
            this.loading = true;
            this.affairGet(getTimeRange(time_range),index,this.isUpdateTime).then((data)=>{
                self.loading = false;
                self.total_data = data;
                self.show_data = self.total_data;
                /* 生成提示信息 */
                for(let index in self.show_data)
                {
                    let data = self.show_data[index];

                    if(data.status == "已完成" || data.status == "已终止")
                    {
                        continue;
                    }

                    let cur_timestamp = new Date().getTime();
                    let start_timestamp = new Date(data.create_date).getTime();
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
                    else if(week >= data.period)
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
                self.loading = false;
                console.dir(res);
            });
        },
        /* 触发表单更新 */
        affairGet(data_range,table_status,isUpdateTime){
            //触发检索
            let req = data_range;

            if(table_status === "incomplete")
            {
                req.iscomplete = false;
            }
            else if(table_status === "complete")
            {
                req.iscomplete = true;
                req.isupdatetime = isUpdateTime;
            }

            return new Promise(function (resolve, reject) {
                axios({
                    url:'/affair',
                    method: 'get',
                    timeout: 5000,
                    responseType: 'json',
                    responseEncoding: 'utf8', 
                    params: req
                }).then((res) => {
                    resolve(res.data);
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
            if(!uuid)
            {
                //表单未提供uuid,说明此为新建项目,生成uuid
                new_data.uuid = creatUuid();
            }

            //编辑数据更新
            this.affairPut(new_data).then((res)=>{
                if(res)
                {
                    if(uuid)
                    {
                        // 修改
                        for(let i=0; i<this.show_data.length; i++) 
                        {
                            if(this.show_data[i].uuid == uuid)
                            {
                                this.show_data[i] = new_data;
                                break;
                            }
                        }
                        this.$message.success('修改记录成功!');
                    }
                    else
                    {
                        //新增
                        this.show_data.unshift(new_data);
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
                create_date: new Date().getTime(),
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
                let req = new Object();

                req.uuid = row.uuid;
                axios({
                    url:'/affair',
                    method: 'delete',
                    timeout: 5000,
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

                        for(let i=0; i<this.show_data.length; i++) 
                        {
                            if(this.show_data[i].uuid == row.uuid)
                            {
                                this.show_data.splice(i,1);
                                break;
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
                    timeout: 5000,
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
        /**
         * @description: 导出项目表单提交
         */
        exportOptSubmit(){
            this.open_export_dialog = false;
        },
        /**
         * @description: 生成导出项目
         * @return {Object} 返回生成的导出选项
         */
        createExportOpt(data){
            let columns = new Object();

            for(let i in this.$refs.data_table.$slots.default)
            {
                if(this.$refs.data_table.$slots.default[i].componentOptions
                    && this.$refs.data_table.$slots.default[i].componentOptions.propsData.prop)
                {
                    let item = this.$refs.data_table.$slots.default[i].componentOptions.propsData;

                    //使用表格里的label和name生成columns,并和tableData对应
                    columns[item.prop]=new Object();
                    columns[item.prop].name = item.label;
                    switch (item.prop)
                    {
                        case 'prjname':{
                            columns[item.prop].wpx = 140;
                            columns[item.prop].alignment = new Object();
                            columns[item.prop].alignment.wrapText = true;
                            break;
                        } 
                        case 'brief': {
                            columns[item.prop].wpx = 200;
                            columns[item.prop].alignment = new Object();
                            columns[item.prop].alignment.wrapText = true;
                            break;
                        }
                        case 'prjtype':{
                            columns[item.prop].wpx = 110;
                            columns[item.prop].alignment = new Object();
                            columns[item.prop].alignment.wrapText = true;
                        }
                        default: columns[item.prop].wpx = 90; break;
                    }
                }
            }

            //添加具体内容选项,后续导出前进行展开
            columns["temp_content"] = new Object();
            columns["temp_content"].name = "具体内容";
            columns["temp_content"].dateRange = [new Date(),new Date()];
            columns["temp_content"].wpx = 240;
            columns["temp_content"].alignment = new Object();
            columns["temp_content"].alignment.wrapText = true;

            //时间范围按照data中时间最早的算
            for(let i in data)
            {
                if(data[i].create_date <columns["temp_content"].dateRange[0].getTime())
                {
                    columns["temp_content"].dateRange[0] = new Date(data[i].create_date);
                }
            }

            return columns;
        },
        /* 导出当前页的记录 */
        curpageExport(){
            //靠挂合成在时间列里隐藏的uuid把具体数据都倒出来,uuid处于第c列
            let tableDom = document.querySelector(".el-table__body-wrapper table");
            let tempSheet = XLSX.utils.table_to_book(tableDom).Sheets.Sheet1;
            let data = [];

            for(let key in tempSheet)
            {
                if(key.search("C") != -1)
                {
                    for(let i in this.show_data)
                    {
                        if(tempSheet[key].v.search(this.show_data[i].uuid) != -1)
                        {
                            //应该push clone
                            data.push(Object.assign({},this.show_data[i]));
                            break;
                        }
                    }
                }
            }

            this.exportAction = async function (columns,dateRange){
                //根据最新到表单项进行导出数据生成
                let filename = new Date().toString()+" 当前页面导出.xlsx";
                let head_style = {
                                    fill: {
                                        fgColor: { rgb: 'FFA3F4B1' }
                                    },
                                    font: {
                                        name: '宋体',
                                        sz: 12,
                                        bold: true
                                    },
                                    border: {
                                        bottom: {
                                        style: 'thin',
                                        color: 'FF000000'
                                        }
                                    }
                                };
                let workbook = XLSX.utils.book_new();
                let bookType = null;
                let ext = path.extname(filename);

                if (ext == null)
                {
                    filename += '.xlsx';
                    bookType = 'xlsx';
                }
                else
                {
                    bookType = ext.substr(1).toLowerCase();
                }

                let sheetname = "当前页面显示导出"
                let style_conf = null;
                               
                //完成数据合规,data为闭包前导入
                for(const j in data)
                {
                    for(const k in data[j])
                    {
                        //时间戳转时间
                        if(k == "create_date")
                        {
                            data[j][k] = date2shortStr(data[j][k]);
                        }
                        else if(k == "period")
                        {
                            data[j][k] = getSchemeStrwithDate(data[j].period,data[j].create_date);
                        }
                        else if(k == "status")
                        {
                            data[j][k] = data[j][k]+"("+data[j].percent+"%)";
                        }
                        
                        //数组转字符串
                        if(Object.prototype.toString.call(data[j][k])=='[object Array]')
                        {
                            //转数组为字符串
                            data[j][k] = data[j][k].toString();
                        }
                    }
                }

                //补充具体内容 columns
                for(let i in data)
                {
                    //生成具体内容,并插入到data中
                    await time_line.methods.getLineContent(data[i].uuid,dateRange).then((timelineData)=>{
                        for(let key in columns)
                        {
                            //查询具有具体时间的列
                            if(columns[key].dateRange)
                            {
                                // console.dir("-----------------------");
                                // console.dir(timelineData);
                                // console.dir(columns[key].dateRange);
                                let content = time_line.methods.line2Text(timelineData,columns[key].dateRange);
                                if(content)
                                {
                                    data[i][columns[key].name] = content;
                                }
                            }
                        }
                    }).catch((err)=>{
                        console.dir(data[i].uuid+":"+err);
                    });
                }

                workbook.SheetNames.push(sheetname);
                workbook.Sheets[sheetname] = exportExcel(data,
                                                         columns,
                                                         bookType,
                                                         head_style,
                                                         style_conf);

                let wbOut = XLSXStyle.write(workbook, { bookType: bookType, bookSST: false, type: 'binary' });

                saveAs(new Blob([s2ab(wbOut)], { type: '' }), filename);
            };
            this.exportOption = this.createExportOpt(data);
            this.exportLabel = "当前页面展示内容导出";
            this.open_export_dialog = true;
        },
        /* 一键导出当前记录 */
        async easyExport(){
            let self = this;

            this.exportAction = async function (columns,dateRange){
                var weekCount = function(){
                    let curDate = new Date();
                    let date = new Date();
                    // 设置本年的第一天
                    date.setMonth(0);
                    date.setDate(1);
                    let dateGap = curDate.getTime() - date.getTime();
                    return Math.ceil(dateGap /(7*24*60*60*1000));
                }

                let filename = "第"+weekCount()+"周周报.xlsx";

                let sheet_table = ['create','complete','incomplete'];
                let head_style= {
                                    fill: {
                                        fgColor: { rgb: 'FFA3F4B1' }
                                    },
                                    font: {
                                        name: '宋体',
                                        sz: 12,
                                        bold: true
                                    },
                                    border: {
                                        bottom: {
                                        style: 'thin',
                                        color: 'FF000000'
                                        }
                                    }
                                };
                let workbook = XLSX.utils.book_new();
                let bookType = null;
                let ext = path.extname(filename);
                if (ext == null)
                {
                    filename += '.xlsx';
                    bookType = 'xlsx';
                }
                else
                {
                    bookType = ext.substr(1).toLowerCase();
                }

                //按照三个表生成
                for(const i in sheet_table)
                {
                    let time_range = new Array(2);
                    let is_updatetime = false;
                    let sheetname = "本周新增"
                    let style_conf = null;

                    // 时间生成为当前周的
                    let now = new Date();//当前日期
                    let nowDayOfWeek = now.getDay(); //今天本周的第几天
                    let nowDay = now.getDate(); //当前日
                    let nowMonth = now.getMonth(); //当前月
                    let nowYear = now.getFullYear(); //当前年

                    time_range[0] = new Date(nowYear, nowMonth, nowDay - nowDayOfWeek+1).getTime();
                    time_range[1] = new Date(nowYear, nowMonth, nowDay + (8 - nowDayOfWeek)).getTime();

                    //和页面显示获取时间一致
                    if(sheet_table[i] === "create")
                    {
                        sheetname = "本周新增"
                        style_conf = null;
                    }
                    else if(sheet_table[i] === "incomplete")
                    {
                        time_range[0] = new Date(1970, 1, 1).getTime();
                        time_range[1] = new Date().getTime();
                        style_conf = null;
                        sheetname = "未完成"
                    }
                    else if(sheet_table[i] === "complete")
                    {
                        style_conf = null;
                        sheetname = "已完成"
                        is_updatetime = true;
                    }

                    await self.affairGet(getTimeRange(time_range),sheet_table[i],is_updatetime).then(async function(data){
                        if(sheet_table[i] != "create")
                        {
                            for(let j=data.length-1;j>=0;j--)
                            {
                                //剔除已完成和未完成的本周项目
                                if(data[j].create_date>new Date(nowYear, nowMonth, nowDay - nowDayOfWeek+1).getTime())
                                {
                                    data.splice(j, 1);
                                }
                            }
                        }

                        //完成数据合规
                        for(const j in data)
                        {
                            for(const k in data[j])
                            {
                                //时间戳转时间
                                if(k == "create_date")
                                {
                                    data[j][k] = self.date2str(data[j][k]);
                                }
                                else if(k == "period")
                                {
                                    data[j][k] = self.getSchemeStr(null,data[j]);
                                }
                                else if(k == "status")
                                {
                                    data[j][k] = data[j][k]+"("+data[j].percent+"%)";
                                }

                                //数组转字符串
                                if(Object.prototype.toString.call(data[j][k])=='[object Array]')
                                {
                                    //转数组为字符串
                                    data[j][k] = data[j][k].toString();
                                }
                            }
                        }

                        //补充具体内容 columns
                        for(let i in data)
                        {
                            //生成具体内容,并插入到data中
                            await time_line.methods.getLineContent(data[i].uuid,dateRange).then((timelineData)=>{
                                for(let key in columns)
                                {
                                    //查询具有具体时间的列
                                    if(columns[key].dateRange)
                                    {
                                        // console.dir("-----------------------");
                                        // console.dir(timelineData);
                                        // console.dir(columns[key].dateRange);
                                        let content = time_line.methods.line2Text(timelineData,columns[key].dateRange);
                                        if(content)
                                        {
                                            data[i][columns[key].name] = content;
                                        }
                                    }
                                }
                            }).catch((err)=>{
                                console.dir(data[i].uuid+":"+err);
                            });
                        }

                        workbook.SheetNames.push(sheetname);
                        workbook.Sheets[sheetname] = exportExcel(data,
                                                                 columns,
                                                                 bookType,
                                                                 head_style,
                                                                 style_conf);
                    }).catch((res)=>{
                        console.dir(res);
                    });
                }

                let wbOut = XLSXStyle.write(workbook, { bookType: bookType, bookSST: false, type: 'binary' });

                saveAs(new Blob([s2ab(wbOut)], { type: '' }), filename);
            }

            this.exportOption = this.createExportOpt(null);
            this.exportLabel = "完整周报导出";
            this.open_export_dialog = true;
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

    .el-progress--line >>> .el-progress-bar{
        padding-right: 10px;
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
