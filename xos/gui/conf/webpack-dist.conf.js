const webpack = require('webpack');
const conf = require('./gulp.conf');
const path = require('path');

const HtmlWebpackPlugin = require('html-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const pkg = require('../package.json');
const autoprefixer = require('autoprefixer');
const BaseHrefWebpackPlugin = require('base-href-webpack-plugin').BaseHrefWebpackPlugin;
const CopyWebpackPlugin = require('copy-webpack-plugin');
const env = process.env.NODE_ENV || 'production';
const brand = process.env.BRAND || 'cord';

module.exports = {
  module: {
    loaders: [
      {
        test: /.json$/,
        loaders: [
          'json'
        ]
      },
      {
        test: /\.(css|scss)$/,
        loaders: ExtractTextPlugin.extract({
          fallbackLoader: 'style',
          loader: 'css?minimize!sass!postcss'
        })
      },
      {
        test: /\.ts$/,
        exclude: /node_modules/,
        loaders: [
          'ng-annotate',
          'ts'
        ]
      },
      {
        test: /.html$/,
        loaders: [
          'html?' + JSON.stringify({
            attrs: ["img:src", "img:ng-src"]
          })
        ]
      },
      {
        test: /\.(png|woff|woff2|eot|ttf|svg|jpg|gif|jpeg)$/,
        loader: 'url-loader?limit=100000'
      }
    ]
  },
  plugins: [
    new CopyWebpackPlugin([
      { from: `./conf/app/app.config.${env}.js`, to: `app.config.js` },
      { from: `./conf/app/style.config.${brand}.js`, to: `style.config.js` },
      { from: `./conf/app/mapconstants.production.js`, to: `mapconstants.js`}
    ]),
    new webpack.optimize.OccurrenceOrderPlugin(),
    new webpack.NoErrorsPlugin(),
    new HtmlWebpackPlugin({
      inject: true,
      template: conf.path.src('index.html')
    }),
    new webpack.optimize.UglifyJsPlugin({
      compress: {unused: true, dead_code: true, warnings: false}, // eslint-disable-line camelcase
      mangle: false // NOTE mangling was breaking the build
    }),
    new ExtractTextPlugin('index.css'),
    new webpack.optimize.CommonsChunkPlugin({name: 'vendor'}),
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery"
    }),
    new BaseHrefWebpackPlugin({
      baseHref: '/xos/'
    }),
  ],
  postcss: () => [autoprefixer],
  output: {
    path: path.join(process.cwd(), conf.paths.dist),
    publicPath: "/xos/", // enable apache proxying on the head node
    filename: '[name].js'
  },
  resolve: {
    extensions: [
      '',
      '.webpack.js',
      '.web.js',
      '.js',
      '.ts'
    ],
      alias: {
          "ngprogress": path.resolve(__dirname, '../node_modules/ngprogress/build/ngProgress.js')
      }
  },
  entry: {
    app: `./${conf.path.src('index')}`,
    vendor: Object.keys(pkg.dependencies)
  },
  ts: {
    configFileName: 'tsconfig.json'
  },
  tslint: {
    configuration: require('../tslint.json')
  }
};

