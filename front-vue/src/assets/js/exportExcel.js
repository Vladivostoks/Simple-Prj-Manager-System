import XLSX from 'xlsx'
import XLSXStyle from 'xlsx-style'
import { saveAs } from 'file-saver'
import path from 'path'
import _ from 'lodash'

/**
 * @description 列参数
 */
const COL_PARAMS = ['hidden', 'wpx', 'width', 'wch', 'MDW']
/**
 * @description 样式参数
 */
const STYLE_PARAMS = ['fill', 'font', 'alignment', 'border']

/**
 * 表头字母转换成数字。（进制转换）
 * @param {string} str 需要装换的字母
 * @returns {Number}
 */
function stringToNum(str) {
    let temp = str.toLowerCase().split('')
    let len = temp.length
    let getCharNumber = function(charx) {
        return charx.charCodeAt() - 96
    }
    let numout = 0
    let charnum = 0
    for (let i = 0; i < len; i++) {
        charnum = getCharNumber(temp[i])
        numout += charnum * Math.pow(26, len - i - 1)
    }
    return numout
}

/**
 * 导出成Excel
 * @param {Array} data 数据
 * @param {Object} columns 每列参数说明。可直接写对应的中文名称，也可以写这一列的样式。比如列宽，背景色
 * @param {String} booktype 文件后缀名
 * @param {Object} head_style 表头 style参数
 * @param {Object} style_conf 其他xlsx-style的参数
 *
 * data数据格式:
 *         [{ name: 'Jerry', sex: 'female', birthday: '1970-3-14', address: 'XX. Street'},
 *          { name: 'Jerry', sex: 'female', birthday: '1970-3-14', address: 'XX. Street'}]
 * 
 * columns数据格式：{
 *         name: '姓名',
 *         sex: '性别',
 *         birthday: {
 *           name: '出生日期',
 *           wch: 14
 *         },
 *         address: {
 *           name: '地址',
 *           wpx: 160,
 *           alignment: { wrapText: true }
 *         }
 *       }
 * 
 * head_style数据格式:{
 *          fill: {
 *              fgColor: { rgb: 'FFA3F4B1' }
 *          },
 *          font: {
 *              name: '宋体',
 *              sz: 12,
 *              bold: true
 *          },
 *          border: {
 *              bottom: {
 *                  style: 'thin',
 *                  color: 'FF000000'
 *              }
 *          }
 *        }
 * 
 * style_conf数据格式: {
 *          'E4': {
 *             font: {
 *               bold: true,
 *               color: { rgb 'FFFF0000' }
 *             }
 *          },
 *          '!merges': [ // 合并第一行
 *             {
 *               s: { c: 0, r: 0 },
 *               e: { c: 7, r: 0 }
 *             }
 *          ]
 *        }
 */
export function exportExcel(data, columns, booktype, head_style, style_conf)
{
    let keys = _.keys(columns);
    let colNames = _.mapValues(columns, o => {
        if (_.isPlainObject(o)) {
            return o.name;
        } else {
            return o;
        }
    })

/*
    // step 1:创建工作簿
    let wb = XLSX.utils.book_new();
*/
    // step 2:显示表头
    const ws = XLSX.utils.json_to_sheet([ colNames ], { header: keys, skipHeader: true });
    // 过滤数据，只显示表头包含的数据
    for (let i = 0; i < data.length; i++)
    {
        data[i] = _.pick(data[i], keys);
    }

    // step 3:追加数据到excel中，从第二行开始
    XLSX.utils.sheet_add_json(ws, data, { header: keys, skipHeader: true, origin: 'A2' });

/*
    wb.SheetNames.push(sheetname);
    wb.Sheets[sheetname] = ws;

    // step 4:根据不同的扩展名,导出不同格式的文件,默认xlsx
    let bookType = null;
    let ext = path.extname(filename);
    if (ext == null)
    {
        filename += '.xlsx';
        bookType = 'xlsx';
    }
    else
    {
        bookType = ext.substr(1).toLowerCase();
    }

    let wbOut;
*/

    // step 5: 添加样式 如果是支持样式的格式,否则无样式导出
    if (['xlsx', 'xlsm', 'xlsb'].includes(booktype))
    {
        for (const key in ws)
        {
            // 表头样式
            if (key.replace(/[^0-9]/ig, '') === '1')
            {
                ws[key].s = head_style;
            }
            else
            {
                let str = key.replace(/[^A-Za-z]+$/ig, '');
                let colIndex = stringToNum(str) - 1;
                if (keys[colIndex] && _.isPlainObject(columns[keys[colIndex]]))
                {
                    const a = _.pick(columns[keys[colIndex]], STYLE_PARAMS);
                    ws[key].s = _.assign(ws[key].s, a);
                }
            }
        }

        // 设置列宽
        const colsP = [];
        _.mapValues(columns, o => {
            colsP.push(_.pick(o, COL_PARAMS));
        })
        ws['!cols'] = colsP;
  
        // 合并其他样式参数
        if (style_conf)
        {
            for (const key in style_conf)
            {
                if (ws.hasOwnProperty(key))
                {
                    ws[key].s = style_conf[key];
                }
            }
        }
/*
        wbOut = XLSXStyle.write(wb, { bookType: bookType, bookSST: false, type: 'binary' });
*/
    }
    else
    {
/*
        //wbOut = XLSX.write(wb, { bookType: bookType, bookSST: false, type: 'binary' });
*/
    }
    
/*
    saveAs(new Blob([s2ab(wbOut)], { type: '' }), filename);
*/
    return ws;
}

