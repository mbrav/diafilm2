const sh = require('shelljs');
const upath = require('upath');

const destPath = upath.resolve(upath.dirname(__filename), '../../backend/templates');

sh.rm('-rf', `${destPath}/*`)

