<template>
<el-container style="height: 100%;">
    <el-menu
      default-active="user_manager"
      background-color="#545c64"
      text-color="#fff"
      style="width:10vw"
      active-text-color="#ffd04b">
      <el-menu-item index="user_manager">
        <i class="el-icon-user"></i>
        <span slot="title">用户管理</span>
      </el-menu-item>
    </el-menu>
    <el-main>
        <el-tabs type="border-card"
                 v-model="user_tab_active">
            <el-tab-pane label="账户管理" name="userManager">
            <el-table :data="user_table"
                      :key="tableKey"
                      :row-class-name="tableRowClassName"
                      style="width: 50%">
                <el-table-column
                    prop="user_name"
                    label="用户名称"
                    min-width="30%">
                    <template v-slot="scope">
                        <el-input v-if="scope.row.is_edit && scope.$index==(user_table.length-1)"
                                  v-model="scope.row.user_name"
                                  size="mini"
                                  placeholder="输入用户名"/>
                        <div v-else> {{ scope.row.user_name }}</div>
                    </template>
                </el-table-column>
                <el-table-column
                    prop="user_prop"
                    label="用户属性"
                    min-width="30%">
                    <template v-slot="scope">
                    <el-select v-if="scope.row.is_edit" v-model="scope.row.user_prop" placeholder="请选择用户属性">
                        <el-option
                        v-for="item in user_proper_options"
                        :key="item"
                        :label="item"
                        :value="item">
                        </el-option>
                    </el-select>
                    <div v-else> {{ scope.row.user_prop }}</div>
                    </template>
                </el-table-column>
                <el-table-column 
                    min-width="40%"
                    label="操作"
                    align="right">
                    <template v-slot="scope">
                        <el-button v-if="!scope.row.is_edit && scope.$index==(user_table.length-1)"
                                   size="mini"
                                   type="primary"
                                   @click="userEdit(scope.row)">新增用户</el-button>
                        <el-button-group v-else-if="!scope.row.is_edit">
                            <el-button
                            size="mini"
                            type="info"
                            @click="userEdit(scope.row)">Edit</el-button>
                            <el-button
                            size="mini"
                            type="danger"
                            @click="userDelete(scope.$index, scope.row)">Delete</el-button>
                        </el-button-group>
                        <el-button-group v-else>
                            <el-button size="mini"
                                       type="success"
                                       icon='el-icon-check'
                                       @click="userConfirm(scope.$index,scope.row)"></el-button>
                            <el-button size="mini"
                                       type="danger"
                                       icon="el-icon-close"
                                       @click="userCancel(scope.$index,scope.row)"></el-button>
                        </el-button-group>
                    </template>
                </el-table-column>
            </el-table>
                </el-tab-pane>
            <el-tab-pane label="统计信息" name="forInfo">信息显示</el-tab-pane>
            <el-tab-pane label="修改密码" name="changePasswd">修改密码</el-tab-pane>
        </el-tabs>
    </el-main>
</el-container>
</template>


<script>
import axios from 'axios'

export default {
    name: 'ctrlPage',
    data() {
        return {
            /* 修改此变量来更新表格 */
            tableKey: Math.random(),
            /*用户界面默认选项*/
            user_tab_active:"userManager",
            /*用户属性选项*/
            user_proper_options:[//"administrators",
                                 "controller",
                                 "normalizer"],
            /*用户列表*/
            user_table: []
        }
    },
    methods: {
        tableRowClassName({row, rowIndex}) {
            if (!row.user_passwd) {
                return 'nopasswd-row';
            }
            return '';
        },
        userEdit(row){
            row.is_edit = true;
            this.tableKey = Math.random();
        },
        userCancel(index,row){
            row.is_edit = false;

            if(index == this.user_table.length-1)
            {
                row.user_name = "";
                row.user_prop = "";
            }
            this.tableKey = Math.random();
        },
        userConfirm(index,row){
            //新增用户则设置空密码
            let data = { 
                username : row.user_name,
                passwd : '',
                prop : row.user_prop
            };
            this.userPut(data).then((data)=>{
                if(index==(this.user_table.length-1))
                {
                    //ADD 
                    let new_line = new Object({user_name: '',
                                               user_prop: '',
                                               is_edit: false});
                    this.user_table.splice(index+1, 0, new_line);
                    this.$message({
                        type: 'success',
                        message: `添加用户成功!`
                    });
                }
                else
                {
                    //Edit
                    this.$message({
                        type: 'success',
                        message: `修改用户属性成功!`
                    });
                }
                row.is_edit = false;
                this.tableKey = Math.random();
            }).catch((error)=>{
                console.dir(error);
                this.$message({
                    type: 'error',
                    message: error,
                });
            })
        },
        userGet(){
            let self = this;
            axios({
                url:'/user',
                method: 'get',
                timeout: 5000,
                responseType: 'json',
                responseEncoding: 'utf8', 
            }).then((res) => {
                let new_line = new Object({user_name: '',
                                            user_prop: '',
                                            is_edit: false});
                self.user_table = res.data;
                self.user_table.splice(self.user_table.length, 0, new_line);
            }).catch((error)=>{
                console.dir(error);
            }); 
        },
        userPut(req){
            return new Promise(function (resolve, reject) {
                axios({
                    url:'/user',
                    method: 'put',
                    timeout: 5000,
                    responseType: 'json',
                    responseEncoding: 'utf8', 
                    data: req
                }).then((res) => {
                    resolve(res.data);
                }).catch((error)=>{
                    reject(error);
                }); 
            });
        },
        userDelete(index,row){
            axios({
                url:'/user',
                method: 'delete',
                timeout: 5000,
                responseType: 'json',
                responseEncoding: 'utf8', 
                data: { username : row.user_name }
            }).then((res) => {
                if(res.data.message)
                {
                    this.$message({
                        type: 'success',
                        message: `删除用户成功!`
                    });
                    this.user_table.splice(index, 1);
                }
            }).catch((error)=>{
                console.dir(error);
                this.$message({
                    type: 'error',
                    message: error,
                });
            }); 
        }
    },
    mounted(){
        this.userGet();
    }
}
</script>

<style scoped>
.el-main{
    padding:1px 0 0 0 ;
}

.el-row {
    margin: 0px;
    width: 100%;
}

.el-tabs__header{
    margin: 0;
}

.el-tabs{
    height:100%;
    border: 0;
}

.el-table .nopasswd-row {
    background: rgb(253, 226, 226);
}

</style>