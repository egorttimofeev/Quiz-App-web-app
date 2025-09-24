module.exports = {
  apps: [
    {
      name: 'quiz-api',
      script: 'main.py',
      interpreter: 'python',
      cwd: './api',
      env: {
        NODE_ENV: 'development',
        API_PORT: 8000
      },
      env_production: {
        NODE_ENV: 'production',
        API_PORT: 8000
      },
      log_file: './logs/combined.log',
      out_file: './logs/out.log',
      error_file: './logs/error.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z'
    },
    {
      name: 'quiz-web',
      script: 'serve',
      env: {
        PM2_SERVE_PATH: './web-app',
        PM2_SERVE_PORT: 3000,
        PM2_SERVE_SPA: 'true',
        PM2_SERVE_HOMEPAGE: '/index.html'
      }
    }
  ]
};