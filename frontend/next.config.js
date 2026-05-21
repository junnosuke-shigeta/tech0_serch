/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "export",
  // NEXT_PUBLIC_API_URL で接続先のAPIを切り替える
  // 開発: http://localhost:8000
  // 本番: https://tech0-search-api.azurewebsites.net
};

module.exports = nextConfig;
