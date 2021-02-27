<template>
<el-container>
    <el-header height="60px">
        <el-col :span="6" style="align-items:left;">
            <el-menu :default-active="chooseStatus"
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
                v-if="chooseStatus=='create'">
            <el-date-picker v-model="weekRange"
                            @change="tableUpdate(weekRange)"
                            type="week"
                            disabled
                            format="yyyy 第 WW 周"
                            placeholder="选择周">
            </el-date-picker>
        </el-col>
        <el-col :span="10"
                class="timerange"
                v-if="chooseStatus=='incomplete'">
        </el-col>
        <el-col :span="10"
                class="timerange"
                v-if="chooseStatus=='complete'">
            <el-switch  style="display: block;padding: 20px"
                        v-model="isWeekRange">
            </el-switch>
            <el-date-picker v-show="!isWeekRange"
                            v-model="weekRange"
                            @change="tableUpdate(weekRange)"
                            type="week"
                            format="自yyyy 第 WW 周起"
                            placeholder="选择周">
            </el-date-picker>
            <span v-show="isWeekRange">
                <el-date-picker
                v-model="weekRange"
                type="daterange"
                @change="tableUpdate(weekRange)"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期">
                </el-date-picker>
            </span>
        </el-col>
        <el-col :span="7" class="timerange">
            <el-button
                size="mini"
                type="primary"
                @click="creatNewitem()">新建项目记录</el-button>
            <el-button
                size="mini"
                type="success"
                @click="creatNewitem()">提交项目记录</el-button>
            <el-button
                size="mini"
                type="info"
                @click="creatNewitem()">导出当前记录</el-button>
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
            style="width: 100%">
            <el-table-column type="expand">
                <template slot-scope="scope">
                    <self-timeline 
                    :projectStatus="getSchemeType(scope.$index,scope.row)"
                    :project_index="{date:scope.row.date,name:scope.row.prjname}">
                    </self-timeline>
                </template>
            </el-table-column>
            <el-table-column
                min-width="3%"
                label="序号">
                <template slot-scope="scope">
                    {{ `${scope.$index}` }}
                </template>
            </el-table-column>
            <el-table-column
                prop="date"
                min-width="6%"
                label="创建日期">
            </el-table-column>
            <el-table-column
                prop="region"
                min-width="5%"
                label="区域">
            </el-table-column>
            <el-table-column
                prop="prjname"
                min-width="8%"
                label="项目名称">
            </el-table-column>
            <el-table-column
                min-width="5%"
                label="项目类型">
                <template slot-scope="scope">
                    <el-tag 
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
                prop="requirement"
                min-width="13%"
                label="原始需求/反馈">
            </el-table-column>
            <el-table-column
                prop="svnurl"
                min-width="14%"
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
                prop="persons"
                :filters="personPairset"
                :filter-method="tableFilter"
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
                min-width="6%"
                prop="link_persons"
                :filters="linkPersonPairset"
                :filter-method="tableFilter"
                label="关联人员">
                <template slot-scope="scope">
                    <el-tag 
                    type="warning"
                    size="small"
                    style="margin: 1px;"
                    v-for="item in scope.row.link_persons"
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
            @dialog-submit="updateData"
            :editIndex="editIndex"
            :value="editDefault"></item-edit>
    </el-main>
    <el-footer height="40px">
        <el-pagination
         layout="prev, pager, next"
         :total="1000">
        </el-pagination>
    </el-footer>
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
  name: 'tempItemPage',
  data() {
        return {
            dataRange: '',
            weekRange: new Date().toString(),
            isWeekRange: false,
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
            chooseStatus:"create",
            /*展示列表*/
            tableData:[{
                date: '2021-02-19',
                prjname: 'xx区域xx项目',
                requirement: '客户反馈xx问题/客户新增xx需求',
                region: '西安',
                scheme_week: 20,
                percent: 80,
                status: '执行中',
                link_persons: ['Ayden.Shu'],
                persons: ['Ayden.Shu',"shuzhengyang"]
            }, {
                date: '2021-02-20',
                prjname: 'xx区域xx项目',
                requirement: '客户反馈xx问题/客户新增xx需求',
                region: '西安',
                scheme_week: 20,
                percent: 80,
                status: '已完成',
                link_persons: ['Ayden.Shu'],
                persons:['Ayden.Shu']
            }, {
                date: '2021-02-21',
                prjname: 'xx区域xx项目',
                requirement: '客户反馈xx问题/客户新增xx需求',
                region: '西安',
                scheme_week: 20,
                percent: 80,
                status: '已终止',
                link_persons: ['Ayden.Shu'],
                persons:['Ayden.Shu']
            }, {
                date: '2021-02-22',
                prjname: 'xx区域xx项目',
                requirement: '客户反馈xx问题/客户新增xx需求',
                region: '西安',
                scheme_week: 20,
                percent: 80,
                status: '暂停中',
                link_persons: ['Ayden.Shu'],
                persons:['Ayden.Shu']
            }, {
                date: '2021-02-23',
                prjname: 'xx区域xx项目',
                requirement: '客户反馈xx问题/客户新增xx需求',
                region: '西安',
                scheme_week: 2,
                percent: 80,
                status: '执行中',
                link_persons: ['Ayden.Shu'],
                persons:['Ayden.Shu']
            }, {
                date: '2021-02-17',
                prjname: 'xx区域xx项目',
                requirement: '客户反馈xx问题/客户新增xx需求',
                region: '西安',
                scheme_week: 2,
                percent: 80,
                status: '执行中',
                link_persons: ['Ayden.Shu'],
                persons:['Ayden.Shu']
            }, {
                date: '2020-02-20',
                prjname: 'xx区域xx项目',
                requirement: '客户反馈xx问题/客户新增xx需求',
                region: '西安',
                scheme_week: 20,
                percent: 80,
                status: '执行中',
                link_persons: ['Ayden.Shu'],
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
    computed: {
        personPairset(){
            let index_t;
            let index_p;
            let set = new Set();
            let ret = [];

            /* 生成当前表格执行人员和关联人员集合 */
            for(index_t in this.tableData)
            {
                for(index_p in this.tableData[index_t].persons)
                {
                    set.add(this.tableData[index_t].persons[index_p]);
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
        linkPersonPairset(){
            let index_t;
            let index_p;
            let set = new Set();
            let ret = [];

            /* 生成当前表格执行人员和关联人员集合 */
            for(index_t in this.tableData)
            {
                for(index_p in this.tableData[index_t].link_persons)
                {
                    set.add(this.tableData[index_t].link_persons[index_p]);
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

        /* 时间范围 */
        tableUpdate(time_range){
            alert("更新table at"+time_range);
        },

        notify(msg_option) {
            this.notifyPromise = this.notifyPromise.then(this.$nextTick).then(()=>{
                this.$notify(msg_option);
            });
        },
        /* 获取执行进度和当前进度比较字符串 */
        getSchemeType(index,row){
            let cur_timestamp = new Date().getTime();
            let start_timestamp = new Date(row.date).getTime();

            let week = (cur_timestamp - start_timestamp) / (1000 * 60 * 60 * 24 * 7);

            week = Math.ceil(week);

            if(week > row.scheme_week)
            {
                return "error"
            }
            else if(week >= (row.scheme_week-1))
            {
                return "warning"
            }
            
            return "success";
        },
        getSchemeStr(index,row){
            let cur_timestamp = new Date().getTime();
            let start_timestamp = new Date(row.date).getTime();

            let week = (cur_timestamp - start_timestamp) / (1000 * 60 * 60 * 24 * 7);

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
        /*对话框事件*/
        closeEdit(){
            this.open_dialog = false;
        },
        updateData(new_data,index)
        {
            if(index>=0)
            {
                //编辑数据更新
                this.tableData[index] = new_data;
            }
            else
            {
                this.tableData.unshift(new_data);
            }

            //更新数据,并关闭
            this.tableKey = Math.random();
            this.open_dialog = false;
        },
        /*单条目创建*/
        creatNewitem(){
            /*无索引*/
            this.editIndex = -1;
            this.editDefault = {
                date: getDate(),
                prjname: '',
                prjtype: [],
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
        openEdit(index,row){
            //给进索引
            this.editIndex = index;
            //设置默认值
            this.editDefault = row;
            //弹编辑窗口
            this.open_dialog = true;
        },
        /*单条目删除*/
        handleDelete(index,row){
            this.$confirm('此操作将删除此条项目记录,是否执行?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                this.tableData.splice(index,1);
                this.$message({
                    type: 'success',
                    message: '删除成功!'
                });
            }).catch(() => {
            });
        },
        headStyle({row, column, rowIndex, columnIndex}){
            return {height: "20px",background: "#303133"};
        }
    },
    created() {},
    mounted() {
        
        let index;
        for(index in this.tableData)
        {
            let data = this.tableData[index];

            /* 生成提示信息 */
            let cur_timestamp = new Date().getTime();
            let start_timestamp = new Date(data.date).getTime();
            let week = (cur_timestamp - start_timestamp) / (1000 * 60 * 60 * 24 * 7);

            week = Math.ceil(week);
            if(week > data.scheme_week)
            {
                //弹框提示
                this.notify({
                    title: '超期提示',
                    type: 'error',
                    duration: 0,
                    message: `项目<${data.prjname}> 已经超过规划时间，请及时处理`
                });
            }
            else if(week >= (data.scheme_week-1))
            {
                //弹框提示
                this.notify({
                    title: '即将超期',
                    type: 'warning',
                    duration: 0,
                    message: `项目<${data.prjname}> 即将超期，请及时处理`
                });
            }
        }
    },
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
        color:#fff;
    }
    
    .el-menu {
        height: 100%;
    }

    .el-menu-item {
        height: 100%;
    }

    .el-footer {
        background-color: #90c1f1;
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

    /* 修改分页器按键背景 */
    .el-pagination >>> button{
        background-color: #90c1f1;
    }
    .el-pagination >>> li{
        background-color: #90c1f1;
    }
    .el-pagination >>> li.active{
        color: #067ef6;
    }

</style>
