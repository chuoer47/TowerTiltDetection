document.getElementById("homeHover").style.backgroundColor = "rgba(27, 101, 185, 1)";
document.getElementById("forumHover").style.backgroundColor = "rgb(96,166,232)";
document.getElementById("InfoHover").style.backgroundColor = "rgba(27, 101, 185, 1)";
document.getElementById("consultHover").style.backgroundColor = "rgba(27, 101, 185, 1)";
document.getElementById("accountHover").style.backgroundColor = "rgba(27, 101, 185, 1)";


function expand(link, questionID) {
    var content = document.getElementById(questionID);
    content.classList.toggle('expanded'); // 切换展开类
    link.innerHTML = content.classList.contains('expanded') ? '展开' : '关闭';
}

function expandContent(link, answerID) {
    var answer = document.getElementById(answerID);
    answer.classList.toggle('expanded'); // 切换展开类
    link.innerHTML = answer.classList.contains('expanded') ? '展开' : '关闭';
}