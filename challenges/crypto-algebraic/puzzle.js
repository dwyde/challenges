
var onChange = function(oldPos, newPos) {
    var fen = ChessBoard.objToFen(newPos);
    $.ajax({
        url: 'fen',
        data: {fen: fen},
        success: function (data) {
            if (data !== '') {
                $('#output').text(data);
                $('#output').css('font-weight', 'bold');
            }
        },
    });
};

var config = {
    pieceTheme: 'chessboardjs/img/chesspieces/wikipedia/{piece}.png',
    position: 'start',
    draggable: true,
    showNotation: false,
    onChange: onChange,
};

var board = ChessBoard('board', config);
