function HideAllFolders() {
    let folders = document.getElementsByClassName("Folder");
    for (let folder = 0; folder < folders.length; folder++) {
        folders[folder].classList.add("Closed");
    }
}

function HideAllFiles() {
    let items = document.getElementsByClassName("File");
    for(let item = 0; item < items.length; item++) {
        items[item].classList.add("Closed");
    }
}

function OpenFolder(id) {
    if(id.classList.contains("Closed")) {
        console.log("Damn, you're fast.")
    }
    else {
        HideAllFolders();
        id.parentNode.classList.add("Open");
        let items = id.parentNode.getElementsByTagName("figure");

        for (let item = 0; item < items.length; item++) {
            items[item].classList.remove("Closed");
        }

        id.classList.add("Closed");

        let sect = document.getElementById(id.getAttribute("data-openid"));
        sect.classList.remove("Closed");
    }
}

function HandleResizeAfterFade(elem) {
    elem.style = ""
}

function ShowAllFolders() {
    HideAllFiles();
    let folders = document.getElementsByClassName("Folder");
    for (let folder = 0; folder < folders.length; folder++) {
        folders[folder].classList.remove("Closed");
        folders[folder].parentElement.classList.remove("Open");
        let sect = document.getElementById(folders[folder].getAttribute("data-openid"));

        if(!sect.classList.contains("Closed")) {
            sect.style = "height: " + sect.clientHeight + "px";
            sect.classList.add("Closed");
            setTimeout(function () {
                HandleResizeAfterFade(sect)
            }, 250);
        }
    }
}

function fadeOutColor(id) {
    id.style = "background: #000";
}

function OpenSection(id) {
    let sect = document.getElementById(id.getAttribute("data-openid"));
    sect.scrollIntoView();
    sect.style = "background: #4a2300";
    setTimeout(function () {
         fadeOutColor(sect)
    }, 350);
}

function GoToWelcome() {

}

function GoUpHandler() {
    let goUp = document.getElementById("returnToTop");
    if(window.scrollY > 0) goUp.classList.add("show");
    else goUp.classList.remove("show");
}

function GoUpThePage() {
    document.documentElement.scrollTop = document.body.scrollTop = 0;
}

document.addEventListener("click", GoUpThePage)

document.addEventListener('scroll', GoUpHandler);

console.log("pageControl.js loaded");