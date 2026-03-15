import cors from "cors";
import express from "express";

import metricsRoutes from "./routes/metrics.routes";

const app = express();
const PORT = 3000;

app.use(cors());
app.use("/api", metricsRoutes);

app.listen(PORT, () => {
  console.log(`Backend running on http://localhost:${PORT}`);
});
