const HtmlWebpackPlugin = require('html-webpack-plugin');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
  entry: './app.js',
  module: {
    rules: [
      { test: /\.js$/, use: 'babel-loader' },
      { test: /\.vue$/, use: 'vue-loader' },
      { test: /\.css$/, use: [{
        loader: MiniCssExtractPlugin.loader,
        options: {
          name: 'style.css',
          outputPath: 'css/',
          // publicPath: '../',
          hmr: process.env.NODE_ENV == 'development'
        },
      }, 'css-loader',]},
      { test: /.(ttf|otf|eot|svg|woff(2)?)(\?[a-z0-9]+)?$/, use: [{
        loader: 'file-loader',
        options: {
          name: '[name].[ext]',
          outputPath: 'webfonts/',
          // publicPath: '../',
        }
      }]}
    ]
  },
  devServer: {
    hot: true,
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './index.html',
    }),
    new MiniCssExtractPlugin({
      filename: 'style.css',
      chunkFilename: '[id].css',
    }),
    new VueLoaderPlugin(),
  ]
};