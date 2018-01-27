function addInput(divName){
      var newdiv = document.createElement('div');
      newdiv.innerHTML = "Entry " + " <br><input type='text' name='myInputs[]'>";
      document.getElementById(divName).appendChild(newdiv);
}