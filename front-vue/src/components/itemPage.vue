<!--
 * @Author: Ayden.Shu
 * @Date: 2021-03-15 15:23:10
 * @LastEditTime: 2021-04-11 00:39:38
 * @Description: Item Page
-->
<template>
<el-container style="height: 100%;">
    <el-menu :default-active="currentItem.id?currentItem.id:'add'"
             background-color="#545c64"
             text-color="#fff"
             style="width:20vw;"
             @select="selectProject"
             active-text-color="#ffd04b">
        <el-submenu index="0">
            <template slot="title">
                <i class="el-icon-loading"></i>
                <span>执行中</span>
            </template>
            <el-menu-item v-for="item in prjDoing" :key="item.id" :index="item.id">
                <template v-slot:title>
                    <i class="el-icon-paperclip"></i>
                    <span>{{ item.name+'  '+item.version }}</span>
                </template>
            </el-menu-item>
        </el-submenu>
        <el-submenu index="1">
            <template slot="title">
                <i class="el-icon-finished"></i>
                <span>已完成</span>
            </template>
            <el-menu-item v-for="item in prjDone" :key="item.id" :index="item.id">
                <template v-slot:title>
                    <i class="el-icon-paperclip"></i>
                    <span>{{ item.name+'  '+item.version }}</span>
                </template>
            </el-menu-item>
        </el-submenu>
        <el-menu-item index="add">
            <template v-slot:title>
                <i class="el-icon-document-add"></i>
                <span style="color:#67C23A;">新建工程</span>
            </template>
        </el-menu-item>
    </el-menu>
    <el-main>
        <el-row class="piperow">
            <span>
                <vue-pipeline   ref="pipeline"
                                lineStyle="default"
                                :data="pipelineShowData"
                                :showArrow="true">
                </vue-pipeline>
            </span>
        </el-row>
        <el-row class="inforow">
            <el-card v-if="!beEdit" class="box-card" shadow="always">
                <template v-slot:header>
                    <div>
                        <span>{{currentItem.name+'  '+currentItem.version}}</span>
                        <el-button style="float: right; padding: 4px 4px;color: #F56C6C;" type="text" @click="deleteProject(currentItem.id)">删除项目</el-button>
                        <el-button style="float: right; padding: 4px 4px;" type="text" @click="selectProject(currentItem.id)">编辑项目</el-button>
                    </div>
                </template>
                <el-row type="flex" justify="space-around">
                <el-col :span="24">
                    <el-collapse v-model="activeName" style="width:100%;">
                        <!-- <el-collapse-item>
                            <template v-slot:title>
                            项目简介<i class="header-icon el-icon-info"></i>
                            </template> -->
                        <el-collapse-item title="简介" name="1">
                            <div>{{ currentItem.brief }}</div>
                        </el-collapse-item>
                        <el-collapse-item title="负责人" name="2">
                            <el-tag disable-transitions style="margin: 2px;" type="success" v-for="i in currentItem.dutyPersons" :key="i">{{i}}</el-tag>
                        </el-collapse-item>
                        <el-collapse-item title="预计时间" name="3">
                            <el-date-picker disabled
                                            v-model="currentItem.timeRanges"
                                            type="daterange"
                                            range-separator="至"
                                            start-placeholder="开始日期"
                                            end-placeholder="结束日期">
                            </el-date-picker>
                        </el-collapse-item>
                        <el-collapse-item title="关联事务列表" name="4">
                           <el-table :data="currentItem.linkAffairs.slice(1)"
                                      :key="Math.random()"
                                      style="width: 100%">
                                <el-table-column
                                label="关联事务"
                                prop="name"
                                min-width="50s%">
                                </el-table-column>
                                <el-table-column
                                label="状态"
                                prop="status"
                                min-width="50%">
                                </el-table-column>
                            </el-table> 
                        </el-collapse-item>
                    </el-collapse>
                </el-col>
                </el-row>
            </el-card>
            <el-card v-else class="box-card" shadow="always" >
                <template v-slot:header>
                    <span>项目名称 
                        <el-input v-model="currentItem.name"
                                           size="mini"
                                           style="width:20%;"
                                           maxlength="15"
                                           show-word-limit
                                           placeholder="输入项目名称"
                                           autocomplete="off"></el-input>
                        项目版本 
                        <el-input v-model="currentItem.version"
                                  size="mini"
                                  style="width:20%;"
                                  maxlength="8"
                                  show-word-limit
                                  placeholder="输入版本号"
                                  autocomplete="off">
                        </el-input>
                        <el-button style="float: right; padding: 4px 4px;color: #F56C6C;" type="text" @click="Cancel">取消</el-button>
                        <el-button style="float: right; padding: 4px 4px;color: #67C23A;" type="text" @click="Submit">提交修改</el-button>
                    </span>
                </template>
                <el-row type="flex" justify="space-around">
                <el-col :span="24">
                    <el-collapse v-model="activeName" style="width:100%;">
                        <el-collapse-item title="简介" name="1">
                            <el-input type="textarea"
                                      v-model="currentItem.brief"
                                      placeholder="输入项目简介"
                                      autocomplete="off"></el-input>
                        </el-collapse-item>
                        <el-collapse-item title="负责人" name="2">
                            <el-select
                                v-model="currentItem.dutyPersons"
                                multiple
                                filterable
                                allow-create
                                default-first-option
                                style="width:100%"
                                placeholder="选择处理人员">
                                <el-option
                                    v-for="item in dutyPersonList"
                                    :key="item"
                                    :label="item"
                                    :value="item">
                                </el-option>
                            </el-select>
                        </el-collapse-item>
                        <el-collapse-item title="预计时间" name="3">
                            <el-date-picker
                                v-model="currentItem.timeRanges"
                                @change="linkAffairListUpdate"
                                type="daterange"
                                range-separator="至"
                                start-placeholder="开始日期"
                                end-placeholder="结束日期">
                            </el-date-picker>
                        </el-collapse-item>
                        <el-collapse-item title="关联事务" name="4">
                            <el-table v-if='currentItem.linkAffairs.length>0'
                                      :data="currentItem.linkAffairs"
                                      :key="Math.random()"
                                      style="width: 100%">
                                <el-table-column
                                label="关联事务"
                                min-width="30%">
                                <template v-slot="scope">
                                    {{ scope.row.name }}
                                </template>
                                </el-table-column>
                                <el-table-column
                                label="后继事务"
                                min-width="30%">
                                <template slot-scope="scope">
                                    <el-select v-model="scope.row.next"
                                               multiple
                                               filterable
                                               @change="nextItemListChange"
                                               default-first-option
                                               style="width:100%"
                                               placeholder="选择后续任务名称">
                                        <el-option
                                            v-for="item in relateList"
                                            :key="item.id"
                                            :label="item.name"
                                            :value="item.id">
                                        </el-option>
                                    </el-select>
                                </template>
                                </el-table-column>
                            </el-table>
                        </el-collapse-item>
                    </el-collapse>
                </el-col>
                </el-row>
            </el-card>
        </el-row>
    </el-main>
