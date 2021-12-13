const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const TerserPlugin = require("terser-webpack-plugin");
const JsonMinimizerPlugin = require("json-minimizer-webpack-plugin");
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
const CopyWebpackPlugin = require('copy-webpack-plugin');
const DashboardPlugin = require('webpack-dashboard/plugin');
const regeneratorRuntime = require("regenerator-runtime");


module.exports = env => {
  const IS_DEV_MODE = env.NODE_ENV === "DEV"
  console.log("NODE ENV", env.NODE_ENV);
  console.log(__dirname);
  let dev_plugins = IS_DEV_MODE? [
    new BundleAnalyzerPlugin({
      analyzerPort: 8998,
      defaultSizes: "stat",
    }),
    new DashboardPlugin({ port: 8091 }),
  ] : [];

  return {
    entry: ['./src/app.js'],
    target: 'electron-main',
    node: {
      __dirname: false,
      __filename: false
    },
    plugins: [
      new HtmlWebpackPlugin({
        template: './src/index.html',
      }),
      new MiniCssExtractPlugin({
        filename: !IS_DEV_MODE? 'css/[name].css' : 'css/[name].[contenthash].css',
        chunkFilename: !IS_DEV_MODE? 'css/[id].css' : 'css/[id].[contenthash].css',
      }),
      new VueLoaderPlugin(),
      ...dev_plugins,
    ],
    module: {
      rules: [{
          test: /\.js$/,
          use: 'babel-loader'
        },
        {
          test: /\.vue$/,
          use: 'vue-loader'
        },
        // {
        //   test: /\.css$/,
        //   use: [
        //     {
        //       loader: MiniCssExtractPlugin.loader,
        //       // options: {
        //       //   name: 'style.css',
        //       //   outputPath: 'css/',
        //       //   hmr: env.NODE_ENV == 'DEV' 
        //       // },
        //     }, "css-loader"
        //   ]
        // },
        {
          test: /\.css$|\.s[ac]ss$/i,
          // test: /\.css$/,
          use: [
            {
              loader: MiniCssExtractPlugin.loader,
            }, 
            {
              loader: "css-loader",
              options: {
                url: false,
              }
            },
            "sass-loader"
          ]
        },
        {
          test: /\.(png|svg|jpg|gif)$/,
          loader: "file-loader",
          options: {
            esModule: false,
             name: "[name].[ext]",
             outputPath: "assets/imgs",
            // publicPath: '../',
          },
        },
        {
          test: /\.(toml)$/,
          loader: "file-loader",
          options: {
            esModule: false,
             name: "[name].[ext]",
             outputPath: "config/",
            // publicPath: '../',
          },
        },
        {
          test: /\.(ico|icns)$/,
          loader: "file-loader",
          options: {
            esModule: false,
             name: "[name].[ext]",
             outputPath: "assets/icons",
            // publicPath: '../',
          },
        },
        {
          test: /\.(ttf|otf|eot|woff(2)?)(\?[a-z0-9]+)?$/,
          use: [{
            loader: "file-loader",
            options: {
              name: "[name].[ext]",
              outputPath: 'webfonts/',
              esModule: false,
              // publicPath: '../',
            },
          }]
        },
        {
          test: /\.node$/,
          loader: "node-loader",
        }
        // { test: /\.node$/, use: 'node_loader' },
      ]
    },
    devServer: {
      hot: true,
      static: {
        directory: path.join(__dirname, "dist"),
      }
    },
    optimization: !IS_DEV_MODE? {
      usedExports: true,
      minimize: true,
      minimizer: [
        new TerserPlugin(),
        new CssMinimizerPlugin(),
        new JsonMinimizerPlugin(),
      ],
    }: {},
    output: {
      filename: "bundle.js",
      path: path.resolve(__dirname, "./dist"),
      publicPath: "",
      // path: path.resolve(__dirname, 'release/html'),
    },
  };
};
