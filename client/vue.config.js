module.exports = {
  runtimeCompiler: true,
  assetsDir: 'static',
  devServer: {
    proxy: {
      '/api/': {
        target: (process.env.VUE_APP_DEV_SERVER_BACKEND || 'http://server:8000') + '/api',
        changeOrigin: true,
        pathRewrite: {
          '^/api': '',
        },
      },
    },
  },
  css: {
    loaderOptions: {
      css: {},
    },
  },
  configureWebpack: {
    watchOptions: {
      poll: process.env.VUE_APP_DEV_POLL_FOR_FILE_CHANGES === 'true' || false,
    },
  },
}
