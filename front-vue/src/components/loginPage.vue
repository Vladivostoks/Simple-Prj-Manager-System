<template>
<el-container>
<el-main>
    <img src="static/image/logo.png" width="300px" height="300px"/>
    <div>
        <el-row>用户:
                    <el-input ref="name"
                              v-model="username"
                              placeholder="用户名"
                              prefix-icon="el-icon-s-check"
                              autocomplete="on"
                              @keyup.enter.native="login">
                    </el-input>
        </el-row>
        <el-row>密码:
                    <el-input placeholder="请输入密码"
                              prefix-icon="el-icon-key"
                              v-model="passwd"
                              @keyup.enter.native="login"
                              show-password>
                    </el-input>
        </el-row>
        <el-row style="margin:50px 0;">
            <el-button type="primary"
                       round
                       @click="login"
                       :disabled="invalid"
                       style="width:200px">进入
            </el-button>
        </el-row>
    </div>
    <user-edit :dialogFormVisible="user_create"
               :headLable="edit_label"
               :value="{'username':username,'user_type': user_prop}"
               v-if="user_create"
               @dialog-close="cancelUserEdit"
               @dialog-submit="getResult"></user-edit>
</el-main>
</el-container>
</template>

<script>
import axios from 'axios'
import user_edit from '@/components/itemboard/adduser'
import CryptoJS from 'crypto-js/crypto-js'
import {setCookie,clearCookie} from '@/assets/js/common.js'

export default {
    name: 'Login',
    data() {
        return {
            /* 用户创建表单显示 */
            user_create:false,
            /* 用户创建表单标题 */
            edit_label:"修改密码",
            /* 默认用户属性 */
            user_prop: "normalizer",
            /* 登陆用户名 */
            username:null,
            /* 登陆密码 */
            passwd:"",
            /* 登陆按键使能 */
            invalid:true
        }
    },
    props: {},
    components: {
        "user-edit":user_edit
    },
    computed: {},
    watch: {
        username:function (newValue, oldValue) {
            if(newValue)
            {
                this.invalid=false;
            }
            else
            {
                //can not?
                this.invalid=true;
            }
        }
    },
    methods: {
        cancelUserEdit(){
            this.user_create=false;
        },
        getResult(form) {
            this.username = form.username;
            this.passwd = form.newPasswd;
            this.user_create=false;
            this.$refs.name.focus();
        },
        login() {
            let form = new Object();
            let self = this;

            form.username = this.username;
            form.passwd = CryptoJS.SHA256(this.passwd).toString();
            // 成功则跳转到主界面,记入cookie
            new Promise(function (resolve, reject) {
                axios({
                    url:'/login',
                    method: 'put',
                    timeout: 5000,
                    responseType: 'json',
                    responseEncoding: 'utf8', 
                    headers: {
                        'Content-Type': 'application/json;charset=UTF-8'
                    },
                    data:form
                }).then((res) => {
                    if(res.data.ret)
                    {
                        if(res.data.message == "登陆成功")
                        {
                            resolve(res.data.user_prop);
                        }
                        else if(res.data.message == "无初始化")
                        {
                            // 如果没有设置密码，需要弹窗设置密码
                            self.edit_label="修改密码";
                            self.user_prop=res.data.user_prop;
                            self.user_create=true;
                        }
                    }
                    else
                    {
                        //密码错误
                        reject(new Error(res.data.message));
                    }
                }).catch((res)=>{
                    //字段有问题
                    reject(res);
                });
            }).then(function success(value){
                /* TODO: 建立websock链路 */
                return value;
            }).then(function success(value){
                setCookie("username",self.username,1);
                setCookie("userprop",value,1);
                self.$router.push({
                                    name: 'mainPage',
                                    params:{ user_prop: value }
                                  });
            }).catch(function failed(error){
                self.$message({
                    type: 'error',
                    message: error.message,
                });
                console.dir(error);
            });
        }
    },
    created() {
        //登陆页面清除cookie
        clearCookie("username");
    },
    mounted() {
        // check是否有超级用户
        axios({
            url:'/user',
            method: 'get',
            timeout: 5000,
            responseType: 'json',
            responseEncoding: 'utf8', 
            params: {"ischeck_super":true}
        }).then((res) => {
            //没有用户则开启对话框生成超级用户
            if(!res.data.hasSuperUser)
            {
                this.edit_label="创建超级用户";
                this.user_prop="administrators"
                this.user_create=true;
            }
            else
            {
                this.$refs.name.focus();
            }
        }).catch((res)=>{
            this.$message({
                type: 'error',
                message: res
            });
            console.dir(res);
        });
    },
    updated() {},
    destroyed() {}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    .el-row {
        margin:10px 0;
    }
    .el-main {
        background-color: #E9EEF3;
        color: #333;
        line-height: 100%;
        height: 100vh;

        text-align: center;
        display: table-cell;
        vertical-align: middle;
    }
    .el-input{
        width: 16vw;
    }
</style>
