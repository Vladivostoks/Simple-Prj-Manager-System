<!--单项目细节-->
<template>
    <el-drawer size="40%"
               :title="affair.prjname"
               :visible.sync="drawer"
               @closed="handleClose"
               direction="rtl">
    <el-collapse v-model="activeName" style="width:100%;">
        <el-collapse-item title="项目信息" name="1">
            <el-form label-position="right"
                     label-width="18%">
                <el-form-item label="创建日期">
                    <span>{{ new Date(affair.create_date) }}</span>
                </el-form-item>
                <el-form-item label="区域">
                    <span>{{ affair.region }}</span>
                </el-form-item>
                <el-form-item label="产品型号">
                    <el-tag 
                    disable-transitions
                    type="info"
                    size="small"
                    style="margin: 1px;"
                    v-for="item in affair.prjmodel"
                    :key="item">
                        {{ item }}
                    </el-tag>
                </el-form-item>
                <el-form-item label="项目类型">
                    <el-tag 
                    disable-transitions
                    type="danger"
                    size="small"
                    style="margin: 1px;"
                    v-for="item in affair.prjtype"
                    :key="item">
                        {{ item }}
                    </el-tag>
                </el-form-item>
                <el-form-item label="原始需求/反馈">
                    <pre >{{ affair.brief }}</pre>
                </el-form-item>
                <el-form-item label="svn/git路径">
                    <pre>{{ affair.svnurl }}</pre>
                </el-form-item>
                <el-form-item label="已执行/预计时间">
                    <el-alert
                    :description="schemeStr"
                    :closable="false"
                    center
                    style="padding: 2px 8px;"
                    :type="schemeType">
                    </el-alert>
                </el-form-item>
                <el-form-item label="执行状态">
                    <self-processline 
                    :percent="affair.percent"
                    :status="affair.status">
                    </self-processline>
                </el-form-item>
                <el-form-item label="当前处理人员">
                    <el-tag 
                    disable-transitions
                    type="success"
                    size="small"
                    style="margin: 1px;"
                    v-for="item in affair.duty_persons"
                    :key="item">
                        {{ item }}
                    </el-tag>
                </el-form-item>
                <el-form-item label="关联人员">
                    <el-tag 
                    disable-transitions
                    size="small"
                    style="margin: 1px;"
                    v-for="item in affair.relate_persons"
                    :key="item">
                        {{ item }}
                    </el-tag>
                </el-form-item>
            </el-form>
        </el-collapse-item>
        <el-collapse-item title="项目时间线" name="2">
            <self-timeline :isEditable="false"
                           :project_uuid="uuid">
            </self-timeline>
        </el-collapse-item>
    </el-collapse>
    </el-drawer>
</template>

<script>
import timeLine from '@/components/itemboard/timeline'
import processLine from '@/components/itemboard/progressline'
import {affairGetWithID} from '@/assets/js/dataAxios.js'
import {getSchemeStrwithDate,getSchemeType} from '@/assets/js/common.js'

export default {
    name:"affair_detail",
    data() {
        return {
            drawer: false,
            activeName:["1","2"],
            /* 项目信息 */
            affair: {}
        };
    },
    props: {
        /* 事务ID */
        uuid: {
            type: String,
            required: true
        }
    },
    components: {
        "self-timeline":timeLine,
        "self-processline":processLine
    },
    computed: {
        schemeStr(){
            if(this.affair.status == "已完成"
            || this.affair.status == "已终止")
            {
                return getSchemeStrwithDate(this.affair.period,this.affair.create_date,this.affair.lastupdate_date);
            }
            else
            {
                return getSchemeStrwithDate(this.affair.period,this.affair.create_date);
            }
        },
        schemeType(){
            if(this.affair.status == "已完成"
            || this.affair.status == "已终止")
            {
                return getSchemeType(this.affair.period,this.affair.create_date,this.affair.lastupdate_date);
            }
            else
            {
                return getSchemeType(this.affair.period,this.affair.create_date);
            }
        }
    },
    watch: {},
    methods: {
        handleClose() {
            this.$emit("close");
        }
    },
    created() {},
    mounted() {
        affairGetWithID(this.uuid).then(res=>{
            this.affair = res.data[0];
            this.drawer = true;
        });
    },
    updated() {},
    destroyed() {}
}
</script>

<style scoped>
.el-drawer__wrapper >>> .el-drawer.rtl{
    overflow: scroll;
}

.el-form-item{
    margin-bottom: 5px;
}

.el-drawer__wrapper >>> .el-collapse-item__header{
    margin-left: 10px;
    font-size:15px;
}
</style>