<!--单项目进度条-->
<template>
    <el-progress
        type="line"
        :percentage="percent"
        :color="color"
        :format="progress_content">
    </el-progress>
</template>

<script>
export default {
    name:"process_line",
    data:function(){
        return{}
    },
    props: {
        /* 百分比 */
        percent: {
            type: Number,
            default: 10,
            validator: function (value) {
                return value<=100 && value >=0;
            }
        },
        /* 状态 */
        status: {
            type: String,
            default: "已终止",
            validator: function (value) {
                return ['已完成','执行中','暂停中','已终止'].indexOf(value) !== -1
            }
        }
    },
    computed: {
        color(){ 
            switch(this.status){
                case '已完成': return '#67C23A';
                case '执行中': return '#409EFF';
                case '暂停中': return '#E6A23C';
                case '已终止': return '#F56C6C';
            }
        }
    },
    watch: {},
    methods: {
        progress_content(percentage){
            return `${percentage}%`+this.status;
        }
    },
    created() {},
    mounted() {},
    updated() {},
    destroyed() {}
}
</script>
