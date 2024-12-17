// moved to pyscript
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
            trick_container.style.maxHeight = "380px";
            trick_container.style.overflowY = "auto";
        }
    });
}

function setup_logic_string() {
    console.log("setup logic string button");
    const logic_str_btn = document.getElementById("logic-str-btn");
    const logic_str_out = document.getElementById("logic-str-out");

    logic_str_btn.addEventListener("click", () => {
        const activated_trick_names = get_activated_trick_names();
        const result_str = python_get_logic_str(activated_trick_names);
        logic_str_out.innerText = result_str;
    });
}

async function populate_presets(preset_data) {
    /* stuff moved to pyscript
    console.log("populate presets");
    const preset_response = await fetch("/presets");
    if (! preset_response.ok) {
        console.error("bad response from presets");
    }
    const preset_data = await preset_response.json();

    // tricks populated before making buttons that act on tricks
    await trick_promise;
    */
    const preset_span = document.getElementById("preset-buttons");

    for (const [preset_name, trick_list] of preset_data) {
        const button = document.createElement('button');
        button.innerText = preset_name;
        const tricks_for_this_preset = trick_list;
        button.addEventListener('click', () => {
            const tricks_table = document.getElementById("tricks");
            for (const row of tricks_table.firstChild.children) {
                const checkbox = row.firstChild.firstChild;
                checkbox.checked = false;
            }
            for (const trick_name of tricks_for_this_preset) {
                const tricks_checkbox = document.getElementById(trick_name);
                if (! tricks_checkbox) {
                    console.error(`no tricks checkbox for ${trick_name}`);
                }
                tricks_checkbox.checked = true;
            }
        });

        preset_span.appendChild(button);
    }
}

async function sleep(seconds) {
    return new Promise((resolve) => setTimeout(resolve, seconds * 1000));
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

// data passed between js and python
var rom_data = "";
var modified_rom_data = "";
var rom_name = "";
var spoiler_text = "";

function read_input_rom(file) {
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            // binary data
            console.log(e.target.result.length);
            console.log(e.target.result.substring(0, 64));
            const expected_begin = "data:application/";
            if (e.target.result.substring(0, expected_begin.length) === expected_begin) {
                const start_index = e.target.result.indexOf(";base64,") + 8;
                if (start_index >= expected_begin.length && start_index < 150) {
                    rom_data = e.target.result.substring(start_index);
                }
                else {
                    console.error(`unexpected file encoding: ${e.target.result.substring(0, 160)}`);
                }
            }
            else {
                console.error(`unexpected file encoding: ${e.target.result.substring(0, 64)}`);
            }
        };
        reader.onerror = function(e) {
            // error occurred
            console.error('Error : ' + e.type);
        };
        reader.readAsDataURL(file);
    }
}

function setup_file_loader() {
    const file_input = document.getElementById("rom");
    file_input.addEventListener('change', function(e) {
        console.log("file change event");
        read_input_rom(e.target.files[0]);
    });

    // in case the browser saved the file from previous session
    read_input_rom(file_input.files[0]);
    // TODO: make sure the browser saves the file from a previous session
}

// https://stackoverflow.com/questions/16245767/creating-a-blob-from-a-base64-string-in-javascript
const b64toBlob = (b64Data, contentType='', sliceSize=512) => {
    const byteCharacters = atob(b64Data);
    const byteArrays = [];

    for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
        const slice = byteCharacters.slice(offset, offset + sliceSize);

        const byteNumbers = new Array(slice.length);
        for (let i = 0; i < slice.length; i++) {
            byteNumbers[i] = slice.charCodeAt(i);
        }

        const byteArray = new Uint8Array(byteNumbers);
        byteArrays.push(byteArray);
    }
  
    const blob = new Blob(byteArrays, {type: contentType});
    return blob;
}

function get_activated_trick_names() {
    const activated_trick_names = [];
    const tricks_table = document.getElementById("tricks");
    for (const row of tricks_table.firstChild.children) {
        const checkbox = row.firstChild.firstChild;
        const trick_name = row.children[1].firstChild.innerText
        if (checkbox.checked) {
            activated_trick_names.push(trick_name);
        }
    }
    return activated_trick_names;
}

