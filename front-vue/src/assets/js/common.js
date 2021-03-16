/**
 * 设置cookie
 * @param {String} cname cookie名称
 * @param {String} cvalue cookie值
 * @param {Number} exdays 超时时间
 */
function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + "; " + expires;
}

/**
 * 获取cookie
 * @param {String} cname cookie名称
 */
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

/**
 * 清除cookie
 * @param {String} name cookie名称
 */
function clearCookie(name) {  
    setCookie(name, "", -1);  
}  


/**
 * 生成uuid
 * @returns {String} uuid字符串
 */
function creatUuid() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
        return v.toString(16);
    });
}

export {setCookie,getCookie,clearCookie,creatUuid};
