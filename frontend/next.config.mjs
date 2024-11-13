/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: [
      "meeca2-dev.s3.amazonaws.com",
      "meeca2-production.s3.amazonaws.com",
    ],
    minimumCacheTTL: 60,
  },
};

export default nextConfig;
