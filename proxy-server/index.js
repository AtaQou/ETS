const express = require("express");
const { createProxyMiddleware } = require("http-proxy-middleware");
const cors = require("cors");

const app = express();

app.use("/translate_a", cors()); // Apply CORS middleware specifically to your proxy route

app.use(
  "/translate_a",
  createProxyMiddleware({
    target: "https://translate.google.com",
    changeOrigin: true,
    onProxyRes: function (proxyRes, req, res) {
      console.log("Proxy Response:", proxyRes.statusCode); // Log status code
    },
    onProxyReq: function (proxyReq, req, res) {
      console.log("Proxy Request to:", proxyReq.path);
    },
    onError: function (err, req, res) {
      console.error("Proxy Error:", err);
    },
    pathRewrite: {
      "^/translate_a": "/translate_a", // Correct path rewriting
    },
  })
);

const PORT = 5002;
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
