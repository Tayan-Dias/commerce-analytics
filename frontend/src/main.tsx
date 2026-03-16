import { createRoot } from "react-dom/client";

import App from "./App";

document.body.style.margin = "0";
document.body.style.fontFamily = "Arial, sans-serif";
document.body.style.background = "#f3f4f6";
document.body.style.color = "#1f2937";

createRoot(document.getElementById("root")!).render(<App />);
