const HtmlWebpackPlugin = require('html-webpack-plugin');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const path = require('path');
// const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
module.exports = env => {
  console.log("NODE ENV", env.NODE_ENV);
  let node_loader = env.NODE_ENV === "DEV"? "node-loader" : "native-ext-loader";
  console.log("used node_loader:", node_loader);
  return {
    entry: './app.js',
    target: 'electron-renderer',
    node: {
      __dirname: false,
      __filename: false
    },
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
            hmr: env.NODE_ENV == 'DEV'
          },
        }, 'css-loader',]},
        {
          test: /\.(png|svg|jpg|gif)$/,
          use: 'file-loader',
        },
        { test: /\.(ttf|otf|eot|svg|woff(2)?)(\?[a-z0-9]+)?$/, use: [{
          loader: 'file-loader',
          options: {
            name: '[name].[ext]',
            outputPath: 'webfonts/',
            // publicPath: '../',
          }
        }]},
        { test: /\.node$/, loader: node_loader, }
        // { test: /\.node$/, use: 'node-loader' },
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
      // new BundleAnalyzerPlugin(),
    ],
    output: {
      filename: 'bundle.js',
      // path: path.resolve(__dirname, 'release/html'),
    },
  };
};
