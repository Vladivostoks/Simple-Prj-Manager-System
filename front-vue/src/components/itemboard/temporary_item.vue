<template>
<el-container>
    <el-header height="60px">
        <el-col :span="6">
            <el-menu    :default-active="chooseStatus"
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
        <el-col :span="14" class="timerange" v-if="chooseStatus!='create'">
            <el-switch
                style="display: block;padding: 20px"
                v-model="timeType">
            </el-switch>
            <el-date-picker v-show="timeType"
                v-model="dataRange"
                @change="tableUpdate(dataRange)"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期">
            </el-date-picker>
            <el-date-picker v-show="!timeType"
                v-model="weekRange"
                @change="tableUpdate(weekRange)"
                type="week"
                format="yyyy 第 WW 周"
                placeholder="选择周">
            </el-date-picker>
        </el-col>
        <el-col :span="14" v-else> </el-col>
        <el-col :span="4">
            <el-button
                size="mini"
                type="primary"
                @click="creatNewitem()">新建项目记录</el-button>
        </el-col>
    </el-header>
    <el-main>
        <el-table
            :data="tableData"
            height="100%"
            :header-cell-style="headStyle"
            :cell-style="cellStyle"
            style="width: 100%">
            <el-table-column type="expand">
                <template slot-scope="scope">
                    <self-timeline 
                    :project_index="{date:scope.row.date,name:scope.row.prjname}">
                    </self-timeline>
                </template>
            </el-table-column>
            <el-table-column
                prop="date"
                min-width="6%"
                label="创建日期">
            </el-table-column>
            <el-table-column
                prop="region"
                min-width="6%"
                label="区域">
            </el-table-column>
            <el-table-column
                prop="prjname"
                min-width="8%"
                label="项目名称">
            </el-table-column>
            <el-table-column
                prop="prjtype"
                min-width="5%"
                label="类型">
            </el-table-column>
            <el-table-column
                prop="requirement"
                min-width="15%"
                label="原始需求/反馈">
            </el-table-column>
            <el-table-column
                prop="svnurl"
                min-width="16%"
                label="svn地址">
            </el-table-column>
            <el-table-column
                min-width="10%"
                label="已执行/预计执行时间(周)">
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
                label="执行状态">
                <template slot-scope="scope">
                    <self-processline 
                    :percent="scope.row.percent"
                    :status="scope.row.status">
                    </self-processline>
                </template>
            </el-table-column>
            <el-table-column
                prop="persons"
                min-width="14%"
                label="当前处理人员">
                <template slot-scope="scope">
                    <el-tag 
                    size="small"
                    style="margin: 1px;"
                    v-for="item in scope.row.persons"
                    :key="item">
                        {{ item }}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column 
                min-width="10%"
                align="right">
                <template slot="header" slot-scope="scope">
                    <el-input
                    v-model="search"
                    size="mini"
                    placeholder="输入关键字搜索"/>
                </template>
                <template slot-scope="scope">
                    <el-button
                    size="mini"
                    @click="openEdit(scope.$index, scope.row)">Edit</el-button>
                    <el-button
                    size="mini"
                    type="danger"
                    @click="handleDelete(scope.$index, scope.row)">Delete</el-button>
                </template>
            </el-table-column>
        </el-table>
        <item-edit 
            v-if="open_dialog"
            @dialog-close="closeEdit"
            @dialog-submit="updateDate"
            :isEdit="isEdit"
            :value="editDefault"></item-edit>
    </el-main>
    <el-footer height="40px">button line</el-footer>
</el-container>
</template>

<script>
import axios from 'axios'
import item_edit from '@/components/itemboard/dialog'
import time_line from '@/components/itemboard/timeline'
import process_line from '@/components/itemboard/progressline'

function getDate(){
    let nowDate = new Date();
    let year = nowDate.getFullYear();
    let month = nowDate.getMonth() + 1 < 10 ? "0" + (nowDate.getMonth() + 1)
            : nowDate.getMonth() + 1;
    let day = nowDate.getDate() < 10 ? "0" + nowDate.getDate() : nowDate
            .getDate();
    return (year + "-" + month + "-" + day);
}

