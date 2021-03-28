
<template>
<el-dialog 
  :title="headLable"
  :show-close="false"
  :visible.sync="dialogFormVisible"
  :before-close="handleClose"
  :close-on-click-modal="false"
  width="30vw">
  <el-form :model="form" ref="form" size="mini" :rules="rules">
    <el-form-item label="用户名" label-width="100px" prop="username">
        <el-input v-model="form.username"
                :disabled="headLable=='修改密码'"
                placeholder="请设置用户名"
                autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item v-if="headLable=='修改密码' && form.curPasswd" label="输入当前密码" label-width="100px" prop="passwd">
        <el-input v-model="form.curPasswd"
                  show-password
                  placeholder="请输入当前密码"
                  autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="输入新密码" label-width="100px" prop="newPasswd">
        <el-input v-model="form.newPasswd"
                  show-password
                  placeholder="请设置一个密码"
                  autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="确认密码" label-width="100px" prop="confirm">
        <el-input v-model="form.confirm"
                  show-password
                  placeholder="再次输入设置密码"
                  autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item v-if="headLable=='添加用户'" prop="user_type" label="添加用户类型" label-width="100px">
        <el-select
            v-model="form.user_type"
            style="width:100%"
            placeholder="选择关联人员类型">
                <el-option label="管理员" value="controller"> </el-option>
                <el-option label="普通用户" value="normalizer"> </el-option>
            </el-select>
    </el-form-item>
  </el-form>
  <div slot="footer" class="dialog-footer">
    <el-button v-if="headLable!='创建超级用户'" @click="Cancel">取 消</el-button>
    <el-button type="primary" @click="Confirm()">提 交</el-button>
  </div>
</el-dialog>
</template>

<script>
import axios from 'axios'
import CryptoJS from 'crypto-js/crypto-js'

export default {
    name: 'user_edit',
    data() {
        let newPasswd = (rule, value, callback) => {
            if(!value) {
                callback(new Error('需要输入新密码'));
            }
            else if(this.form.passwd == value) {
                callback(new Error('新密码不能和旧密码一致'));
            }

            callback();
            return true;
        }
        let confirmPasswd = (rule, value, callback) => {
            if(!value) {
                callback(new Error('需要确认输入密码'));
            }
            else if(this.form.newPasswd != value) {
                callback(new Error('两次输入密码不一致'));
            }

            callback();
            return true;
        };

        return {
            /* 输入输出表单 */
            form: {
                /* 用户名 */
                username:"",
                /* 当前密码 */
                passwd:"",
                /* 设置新密码 */
                newPasswd:"",
                /* 确认密码 */
                confirm:"",
                /* 用户类型 */
                user_type:""
            },
            /* 输入校验规则 */
            rules: {
                username: [
                    { required: true, message: '需要填写用户名', trigger: 'blur' }
                ],
                passwd: [
                    { min: 1,required: true, message: '需要填写密码', trigger: 'blur' }
                ],
                newPasswd: [
                    { required: true, validator: newPasswd, trigger: 'blur' }
                ],
                user_type: [
                    { required: true, message: '需要选择用户类型', trigger: 'blur' }
                ],
                confirm: [
                    { required: true, validator: confirmPasswd, trigger: 'blur' }
                ]
            }
        }
    },
    props: {
        /* 表单可见状态 */
        dialogFormVisible:{
            type: Boolean,
            required: true
        },
        /*标题*/
        headLable:{
            type: String,
            default: "添加用户",
            validator: function (value) {
                return ['添加用户','修改密码','创建超级用户'].indexOf(value) !== -1
            }
        },
        /*如果是编辑需要传入被编辑值*/
        value:{
            type: Object,
            default: null,
            validator: function (value) {
                //todo:入参校验
                return true
            }
        }
    },
    components: {},
    computed: {},
    watch: {},
    methods: {
        handleClose(done) {
            if(this.headLable == '创建超级用户')
            {
                //无root用户情况下，不允许关闭创建窗口
                return;
            }
            this.$emit("dialog-close")
            .then(() => {
                done();
            })
            .catch(() => {});
        },
        Cancel(){
            if(this.headLable == '创建超级用户')
            {
                //无root用户情况下，不允许关闭创建窗口
                return;
            }
            this.$emit("dialog-close");
        },
        Confirm(){
            this.$refs['form'].validate((valid) => {
                
                if (valid)
                {
                    let form = new Object();

                    //修改密码的话需要校验原始密码 TODO
                    form.username = this.form.username;
                    form.passwd = CryptoJS.SHA256(this.form.newPasswd).toString();
                    /* 用户类型设置管理员 */
                    form.prop = this.value.user_type;

                    /* call backend */
                    axios({
                        url:'/user',
                        method: 'put',
                        timeout: 5000,
                        responseType: 'json',
                        responseEncoding: 'utf8', 
                        headers: {
                            'Content-Type': 'application/json;charset=UTF-8'
                        },
                        data:form
                    }).then((res) => {
                        //判断返回值 
                        if(!res.data.ret)
                        {
                            this.$message({
                                type: 'error',
                                message: '创建用户失败'
                            });
                        }
                        this.$emit("dialog-submit",this.form);
                    }).catch((res)=>{
                        this.$message({
                            type: 'error',
                            message: res
                        });
                        //test
                        this.$emit("dialog-submit",this.form);
                    });
                } else {
                    return false;
                }
            });
        }
    },
    created() {},
    mounted() {
        //deep copy
        if(this.value != null) {
            this.form = Object.assign({},this.value);
        }
    },
    updated() {
    },
    destroyed() {}
}
</script>

<style scoped>
    .el-form-item{
        text-align: left;
    }
</style>