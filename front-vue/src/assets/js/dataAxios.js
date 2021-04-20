import axios from 'axios'
import {deepCopy} from '@/assets/js/common.js'

/**
 * 获取选项列表
 * @param {String} opt 选项名称
 * @return {Promise} 请求promise,弹出选项数组
 */
function getOption(opt)
{
    return new Promise(function(resolve,reject){
        axios({
            url:'/option',
            method: 'get',
            timeout: 5000,
            responseType: 'json',
            responseEncoding: 'utf8', 
            params: {'option_name':opt}
        }).then((res) => {
            resolve(res.data.option);
        }).catch((error)=>{
            reject(error);
        }); 
    })
}

/**
 * 获取事务列表
 * @param {String} dataRange 事务时间范围
 * @param {Boolean} isUpdateTime 是否是最后更新时间
 * @param {String} type 项目类型,可以缺省
 * @param {String} status 项目状态,可以缺省
 * @return {Promise} 请求promise,弹出被请求的事务列表
 */
function affairGet(dataRange,isUpdateTime,type,id)
{
    //触发检索
    let req = new Object();

    req.start_time = dataRange[0].getTime();
    req.end_time = dataRange[1].getTime();

    req.isupdatetime = isUpdateTime;

    req.type = type;
    req.id = id; 

    return new Promise(function (resolve, reject) {
        axios({
            url:'/affair',
            method: 'get',
            timeout: 5000,
            responseType: 'json',
            responseEncoding: 'utf8', 
            params: req
        }).then((res) => {
            resolve(res.data);
        }).catch((error)=>{
            reject(error);
        }); 
    });
}

/**
 * 获取事务列表
 * @param {String} dataRange 事务时间范围
 * @param {Boolean} isUpdateTime 是否是最后更新时间
 * @param {String} type 项目类型,可以缺省
 * @param {String} status 项目状态,可以缺省
 * @return {Promise} 请求promise,弹出被请求的事务列表
 */
function affairGetWithID(id,item)
{
    //触发检索
    let req = new Object();
 
    req.start_time = new Date().getTime();
    req.end_time = new Date().getTime();
 
    req.id = id; 
 
    return new Promise(function (resolve, reject) {
        axios({
            url:'/affair',
            method: 'get',
            timeout: 5000,
            responseType: 'json',
            responseEncoding: 'utf8', 
            params: req
        }).then((res) => {
            //携带item数据到下一个then
            res.item = item;
            resolve(res);
        }).catch((error)=>{
            reject(error);
        }); 
    });
}

/**
 * 获取工程列表项目
 * @param {String} uuid 项目id
 * @return {Promise} 请求promise,弹出被请求的事务列表
 */
function itemGet(uuid)
{
    let itemReq = new Promise(function (resolve, reject) {
        axios({
            url:'/item',
            method: 'get',
            timeout: 5000,
            responseType: 'json',
            responseEncoding: 'utf8', 
            params: uuid?{id:uuid}:null
        }).then(async (res) => {
            resolve(res.data);
        }).catch((error)=>{
            reject(error);
        }); 
    });

    return itemReq.then(data=>{
        //检索具体的事务信息，补充data中的Affair字段
        let promiseArray = [];

        data.forEach(element => {
            element.timeRanges = [new Date(element.startTime),new Date(element.endTime)];

            delete element.startTime;
            delete element.endTime;
            
            element.linkAffairs.forEach(affair=>{
                promiseArray.push(affairGetWithID(affair.id,element));
            });
        });

        return Promise.all(promiseArray);
    }).then(res=>{
        let item = [];
        let curItem = new Object();
        let j = 0;

        //每个数组到item都一样,直接用第0个即可
        for(let i in res)
        {
            if(curItem != res[i].item)
            {
                curItem = res[i].item;
                j = 0;
                curItem.linkAffairs[j].name = "开始";
                item.push(curItem);
            }
            else
            {
                j = j+1;
                curItem.linkAffairs[j].name = res[i].data[0].prjname;
                curItem.linkAffairs[j].status = res[i].data[0].status;
            }
        }

        return Promise.resolve(item);
    });
}
/**
 * 修改/创建工程项目
 * @param {Object} itemInfo 项目信息
                    {
                        id:"uuid1",
                        name:"视频测速功能开发",
                        version:"V0.0.1",
                        brief:"使用视频特征进行目标测速",
                        dutyPersons:["Ayden","Shuzhengyang"],
                        timeRanges:[new Date(),new Date()],
                        linkAffairs:[{
                            id:"Start",
                            name:"Start",
                            status:"未开始",
                            next:[],
                        }]
                    }
 * @return {Promise} 请求promise,弹出被请求的事务列表
 */
function itemPut(itemInfo)
{
    let data = deepCopy(itemInfo);
    data.startTime = itemInfo.timeRanges[0].getTime();
    data.endTime = itemInfo.timeRanges[1].getTime();

    delete data.timeRanges;

    //关联事务只存id和next
    data.linkAffairs.forEach((affair)=>{
        for(let key in affair)
        {
            if(key != "id" && key != "next")
            {
                delete affair[key];
            }
        }
    });

    return new Promise(function (resolve, reject) {
        axios({
            url:'/item',
            method: 'put',
            timeout: 5000,
            responseType: 'json',
            responseEncoding: 'utf8', 
            headers: {
                    'Content-Type': 'application/json;charset=UTF-8'
            },
            data:data
        }).then((res) => {
            res.data.ret?resolve(res.data.message):reject(res.data.message);
        }).catch((error)=>{
            reject(error);
        }); 
    });
}

/**
 * 删除工程项目
 * @param {String} uuid 项目id
 * @return {Promise} 请求promise,弹出被请求的事务列表
 */
function itemDelete(uuid)
{
    return new Promise(function (resolve, reject) {
        axios({
            url:'/item',
            method: 'delete',
            timeout: 5000,
            responseType: 'json',
            responseEncoding: 'utf8', 
            headers: {
                    'Content-Type': 'application/json;charset=UTF-8'
            },
            data:{
                id:uuid
            }
        }).then((res) => {
            res.data.ret?resolve(res.data.message):reject(res.data.message);
        }).catch((error)=>{
            reject(error);
        }); 
    });
}

export {getOption,affairGet,itemGet,itemPut,itemDelete}
