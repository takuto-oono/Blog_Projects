function exchangeToDate(dateString) {
    let index = 0;
    while (index < dateString.length) {
        if (dateString[index] === '月') {
            break;
        }
        index += 1;
    }
    const month = dateString.slice(0, index)
    let nextIndex = index + 1;
    while (nextIndex < dateString.length) {
        if (dateString[nextIndex] === ',') {
            break;
        }
        nextIndex += 1;
    }
    const day = dateString.slice(index + 2, nextIndex);
    const year = dateString.slice(nextIndex + 2,);
    console.log(year, month, day);
    return new Date(parseInt(year), parseInt(month) - 1, parseInt(day));
}

function GetDiffDay(nowDate, date) {
    if (nowDate.getFullYear() === date.getFullYear() && nowDate.getMonth() === date.getMonth() && nowDate.getDate() === date.getDate()) {
        return 0;
    }
    return Math.floor((nowDate - date) / (60 * 60 * 24 * 1000));
}

function CreateHTML(dif, date, text) {
    let showDate = '';
    if (dif === 0) {
        showDate = '今日';
    } else if (dif === 1) {
        showDate = '昨日';
    } else if (dif === 2) {
        showDate = '2日前';
    } else if (dif === 3) {
        showDate = '3日前';
    } else {
        showDate = date.getFullYear() + '/' + Number(date.getMonth() + 1) + '/' + date.getDate();
    }

    return text + ': ' + showDate;
}

function ChangeFormatDate() {
    console.log('change date')
    const textDic = {
        'date-1': '閲覧日',
        'date-2': '高評価日',
        'date-3': '追加日',
        'date-comment': '投稿日',
        'date-public-article': '投稿日',
    }
    const nowDate = new Date();
    for (let key in textDic) {
        let elements = document.getElementsByClassName(key);
        for (let i = 0; i < elements.length; i ++) {
            const date = exchangeToDate(elements[i].innerHTML);
            console.log(date)
            elements[i].innerHTML = CreateHTML(GetDiffDay(nowDate, date), date, textDic[key]);
            console.log(textDic[key]);
        }

    }
}

addEventListener('load', ChangeFormatDate);