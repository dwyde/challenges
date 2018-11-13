//
// Call ``result = flag(null)`` in a JavaScript sandbox.
//

// The maximum length of user input
const MAX_LENGTH = 70;

// The user's code will stop running after TIMEOUT milliseconds.
const TIMEOUT = 500;

// The coveted flag.
const THE_FLAG = (function () {
    const fs = require('fs');
    const contents = fs.readFileSync('flag').toString();
    return contents.trim();
}());

// Run the user's JavaScript code in a sandbox.
const runCode = function(code) {
    const banned = /(\s|[\[\]\(\)]|call|apply|Symbol)/.exec(code);
    
    if (banned !== null) {
        return 'Banned syntax: "' + banned[0] + '"';
    }

    if (code.length > MAX_LENGTH) {
        return 'Maximum input length is ' + MAX_LENGTH;
    }

    try {
        const unique = {};
        const vm = require('vm');

        const sandbox = {
            flag: function(nullArg) {
                if (nullArg === null) {
                    return unique
                }
            }
        };

        const script = new vm.Script(code);
        const context = new vm.createContext(sandbox);
        const options = {timeout: TIMEOUT};
        script.runInContext(context, options);

        if (context.result === unique) {
            return 'You got the flag: ' + THE_FLAG
        } else {
            return 'No flag yet!'
        }

    } catch (e) {
        return 'Error on evaluation: ' + e
    }
};

//
// Main code
//

// Read argv, run the user's code, and print the result.
if (process.argv.length == 3) {
    const userInput = process.argv[2];
    const output = runCode(userInput);
    console.log(output);
} else {
    console.log('Wrong argv length: ' + process.argv.length);
}