</el-container>
</template>


<script>
import {itemPut,itemDelete,itemGet,getOption,affairGet} from '@/assets/js/dataAxios.js'
import {creatUuid} from '@/assets/js/common.js'
import VuePipeline from 'vue-pipeline'

const defaultItem = {
                    name:"无项目数据显示",
                    version:"",
                    brief:"",
                    dutyPersons:[],
                    timeRanges:[new Date(1970,1,1),new Date()],
                    linkAffairs:[{
                        id:"Start",
                        name:"Start",
                        next:[],
                    }]
                  };

export default {
    name: 'itemPage',
    data() {
        return {
            /* 项目列表 */
            items:[],
            // [{
            //     id:"uuid1",
            //     name:"视频测速功能开发",
            //     version:"V0.0.1",
            //     brief:"使用视频特征进行目标测速",
            //     dutyPersons:["Ayden","Shuzhengyang"],
            //     timeRanges:[new Date(),new Date()],
            //     linkAffairs:[{
            //         id:"Start",
            //         name:"Start",
            //         next:[],
            //     }]
            // }],
            /* 是否切换到添加工程页面 */
            beEdit:false,
            /* 当前面板表单 */
            currentItem: Object.assign({},defaultItem),
            /* 展开面板 */
            activeName:['1','2','3','4'],

            /* 负责人列表选项 */
            dutyPersonList:[],
            /* 关联列表选项 TODO */
            relateList:[]
            // [{
            //         id:"uuid1",
            //         name:"测试",
            //         status:"已完成",
            //         next:[],
            // }]
        }
    },
    components: {
        "pipe-line":VuePipeline,
    },
    watch:{
        pipelineShowData(newValue,oldValue){
            this.$nextTick(() => {
                // 如果不使用 nextTick的话，子组件方法内获取到的有可能是这次赋值之前的值，下次调用时才能获取到此次赋值的值（应该是跟 Vue的异步事件队列有关系）
                this.$refs["pipeline"].render();
            })
        }
    },
    computed: {
        prjDoing(){
            let ret = [];
            this.items.forEach((value,index,array) => {
                for(let i in value.linkAffairs)
                {
                    if(value.linkAffairs[i].id == "Start")
                    {
                        continue;
                    }

                    if(value.linkAffairs[i].status != "已完成"
                    && value.linkAffairs[i].status != "已终止")
                    {
                        ret.push(value);
                        break;
                    }
                }
            });
            return ret;
        },
        prjDone(){
            let ret = [];

            this.items.forEach((value,index,array) => {
                let flag = true;

                for(let i in value.linkAffairs)
                {
                    if(value.linkAffairs[i].id == "Start")
                    {
                        continue;
                    }

                    if(value.linkAffairs[i].status != "已完成" 
                    && value.linkAffairs[i].status != "已终止")
                    {
                        flag = false;
                        break;
                    }
                }

                if(flag)
                {
                    ret.push(value);
                }
            });
            return ret;
        },
        /**
         * @description: 获取当前页项目到pipeline,根据关联项目生成
         */
        pipelineShowData(){
            // let ret = [{
            //             name: "Start",
            //             hint: this.currentItem.timeRanges[0].toString(),
            //             status: "start",
            //             next: []
            //           }];
            let ret = new Array();
            const affairs = this.currentItem.linkAffairs;
            let indexWithidMap = new Object();
            let weightWithidMap = new Object();
            
            const statusMap={
                "未开始":"start",
                "执行中":"running",
                "暂停中":"paused",
                "已完成":"success",
                "已终止":"failure"
            };

            for(let i in affairs)
            {
                let node = new Object({
                    name: affairs[i].name,
                    hint: affairs[i].name,
                    //没状态视为没创建任务
                    status: statusMap[affairs[i].status]?statusMap[affairs[i].status]:"start",
                    next: affairs[i].next.slice(0),
                });
                
                ret.push(node);

                //同时记录位置和id,用于后续替换
                indexWithidMap[affairs[i].id] = parseInt(i);
                //3档weight 0:未创建任务 1:已创建但是未执行 2:正在执行
                switch(node.status){
                    case "unstable":
                    case "paused": weightWithidMap[affairs[i].id] = 1;break;
                    case "end":
                    case "failure": weightWithidMap[affairs[i].id] = 0;break;
                    case "running": 
                    case "success": weightWithidMap[affairs[i].id] = 2;break;
                    default: weightWithidMap[affairs[i].id] = 0;break;
                }
            }

            //将node节点中的next替换为真正的位置
            ret.forEach((node)=>{
                for(let i in node.next)
                {
                    node.next[i] = {
                        index: indexWithidMap[node.next[i]],
                        weight: weightWithidMap[node.next[i]]
                    }
                }
            })

            for(let i in ret)
            {
                if(ret[i].x)
                {
                    delete ret[i].x;
                }

                if(ret[i].y)
                {
                    delete ret[i].y;
                }
            }

            return ret;
            // [{
            //     name: "Start",
            //     hint: "1m23s",
            //     status: "start",
            //     next: [{ index: 1, weight: 2 }]
            // }]
        },
    },
    methods: {
        /* 后继项目列表改变 */
        nextItemListChange(currentValue)
        {
            let again = true;
            let item = this.currentItem;

            while(again)
            {
                let index_t;
                let index_p;
                let set = new Set();
                let ret = [];

                again = false;
                /* 生成列表应该显示的对象合集 */
                for(index_t in item.linkAffairs)
                {
                    for(index_p in item.linkAffairs[index_t].next)
                    {
                        set.add(item.linkAffairs[index_t].next[index_p]);
                    }
                }

                for(index_t in item.linkAffairs)
                {
                    if(item.linkAffairs[index_t].id == "Start")
                    {
                        continue;
                    }
                    // 检查set中还是否存在此事务
                    if(set.has(item.linkAffairs[index_t].id))
                    {
                        //同时从set中移除，set中剩下的就是需要添加的 
                        set.delete(item.linkAffairs[index_t].id);
                    }
                    else
                    {
                        //从linkAffairs删除
                        item.linkAffairs.splice(index_t,1);
                        again = true;
                    }
                }

                let array = Array.from(set);
                for(index_t in array)
                {
                    //从待选项列表中添加到linkAffairs
                    for(index_p in this.relateList)
                    {
                        if(this.relateList[index_p].id == array[index_t])
                        {
                            item.linkAffairs.push(Object.assign({},this.relateList[index_p]));
                            break;
                        }
                    }
                }
            }
        },
        /* 取消项目添加 */
        Cancel()
        {
            if(this.currentItem.id)
            {
                //重新单独获取一下这个项目
                itemGet(this.currentItem.id).then((data)=>{
                    this.currentItem = data[0];
                }).catch((err)=>{
                    this.$message({
                        type: 'error',
                        message: err,
                    });
                })
            }
            else
            {
                //新增项的取消处理
                if(this.items.length>0)
                {
                    this.currentItem = this.items[0];
                }
                else
                {
                    this.currentItem = Object.assign({},defaultItem);
                }
            }
            this.beEdit = false;
        },
        /* 提交项目添加 */
        Submit()
        {
            let flag = false;

            // 新项目创建uuid
            if(!this.currentItem.id)
            {
                this.currentItem.id = creatUuid();
                flag = true;
            }

            itemPut(this.currentItem).then((msg)=>{
                if(flag)
                {
                    this.items.push(this.currentItem);
                }
                this.$message({
                    type: 'success',
                    message: "项目记录提交成功!",
                });
            }).catch((err)=>{
                this.$message({
                    type: 'error',
                    message: "项目记录提交失败!",
                });
            });

            this.beEdit = false;
        },
        /* 删除项目 */
        deleteProject(projectId)
        {
            this.$confirm('此操作将删除此项目,是否执行?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                itemDelete(projectId).then(()=>{
                    this.$message({
                        type: 'success',
                        message: "项目删除成功",
                    });
                    for(let i in this.items)
                    {
                        if(this.items[i].id == projectId)
                        {
                            this.items.splice(i,1);
                            break;
                        }
                    }
                    if(this.items.length>0)
                    {
                        this.currentItem = this.items[0];
                    }
                    else
                    {
                        this.currentItem = defaultItem;
                    }
                }).catch(()=>{
                    this.$message({
                        type: 'error',
                        message: "项目删除失败",
                    });
                });
            }).catch(() => {
            });
        },
        /* 切换到项目/编辑界面 */
        selectProject(projectId,path)
        {
            if(projectId != "add" && path)
            {
                //切换项目展示
                for(let i in this.items)
                {
                    if(this.items[i].id == projectId)
                    {
                        this.currentItem = this.items[i];
                        break;
                    }
                }

                this.beEdit = false;
            }
            else
            {
                //切换项目编辑
                if(projectId == "add")
                {
                    this.currentItem = Object.assign({},defaultItem);
                }

                //生成当前编辑项的可选pipeline事务列表,只检索带基线版本标签的
                this.linkAffairListUpdate();

                //添加项目
                this.beEdit = true;
            }
        },
        /* 项目时间更新,后继项目选项的列表也要修改 */
        linkAffairListUpdate()
        {
            //生成当前编辑项的可选pipeline事务列表,只检索带基线版本标签的
            affairGet(this.currentItem.timeRanges,false,"基线版本").then((data)=>{
                let array=[];
                data.forEach(element => {
                    let temp = new Object();

                    temp.id = element.uuid;
                    temp.name = element.prjname;
                    temp.status = element.status;
                    temp.next = [];

                    array.push(temp);
                });
                this.relateList = array;
            });
        }
    },
    created(){
        //获取显示的项目
        itemGet().then((data)=>{
            this.items = data;

            //初始化展示项目
            if(this.items.length > 0)
            {
                for(let j in this.items)
                {
                    let value = this.items[j];

                    for(let i in value.linkAffairs)
                    {
                        if(value.linkAffairs[i].status != "已完成"
                        && value.linkAffairs[i].status != "已终止")
                        {
                            this.currentItem = value;
                            break;
                        }
                    }

                    if(this.currentItem)
                    {
                        break;
                    }
                }

                if(!this.currentItem)
                {
                    this.currentItem = this.items[0];
                }
            }
            
        }).catch((err)=>{
            this.$message({
                type: 'error',
                message: err,
            });
        })
    },
    mounted(){
        //初始化选项
        getOption("dutyperson_opt").then((data)=>{
            this.dutyPersonList = data;
        });
    }
}
</script>

