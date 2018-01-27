var i = 0;

function duplicate(divID) {
    var original = document.getElementById(divID);
    var clone = original.cloneNode(true);
    clone.id = divID + ++i;
    original.parentNode.appendChild(clone);
}