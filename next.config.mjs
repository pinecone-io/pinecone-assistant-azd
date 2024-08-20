/** @type {import('next').NextConfig} */
const nextConfig = {
    env: {
        REACT_APP_API_BASE_URL: process.env.REACT_APP_API_BASE_URL,
    }
};

export default nextConfig;