function setup_roll_button() {
    const roll_button = document.getElementById("roll-button");
    roll_button.addEventListener("click", async () => {
        const activated_trick_names = get_activated_trick_names();
        const area_rando_box = document.getElementById("area-rando");
        const small_spaceport_box = document.getElementById("small-spaceport");
        const escape_shortcuts_box = document.getElementById("escape-shortcuts");
        const fill_select = document.getElementById("fill");
        const daphne_box = document.getElementById("daphne-gate");
        const cypher_select = document.getElementById("cypher");
        const objectives_box = document.getElementById("objective-rando");
        const objectives_slider = document.getElementById("objective-count");
        const skip_crash_space_port_box = document.getElementById("skip-crash-space-port");

        const item_marker_radios = document.getElementsByName("item_markers");
        // TODO: find out whether this Array.from is needed - item_marker_radios.find(button => button.checked);
        const item_marker_selected = Array.from(item_marker_radios).find(button => button.checked);
        const item_markers = item_marker_selected ? item_marker_selected.value : "Simple";

        const objectives = objectives_box.checked ? objectives_slider.value : "0";

        const params = {
            "area_rando": area_rando_box.checked,
            "small_spaceport": small_spaceport_box.checked,
            "escape_shortcuts": escape_shortcuts_box.checked,
            "fill": fill_select.value,
            "cypher": cypher_select.value,
            "tricks": activated_trick_names,
            "daphne_gate": daphne_box.checked,
            "item_markers": item_markers,
            "objective_rando": objectives,
            "skip_crash_space_port": skip_crash_space_port_box.checked
        };
        roll_button.disabled = true;
        const status_div = document.getElementById("status");
        status_div.innerText = "rolling...";
        await sleep(0.01);
        const roll1_success = python_roll1_function();
        if (! roll1_success) {
            console.log("roll1 failed");
            status_div.innerText = "failed";
            roll_button.disabled = false;
            return;
        }
        await sleep(0.01)
        python_roll2_function(JSON.stringify(params));
        await sleep(0.01)
        const roll3_success = python_roll3_function();
        if (! roll3_success) {
            console.log("roll3 failed");
            status_div.innerText = "failed";
            roll_button.disabled = false;
            return;
        }
        await sleep(0.01);
        python_roll4_function();
        await sleep(0.01);

        if (modified_rom_data.length) {
            await sleep(0.01);
            const data_blob = b64toBlob(modified_rom_data);
            await sleep(0.01);

            // rom download link
            const a = document.createElement("a");
            a.href = URL.createObjectURL(data_blob);
            await sleep(0.01);
            const filename = rom_name || "SubFileNameError.sfc";
            console.log(filename);
            a.setAttribute("download", filename);
            a.innerText = `download file ${filename}`;
            status_div.innerText = "done";
            status_div.appendChild(document.createElement("br"));
            status_div.appendChild(a);

            // spoiler download link
            const spoiler_a = document.createElement('a');
            spoiler_a.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(spoiler_text));
            spoiler_a.setAttribute('download', `${filename}.spoiler.txt`);
            spoiler_a.innerText = `download spoiler ${filename}.spoiler.txt`;
            status_div.appendChild(document.createElement("br"));
            status_div.appendChild(spoiler_a);
        }
        else {
            status_div.innerText = "failed";
        }
        roll_button.disabled = false;

        /*
        console.log(roll_response);
        const roll_blob = await roll_response.blob();
        const a = document.createElement("a");
        a.href = URL.createObjectURL(roll_blob);
        const filename = roll_response.headers.get("content-disposition").substring(21);
        console.log(filename);
        a.setAttribute("download", filename);
        a.click();
        */
    });
}

function setup_objective_rando() {
    const objectives_box = document.getElementById("objective-rando");
    const objectives_slider_span = document.getElementById("objective-count-span");
    const checkbox_handler = () => {
        objectives_slider_span.style.display = objectives_box.checked ? "inline" : "none";
    };
    objectives_box.addEventListener("change", checkbox_handler);
    checkbox_handler();

    const objectives_slider = document.getElementById("objective-count");
    const objectives_label = document.getElementById("objective-count-label");
    const slider_handler = () => {
        objectives_label.innerText = `${objectives_slider.value} objectives`
    };
    objectives_slider.addEventListener("input", slider_handler);
    slider_handler();
}

window.addEventListener("load", (event) => {
    setup_collapsible();
    // const trick_promise = populate_tricks();
    // populate_presets(trick_promise);
    setup_roll_button();
    setup_file_loader();
    setup_logic_string();
    setup_objective_rando();
});
