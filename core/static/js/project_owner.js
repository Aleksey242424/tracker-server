function copy(){
    const textCopy = document.querySelector("#token");
    textCopy.select();
    document.execCommand("copy");
}