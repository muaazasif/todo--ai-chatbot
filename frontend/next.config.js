/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_OPENAI_DOMAIN_KEY: process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY || '',
  },
};

module.exports = nextConfig;