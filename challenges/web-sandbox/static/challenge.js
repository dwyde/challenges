// The user's code will stop running after TIMEOUT milliseconds.
var TIMEOUT = 500;

// The coveted flag.
var THE_FLAG = (function () {
    var fs = require('fs');
    var contents = fs.readFileSync('flag').toString();
    return contents.trim();
}());

// Run the user's JavaScript code in a sandbox.
const runCode = function(code) {
    const banned = /([\[\]\(\)]|call|apply|Symbol)/.exec(code);
    
    if (banned !== null) {
        return 'Banned syntax: ' + banned[0];
    }

    try {
        var unique = {};
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

// Read stdin
process.stdin.resume();
var fs = require('fs');
var userInput = fs.readFileSync(process.stdin.fd).toString().trim();

// Run the user's code, and print the result.
const output = runCode(userInput);
console.log(output);
