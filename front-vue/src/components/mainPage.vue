<template>
<el-container>
    <el-header height="10vh" >
        <el-col :span="20" class="guide">
            <el-menu default-active="shortItem"
                     mode="horizontal"
                     @select="tableChoose"
                     background-color="#E9EEF3"
                     text-color="#545c64"
                     active-text-color="#0b71df">
                <el-menu-item index="shortItem"><h1>需求/反馈汇总</h1></el-menu-item>
                <el-menu-item index="baselineItem"><h1>版本/项目跟踪</h1></el-menu-item>
                <el-menu-item index="contrlBroad"><h1>管理选项</h1></el-menu-item>
            </el-menu>
        </el-col>
        <el-col :span="4" class="exit">
            <el-button type="danger" 
                        :icon="iconName"
                        @click="logout"
                        @mouseenter.native="enter"
                        @mouseleave.native="leave"
                        plain>
                {{ message }}
            </el-button>
        </el-col>
    </el-header>
    <el-main>
        <div v-if="global">
            <el-row style="background-color: #F0A5FF"
                    @click.native="normalItem">
                短周期项目
            </el-row>
            <el-row style="background-color: #50EEFF">长周期项目</el-row>
            <el-row style="background-color: #60FEFF">TVD项目</el-row>
        </div>
        <div v-else>
            <new-item></new-item>
        </div>
    </el-main>
    <el-footer height="5vh">©2021 Ayden.Shu. All Rights Reserved.</el-footer>
</el-container>
</template>


<script>
import newItem from '@/components/itemboard/temporary_item'

export default {
  name: 'mainPage',
  data() {
        return {
            message : this.$route.query.id,
            iconName : "el-icon-user-solid",
            plain   : true,
            round   : false,
            global  : false,
            activeName : null
        }
    },
    props: {
    },
    components: {
        'new-item' : newItem,
    },
    computed: {},
    watch: {},
    methods: {
        tableChoose(){

        },
        leave(){
            this.iconName = "el-icon-user-solid";
        },
        enter(){
            this.iconName = "el-icon-circle-close";
        },
        logout(){
            this.$router.push({ path: '/' });
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
        height: 100vh;
    }
    .el-header {
        background-color: #E9EEF3;
        padding: 0px;
    }

    .guide {
        display:flex;
        justify-content:left;/*主轴上居中*/
        align-items:flex-end;/*侧轴上居中*/
    }

    .exit {
        display:flex;
        justify-content:center;/*主轴上居中*/
        align-items:center;/*侧轴上居中*/
        height: 100%;
    }

    .el-header .el-col {
        height: 100%;
    }

    .el-menu {
        height: 100%;
    }

    .el-menu-item {
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
