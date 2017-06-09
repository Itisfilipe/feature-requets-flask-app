var path = require('path');
var webpack = require('webpack');
module.exports = {
  entry: [
    "./src/vendors.js",
    "./src/app.js"
  ],
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'app.bundle.js'
  },
  module: {
    rules: [{
      test: /\.css?$/,
      use: [
        'style-loader',
        'css-loader'
      ]
    },{ test: /\.(png|woff|woff2|eot|ttf|svg)$/, loader: 'url-loader' }]
  },
  plugins: [
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery",
      Sammy: "sammy",
      ko: "knockout"
    })
  ]
};
