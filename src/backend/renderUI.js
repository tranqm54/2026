import {translator} from './languages.js';

function button_select(){
    const nav = ["nav_intro", "nav_customs", "nav_cuisine", "nav_significance"]
    // initialization

    const header = document.createElement("header");
    header.className = "tet-header";

    // title
    const title = document.createElement("h1");
    title.textContent = translator.get("main_title");
    title.className = "main-title";

    // setup nav
    const div = document.createElement("div");
    div.className = "nav";

    for (let item of nav){
        const button = document.createElement("a");
        button.textContent = translator.get(item);
        button.href = "#";
        button.className = "btn";
        div.appendChild(button);
    }



    header.appendChild(title);
    header.appendChild(div);


    document.body.prepend(header);
}


function main(){
    button_select();
}

main();