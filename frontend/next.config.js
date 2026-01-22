/** @type {import('next').NextConfig} */
const nextConfig = {
  trailingSlash: true,
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_OPENAI_DOMAIN_KEY: process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY || '',
  },
  output: 'export', // Enable static exports for GitHub Pages
  basePath: '/todo--ai-chatbot', // Match your GitHub repository name
  assetPrefix: '/todo--ai-chatbot/', // Ensure assets are loaded with the correct path
  trailingSlash: true,
  images: {
    unoptimized: true, // Important for GitHub Pages
  },
};

module.exports = nextConfig;