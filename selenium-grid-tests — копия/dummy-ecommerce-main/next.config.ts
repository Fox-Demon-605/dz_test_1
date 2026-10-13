import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  allowedDevOrigins: ["host.docker.internal", "192.168.100.1"],
};

export default nextConfig;
