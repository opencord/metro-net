const conf = require('./gulp.conf');
const proxy = require('./proxy');

module.exports = function () {
    return {
        server: {
            baseDir: [
                conf.paths.tmp,
                conf.paths.src
            ],
            middleware: function (req, res, next) {
                if (req.url.indexOf('xosapi') !== -1 || req.url.indexOf('xos') !== -1 || req.url.indexOf('socket') !== -1) {
                    proxy.api.web(req, res);
                }
                else {
                    next();
                }
            }
        },
        open: false
    };
};