



//设置cookie
function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + "; " + expires;
}

//获取cookie
function getCookie(cname) {
    let name = cname + "=";
    let ca = document.cookie.split(';');

    for(let i=0; i<ca.length; i++) 
    {
        let c = ca[i].trim();
        if (c.indexOf(name)==0) return c.substring(name.length,c.length);
    }
    return "";
}

//清除cookie  
function clearCookie(name) {  
    setCookie(name, "", -1);  
}  


//生成uuid
function creatUuid() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
        return v.toString(16);
    });
}

//时间转字符串
function date2str(date_input){
    let date_obj = new Date(date_input);
    let year = date_obj.getFullYear();
    let month = date_obj.getMonth() + 1 < 10 ? "0" + (date_obj.getMonth() + 1)
            : date_obj.getMonth() + 1;
    let day = date_obj.getDate() < 10 ? "0" + date_obj.getDate() : date_obj.getDate();
    return (year + "-" + month + "-" + day);
}

export {setCookie,getCookie,clearCookie,creatUuid,date2str};
