<template>
<el-dialog 
  :title="isEdit?'编辑项目':'新建项目'"
  :visible.sync="dialogFormVisible"
  :before-close="handleClose"
  width="30%">
  <el-form :model="form" size="mini" :rules="rules">
    <el-form-item label="创建日期" label-width="120px">
        <el-date-picker
        v-model="form.date"
        type="date"
        :disabled="true"
        placeholder="选择日期">
        </el-date-picker>
    </el-form-item>
    <el-form-item label="区域" label-width="120px">
      <el-input v-model="form.region"
                placeholder="输入项目归属区域"
                autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="项目名称" label-width="120px">
      <el-input v-model="form.prjname"
                placeholder="输入项目名称"
                autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="项目类型" label-width="120px">
        <el-input v-model="form.prjtype"
                  placeholder="输入项目类型"
                  autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="原始需求" label-width="120px">
      <el-input type="textarea"
                v-model="form.requirement"
                placeholder="项目具体需求/问题反馈说明"
                autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="svn/git" label-width="120px">
      <el-input v-model="form.svnurl"
                placeholder="项目关联代码路径"
                autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="预计执行时间(周)" label-width="120px">
        <el-input-number
        v-model="form.scheme_week" 
        :min="1"
        :disabled="isEdit"
        label="输入项目计划完成所需周数">
        </el-input-number>
    </el-form-item>
    <el-form-item label="执行进度/状态" label-width="120px">
        <el-col :span="18">
            <el-slider v-model="form.progress"></el-slider>
        </el-col>
        <el-col :span="6">
            <el-select v-model="form.status" placeholder="选择状态">
                <el-option label="已完成" value="已完成"> </el-option>
                <el-option label="执行中" value="执行中"> </el-option>
                <el-option label="暂停中" value="暂停中"> </el-option>
                <el-option label="已终止" value="已终止"> </el-option>
            </el-select>
        </el-col>
    </el-form-item>
    <el-form-item label="当前处理人员" label-width="120px">
        <el-select
            v-model="form.persons"
            multiple
            filterable
            allow-create
            default-first-option
            style="width:100%"
            placeholder="选择处理人员">
        <el-option
            v-for="item in personList"
            :key="item"
            :label="item"
            :value="item">
        </el-option>
  </el-select>
    </el-form-item>
  </el-form>
  <div slot="footer" class="dialog-footer">
    <el-button @click="Cancel">取 消</el-button>
    <el-button type="primary" @click="Confirm">提 交</el-button>
  </div>
</el-dialog>
</template>

<script>
export default {
    name: 'item_edit',
    data() {
        var statusCheck = (rule, value, callback) => {
            if(['已完成','执行中','已暂停', '已终止'].indexOf(value) !== -1)
            {
                //correct
                return true;
            }
            else
            {
                //err
                return callback(new Error("状态仅限于'已完成','执行中','已暂停', '已终止'中的一种"));
            }
        };

        var personCheck = (rule, value, callback) => {
            //todo
            return true;
        };

        function getDate(){
            let nowDate = new Date();
            let year = nowDate.getFullYear();
            let month = nowDate.getMonth() + 1 < 10 ? "0" + (nowDate.getMonth() + 1)
                    : nowDate.getMonth() + 1;
            let day = nowDate.getDate() < 10 ? "0" + nowDate.getDate() : nowDate
                    .getDate();
            return (year + "-" + month + "-" + day);
        }

        return {
            dialogFormVisible: false,
            /* 待处理人员列表 */
            personList:["Ayden.Shu","shuzhengyang"],
            /* 输入输出表单 */
            form: {},
            rules: {
                date: [
                    { required: true, type: 'date', message: '请选择日期', trigger: 'change' }
                ],
                name: [
                    { required: true, message: '请输入项目名称', trigger: 'blur' }
                ],
                requirement: [
                    { required: true, message: '请原始需求/问题反馈', trigger: 'blur' }
                ],
                region: [
                    { required: true, message: '请输入项目归属区域', trigger: 'blur' }
                ],
                scheme_week: [
                    { required: true, type: 'integer', min: 1, max: 100, message: '计划完成时间至少需要大于1', trigger: 'blur' }
                ],
                percent: [
                    { required: true, type: 'integer', min: 0, max: 100, message: '进度应该在0-100之间', trigger: 'blur' }
                ],
                status: [
                    { validator: statusCheck, trigger: 'blur' }
                ],
                persons: [
                    { validator: personCheck, trigger: 'blur' }
                ]
            }
        }
    },
    props: {
        /*新建还是编辑*/
        isEdit:{
            type: Boolean,
            default: true 
        },
        /*如果是编辑需要传入被编辑值*/
        value:{
            type: Object,
            validator: function (value) {
                //todo:入参校验
                return true
            }
        }
    },
    components: {},
    computed: {},
    watch: {
    },
    methods: {
        handleClose(done) {
            this.$emit("dialog-close")
            .then(_ => {
                done();
            })
            .catch(_ => {});
        },
        Cancel(){
            this.dialogFormVisible = false;
            this.$emit("dialog-close");
        },
        Confirm(){
            this.dialogFormVisible = false;
            if(1)
            {
                //抛出编辑后的值
                this.$emit("dialog-submit",this.form);
            }
            else
            {
                //报错
            }

            this.$emit("dialog-close");
        }
    },
    created() {},
    mounted() {
        this.form = this.value;
        this.dialogFormVisible = true;
    },
    updated() {
    },
    destroyed() {}
}
</script>

<style scoped>
    el-slider.el-slider__runway {
        margin: 11px 0; /*没有生效*/
    }

    .el-slider {
        width: 90%;
    }

    .el-form-item{
        text-align: left;
    }
</style>>