import {translator} from './languages.js';


// header
function init_header(){
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
        // button.href = "#";
        button.className = "btn";
        button.onclick = () => onclick_header(item);
        div.appendChild(button);
    }


    header.appendChild(title);
    header.appendChild(div);


    document.body.prepend(header);
}

function onclick_header(key){
    console.log(key)
    // translator.setMode(key);
    // translator.updateUI();
}

// layout create
function create_layout_intro(main){
    main.className = "content-card";

    const div = document.createElement("div");
    div.className = "intro-text";

    const h2 = document.createElement("h2");
    h2.textContent = translator.get("nav_intro_general_introduction");

    const p = document.createElement("p");
    p.textContent = translator.get("nav_intro_content");

    div.appendChild(h2);
    div.appendChild(p);

    main.appendChild(div)
}


// main
function set_layout(key){
    let main = document.querySelector("main");

    if (main){
        main.interHTML = "";
    }else{
        main = document.createElement("main");
        main.className = "content-card";
        document.body.appendChild(main);
    }


    const layouts = {
        "nav_intro": () => create_layout_intro(main),
        "nav_customs": () => create_layout_customs(main),
        "nav_cuisine": () => create_layout_cuisine(main)
    };

    const renderFunc = layouts[key];
    if (renderFunc) {
        main.innerHTML = "";
        renderFunc();
    }
}



function main(){
    init_header();
    set_layout();
}

main();