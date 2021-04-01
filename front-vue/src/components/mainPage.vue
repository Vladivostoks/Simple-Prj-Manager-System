<template>
<el-container>
    <el-header height="8vh" >
        <el-col :span="20" class="guide">
            <el-menu :default-active="curPage"
                     mode="horizontal"
                     v-model="curPage"
                     :router="true"
                     background-color="#E9EEF3"
                     text-color="#545c64"
                     active-text-color="#0b71df">
                <el-menu-item index="shortItem">
                    <div class="el-icon-edit-outline"> 事 务 </div>
                </el-menu-item>
                <!--el-menu-item index="baselineItem">
                    <div class="el-icon-guide"> 项 目 </div>
                </el-menu-item-->
                <el-menu-item index="contrlBroad" v-if="user_prop=='administrators'">
                    <div class="el-icon-setting"> 系 统 </div>
                </el-menu-item>
            </el-menu>
        </el-col>
        <el-col :span="4" class="exit">
            <el-button type="danger" 
                        :icon="iconName"
                        @click="logout"
                        @mouseenter.native="enter"
                        @mouseleave.native="leave"
                        plain>
                {{ username }}
            </el-button>
        </el-col>
    </el-header>
    <el-main>
        <router-view/>
    </el-main>
    <el-footer height="5vh">Report System {{ version }} Copyright ©2021 Ayden.Shu. All Rights Reserved.</el-footer>
</el-container>
</template>


<script>
import {getCookie,clearCookie} from '@/assets/js/common.js'

export default {
  name: 'mainPage',
  data() {
        return {
            version : "v0.0.3",
            username : getCookie("username"),
            user_prop : getCookie("userprop"),
            iconName : "el-icon-user-solid",
            plain   : true,
            round   : false,
            global  : false,
            curPage : "shortItem",
        }
    },
    props: {},
    components: {},
    computed: {},
    watch: {},
    methods: {
        leave(){
            this.iconName = "el-icon-user-solid";
        },
        enter(){
            this.iconName = "el-icon-circle-close";
        },
        logout(){
            clearCookie("username");
            clearCookie("userprop");
            this.$router.push({ path: '/' });
        }
    },
    created() {},
    mounted() {
        if(this.username){
            this.$router.replace({
                path: '/mainPage/shortItem'
            });
        }
        else{
            this.logout();
        }
    },
    updated() {},
    destroyed() {}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    .el-container {
        height: 100vh;
    }
    .el-header {
        background-color: #E9EEF3;
        padding: 0px;
    }

    .el-header .guide {
        display:flex;
        justify-content:left;/*主轴上居左*/
        align-items:center;/*侧轴上居中*/
    }

    .el-header h1{
        height:8vh;
    }

    .el-menu-item{
        width:10vw;
        display:flex;
        justify-content:left;/*主轴上居中*/
        align-items:center;/*侧轴上居中*/
    }

    .el-menu-item >>> div{
        font-size: 20px;
        font-weight:bold;
    }

    .el-header .el-col,
    .el-header .el-menu,
    .el-header .el-menu-item{
        height: 100%;
    }

    .exit {
        display:flex;
        justify-content:center;/*主轴上居中*/
        align-items:center;/*侧轴上居中*/
        height: 100%;
    }

    .el-main {
        background-color: #c2d6ec;
        color: #333;
        text-align: center;
        padding: 0px;
        min-height: fit-content;
    }
    .el-menu {
        background-color: #c2d6ec;
    }
</style>
