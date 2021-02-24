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
</el-main>
</el-container>
</template>

<script>
export default {
    name: 'Login',
    data() {
      return {
        username:null,
        invalid:true,
        passwd:""
      }
    },
    props: {
/*
      color: {
        type: String,
        required: true
      }
*/
    },
    components: {},
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
        login() {
            // TODO:后台check用户
            // 成功则跳转到主界面,记入cookie
            document.cookie=`username=${this.username}`;
            this.$router.push({
                                path: '/mainPage',
                                query:{ id:this.username}
                              });

        }
    },
    created() {},
    mounted() {
        this.$refs.name.focus();
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
