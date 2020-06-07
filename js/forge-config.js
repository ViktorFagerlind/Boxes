module.exports = {
    packagerConfig: {},
    makers: [
      {
        "name": "@electron-forge/maker-squirrel",
        "config": {
          "name": "plotter2"
        }
      },
      {
        "name": "@electron-forge/maker-zip",
        "platforms": [
          "darwin"
        ]
      },
      {
        "name": "@electron-forge/maker-deb",
        "config": {}
      },
      {
        "name": "@electron-forge/maker-rpm",
        "config": {}
      }
    ],
    hooks: {
        generateAssets: async () => {
          copy("./src/index.html", "./dist/index.html");
          copy("./src/index.css", "./dist/index.css");
        } 
    }
}

function copy(src, dest)
{
  const fs = require('fs');

  console.log(`Copying file from ${src} to ${dest}`, )

  fs.copyFile(src, dest, (err) => {
    if (err) throw err;
    console.log('File was copied to destination');});
}
