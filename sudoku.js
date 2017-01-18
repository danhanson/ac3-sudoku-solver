
var board = new Array(9);
for(var i = 9; i--;){
	board[i] = new Array(9);
}

window.onload = function(){
	var tiles = document.getElementsByClassName('column');
	for(var i = 81; i--;){
		var tile = tiles[i];
		var row = tile.dataset.row;
		var col = tile.dataset.column;
		board[row][col] = tile;
	}
};

function handleKeyPress(event){
	var tile = event.target;
	var row = tile.dataset.row;
	var col = tile.dataset.column;
	switch(event.keyCode){
		case 37:
			if(col == 0){
				col = 8;
			} else {
				col--;
			}
			board[row][col].focus();
			break;
		case 38:
			if(row == 0){
				row = 8;
			} else {
				row--;
			}
			board[row][col].focus();
			break;
		case 39:
			if(col == 8){
				col = 0;
			} else {
				col++;
			}
			board[row][col].focus();
			break;		
		case 40:
			if(row == 8){
				row = 0;
			} else {
				row++;
			}
			board[row][col].focus();
			break;
		case 46:
		case 8:
			tile.innerHTML = '&nbsp;';
			tile.className = 'column';
			break;
		default:
			if(event.charCode >= 49 && event.charCode <= 57){
				tile.innerHTML = String.fromCharCode(event.charCode);
				tile.className = 'init-value';
			}
	}
}

function solve(){
	var initVals = document.getElementsByClassName('init-value');
	var message = new Array(initVals.length);
	for(var i = initVals.length; i--;){
		var tile = initVals[i];
		var val = {};
		val.row = tile.dataset.row;
		val.col = tile.dataset.column;
		val.value = Number(tile.innerHTML);
		message[i] = val;
	}
	var req = new XMLHttpRequest();
	req.onreadystatechange = function(){
		if(req.readyState != 4){
			return;
		}
		if(req.status != 200){
			alert("cannot be solved");
			return;
		}
		solution = JSON.parse(req.responseText);
		for(var i = 9; i--;){
			for(var j = 9; j--;){
				if(board[i][j].className == 'init-value'){
					continue;
				} else {
					board[i][j].innerHTML = String(solution[i][j] || '&nbsp;')
					board[i][j].className = 'found-value'
				}
			}
		}
	}
	req.open("POST","/init-values");
	req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
	req.send(JSON.stringify(message));
}

