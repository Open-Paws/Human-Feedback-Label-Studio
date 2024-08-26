const fs = require('fs');

// Read the original JSON file
fs.readFile('languages.json', 'utf8', (err, data) => {
    if (err) {
        console.error('Error reading file:', err);
        return;
    }

    // Parse the JSON data
    const originalJson = JSON.parse(data);

    // Transform the JSON data to the new format
    const newFormat = Object.keys(originalJson).map(key => ({
        code: originalJson[key],
        name: key
    }));

    // Convert the new format to JSON string
    const newJson = JSON.stringify(newFormat, null, 4);

    // Write the new JSON to a file
    fs.writeFile('new_languages.json', newJson, 'utf8', err => {
        if (err) {
            console.error('Error writing file:', err);
            return;
        }
        console.log('File has been saved.');
    });
});