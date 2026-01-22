/** @type {import('next').NextConfig} */
const nextConfig = {
  trailingSlash: true,
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_OPENAI_DOMAIN_KEY: process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY || '',
  },
  output: 'export', // Enable static exports for GitHub Pages
  assetPrefix: './', // Use relative paths for GitHub Pages
  trailingSlash: true,
  images: {
    unoptimized: true, // Important for GitHub Pages
  },
};

module.exports = nextConfig;