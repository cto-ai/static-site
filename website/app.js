/**
 * Module dependencies.
 */
const express = require('express');
const compression = require('compression');
const errorHandler = require('errorhandler');
const path = require('path');
const sass = require('node-sass-middleware');
const { MAIN_ROUTE } = require('./config');

/**
 * Create Express server.
 */
const app = express();

/**
 * Express configuration.
 */
app.set('host', process.env.OPENSHIFT_NODEJS_IP || '0.0.0.0');
app.set('port', process.env.PORT || process.env.OPENSHIFT_NODEJS_PORT || 8080);
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');
app.use(compression());
app.disable('x-powered-by');
app.use((req, res, next) => {
  res.locals.user = req.user;
  next();
});

// No cache
app.use(function (req, res, next) {
  res.header('Cache-Control', 'private, no-cache, no-store, must-revalidate');
  res.header('Expires', '-1');
  res.header('Pragma', 'no-cache');
  next()
});

/**
 * Primary app routes.
 */
const mainRouter = express.Router();
mainRouter.get('/', (req, res) => {
  res.sendFile(__dirname + '/views/home.html');
});
mainRouter.get('/contact', (req, res) => {
  res.sendFile(__dirname + '/views/contact.html');
});

mainRouter.use(sass({
  src: path.join(__dirname, 'public'),
  dest: path.join(__dirname, 'public')
}));

mainRouter.use('/', express.static(path.join(__dirname, 'public'), { maxAge: 31557600000 }));
mainRouter.use('/js/lib', express.static(path.join(__dirname, 'node_modules/bootstrap/dist/js'), { maxAge: 31557600000 }));
mainRouter.use('/js/lib', express.static(path.join(__dirname, 'node_modules/jquery/dist'), { maxAge: 31557600000 }));
mainRouter.use('/webfonts', express.static(path.join(__dirname, 'node_modules/@fortawesome/fontawesome-free/webfonts'), { maxAge: 31557600000 }));

app.use(MAIN_ROUTE, mainRouter);

/**
 * Error Handler.
 */
if (process.env.NODE_ENV === 'development') {
  // only use in development
  app.use(errorHandler());
} else {
  app.use((err, req, res, next) => {
    console.error(err);
    res.status(500).send('Server Error');
  });
}

/**
 * Start Express server.
 */
app.listen(app.get('port'), () => {
  console.log('%s App is running at http://localhost:%d in %s mode', '✓', app.get('port'), app.get('env'));
  console.log('  Press CTRL-C to stop\n');
});

module.exports = app;
