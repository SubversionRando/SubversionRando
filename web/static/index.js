async function populate_tricks() {
    console.log("populate tricks");
    const logic_response = await fetch("/tricks");
    if (! logic_response.ok) {
        console.error("bad response from tricks");
    }
    const tricks = document.getElementById("tricks");
    const trick_data = await logic_response.json();
    for (const [trick_name, trick_desc] of trick_data) {
        const check = document.createElement('input');
        check.type = "checkbox";
        check.id = trick_name;

        const label = document.createElement('label');
        label.htmlFor = trick_name;
        label.innerText = trick_name;

        const desc = document.createElement('span');
        desc.innerText = trick_desc;

        const row = document.createElement('tr');

        const box = document.createElement('td');
        box.appendChild(check);
        row.appendChild(box);

        const name = document.createElement('td');
        name.appendChild(label);
        row.appendChild(name);

        const desc_cell = document.createElement('td');
        desc_cell.appendChild(desc);
        row.appendChild(desc_cell);

        tricks.appendChild(row);
    }
}

function setup_collapsible() {
    console.log("setup collapsible");
    const coll = document.getElementById("collapse-control");
    const trick_container = document.getElementById("trick-container");
    trick_container.style.maxHeight = "0px";
    trick_container.style.overflowY = "hidden";
    trick_container.style.transition = "max-height 0.2s ease-out";

    coll.addEventListener("click", () => {
        console.log(trick_container.style.maxHeight);
        console.log(trick_container.scrollHeight);
        if (trick_container.style.maxHeight !== "0px") {
            trick_container.style.maxHeight = "0px";
            trick_container.style.overflowY = "hidden";
        } else {
            trick_container.style.maxHeight = "400px";
            trick_container.style.overflowY = "auto";
        }
    });
}

async function populate_presets(trick_promise) {
    console.log("populate presets");
    const preset_response = await fetch("/presets");
    if (! preset_response.ok) {
        console.error("bad response from presets");
    }
    const preset_span = document.getElementById("preset-buttons");
    const preset_data = await preset_response.json();

    // tricks populated before making buttons that act on tricks
    await trick_promise;

    for (const [preset_name, trick_list] of preset_data) {
        const button = document.createElement('button');
        button.innerText = preset_name;
        const tricks_for_this_preset = trick_list;
        button.addEventListener('click', () => {
            const tricks_table = document.getElementById("tricks");
            for (const row of tricks_table.children) {
                const checkbox = row.firstChild.firstChild;
                checkbox.checked = false;
            }
            for (const trick_name of tricks_for_this_preset) {
                const tricks_checkbox = document.getElementById(trick_name);
                tricks_checkbox.checked = true;
            }
        });

        preset_span.appendChild(button);
    }
}

function download(url, filename) {
    fetch(url).then(function(t) {
        return t.blob().then((b)=>{
            var a = document.createElement("a");
            a.href = URL.createObjectURL(b);
            a.setAttribute("download", filename);
            a.click();
        }
        );
    });
}

function setup_roll_button() {
    const roll_button = document.getElementById("roll-button");
    roll_button.addEventListener("click", async () => {
        const activated_trick_names = [];
        const tricks_table = document.getElementById("tricks");
        for (const row of tricks_table.children) {
            const checkbox = row.firstChild.firstChild;
            const trick_name = row.children[1].firstChild.innerText
            if (checkbox.checked) {
                activated_trick_names.push(trick_name);
            }
        }
        const area_rando_box = document.getElementById("area-rando");
        const small_spaceport_box = document.getElementById("small-spaceport");
        const escape_shortcuts_box = document.getElementById("escape-shortcuts");
        const mmb_box = document.getElementById("mmb");
        const cypher_select = document.getElementById("cypher");

        const params = {
            "area_rando": area_rando_box.checked,
            "small_spaceport": small_spaceport_box.checked,
            "escape_shortcuts": escape_shortcuts_box.checked,
            "mmb": mmb_box.checked,
            "cypher": cypher_select.value,
            "tricks": activated_trick_names
        };
        roll_button.disabled = true;
        const roll_response = await fetch("/rollseed", {method: "POST", headers: {'Content-Type': 'text/json'}, body: JSON.stringify(params)});
        roll_button.disabled = false;
        console.log(roll_response);
        const roll_blob = await roll_response.blob();
        const a = document.createElement("a");
        a.href = URL.createObjectURL(roll_blob);
        const filename = roll_response.headers.get("content-disposition").substring(21);
        console.log(filename);
        a.setAttribute("download", filename);
        a.click();
    });
}

window.addEventListener("load", (event) => {
    setup_collapsible();
    const trick_promise = populate_tricks();
    populate_presets(trick_promise);
    setup_roll_button();
});
