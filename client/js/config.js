const PORT = 8020
const API_BASE =
    window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1"
        ? `http://127.0.0.1:${PORT}`
        : "https://can-you-trust-them.vercel.app";