// Emphasize and de-emphasize two pieces of text:
// the positions to emphasize are stored as data-pos1 and data-pos2
// in the HTML object with ID pos_id.
// Emphasize the ith piece, an html element with id idi,
// at data-posi. Emphasize both by applying the emphasis class.

function pair_emphasize(pos_id, id1, id2, emphasis) {
    const pos_store = document.getElementById(pos_id);
    const pos1 = JSON.parse(pos_store.getAttribute("data-pos1"));
    const pos2 = JSON.parse(pos_store.getAttribute("data-pos2"));

    if (pos1 == '*') { // highlight it all
        document.getElementById(id1).classList.add(emphasis);
    } else { // specific positions given
        const start1 = pos1[0];
        const end1 = pos1[1];
        if (start1 < 0 || end1 < 0) {
            return;
        }
        
        const first = document.getElementById(id1);
        var text1 = first.innerHTML;
        text1 = text1.substring(0, start1) +
            '<span class="' + emphasis + '">' + 
            text1.substring(start1, end1) +
            '</span>' +
            text1.substring(end1);
        first.innerHTML = text1;
    }

    if (pos2 == '*') {
        document.getElementById(id2).classList.add(emphasis);
    } else {
        const start2 = pos2[0];
        const end2 = pos2[1];

        if (start2 < 0 || end2 < 0) {
            return;
        }
        
        const second = document.getElementById(id2);
        var text2 = second.innerHTML;
        text2 = text2.substring(0, start2) +
            '<span class="' + emphasis + '">' + 
            text2.substring(start2, end2) +
            '</span>' +
            text2.substring(end2);
        second.innerHTML = text2;
    }

}

function pair_deemphasize(pos_id, id1, id2, emphasis) {
    const pos_store = document.getElementById(pos_id);
    const pos1 = JSON.parse(pos_store.getAttribute("data-pos1"));
    const pos2 = JSON.parse(pos_store.getAttribute("data-pos2"));

    if (pos1 == '*') { // highlight it all
        document.getElementById(id1).classList.remove(emphasis);
    } else { // specific positions given

        const start1 = pos1[0];
        const end1 = pos1[1];

        if (start1 < 0 || end1 < 0) {
            return;
        }
        
        const first = document.getElementById(id1);
        var text1 = first.innerHTML;
        const offset1_1 = ('<span class="' + emphasis + '">').length;
        const offset1_2 = '</span>'.length;

        // untouched text, text between highlight classes, text at end
        text1 = text1.substring(0, start1) + 
            text1.substring(start1 + offset1_1, end1 + offset1_1) +
            text1.substring(end1 + offset1_1 + offset1_2);
        
        first.innerHTML = text1;
    }

    if (pos2 == '*') { // highlight it all
        document.getElementById(id2).classList.remove(emphasis);
    } else { // specific positions given
        const start2 = pos2[0];
        const end2 = pos2[1];

        if (start2 < 0 || end2 < 0) {
            return;
        }
        
        const second = document.getElementById(id2);
        var text2 = second.innerHTML;
        const offset2_1 = ('<span class="' + emphasis + '">').length;
        const offset2_2 = '</span>'.length;

        // untouched text, text between highlight classes, text at end
        text2 = text2.substring(0, start2) + 
            text2.substring(start2 + offset2_1, end2 + offset2_1) +
            text2.substring(end2 + offset2_1 + offset2_2);
        second.innerHTML = text2;
    }
    
}

// Open and close the "sidebar" presenting extra information to the user
// (the sidebar has taken the form of a sidebar, tooltip, etc. and is currently
// a hidden line in the code response table)
function open_sidebar(i) {
    document.getElementById('pp-line-exp-' + i).style.display = 'block';
    document.getElementById('pp-below-' + i).style.display = 'table-row';
}

function close_sidebar(i) {
    document.getElementById('pp-line-exp-' + i).style.display = 'none';
    document.getElementById('pp-below-' + i).style.display = 'none';
}

// Switch out two pieces of code from the same 'or' node
function switch_or(i) {
    // switch the main code being presented to the user
    line = document.getElementById('pp-line-' + i);
    const newText = line.getAttribute("data-or");
    line.setAttribute("data-or", line.innerText);
    line.innerText = newText;

    // switch the alternate code (1) in the sidebar (2) in the table row below
    document.getElementById('pp-line-alt-' + i).innerText = line.getAttribute("data-or");
    document.getElementById('pp-below-txt-' + i).innerText = line.getAttribute("data-or");

    // switch the highlighted sections of the two
    poss = document.getElementById('pp-line-switch-' + i);
    const pos1 = poss.getAttribute("data-pos1");
    const pos2 = poss.getAttribute("data-pos2");
    poss.setAttribute("data-pos1", pos2);
    poss.setAttribute("data-pos2", pos1);
}

// Copy the Pandas code to clipboard (for the purpose of running it)
function copy_clipboard() {
    const table = document.getElementById('pp-response-table');
    let result = '';

    for (let i = 0; i < table.rows.length; i++) {    
        let row = table.rows[i];
        if (!(row.id.startsWith('pp-below'))) { // these are the alternative options
            result += row.cells[1].innerText + '\n' // first cell is reversed for 'or' symbol
        }  
    }  

    var promise = navigator.clipboard.writeText(result);
}

module.exports = { pair_emphasize, pair_deemphasize, open_sidebar, close_sidebar, switch_or, copy_clipboard };