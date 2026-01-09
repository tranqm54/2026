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
    set_layout(key);
    // translator.setMode(key);
    // translator.updateUI();
}

// layout create
function create_layout_intro(main){
    const image_list = ["images/thumb1.jpg", "images/thumb2.jpg", "images/thumb3.jpg", "images/thumb4.jpg"];

    // div index 0
    const div = document.createElement("div");
    div.className = "intro-text";

        const h2 = document.createElement("h2");
        h2.textContent = translator.get("nav_intro_general_introduction");
        div.appendChild(h2);

        const p = document.createElement("p");
        p.textContent = translator.get("nav_intro_content");
        div.appendChild(p);

    
    main.appendChild(div)


    const div1 = document.createElement("div");
    div1.className = "image-side";
        // div index 1 1
        const div1_div = document.createElement("div");
        div1_div.className = "main-photo";

        const img = document.createElement("img");
        img.src = "images/family.jpg";
        img.alt = "Gia đình sum vầy";
        div1_div.appendChild(img);

        div1.appendChild(div1_div);
        // div index 1 2
        const div1_div2 = document.createElement("div");
        div1_div2.className = "thumb-gallery";

        for (let item of image_list){
            const img = document.createElement("img");
            img.src = item;
            div1_div2.appendChild(img);
        }

        div1.appendChild(div1_div2);

    main.appendChild(div1);


    document.body.appendChild(main);
}

function create_layout_customs(main){
    main.innerHTML = "Phong tục";
}

function create_layout_cuisine(main){
    main.innerHTML = "Ẩm thực";
}

function create_layout_significance(main){
    main.innerHTML = "Ý nghĩa";
}


// main
function set_layout(key = "nav_intro"){
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
        "nav_cuisine": () => create_layout_cuisine(main),   
        "nav_significance": () => create_layout_significance(main),
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