function getCookie(cname)
{
    var name = cname + "=";
    var ca = document.cookie.split(';');

    for(var i=0; i<ca.length; i++) 
    {
        var c = ca[i].trim();
        if (c.indexOf(name)==0) return c.substring(name.length,c.length);
    }
    return "";
}

export default {
  name: 'newItem',
  data() {
        return {
            dataRange: '',
            weekRange: '',
            timeType: true,
            /*打开编辑或者展示框*/
            isEdit: false,
            editDefault:{},     //  打开编辑框时候的默认参数
            open_dialog: false,
            /*检索显示内容*/
            search: '',
            /*当前展示当前表单类型 默认为本周新增*/
            chooseStatus:"create",
            /*展示列表*/
            tableData:[{
                date: '2021-02-19',
                prjname: '西安雷视项目',
                requirement: '客户反馈现场流量计数不准',
                region: '西安',
                scheme_week: 20,
                percent: 80,
                status: '执行中',
                persons: ['Ayden.Shu',"shuzhengyang"]
            }, {
                date: '2021-02-20',
                prjname: '西安雷视项目',
                requirement: '客户反馈现场流量计数不准',
                region: '西安',
                scheme_week: 20,
                percent: 80,
                status: '已完成',
                persons:['Ayden.Shu']
            }, {
                date: '2021-02-21',
                prjname: '西安雷视项目',
                requirement: '客户反馈现场流量计数不准',
                region: '西安',
                scheme_week: 20,
                percent: 80,
                status: '已终止',
                persons:['Ayden.Shu']
            }, {
                date: '2021-02-22',
                prjname: '西安雷视项目',
                requirement: '客户反馈现场流量计数不准',
                region: '西安',
                scheme_week: 20,
                percent: 80,
                status: '暂停中',
                persons:['Ayden.Shu']
            }, {
                date: '2021-02-23',
                prjname: '西安雷视项目',
                requirement: '客户反馈现场流量计数不准',
                region: '西安',
                scheme_week: 20,
                percent: 80,
                status: '执行中',
                persons:['Ayden.Shu']
            }, {
                date: '2021-02-17',
                prjname: '西安雷视项目',
                requirement: '客户反馈现场流量计数不准',
                region: '西安',
                scheme_week: 20,
                percent: 80,
                status: '执行中',
                persons:['Ayden.Shu']
            }, {
                date: '2021-02-20',
                prjname: '西安雷视项目',
                requirement: '客户反馈现场流量计数不准',
                region: '西安',
                scheme_week: 20,
                percent: 80,
                status: '执行中',
                persons:['Ayden.Shu']
            }, {
                date: '2021-02-20',
                prjname: '西安雷视项目',
                requirement: '客户反馈现场流量计数不准',
                region: '西安',
                scheme_week: 20,
                percent: 80,
                status: '执行中',
                persons:['Ayden.Shu']
            }, {
                date: '2021-02-20',
                prjname: '西安雷视项目',
                requirement: '客户反馈现场流量计数不准',
                region: '西安',
                scheme_week: 20,
                percent: 80,
                status: '执行中',
                persons:['Ayden.Shu']
            }, {
                date: '2021-02-20',
                prjname: '西安雷视项目',
                requirement: '客户反馈现场流量计数不准',
                region: '西安',
                scheme_week: 20,
                percent: 80,
                status: '执行中',
                persons:['Ayden.Shu']
            }, {
                date: '2021-02-20',
                prjname: '西安雷视项目',
                requirement: '客户反馈现场流量计数不准',
                region: '西安',
                scheme_week: 20,
                percent: 80,
                status: '执行中',
                persons:['Ayden.Shu']
            }, {
                date: '2021-02-20',
                prjname: '西安雷视项目',
                requirement: '客户反馈现场流量计数不准',
                region: '西安',
                scheme_week: 20,
                percent: 80,
                status: '执行中',
                persons:['Ayden.Shu']
            }, {
                date: '2021-02-20',
                prjname: '西安雷视项目',
                requirement: '客户反馈现场流量计数不准',
                region: '西安',
                scheme_week: 20,
                percent: 80,
                status: '执行中',
                persons:['Ayden.Shu']
            }, {
                date: '2021-02-20',
                prjname: '西安雷视项目',
                requirement: '客户反馈现场流量计数不准',
                region: '西安',
                scheme_week: 20,
                percent: 80,
                status: '执行中',
                persons:['Ayden.Shu']
            }, {
                date: '2021-02-20',
                prjname: '西安雷视项目',
                requirement: '客户反馈现场流量计数不准',
                region: '西安',
                scheme_week: 20,
                percent: 80,
                status: '执行中',
                persons:['Ayden.Shu']
            }, {
                date: '2021-02-20',
                prjname: '西安雷视项目',
                requirement: '客户反馈现场流量计数不准',
                region: '西安',
                scheme_week: 20,
                percent: 80,
                status: '执行中',
                persons:['Ayden.Shu']
            }, {
                date: '2021-02-20',
                prjname: '西安雷视项目',
                requirement: '客户反馈现场流量计数不准',
                region: '西安',
                scheme_week: 20,
                percent: 80,
                status: '执行中',
                persons:['Ayden.Shu']
            }, {
                date: '2021-02-20',
                prjname: '西安雷视项目',
                requirement: '客户反馈现场流量计数不准',
                region: '西安',
                scheme_week: 20,
                percent: 80,
                status: '执行中',
                persons:['Ayden.Shu']
            }]
        }
    },
    props: {},
    components: {
        "self-timeline":time_line,
        "self-processline":process_line,
        "item-edit":item_edit
    },
    computed: {},
    watch: {},
    methods: {
        tableUpdate(time_range){
            alert("更新table at"+time_range);
        },
        /* 获取执行进度和当前进度比较字符串 */
        getSchemeType(index,row){
            var cur_timestamp = new Date().getTime();
            var start_timestamp = new Date(row.date).getTime();

            var week = (cur_timestamp - start_timestamp) / (1000 * 60 * 60 * 24 * 7);

            week = Math.ceil(week);

            if(week > row.scheme_week)
            {
                return "error"
            }
            else if(week == (row.scheme_week-1))
            {
                return "warning"
            }
            
            return "success";
        },
        getSchemeStr(index,row){
            var cur_timestamp = new Date().getTime();
            var start_timestamp = new Date(row.date).getTime();

            var week = (cur_timestamp - start_timestamp) / (1000 * 60 * 60 * 24 * 7);

            if(week<1)
            {
                week = 1;
            }
            else
            {
                week = Math.ceil(week);
            }

            return `${week}周/${row.scheme_week}周`;
        },
        /* 根据项目类型进行暂时 */
        selectItemWithStatus(index,indexPath){
            this.chooseStatus = index;

            //发起请求并,后端筛选
            if(index === "create")
            {
            }
            else if(index === "incomplete")
            {

            }
            else if(index === "complete")
            {

            }
            
        },
        /*单条目创建*/
        creatNewitem(){
            this.isEdit = false;
            this.editDefault = {
                date: getDate(),
                prjname: '',
                prjtype: '',
                requirement: '',
                region: '',
                scheme_week: 2,
                percent: 0,
                status: '执行中',
                persons: [getCookie("username")]
            };
            this.open_dialog = true;
        },
        /*单条目编辑*/
        closeEdit(){
            this.open_dialog = false;
        },
        updateDate(new_date)
        {
            //更新数据
            this.open_dialog = false;
        },
        openEdit(index,row){
            this.isEdit = true;
            //设置默认值
            this.editDefault = row;
            //弹编辑窗口
            this.open_dialog = true;
        },
        /*单条目删除*/
        handleDelete(index,row){
            this.tableData.splice(index,1);
        },
        headStyle({row, column, rowIndex, columnIndex}){
            return {height: "20px",background: "#303133"};
        },
        cellStyle({row, column, rowIndex, columnIndex}){
        }
    },
    created() {},
    mounted() {},
    updated() {},
    destroyed() {}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    .el-container {
        height: 85vh;
    }

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
    }
    
    .el-menu {
        height: 100%;
    }

    .el-menu-item {
        height: 100%;
    }

    .el-footer {
        background-color: #409EFF;
        color: #333;
        text-align: center;
        line-height: 40px;
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
</style>