<style scoped>

.el-menu-item,.el-submenu{
    text-align: left;
}

.el-tabs__header{
    margin: 0;
}

.el-tabs{
    height:100%;
    border: 0;
}

.el-main{
    height:100%;
    padding:0;
}

.toprow{
    background: #faecd8;

    display:flex;
    justify-content:center;/*主轴上居中*/
    align-items:center;/*侧轴上居中*/
}

.piperow{
    background: #faecd8;

    min-height: 50%;
    min-width: 100%;

    display:flex;
    justify-content:center;/*主轴上居中*/
    align-items:center;/*侧轴上居中*/
}

.inforow{
    margin: 0px;
    margin-bottom: 0;

    min-height: 50%;
    min-width: 100%;

    display:flex;
    justify-content:center;/*主轴上居中*/
    align-items:flex-start;/*侧轴上居中*/

    background: #e9e9eb;
}
 
.el-card {
    text-align: left;
    min-height: 35vh;
    min-width: 75vw;
    margin: 20px;
}

.el-card >>> .el-card__body{
    padding: 0px 10px;
}

.el-card .infocol{
    width: 30%;
    display:inline;
    justify-content:start;/*主轴上居中*/
    align-items:flex-start;/*侧轴上居中*/
}
 .bg-purple {
    background: #d3dce6;
  }
  .grid-content {
      margin-bottom: 20px;
    border-radius: 4px;
    min-height: 36px;
  }
</style>
