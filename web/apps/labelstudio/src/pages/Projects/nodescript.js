const fs = require('fs');

// Read the original JSON file
fs.readFile('languages.json', 'utf8', (err, data) => {
	if (err) {
		console.error(err);
		return;
	}
	const languages = JSON.parse(data);

	// Reformat the JSON structure
	const reformattedLanguages = languages.map(language => {
		const code = Object.keys(language)[0];
		const name = language[code];
		return { code, name };
	});

	// Write the reformatted JSON to a new file
	fs.writeFile('reformatted_languages.json', JSON.stringify(reformattedLanguages, null, 4), 'utf8', err => {
		if (err) {
			console.error(err);
			return;
		}
		console.log("Reformatted JSON saved to reformatted_languages.json");
	});
});