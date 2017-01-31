(function () {
    var key = 0;
    var text = '\u047f\u0475\u0478\u047e\u0462\u0461\u046b\u0478' +
                '\u0470\u0477\u0446\u0461\u0476\u046b\u0446\u0461\u046a\u0471' +
                '\u0470\u0477\u047c\u0464';

    var decrypt = function (key) {
        var i, newChar, decrypted = '';
        for (i = 0; i < text.length; i++) {
            newChar = text.charCodeAt(i) ^ key;
            decrypted += String.fromCharCode(newChar);
        }
        return decrypted;
    };

    var showDecrypted = function () {
        var result = decrypt(key++);
        $('#output').text(result);
    };

    // Randomize button position
    var moveButton = function () {
        var button = $('#click-me');
        var container = $('#container');
        var vertical = container.height() - button.height();
        var horizontal = container.width() - button.width();
        var buffer = 32;
        var topPos = getRandomInt(buffer, vertical - buffer);
        var leftPos = getRandomInt(buffer, horizontal - buffer);
        button.css({'top': topPos, 'left': leftPos})
    };

    var getRandomInt = function (min, max) {
        return Math.floor(Math.random() * (max - min)) + min;
    }

    // Set up event handlers
    $('#click-me').bind('click', showDecrypted);
    setInterval(moveButton, 2000);

}());

